"""Shared helpers for the ``scripts/`` build pipeline.

Only utilities that are duplicated verbatim across two or more scripts live
here. Generator-specific helpers (``dump_yaml`` with custom blank-line
post-processing, RDF enrichment, collision handling) intentionally remain
in ``dpv_core_to_linkml.py``; that module owns its bespoke formatting.

Keep this module dependency-light: importing it must not trigger LinkML or
rdflib parsing.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml


def write_if_changed(path: Path, content: str) -> bool:
    """Write ``content`` to ``path`` only when it differs.

    Returns ``True`` when the file was written, ``False`` when the
    existing on-disk content already matched. Parent directories are
    created on demand. This is the idempotency primitive used by every
    generator in this directory so re-running a build is a no-op when
    upstream inputs have not changed.
    """
    if path.exists() and path.read_text() == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return True


_PASCAL_SPLIT = re.compile(r"[^A-Za-z0-9]+")


def to_pascal(local: str) -> str:
    """Convert a kebab/snake-case local name to PascalCase NCName.

    ``record`` -> ``Record``; ``record-eu-gdpr`` -> ``RecordEuGdpr``.
    Non-alphanumeric runs (including ``-``, ``_``, ``/``, ``.``) act as
    word boundaries; each segment's first character is upper-cased and
    the rest is kept verbatim (so existing camelCase fragments survive).
    """
    parts = _PASCAL_SPLIT.split(local)
    return "".join(p[:1].upper() + p[1:] for p in parts if p)


class _IndentedSafeDumper(yaml.SafeDumper):
    """Safe dumper that indents block sequence markers under their parent key."""

    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def yaml_dump_indented(
    data: object,
    *,
    sort_keys: bool = False,
    width: int = 100,
) -> str:
    """Dump YAML with yamllint-friendly list indentation.

    PyYAML defaults to indentless block sequences:

    key:
    - item

    which often triggers yamllint indentation complaints. This helper forces:

    key:
      - item
    """
    return yaml.dump(
        data,
        Dumper=_IndentedSafeDumper,
        sort_keys=sort_keys,
        default_flow_style=False,
        allow_unicode=True,
        width=width,
    )
