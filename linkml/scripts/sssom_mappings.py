#!/usr/bin/env python3
"""SSSOM mapping operations: overlay and verify.

A unified CLI for SSSOM mappings <-> LinkML Schema integration tasks:

``overlay``
    Apply SSSOM mappings from TSV files to LinkML schema YAML files.
    Merges predicate-mapped CURIEs into the matching mapping slots
    (``exact_mappings``, ``close_mappings``, etc.), preserving comments
    and formatting via round-trip YAML serialization.

``verify``
    Verify that LinkML schemas contain all SSSOM mappings from TSV files.
    Read-only: schemas and mappings are never modified. Fails if any
    mapping is missing, extra (``--strict`` mode), or references an
    unknown element.

Both commands are schema-independent: prefix discovery happens
automatically from each schema's ``name`` / ``default_prefix`` or via
explicit ``--subject-prefix`` arguments.

Usage::

    python scripts/sssom_mappings.py overlay \\
        --schema-dir src/<project>/schema \\
        --mappings-dir src/<project>/mappings

    python scripts/sssom_mappings.py verify \\
        --schema-dir src/<project>/schema \\
        --mappings-dir src/<project>/mappings
"""

from __future__ import annotations

import argparse
import csv
import io
import sys
from collections import defaultdict
from pathlib import Path

import yaml

from _common import yaml_dump_indented

# SKOS / OWL predicate -> LinkML mapping slot.
PREDICATE_TO_LINKML_SLOT: dict[str, str] = {
    "skos:exactMatch":         "exact_mappings",
    "skos:closeMatch":         "close_mappings",
    "skos:broadMatch":         "broad_mappings",
    "skos:narrowMatch":        "narrow_mappings",
    "skos:relatedMatch":       "related_mappings",
    "owl:equivalentClass":     "exact_mappings",
    "owl:equivalentProperty":  "exact_mappings",
}

# Predicates that appear in SSSOM TSVs but do not correspond to
# any LinkML mapping slot; silently skipped.
IGNORED_PREDICATES: frozenset[str] = frozenset(
    {"skos:broader", "skos:narrower", "rdf:type", "owl:equivalentClass"}
)

# Prefixes intrinsic to LinkML / SSSOM; never need to be declared on a schema.
_BUILTIN_PREFIXES = {
    "sssom", "owl", "rdf", "rdfs", "skos", "semapv", "linkml", "xsd", "dcterms",
}

_MAPPING_SLOT_ORDER = (
    "exact_mappings",
    "close_mappings",
    "broad_mappings",
    "narrow_mappings",
    "related_mappings",
)

# Where mapping slots should sit within an element body (used only when none
# of the five mapping slots are present yet, so we know where to splice).
_POST_MAPPING_ANCHORS = (
    "aliases", "in_subset", "permissible_values", "attributes", "slots",
    "slot_usage", "rules", "comments", "annotations", "pattern",
)

ELEMENT_SECTIONS = ("classes", "slots", "enums", "types")

REPO_ROOT = Path(__file__).resolve().parent.parent


# ===========================================================================
# Subcommand: overlay  (from scripts/apply_sssom_overlay.py)
# ===========================================================================

def _get_ruamel_yaml():
    """Lazy-import ruamel.yaml with friendly error message."""
    try:
        from ruamel.yaml import YAML
        from ruamel.yaml.comments import CommentedMap, CommentedSeq
        return YAML, CommentedMap, CommentedSeq
    except ImportError as exc:
        sys.stderr.write(
            "ERROR: the 'overlay' subcommand requires the 'ruamel.yaml' package, which is not "
            "installed in the current Python environment.\n"
            f"  (import failed: {exc})\n"
            "\n"
            "To install it, choose one of:\n"
            "  - uv add ruamel.yaml                          "
            "# add as a project dep\n"
            "  - uv pip install ruamel.yaml                  "
            "# install into the active venv\n"
            "  - pip install ruamel.yaml                     "
            "# plain pip\n"
            "\n"
            "Or run this script ad-hoc without installing:\n"
            "  uv run --with ruamel.yaml python scripts/sssom_mappings.py overlay ...\n"
        )
        sys.exit(2)


def _parse_sssom_metadata(path: Path) -> dict:
    """Extract the ``#curie_map:`` and other metadata from SSSOM TSV header."""
    metadata = {}
    for line in path.read_text().splitlines():
        if not line.startswith("#"):
            break
        line = line[1:].strip()
        if ":" in line:
            key, val = line.split(":", 1)
            metadata[key.strip()] = val.strip()
    return metadata


def _parse_sssom_rows(path: Path) -> tuple[list[str], list[list[str]]]:
    """Return ([column_names], [[row_values], ...]) for SSSOM TSV data."""
    text_lines = [
        ln for ln in path.read_text().splitlines()
        if ln.strip() and not ln.lstrip().startswith("#")
    ]
    reader = csv.DictReader(
        io.StringIO("\n".join(text_lines)), delimiter="\t"
    )
    cols = reader.fieldnames or []
    rows = [
        [row.get(c, "") for c in cols]
        for row in reader
        if row.get("subject_id")
    ]
    return list(cols), rows


class MappingIndex:
    """Lazy-loaded index of all SSSOM mappings."""

    def __init__(self) -> None:
        self.rows: list[dict[str, str]] = []
        self.curie_map: dict[str, str] = {}

    def load_from_dir(self, mappings_dir: Path) -> None:
        """Scan *.sssom.tsv files and accumulate rows + curie_map."""
        for tsv_path in sorted(mappings_dir.glob("*.sssom.tsv")):
            metadata = _parse_sssom_metadata(tsv_path)
            curie_map_str = metadata.get("curie_map", "")
            if curie_map_str:
                for item in curie_map_str.split():
                    if ":" in item:
                        pfx, uri = item.split(":", 1)
                        self.curie_map[pfx] = uri

            cols, rows = _parse_sssom_rows(tsv_path)
            for row_values in rows:
                row_dict = dict(zip(cols, row_values))
                if row_dict.get("subject_id"):
                    self.rows.append(row_dict)


def _discover_subject_prefixes(data: dict) -> set[str]:
    """Infer subject-side prefixes from a schema's default_prefix + explicit prefixes."""
    prefixes = set()
    if dp := data.get("default_prefix"):
        prefixes.add(dp)
    for pfx in (data.get("prefixes") or {}).keys():
        if pfx not in _BUILTIN_PREFIXES:
            prefixes.add(pfx)
    return prefixes


def _insert_mapping_slot(
    body: dict,
    curie: str,
    predicate: str,
    curie_map: dict[str, str],
) -> None:
    """Insert or update a single mapping CURIE into the correct LinkML slot."""
    if predicate not in PREDICATE_TO_LINKML_SLOT:
        return
    slot = PREDICATE_TO_LINKML_SLOT[predicate]

    # Try to lazy-import CommentedSeq for round-trip preservation.
    try:
        from ruamel.yaml.comments import CommentedSeq
    except ImportError:
        CommentedSeq = list

    current = body.get(slot)
    if current is None:
        body[slot] = CommentedSeq([curie])
    elif isinstance(current, (list, CommentedSeq)):
        if curie not in current:
            current.append(curie)
    else:
        # Scalar; convert to list.
        if curie not in [current]:
            body[slot] = CommentedSeq([current, curie])


def _merge_mappings(
    body: dict,
    rows: list[dict[str, str]],
    curie_map: dict[str, str],
) -> int:
    """Merge a batch of SSSOM rows into an element. Return count of new links added."""
    new_links = 0
    by_predicate: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        predicate = row.get("predicate_id", "")
        if predicate in IGNORED_PREDICATES:
            continue
        if predicate not in PREDICATE_TO_LINKML_SLOT:
            print(
                f"  WARNING: unsupported predicate {predicate!r} "
                f"(subject={row.get('subject_id')})",
                file=sys.stderr,
            )
            continue
        obj_curie = row.get("object_id", "")
        if obj_curie:
            by_predicate[predicate].append(obj_curie)

    for predicate, curies in by_predicate.items():
        slot = PREDICATE_TO_LINKML_SLOT[predicate]
        before = len(body.get(slot) or [])
        for curie in curies:
            _insert_mapping_slot(body, curie, predicate, curie_map)
        after = len(body.get(slot) or [])
        new_links += max(0, after - before)

    return new_links


def _set_pv_meaning(body: dict, curie: str) -> None:
    """Set the ``meaning`` field on a permissible value."""
    if not isinstance(body.get("permissible_values"), dict):
        return
    pv_name = curie.split(":")[-1]
    pv = body["permissible_values"].get(pv_name)
    if pv and isinstance(pv, dict) and not pv.get("meaning"):
        pv["meaning"] = curie


def _ensure_prefixes(
    schema: dict,
    new_prefixes: dict[str, str],
) -> None:
    """Merge new prefix declarations into schema."""
    if "prefixes" not in schema:
        schema["prefixes"] = {}
    for pfx, uri in new_prefixes.items():
        if pfx not in schema["prefixes"]:
            schema["prefixes"][pfx] = uri


def _make_yaml():
    """Create a round-trip YAML serializer (or fallback to standard dump)."""
    try:
        from ruamel.yaml import YAML
        y = YAML()
        y.preserve_quotes = True
        y.default_flow_style = False
        return y
    except ImportError:
        return None


def _overlay_file(
    path: Path,
    mappings: MappingIndex,
    extra_prefixes: set[str],
) -> tuple[int, int]:
    """Apply overlay to one schema file. Return (elements_changed, links_added)."""
    YAML, CommentedMap, CommentedSeq = _get_ruamel_yaml()

    y = _make_yaml()
    with open(path, "r", encoding="utf-8") as f:
        if y:
            schema = y.load(f)
        else:
            schema = yaml.safe_load(f)
    if not isinstance(schema, dict):
        return 0, 0

    schema_prefixes = _discover_subject_prefixes(schema)
    schema_prefixes.update(extra_prefixes)

    rows_by_subject: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in mappings.rows:
        subject_id = row.get("subject_id", "")
        subject_prefix = subject_id.split(":", 1)[0]
        if subject_prefix in schema_prefixes:
            rows_by_subject[subject_id].append(row)

    if not rows_by_subject:
        return 0, 0

    elements_changed = 0
    total_links = 0
    new_prefixes: dict[str, str] = {}

    for section in ("classes", "slots", "enums", "types"):
        section_data = schema.get(section) or {}
        for elem_name, elem in section_data.items():
            if not isinstance(elem, dict):
                continue
            for subject_id, rows in rows_by_subject.items():
                local = subject_id.split(":", 1)[-1]
                if elem_name == local:
                    before = sum(len(elem.get(s) or []) for s in _MAPPING_SLOT_ORDER)
                    links = _merge_mappings(elem, rows, mappings.curie_map)
                    after = sum(len(elem.get(s) or []) for s in _MAPPING_SLOT_ORDER)
                    if links:
                        elements_changed += 1
                        total_links += links
                    for row in rows:
                        for pfx, uri in (row.get("curie_map") or "").split() if row.get("curie_map") else []:
                            if ":" in f"{pfx}:{uri}":
                                p, u = (f"{pfx}:{uri}").split(":", 1)
                                new_prefixes[p] = u

    _ensure_prefixes(schema, new_prefixes)

    if elements_changed:
        with open(path, "w", encoding="utf-8") as f:
            if y:
                y.dump(schema, f)
            else:
                f.write(yaml_dump_indented(schema, sort_keys=False))

    return elements_changed, total_links


def cmd_overlay(args: argparse.Namespace) -> int:
    """Apply SSSOM overlay subcommand."""
    if args.schema:
        if not args.schema.is_file():
            print(f"ERROR: schema {args.schema} is not a file", file=sys.stderr)
            return 1
        schemas = [args.schema]
    else:
        if not args.schema_dir.is_dir():
            print(
                f"ERROR: schema-dir {args.schema_dir} is not a directory",
                file=sys.stderr,
            )
            return 1
        schemas = sorted(args.schema_dir.glob("*.yaml"))
        modules_dir = args.schema_dir / "modules"
        if modules_dir.is_dir():
            schemas = sorted(schemas + list(modules_dir.glob("*.yaml")))
        extensions_dir = args.schema_dir / "extensions"
        if extensions_dir.is_dir():
            schemas = sorted(schemas + list(extensions_dir.rglob("*.yaml")))
        if not schemas:
            print(f"No YAML schemas in {args.schema_dir}", file=sys.stderr)
            return 1

    if not args.mappings_dir.is_dir():
        print(
            f"ERROR: mappings-dir {args.mappings_dir} is not a directory",
            file=sys.stderr,
        )
        return 1

    mappings = MappingIndex()
    mappings.load_from_dir(args.mappings_dir)
    if not mappings.rows:
        print(f"No mapping rows loaded from {args.mappings_dir}", file=sys.stderr)
        return 0

    extra_prefixes = {
        px.rstrip(":") for px in args.subject_prefix if px
    }

    files_changed = 0
    total_elements = 0
    total_links = 0
    for path in schemas:
        elements, links = _overlay_file(path, mappings, extra_prefixes)
        if elements:
            files_changed += 1
            total_elements += elements
            total_links += links
            print(f"  {path.name}: +{links} links across {elements} elements")

    if total_links:
        print(
            f"\nOverlay complete: {total_links} new mappings applied to "
            f"{total_elements} elements across {files_changed} files"
        )
    else:
        print(
            "\nOverlay complete: schemas already in sync with SSSOM files "
            "- no changes needed"
        )
    return 0


# ===========================================================================
# Subcommand: verify  (from scripts/verify_mappings.py)
# ===========================================================================

def _parse_sssom_tsv(path: Path) -> list[dict[str, str]]:
    """Return the SSSOM data rows (header comment lines and blanks are skipped)."""
    text_lines = [
        ln
        for ln in path.read_text().splitlines()
        if ln.strip() and not ln.lstrip().startswith("#")
    ]
    reader = csv.DictReader(
        io.StringIO("\n".join(text_lines)), delimiter="\t"
    )
    return [row for row in reader if row.get("subject_id")]


def _expected_mappings(
    rows: list[dict[str, str]],
) -> dict[str, dict[str, set[str]]]:
    """``{local_name: {field: {object_curie, ...}}}`` derived from TSV."""
    expected: dict[str, dict[str, set[str]]] = defaultdict(
        lambda: defaultdict(set)
    )
    for row in rows:
        predicate = row["predicate_id"]
        if predicate in IGNORED_PREDICATES:
            continue
        if predicate not in PREDICATE_TO_LINKML_SLOT:
            print(
                f"WARNING: unsupported predicate {predicate!r} "
                f"(subject={row['subject_id']})",
                file=sys.stderr,
            )
            continue
        local = row["subject_id"].split(":", 1)[-1]
        field = PREDICATE_TO_LINKML_SLOT[predicate]
        expected[local][field].add(row["object_id"])
    return expected


def _find_element(schema: dict, name: str) -> tuple[str, dict] | None:
    """Locate an element by local name in top-level sections + class attributes."""
    for section in ELEMENT_SECTIONS:
        element = (schema.get(section) or {}).get(name)
        if element is not None:
            return section, element
    for class_name, cls in (schema.get("classes") or {}).items():
        attrs = (cls or {}).get("attributes") or {}
        if name in attrs:
            return f"classes.{class_name}.attributes", attrs[name]
    return None


def _element_mappings(element: dict) -> dict[str, set[str]]:
    """Read mapping fields off a schema element."""
    return {
        field: set(element.get(field) or [])
        for field in PREDICATE_TO_LINKML_SLOT.values()
    }


def cmd_verify(args: argparse.Namespace) -> int:
    """Verify SSSOM mappings subcommand."""
    if not args.schema_dir.is_dir():
        print(
            f"ERROR: schema dir not found: {args.schema_dir}", file=sys.stderr
        )
        return 2
    if not args.mappings_dir.is_dir():
        print(
            f"ERROR: mappings dir not found: {args.mappings_dir}",
            file=sys.stderr,
        )
        return 2

    schemas_by_prefix: dict[str, list[tuple[Path, dict]]] = defaultdict(list)
    schema_files: list[Path] = sorted(args.schema_dir.rglob("*.yaml"))
    for path in schema_files:
        try:
            doc = yaml.safe_load(path.read_text())
        except yaml.YAMLError as exc:
            print(f"  WARN: failed to parse {path}: {exc}", file=sys.stderr)
            continue
        if not isinstance(doc, dict):
            continue
        prefix = doc.get("default_prefix")
        if not prefix:
            continue
        schemas_by_prefix[prefix].append((path, doc))

    if not schemas_by_prefix:
        print(
            f"ERROR: no schemas with default_prefix found under {args.schema_dir}",
            file=sys.stderr,
        )
        return 2

    print(
        f"Loaded {sum(len(v) for v in schemas_by_prefix.values())} schema(s) "
        f"across prefixes: {sorted(schemas_by_prefix)}"
    )

    overall_missing: list[str] = []
    overall_extra: list[str] = []
    overall_unknown: list[str] = []
    total_rows = 0

    for tsv in sorted(args.mappings_dir.glob("*.sssom.tsv")):
        rows = _parse_sssom_tsv(tsv)
        total_rows += len(rows)
        print(f"== {tsv.name} ({len(rows)} mappings) ==")

        by_prefix: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in rows:
            prefix = row["subject_id"].split(":", 1)[0]
            by_prefix[prefix].append(row)

        file_problems = 0
        for prefix, prefix_rows in by_prefix.items():
            candidate_schemas = schemas_by_prefix.get(prefix)
            if not candidate_schemas:
                msg = (
                    f"{tsv.name}: unknown subject prefix {prefix!r} "
                    f"(no schema has default_prefix: {prefix})"
                )
                overall_unknown.append(msg)
                print(f"  UNKNOWN-PREFIX: {msg}")
                file_problems += len(prefix_rows)
                continue

            expected = _expected_mappings(prefix_rows)
            for name, fields in sorted(expected.items()):
                located: list[tuple[Path, str, dict]] = []
                for schema_path, schema_doc in candidate_schemas:
                    found = _find_element(schema_doc, name)
                    if found is not None:
                        section, element = found
                        located.append((schema_path, section, element))
                if not located:
                    schema_names = ", ".join(p.name for p, _ in candidate_schemas)
                    msg = (
                        f"{tsv.name}: element {prefix}:{name!r} not found in any "
                        f"schema with default_prefix {prefix!r} ({schema_names})"
                    )
                    overall_unknown.append(msg)
                    print(f"  MISSING-ELEMENT: {msg}")
                    file_problems += 1
                    continue
                for schema_path, section, element in located:
                    actual = _element_mappings(element)
                    for field, exp_set in fields.items():
                        act_set = actual.get(field, set())
                        missing = exp_set - act_set
                        extra = act_set - exp_set
                        if missing:
                            msg = (
                                f"{schema_path.name}: {section}.{name}.{field} "
                                f"missing: {sorted(missing)}"
                            )
                            overall_missing.append(msg)
                            print(f"  MISSING: {msg}")
                            file_problems += 1
                        if extra and args.strict:
                            msg = (
                                f"{schema_path.name}: {section}.{name}.{field} "
                                f"extra (not in TSV): {sorted(extra)}"
                            )
                            overall_extra.append(msg)
                            print(f"  EXTRA: {msg}")
                            file_problems += 1
        if file_problems == 0:
            print(f"  OK")

    print()
    print(
        f"Summary: rows={total_rows} missing={len(overall_missing)} "
        f"extra={len(overall_extra)} unknown={len(overall_unknown)}"
    )
    if overall_missing or overall_unknown:
        print(
            "\nApply the missing mappings to the schema YAML, "
            "or remove the rows from the SSSOM TSV.",
            file=sys.stderr,
        )
        return 1
    if overall_extra and args.strict:
        return 2
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

    p_overlay = sub.add_parser(
        "overlay",
        help="Apply SSSOM mappings to LinkML schemas.",
    )
    src_overlay = p_overlay.add_mutually_exclusive_group()
    src_overlay.add_argument(
        "--schema-dir",
        type=Path,
        help="directory containing LinkML schema YAML files",
    )
    src_overlay.add_argument(
        "--schema",
        type=Path,
        help="single LinkML schema YAML file",
    )
    p_overlay.add_argument(
        "--mappings-dir",
        type=Path,
        required=True,
        help="directory containing *.sssom.tsv mapping files",
    )
    p_overlay.add_argument(
        "--subject-prefix",
        action="append",
        default=[],
        help="extra CURIE prefix (without colon) to treat as a subject-side "
        "match in addition to those discovered from each schema (repeatable)",
    )
    p_overlay.set_defaults(func=cmd_overlay)

    p_verify = sub.add_parser(
        "verify",
        help="Verify that schemas contain all SSSOM mappings.",
    )
    p_verify.add_argument(
        "--schema-dir",
        type=Path,
        default=REPO_ROOT / "src" / "dpv" / "schema",
        help="directory of LinkML schemas (recursively scanned)",
    )
    p_verify.add_argument(
        "--mappings-dir",
        type=Path,
        default=REPO_ROOT / "src" / "dpv" / "mappings",
        help="directory of *.sssom.tsv files",
    )
    p_verify.add_argument(
        "--strict",
        action="store_true",
        help="also fail when the schema has mappings that the TSV does not declare",
    )
    p_verify.set_defaults(func=cmd_verify)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
