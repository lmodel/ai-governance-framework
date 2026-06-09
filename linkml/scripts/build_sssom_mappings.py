#!/usr/bin/env python3
"""Populate FINOS → external-framework SSSOM TSVs from the normalised dumps.

Risks (``ri-N``) and mitigations (``mi-N``) are sourced from the FINOS
standalone Container dump at
``linkml/tests/data/finos/finos_ai_governance_framework_v2.yaml``:
each FINOS-scoped ``entries`` / ``actions`` / ``controls`` record
contributes its ``name`` (subject_label) plus the external citations in
its ``related_mappings`` slot. Use cases (``uc-N``) still fall back to
``docs/_usecases/uc-*.md`` front-matter because the dump's ``aitasks``
collection does not yet carry the ``related_mappings`` slot. For every
cited section, emits one SSSOM row (``skos:relatedMatch`` predicate,
``semapv:LLMBasedMatching`` justification) linking the FINOS
entity to the corresponding section in the matching standalone
Container dump under ``linkml/tests/data/finos/<dump_stem>.yaml``
(produced by :mod:`build_finos_data`).

The dump record is located by reconstructing its prefixed ``id`` from
the cited source id and the per-registry ``id_prefix`` (mirroring the
forward composition performed by :mod:`build_finos_data`), and the
``object_label`` column is taken from the dump's ``name`` slot. This
ensures cross-walks and standalone dumps stay in lock-step and that any
normalisation applied during the dump pass (canonical URLs, normalised
titles, etc.) is reflected in the SSSOM output, without requiring the
dumps to carry any non-schema slots.

This is the reproducible counterpart to :mod:`build_finos_data` for the
SSSOM concern: rerunning the script overwrites the data block of each
``linkml/src/ai_governance_framework/mappings/finos_to_<framework>.sssom.tsv``
byte-for-byte. The header block of each TSV (curie_map, mapping_set_id,
description, ...) is **also** reproducibly generated: if a TSV is missing,
a canonical skeleton (header + empty data block) is written from the
per-registry metadata before the data block is populated. Existing
headers are preserved verbatim across reruns to honour any downstream
edits that have been version-controlled.

Usage::

    python linkml/scripts/build_sssom_mappings.py [--repo-root PATH]

Dependencies: ``PyYAML``.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

DEFAULT_REPO_ROOT = Path(__file__).resolve().parent.parent.parent

_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_ID_RE = re.compile(r"^((?:ri|mi|uc)-\d+)")

# SSSOM constants applied to every emitted row.
PREDICATE_ID = "skos:relatedMatch"
MAPPING_JUSTIFICATION = "semapv:LLMBasedMatching"
AUTHOR_ID = "https://github.com/finos/ai-governance-framework"
MAPPING_DATE = "2026-06-04"

# Skeleton-header constants. The header block of every SSSOM TSV is
# reproducibly composed from these constants and the per-registry
# ``finos_path`` / ``extra_prefixes`` / ``description`` metadata. See
# :func:`_build_skeleton_header` for the exact line ordering, which must
# remain byte-stable so reruns are no-ops on disk.
FINOS_BASE_URI = "https://air-governance-framework.finos.org/"
SEMAPV_URI = "https://w3id.org/semapv/vocab/"
SKOS_URI = "http://www.w3.org/2004/02/skos/core#"
LICENSE_URI = "https://www.apache.org/licenses/LICENSE-2.0.html"
MAPPING_SET_VERSION = "0.1.0"
MAPPING_SET_ID_BASE = (
    "https://github.com/finos/ai-governance-framework/tree/main/"
    "linkml/src/ai_governance_framework/mappings/"
)

# One entry per FINOS framework citation slot. ``key`` matches the
# ``<key>_references`` front-matter slot name. ``tsv_stem`` names the
# SSSOM file under ``linkml/src/ai_governance_framework/mappings/``.
# ``object_prefix`` is the CURIE prefix used in the ``object_id`` column;
# the corresponding ``curie_map:`` entry must already exist in the TSV
# header block. ``upper_object`` controls whether section ids are
# upper-cased before emission (NIST control codes are conventionally
# upper-case; framework section keys mostly stay as-is). ``dump_stem``
# names the standalone Container dump file under
# ``linkml/tests/data/finos/<dump_stem>.yaml`` consulted for the
# ``object_label`` lookup. ``id_prefix`` is the string prepended (with a
# ``-`` separator) by :mod:`build_finos_data` to compose each dump
# record's ``id`` from the original source-file id; an empty string
# means dump ids equal source ids verbatim (NIST SP 800-53 controls).
FRAMEWORK_SSSOM_REGISTRY: list[dict[str, Any]] = [
    {
        "key": "iso-42001",
        "tsv_stem": "finos_to_iso42001",
        "object_prefix": "iso42001",
        "upper_object": False,
        "dump_stem": "iso_42001",
        "id_prefix": "iso-42001",
        "finos_path": "mitigations/",
        "object_uri": "https://w3id.org/lmodel/iso42001/",
        "description": (
            "FINOS AI Governance Framework mitigations (mi-N) to "
            "ISO/IEC 42001:2023 Annex A controls."
        ),
    },
    {
        "key": "nist-ai-600-1",
        "tsv_stem": "finos_to_nist_ai_600_1",
        "object_prefix": "nist_ai_600_1",
        "upper_object": False,
        "dump_stem": "nist_ai_600_1",
        "id_prefix": "nist-ai-600-1",
        "finos_path": "risks/",
        "object_uri": "https://w3id.org/lmodel/nist-ai-600-1/",
        "description": (
            "FINOS AI Governance Framework risks (ri-N) to NIST AI 600-1 "
            "GenAI Profile risks."
        ),
    },
    {
        "key": "nist-sp-800-53r5",
        "tsv_stem": "finos_to_nist_sp_800_53r5",
        "object_prefix": "nist_sp_800_53r5",
        "upper_object": True,
        "dump_stem": "nist_sp_800_53_r5",
        "id_prefix": "",
        "finos_path": "",
        "object_uri": "https://w3id.org/lmodel/nist_sp_800_53/",
        "description": (
            "FINOS AI Governance Framework mitigations (mi-N) and risks "
            "(ri-N) to NIST SP 800-53 Revision 5 security and privacy "
            "controls. Each row records that the FINOS catalogue entry "
            "cites the NIST control in its `nist-sp-800-53r5_references:` "
            "front-matter; relationship is `skos:relatedMatch` because "
            "FINOS mitigations are scoped to AI governance and NIST "
            "controls are general-purpose, so the alignment is "
            "associative rather than equivalent."
        ),
    },
    {
        "key": "eu-ai-act",
        "tsv_stem": "finos_to_eu_ai_act",
        "object_prefix": "eu_ai_act",
        "upper_object": False,
        "dump_stem": "eu_ai_act",
        "id_prefix": "eu-ai-act",
        "finos_path": "",
        "object_uri": "https://artificialintelligenceact.eu/article/",
        "description": (
            "FINOS AI Governance Framework risks (ri-N), mitigations "
            "(mi-N), and use cases (uc-N) to EU Artificial Intelligence "
            "Act articles, recitals, and annexes."
        ),
    },
    {
        "key": "sr11-7",
        "tsv_stem": "finos_to_sr_11_7",
        "object_prefix": "sr_11_7",
        "upper_object": False,
        "dump_stem": "sr_11_7",
        "id_prefix": "sr-11-7",
        "finos_path": "usecases/",
        "object_uri": "https://www.federalreserve.gov/supervisionreg/srletters/",
        "description": (
            "FINOS AI Governance Framework use cases (uc-N) and "
            "mitigations (mi-N) to Federal Reserve / OCC SR 11-7 "
            "(Supervisory Guidance on Model Risk Management) sections."
        ),
    },
    {
        "key": "ffiec-itbooklets",
        "tsv_stem": "finos_to_ffiec_it",
        "object_prefix": "ffiec_it",
        "upper_object": False,
        "dump_stem": "ffiec_it_handbook",
        "id_prefix": "ffiec-itbook",
        "finos_path": "",
        "object_uri": "https://ithandbook.ffiec.gov/it-booklets/",
        "description": (
            "FINOS AI Governance Framework risks (ri-N) and use cases "
            "(uc-N) to FFIEC IT Examination Handbook booklet sections."
        ),
    },
    {
        "key": "owasp-llm",
        "tsv_stem": "finos_to_owasp_llm",
        "object_prefix": "owasp_llm",
        "upper_object": False,
        "dump_stem": "owasp_llm_top_10",
        "id_prefix": "owasp-llm-top-10-2025",
        "finos_path": "mitigations/",
        "object_uri": (
            "https://owasp.org/"
            "www-project-top-10-for-large-language-model-applications/"
        ),
        "description": (
            "FINOS AI Governance Framework mitigations (mi-N) to OWASP "
            "LLM Top 10 (2025 edition)."
        ),
    },
    {
        "key": "owasp-ml",
        "tsv_stem": "finos_to_owasp_ml",
        "object_prefix": "owasp_ml",
        "upper_object": False,
        "dump_stem": "owasp_ml_top_10",
        "id_prefix": "owasp-ml-top-10-2023",
        "finos_path": "risks/",
        "object_uri": (
            "https://owasp.org/"
            "www-project-machine-learning-security-top-10/docs/"
        ),
        "description": (
            "FINOS AI Governance Framework risks (ri-N) to OWASP Machine "
            "Learning Security Top 10 (2023) entries."
        ),
    },
]

# Skeleton-only registry: SSSOM TSVs whose header block is reproducibly
# generated from this script but whose data rows are populated by some
# other process (manual curation, upstream import, etc.). Entries here
# only contribute to skeleton creation; ``populate_one`` never touches
# them. Each entry must supply ``tsv_stem``, ``finos_path``,
# ``extra_prefixes`` (mapping of additional CURIE prefix → URI for the
# ``curie_map:`` header block), and ``description``.
SKELETON_ONLY_REGISTRY: list[dict[str, Any]] = [
    {
        "tsv_stem": "finos_to_dpv_ai",
        "finos_path": "",
        "extra_prefixes": {
            "ai": "https://w3id.org/dpv/ai#",
            "risk": "https://w3id.org/dpv/risk#",
        },
        "description": (
            "FINOS AI Governance Framework risks (ri-N) and mitigations "
            "(mi-N) to W3C DPV-AI extension (ai:* and risk:* terms)."
        ),
    },
    {
        "tsv_stem": "finos_to_ibm_risk_atlas",
        "finos_path": "",
        "extra_prefixes": {
            "ibm_risk_atlas": (
                "https://ibm.github.io/ai-atlas-nexus/risk-atlas/"
            ),
        },
        "description": (
            "FINOS AI Governance Framework risks (ri-N) and mitigations "
            "(mi-N) to IBM Risk Atlas (ai-atlas-nexus) entries. Acts as "
            "a bridge enabling chained inference through the upstream "
            "IBM mapping sets (`ibm2owasp.tsv`, `ibm2nistgenai.tsv`, "
            "`mit-ai-risk-repository_ibm-risk-atlas.tsv`, "
            "`shieldgemma_risk_mappings.tsv`, `credo-ucf.sssom.tsv`, "
            "`ailuminate-v1.0.sssom.tsv`) vendored under "
            "`linkml/upstream-releases/ai-atlas-nexus/src/"
            "ai_atlas_nexus/data/mappings/`."
        ),
    },
]

COLUMN_HEADER = (
    "subject_id\tsubject_label\tpredicate_id\tobject_id\tobject_label\t"
    "mapping_justification\tauthor_id\tmapping_date\tcomment\n"
)


def _parse_front_matter(md_path: Path) -> dict[str, Any]:
    match = _FRONT_MATTER_RE.match(md_path.read_text(encoding="utf-8"))
    if not match:
        return {}
    fm = yaml.safe_load(match.group(1)) or {}
    return fm if isinstance(fm, dict) else {}


def _entity_id(md_path: Path) -> str | None:
    m = _ID_RE.match(md_path.name)
    return m.group(1) if m else None


def _numeric_key(p: Path) -> int:
    m = re.match(r"^[a-z]+-(\d+)", p.name)
    return int(m.group(1)) if m else 0


def _iter_usecase_posts(repo_root: Path):
    """Yield use-case markdown paths in deterministic numeric order.

    The FINOS standalone dump's ``aitasks`` collection does not (yet)
    carry the ``related_mappings`` slot, so use-case SSSOM rows are
    still sourced from ``docs/_usecases/uc-*.md`` front-matter. Risks
    and mitigations have switched to the normalised dump under
    ``linkml/tests/data/finos/finos_ai_governance_framework_v2.yaml``
    (see :func:`_load_finos_subject_index`).
    """
    docs = repo_root / "docs"
    for p in sorted(
        (docs / "_usecases").glob("uc-*.md"), key=_numeric_key
    ):
        yield p


def _load_dump_id_index(
    repo_root: Path, dump_stem: str
) -> dict[str, str]:
    """Return ``{record_id: name}`` indexed across all dump collections.

    Loads the standalone Container dump emitted by
    :mod:`build_finos_data` at
    ``linkml/tests/data/finos/<dump_stem>.yaml`` and walks every
    container collection. Records carrying both ``id`` and ``name`` are
    added to the returned index keyed by the dump's prefixed ``id``;
    the SSSOM builder reconstructs that prefixed id from each cited
    source section using the per-registry ``id_prefix``.

    The dump is the authoritative source for normalised titles
    (e.g. NIST control titles re-cased from PDF bookmark form) so the
    SSSOM rows reflect whatever the dump pass produced rather than the
    raw ``docs/_data/<key>.yml`` source. A missing dump raises so the
    failure mode is obvious (``run build_finos_data.py first``).
    """
    path = (
        repo_root
        / "linkml"
        / "tests"
        / "data"
        / "finos"
        / f"{dump_stem}.yaml"
    )
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found; run linkml/scripts/build_finos_data.py "
            f"first to emit the standalone Container dumps."
        )
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        return {}
    index: dict[str, str] = {}
    for collection_key in _DUMP_COLLECTION_KEYS:
        rows = loaded.get(collection_key) or []
        if not isinstance(rows, list):
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            rid = row.get("id")
            name = row.get("name")
            if isinstance(rid, str) and isinstance(name, str) and rid:
                index.setdefault(rid.strip(), name.strip())
    return index


# Container collection keys (matches
# build_finos_data._CONTAINER_COLLECTION_KEYS, plus ``rules`` and
# ``organizations`` which are emitted by the framework-specific dumps
# but not registered in the upstream Container check). Each holds a
# list of records that may carry ``id`` + ``name`` slots.
_DUMP_COLLECTION_KEYS: tuple[str, ...] = (
    "documents",
    "taxonomies",
    "vocabularies",
    "groups",
    "entries",
    "actions",
    "aitasks",
    "stakeholders",
    "controls",
    "rules",
    "organizations",
)

# Taxonomy id identifying FINOS-owned Risk / Action / RiskControl
# records in the standalone Container dump. Records carrying any other
# ``isDefinedByTaxonomy`` value are external (IBM, OWASP, etc.) and
# must not surface as SSSOM subjects.
_FINOS_TAXONOMY_ID = "finos-ai-governance-framework-v2"

# Standalone Container dump consulted for FINOS Risk / Action /
# RiskControl subject records (and their ``related_mappings`` slot).
_FINOS_DUMP_STEM = "finos_ai_governance_framework_v2"


def _air_sequence(air_id: str) -> int:
    """Return the numeric suffix of an AIR-style id (``AIR-RC-001`` -> 1)."""
    try:
        return int(air_id.rsplit("-", 1)[-1])
    except (ValueError, AttributeError):
        return 0


def _load_finos_subject_index(
    repo_root: Path,
) -> dict[str, list[dict[str, Any]]]:
    """Return FINOS Risk / Mitigation subject records from the dump.

    Loads ``linkml/tests/data/finos/finos_ai_governance_framework_v2.yaml``
    and groups its FINOS-scoped records by legacy SSSOM subject prefix:

    * ``"ri"`` -> ``entries`` rows with ``type == 'Risk'``
    * ``"mi"`` -> union of ``actions`` and ``controls`` rows

    Each list is sorted by the numeric suffix of the AIR id so the
    emitted SSSOM rows preserve the same risk-then-mitigation, sorted
    by sequence ordering that the previous filename-driven
    implementation produced. Only records whose
    ``isDefinedByTaxonomy`` matches :data:`_FINOS_TAXONOMY_ID` are
    included, which excludes vendored upstream catalogues (IBM Risk
    Atlas, OWASP, etc.) that share the dump.

    The dump is produced by :mod:`build_finos_data`; a missing file
    raises so the failure mode points at the right reproducible step.
    """
    path = (
        repo_root
        / "linkml"
        / "tests"
        / "data"
        / "finos"
        / f"{_FINOS_DUMP_STEM}.yaml"
    )
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found; run linkml/scripts/build_finos_data.py "
            f"first to emit the FINOS standalone Container dump."
        )
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        return {"ri": [], "mi": []}

    def _finos_rows(
        key: str, want_type: str | None = None
    ) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for row in loaded.get(key) or []:
            if not isinstance(row, dict):
                continue
            if row.get("isDefinedByTaxonomy") != _FINOS_TAXONOMY_ID:
                continue
            if want_type is not None and row.get("type") != want_type:
                continue
            if not isinstance(row.get("id"), str):
                continue
            out.append(row)
        return out

    risks = sorted(
        _finos_rows("entries", want_type="Risk"),
        key=lambda r: _air_sequence(r["id"]),
    )
    mitigations = sorted(
        _finos_rows("actions") + _finos_rows("controls"),
        key=lambda r: _air_sequence(r["id"]),
    )
    return {"ri": risks, "mi": mitigations}


def _strip_id_prefix(dump_id: str, id_prefix: str) -> str:
    """Reverse :func:`build_finos_data._compose_framework_ref_id`.

    The dump stores each cross-walk citation as ``{id_prefix}-{src_id}``
    (NIST SP 800-53 is the exception: no prefix at all). To project a
    dump id back into the unprefixed source id used in the SSSOM
    ``object_id`` column we strip the framework prefix when present.
    """
    if not id_prefix:
        return dump_id
    needle = f"{id_prefix}-"
    if dump_id.startswith(needle):
        return dump_id[len(needle):]
    return dump_id


def _iter_subject_rows(
    repo_root: Path,
    key: str,
    entry: dict[str, Any],
    dump_index: dict[str, str],
    finos_subjects: dict[str, list[dict[str, Any]]],
):
    """Yield ``(subject_id, subject_label, [section_id, ...])`` tuples.

    Risks (``ri-N``) and mitigations (``mi-N``) are sourced from the
    FINOS standalone dump's ``entries`` / ``actions`` / ``controls``
    collections: each subject's external cross-walks are recovered
    from its ``related_mappings`` slot, filtered to the ids present in
    ``dump_index`` (i.e. those that belong to the current framework's
    dump), and projected back to unprefixed source ids via
    :func:`_strip_id_prefix`.

    Use cases (``uc-N``) are still sourced from
    ``docs/_usecases/uc-*.md`` front-matter because the dump's
    ``aitasks`` collection does not yet carry the ``related_mappings``
    slot; switching that path requires a corresponding change in
    :mod:`build_finos_data`. Subject ids in every yielded tuple are
    the AIR-style ids that also appear in the standalone dumps
    (``AIR-RC-001``, ``AIR-PREV-002``, ``UC-002``); the legacy
    ``ri-N`` / ``mi-N`` / ``uc-N`` filenames are not surfaced.
    """
    id_prefix = entry["id_prefix"]
    for prefix in ("ri", "mi"):
        for record in finos_subjects.get(prefix, []):
            sid = record["id"]
            slbl = str(record.get("name") or sid).strip()
            section_ids = [
                _strip_id_prefix(ref, id_prefix)
                for ref in (record.get("related_mappings") or [])
                if isinstance(ref, str) and ref in dump_index
            ]
            if section_ids:
                yield sid, slbl, section_ids

    slot = f"{key}_references"
    for post in _iter_usecase_posts(repo_root):
        fm = _parse_front_matter(post)
        refs = fm.get(slot) or []
        if not isinstance(refs, list):
            continue
        legacy = _entity_id(post)
        if not legacy:
            continue
        # Mirror build_finos_data._air_usecase_id: ``uc-N`` -> ``UC-NNN``.
        sid = f"UC-{int(legacy.split('-', 1)[1]):03d}"
        slbl = str(fm.get("title", sid)).strip().strip('"')
        section_ids = [
            raw.strip()
            for raw in refs
            if isinstance(raw, str) and raw.strip()
        ]
        if section_ids:
            yield sid, slbl, section_ids


def _entry_extra_prefixes(entry: dict[str, Any]) -> dict[str, str]:
    """Return the framework-specific CURIE prefixes for ``entry``.

    For full registry entries the framework contributes a single
    ``object_prefix`` → ``object_uri`` mapping. Skeleton-only entries
    declare their own (possibly multi-key) ``extra_prefixes`` map
    instead. Either shape is normalised here so
    :func:`_build_skeleton_header` can render both uniformly.
    """
    if "extra_prefixes" in entry:
        return dict(entry["extra_prefixes"])
    return {entry["object_prefix"]: entry["object_uri"]}


def _build_skeleton_header(entry: dict[str, Any]) -> str:
    """Return the canonical SSSOM header block for ``entry``.

    The header is composed deterministically from the per-registry
    metadata so reruns of the script are byte-stable. Line ordering
    matches the existing hand-authored TSVs (curie_map first, then
    metadata fields in alphabetical order; within ``curie_map`` the
    ``finos`` prefix comes first, framework-specific prefixes follow in
    alphabetical order, and ``semapv`` + ``skos`` close the block).
    """
    finos_uri = FINOS_BASE_URI + entry.get("finos_path", "")
    extras = _entry_extra_prefixes(entry)
    lines: list[str] = ["# curie_map:\n", f"#   finos: {finos_uri}\n"]
    for prefix in sorted(extras):
        lines.append(f"#   {prefix}: {extras[prefix]}\n")
    lines.append(f"#   semapv: {SEMAPV_URI}\n")
    lines.append(f"#   skos: {SKOS_URI}\n")
    lines.append(f"# license: {LICENSE_URI}\n")
    lines.append(f"# mapping_date: '{MAPPING_DATE}'\n")
    lines.append(
        f"# mapping_set_description: {entry['description']}\n"
    )
    mapping_set_id = (
        f"{MAPPING_SET_ID_BASE}{entry['tsv_stem']}.sssom.tsv"
    )
    lines.append(f"# mapping_set_id: {mapping_set_id}\n")
    lines.append(f"# mapping_set_version: {MAPPING_SET_VERSION}\n")
    return "".join(lines)


def _tsv_path_for(repo_root: Path, tsv_stem: str) -> Path:
    return (
        repo_root
        / "linkml"
        / "src"
        / "ai_governance_framework"
        / "mappings"
        / f"{tsv_stem}.sssom.tsv"
    )


def _ensure_skeleton_tsv(
    tsv_path: Path, entry: dict[str, Any]
) -> bool:
    """Create ``tsv_path`` with a freshly generated skeleton if missing.

    Returns True if the file was created, False if it already existed.
    Parent directories are created on demand so the script works on a
    clean checkout.
    """
    if tsv_path.exists():
        return False
    tsv_path.parent.mkdir(parents=True, exist_ok=True)
    tsv_path.write_text(
        _build_skeleton_header(entry) + COLUMN_HEADER, encoding="utf-8"
    )
    return True


def _read_header_block(
    tsv_path: Path, entry: dict[str, Any]
) -> str:
    """Return the leading ``#``-prefixed comment lines from the TSV.

    If ``tsv_path`` does not exist, a canonical skeleton is written
    first from ``entry`` (see :func:`_build_skeleton_header`) so the
    SSSOM mappings tree is reproducibly bootstrappable from an empty
    state. Any subsequent edits to existing headers are preserved on
    rerun — only missing files are (re)created.
    """
    _ensure_skeleton_tsv(tsv_path, entry)
    header_lines: list[str] = []
    for line in tsv_path.read_text(encoding="utf-8").splitlines(True):
        if line.startswith("#"):
            header_lines.append(line)
        else:
            break
    return "".join(header_lines)


def populate_one(
    repo_root: Path,
    entry: dict[str, Any],
    finos_subjects: dict[str, list[dict[str, Any]]] | None = None,
) -> tuple[Path, int]:
    """Rewrite the data block of one SSSOM TSV. Header is preserved.

    ``finos_subjects`` is the cached output of
    :func:`_load_finos_subject_index`; pass ``None`` to load lazily
    (convenient for ad-hoc / one-off invocations).
    """
    key = entry["key"]
    tsv_path = _tsv_path_for(repo_root, entry["tsv_stem"])
    header = _read_header_block(tsv_path, entry)
    dump_index = _load_dump_id_index(repo_root, entry["dump_stem"])
    if finos_subjects is None:
        finos_subjects = _load_finos_subject_index(repo_root)
    prefix_cur = entry["object_prefix"]
    upper = entry["upper_object"]
    id_prefix = entry["id_prefix"]

    rows: list[str] = []
    for sid, slbl, section_ids in _iter_subject_rows(
        repo_root, key, entry, dump_index, finos_subjects
    ):
        for section_id in section_ids:
            dump_id = (
                f"{id_prefix}-{section_id}" if id_prefix else section_id
            )
            obj_label = dump_index.get(dump_id, section_id)
            obj_id = section_id.upper() if upper else section_id
            rows.append(
                f"finos:{sid}\t{slbl}\t{PREDICATE_ID}\t"
                f"{prefix_cur}:{obj_id}\t{obj_label}\t"
                f"{MAPPING_JUSTIFICATION}\t{AUTHOR_ID}\t{MAPPING_DATE}\t\n"
            )

    tsv_path.write_text(header + COLUMN_HEADER + "".join(rows), encoding="utf-8")
    return tsv_path, len(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help="Repository root (defaults to two levels above this script).",
    )
    args = parser.parse_args(argv)

    skeletons_created = 0
    for entry in SKELETON_ONLY_REGISTRY:
        path = _tsv_path_for(args.repo_root, entry["tsv_stem"])
        if _ensure_skeleton_tsv(path, entry):
            rel = path.relative_to(args.repo_root)
            print(f"Created skeleton SSSOM TSV {rel}")
            skeletons_created += 1

    finos_subjects = _load_finos_subject_index(args.repo_root)

    totals = 0
    for entry in FRAMEWORK_SSSOM_REGISTRY:
        path = _tsv_path_for(args.repo_root, entry["tsv_stem"])
        existed_before = path.exists()
        path, n = populate_one(args.repo_root, entry, finos_subjects)
        rel = path.relative_to(args.repo_root)
        if not existed_before:
            print(f"Created skeleton SSSOM TSV {rel}")
            skeletons_created += 1
        print(f"Wrote {n:>3} mapping rows to {rel}")
        totals += n
    print(
        f"Total: {totals} SSSOM mapping rows across "
        f"{len(FRAMEWORK_SSSOM_REGISTRY)} framework TSVs "
        f"({skeletons_created} skeleton TSV(s) created this run)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
