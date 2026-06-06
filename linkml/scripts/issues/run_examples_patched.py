#!/usr/bin/env python3
"""Wrapper around ``linkml-run-examples`` that applies the same
post-processing as ``scripts/patch_pythongen.py`` to the generated
python source *before* it is compiled in-process for example
validation.

``linkml-run-examples`` invokes ``PythonGenerator.compile_module()``
to load a fresh python module per example. That code path bypasses
our on-disk patched module entirely, so it trips over upstream
``pythongen`` defects (notably linkml/linkml#3572 - wrapper classes
emitted before the referenced enum bodies). This wrapper monkey-
patches ``compile_module`` so the in-process compile path goes
through the same fix-ups documented in ``ISSUE.md`` (Issues C, D, E
and #3572).
"""
from __future__ import annotations

import sys
from pathlib import Path

# Make sibling ``patch_pythongen`` importable without installing.
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from patch_pythongen import (  # noqa: E402
        alias_enum_wrappers,
        inject_enum_hash_patch,
        reorder,
    )
except ModuleNotFoundError:  # pragma: no cover - optional local patch helper
    # Keep this wrapper usable even when patch_pythongen.py is absent.
    def reorder(code: str) -> str:
        return code

    def alias_enum_wrappers(code: str) -> str:
        return code

    def inject_enum_hash_patch(code: str) -> str:
        return code

from linkml.generators.pythongen import PythonGenerator  # noqa: E402
from linkml_runtime.utils.compile_python import compile_python  # noqa: E402


def _patched_compile_module(self, **kwargs):
    pycode = self.serialize(**kwargs)
    pycode = inject_enum_hash_patch(alias_enum_wrappers(reorder(pycode)))
    try:
        return compile_python(pycode)
    except NameError as e:
        # Keep the upstream diagnostic but route through stderr so it
        # does not pollute the markdown summary on stdout.
        print(f"Error compiling generated python code: {e}", file=sys.stderr)
        raise


PythonGenerator.compile_module = _patched_compile_module

from linkml.utils.helpers import get_range_associated_slots  # noqa: E402
from linkml.workspaces.example_runner import ExampleRunner, cli  # noqa: E402
from linkml_runtime.utils.formatutils import camelcase  # noqa: E402


def _patched_load_from_dict(self, dict_obj: dict, target_class: str = None):
    """Handle list-valued inlined multivalued slots in example payloads.

    Upstream currently assumes dict values for inlined multivalued slots when
    ``inlined_as_list`` is false and unconditionally calls ``v.items()``.
    Some valid examples provide a list there, which raises
    ``AttributeError: 'list' object has no attribute 'items'``.
    """
    if not self.use_type_designators:
        return dict_obj
    sv = self.schemaview
    if target_class is None:
        target_class_names = [c.name for c in sv.all_classes().values() if c.tree_root]
        if len(target_class_names) != 1:
            raise ValueError(f"Cannot determine single target class, found: {target_class_names}")
        target_class = target_class_names[0]
    if isinstance(dict_obj, dict):
        if target_class not in sv.all_classes():
            raise ValueError(f"No such class as {target_class}")
        target_cls_def = sv.get_class(target_class)
        if target_cls_def and target_cls_def.class_uri == "linkml:Any":
            return dict_obj
        td_slot = sv.get_type_designator_slot(target_class) if target_class else None
        if td_slot:
            if td_slot.name in dict_obj:
                target_class = dict_obj[td_slot.name]
        elif "@type" in dict_obj:
            target_class = dict_obj["@type"]
            del dict_obj["@type"]
        if ":" in target_class:
            target_classes = [c for c in sv.all_classes() if sv.get_uri(c) == target_class]
            if len(target_classes) != 1:
                raise ValueError(f"Cannot find unique class for URI {target_class}; got: {target_classes}")
            target_class = target_classes[0]
        new_dict_obj = {}

        for k, v in dict_obj.items():
            if v is not None:
                islot = sv.induced_slot(k, target_class)
                if islot.multivalued and islot.inlined and not islot.inlined_as_list:
                    if isinstance(v, list):
                        v2 = self._load_from_dict(v, target_class=islot.range)
                    else:
                        (range_id_slot, range_simple_dict_value_slot, _) = get_range_associated_slots(
                            self.schemaview, islot.range
                        )
                        v_as_list = []
                        for ik, iv in v.items():
                            if range_simple_dict_value_slot is not None:
                                value = {range_id_slot.name: ik, range_simple_dict_value_slot.name: iv}
                            else:
                                value = iv
                                value[range_id_slot.name] = ik
                            v_as_list.append(value)
                        v2 = self._load_from_dict(v_as_list, target_class=islot.range)
                else:
                    v2 = self._load_from_dict(v, target_class=islot.range)
                new_dict_obj[k.replace("-", "_")] = v2
        py_target_class = getattr(self.python_module, camelcase(target_class))
        return py_target_class(**new_dict_obj)
    if isinstance(dict_obj, list):
        return [self._load_from_dict(x, target_class) for x in dict_obj]
    return dict_obj


ExampleRunner._load_from_dict = _patched_load_from_dict

if __name__ == "__main__":
    sys.exit(cli())
