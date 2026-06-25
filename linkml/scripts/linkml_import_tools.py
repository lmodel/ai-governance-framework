#!/usr/bin/env python3
"""LinkML import-resolution helpers (``merge`` and ``strip-siblings``).

Two related workarounds for SchemaLoader limitations live behind one CLI:

``merge``
    Pre-flatten a LinkML schema, resolving URI-style imports via the import
    map, then strip non-built-in entries from ``imports:`` so downstream
    generators do not re-HTTP-fetch them.

    Background: SchemaLoader-based generators in LinkML (``gen-pydantic``
    and the ``python``/``sqltable``/``excel`` slots of ``gen-project``)
    construct a secondary ``SchemaView`` from the merged schema *without*
    propagating the ``importmap`` they were given. The secondary view then
    re-reads the merged schema's preserved ``imports:`` list and
    HTTP-fetches every URI entry. For canonical URI imports such as
    ``dpv:schema/dpv_common`` this manifests as a hard 404 before the
    upstream package is published. Flattening up-front and stripping all
    non-built-in entries avoids the secondary fetch.

``strip-siblings``
    Prepare a DPV extension YAML for isolated ``gen-doc`` rendering: drop
    every non-built-in import (sibling extensions *and* the core schema)
    and drop any local ``is_a`` / ``mixins`` / slot-``is_a`` references
    whose target is not declared locally in the same extension. This
    sidesteps cross-extension class collisions and the dangling parent
    references that result from removing the imports.

Usage::

    uv run python scripts/linkml_import_tools.py merge <schema.yaml> \\
        --importmap importmap.json --output merged.yaml
    uv run python scripts/linkml_import_tools.py strip-siblings <src.yaml> <dst.yaml>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from _common import yaml_dump_indented

# After SchemaLoader merges everything (including the built-in linkml types),
# the merged schema attributes every element to the top-level schema's URI.
# If we leave *any* import in the list, a downstream SchemaLoader re-resolves
# that import and tries to re-merge its elements, producing
# "Conflicting URIs ... for item: string"-style errors. So strip them all.
MERGE_BUILTIN_IMPORTS: set[str] = set()

# For per-extension stripping we keep the linkml:types built-in so the
# extension YAML remains validatable in isolation.
STRIP_KEEP_IMPORTS: set[str] = {"linkml:types"}


# ===========================================================================
# Subcommand: merge  (was scripts/merge_linkml_schema.py)
# ===========================================================================

def cmd_merge(args: argparse.Namespace) -> int:
    # Deferred to avoid the linkml import cost on `strip-siblings` runs.
    from linkml.utils.schemaloader import SchemaLoader
    from linkml_runtime.dumpers import yaml_dumper
    from linkml_runtime.linkml_model.meta import Prefix

    loader = SchemaLoader(
        str(args.schema),
        importmap=str(args.importmap),
        mergeimports=True,
    )
    loader.resolve()
    schema = loader.schema
    # SchemaLoader merges imported-module prefix maps into the runtime
    # `namespaces` object but does NOT write them back into `schema.prefixes`
    # (the serialized slot). Once the imports are stripped below, the dumped
    # schema would then carry CURIEs (e.g. `skos:member`, `dpv:hasRule`,
    # `xsd:string`) whose prefixes are undeclared, making every downstream
    # generator emit "Unrecognized prefix" warnings. Repopulate `schema.prefixes`
    # from the loader's full namespace set so the merged YAML is self-contained.
    for prefix, reference in loader.namespaces.items():
        if prefix and not prefix.startswith("@") and prefix not in schema.prefixes:
            schema.prefixes[prefix] = Prefix(
                prefix_prefix=prefix, prefix_reference=str(reference)
            )
    schema.imports = [
        imp for imp in (schema.imports or []) if imp in MERGE_BUILTIN_IMPORTS
    ]
    schema.source_file = str(args.schema.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    serialized = yaml_dumper.dumps(schema)
    args.output.write_text(serialized)
    # Sanity check: make sure the round-tripped file actually has no leftover
    # URI imports (defensive against future linkml_runtime serializer changes).
    parsed = yaml.safe_load(args.output.read_text())
    leftover = [
        i for i in parsed.get("imports", []) if i not in MERGE_BUILTIN_IMPORTS
    ]
    if leftover:
        print(
            f"Unexpected leftover imports in {args.output}: {leftover}",
            file=sys.stderr,
        )
        return 1
    print(f"Wrote merged schema: {args.output}")
    return 0


# ===========================================================================
# Subcommand: strip-siblings  (was scripts/strip_sibling_imports.py)
# ===========================================================================

def cmd_strip_siblings(args: argparse.Namespace) -> int:
    data = yaml.safe_load(args.src.read_text(encoding="utf-8")) or {}

    original_imports = list(data.get("imports") or [])
    data["imports"] = [i for i in original_imports if i in STRIP_KEEP_IMPORTS]

    classes = data.get("classes") or {}
    slots = data.get("slots") or {}
    local_class_names = set(classes)
    local_slot_names = set(slots)

    stripped_isa = stripped_mixins = stripped_slot_isa = 0

    for cls_def in classes.values():
        if not isinstance(cls_def, dict):
            continue
        parent = cls_def.get("is_a")
        if parent and parent not in local_class_names:
            del cls_def["is_a"]
            stripped_isa += 1
        mixins = cls_def.get("mixins")
        if isinstance(mixins, list):
            kept = [m for m in mixins if m in local_class_names]
            stripped_mixins += len(mixins) - len(kept)
            if kept:
                cls_def["mixins"] = kept
            else:
                cls_def.pop("mixins", None)

    for slot_def in slots.values():
        if not isinstance(slot_def, dict):
            continue
        parent = slot_def.get("is_a")
        if parent and parent not in local_slot_names:
            del slot_def["is_a"]
            stripped_slot_isa += 1

    args.dst.parent.mkdir(parents=True, exist_ok=True)
    args.dst.write_text(yaml_dump_indented(data, sort_keys=False), encoding="utf-8")

    print(
        f"  imports kept: {data['imports']} "
        f"(dropped {len(original_imports) - len(data['imports'])}); "
        f"dangling class is_a stripped: {stripped_isa}, "
        f"dangling mixins stripped: {stripped_mixins}, "
        f"dangling slot is_a stripped: {stripped_slot_isa}",
        file=sys.stderr,
    )
    return 0


# ===========================================================================
# CLI
# ===========================================================================

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_merge = sub.add_parser(
        "merge", help="Pre-flatten a schema and strip non-built-in imports.",
    )
    p_merge.add_argument(
        "schema", type=Path,
        help="Path to the entry-point LinkML schema YAML.",
    )
    p_merge.add_argument(
        "--importmap", type=Path, required=True,
        help="Path to the importmap JSON.",
    )
    p_merge.add_argument(
        "--output", type=Path, required=True,
        help="Path of merged YAML to write.",
    )
    p_merge.set_defaults(func=cmd_merge)

    p_strip = sub.add_parser(
        "strip-siblings",
        help="Strip sibling/core imports + dangling refs from one extension YAML.",
    )
    p_strip.add_argument("src", type=Path, help="Source extension YAML.")
    p_strip.add_argument("dst", type=Path, help="Destination YAML.")
    p_strip.set_defaults(func=cmd_strip_siblings)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
