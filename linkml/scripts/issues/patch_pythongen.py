#!/usr/bin/env python3
"""Post-process a ``gen-python`` output file to fix forward references.

``pythongen`` emits a "Class references" section near the top of the
generated module containing wrapper classes such as::

    class FIXDatatypeDatatypeName(FIXDatatypeName):
        pass

Tracked upstream: https://github.com/linkml/linkml/issues/3572

This script also converts empty wrapper subclasses of enum classes
into plain module-level aliases. ``pythongen`` emits e.g.::

    class FIXDatatypeDatatypeName(FIXDatatypeName):
        pass

for identifier slots whose ``range`` is an enum. ``linkml_runtime``'s
``EnumDefinitionMeta.__contains__`` checks ``cls.__dict__`` only — it
does not walk the MRO — so the subclass appears empty at lookup time
and instantiation fails with::

    ValueError: Unknown FIXDatatypeDatatypeName enumeration code: Country

Replacing each such empty subclass with ``Wrapper = Parent`` preserves
the identity used in type annotations / ``isinstance`` checks / value
construction while routing membership tests to the parent enum that
actually holds the permissible values.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

CLASS_REFS_MARKER = "# Class references"
ENUMS_MARKER = "# Enumerations"
SLOTS_MARKER = "# Slots"


def _find_section_start(lines: list[str], marker: str) -> int:
    for i, line in enumerate(lines):
        if line.rstrip() == marker:
            return i
    raise SystemExit(f"marker {marker!r} not found")


def _find_next_section_start(lines: list[str], start: int) -> int:
    """Return the line index where the next top-level ``# `` section
    header begins after ``start`` (or ``len(lines)`` if none)."""
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if line.startswith("# ") and not line.startswith("# - "):
            # A section header is a top-level comment that introduces a
            # new logical block. Heuristic: it sits at column 0 and is
            # preceded by a blank line.
            if i > 0 and lines[i - 1].strip() == "":
                return i
    return len(lines)


def reorder(text: str) -> str:
    lines = text.splitlines(keepends=True)

    refs_start = _find_section_start(lines, CLASS_REFS_MARKER)
    enums_start = _find_section_start(lines, ENUMS_MARKER)

    if refs_start > enums_start:
        # Already in the correct order; nothing to do.
        return text

    refs_end = _find_next_section_start(lines, refs_start)
    # Trim a single trailing blank line from the block so we don't
    # accumulate them on repeated runs.
    while refs_end > refs_start and lines[refs_end - 1].strip() == "":
        refs_end -= 1

    refs_block = lines[refs_start:refs_end]

    # Splice out the refs block.
    remaining = lines[:refs_start] + lines[refs_end:]

    # Recompute the enums-section end in the spliced list and insert
    # the refs block just before whatever comes next (typically the
    # ``# Slots`` section).
    enums_start_new = _find_section_start(remaining, ENUMS_MARKER)
    insertion_point = _find_section_start(remaining, SLOTS_MARKER)
    if insertion_point <= enums_start_new:
        insertion_point = len(remaining)

    # Ensure separation around the relocated block.
    block = list(refs_block)
    if block and block[-1].strip() != "":
        block.append("\n")
    if block and block[0].strip() != "":
        block.insert(0, "\n")

    patched = remaining[:insertion_point] + block + remaining[insertion_point:]
    return "".join(patched)


_ENUM_BASE_RE = re.compile(
    r"^class\s+([A-Za-z_][A-Za-z0-9_]*)\(EnumDefinitionImpl\)\s*:\s*$",
    re.MULTILINE,
)
_WRAPPER_RE = re.compile(
    r"^class\s+([A-Za-z_][A-Za-z0-9_]*)\(([A-Za-z_][A-Za-z0-9_]*)\)\s*:\s*\n"
    r"\s+pass\s*\n",
    re.MULTILINE,
)


def alias_enum_wrappers(text: str) -> str:
    """Replace ``class W(E): pass`` with ``W = E`` when ``E`` is an enum."""
    enum_names = {m.group(1) for m in _ENUM_BASE_RE.finditer(text)}
    if not enum_names:
        return text

    def _sub(match: re.Match[str]) -> str:
        wrapper, base = match.group(1), match.group(2)
        if base in enum_names:
            return f"{wrapper} = {base}\n"
        return match.group(0)

    return _WRAPPER_RE.sub(_sub, text)


_ENUM_IMPORT_LINE = (
    "from linkml_runtime.utils.enumerations import EnumDefinitionImpl\n"
)
_HASH_PATCH = """

# --- patched by scripts/patch_pythongen.py ---------------------------
# ``EnumDefinitionImpl`` inherits from ``YAMLRoot`` which defines
# ``__eq__`` without ``__hash__``, making enum instances unhashable.
# That breaks ``linkml_runtime.utils.yamlutils.as_yaml_obj`` when an
# enum-typed key is used in a keyed slot: ``cooked_keys.add(key)``
# raises ``TypeError``. Restore hashability based on the permissible
# value text, and make equality compare by text against both strings
# and other enum instances so that ``cooked_entry[key] != yaml_key``
# does not spuriously fail when the cooked side has been promoted to
# an enum instance and the yaml side is still the raw string.
def _edi_eq(self, other):
    if isinstance(other, str):
        return str(self) == other
    if isinstance(other, EnumDefinitionImpl):
        return str(self) == str(other)
    return NotImplemented


# Bypass ``EnumDefinitionMeta.__setattr__`` which dereferences
# ``cls._defn`` (None on the base class).
type.__setattr__(EnumDefinitionImpl, "__eq__", _edi_eq)
type.__setattr__(
    EnumDefinitionImpl, "__hash__", lambda self: hash(str(self))
)
# ---------------------------------------------------------------------
"""


def inject_enum_hash_patch(text: str) -> str:
    if "patched by scripts/patch_pythongen.py" in text:
        return text
    if _ENUM_IMPORT_LINE not in text:
        return text
    return text.replace(
        _ENUM_IMPORT_LINE, _ENUM_IMPORT_LINE + _HASH_PATCH, 1
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} <path-to-generated.py>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    text = path.read_text(encoding="utf-8")
    new_text = inject_enum_hash_patch(alias_enum_wrappers(reorder(text)))
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"patched {path}")
    else:
        print(f"no change needed for {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
