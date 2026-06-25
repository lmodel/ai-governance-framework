#!/usr/bin/env python3
"""Generate `ai-risk-ontology`-shaped data from the FINOS Jekyll corpus.

Sole data-generation script for the FINOS AI Governance Framework LinkML
project. Reads the authoritative FINOS documents under

  * ``docs/_risks/ri-*.md``
  * ``docs/_mitigations/mi-*.md``
  * ``docs/_usecases/uc-*.md``

and emits native ``ai-risk-ontology`` instances (``Container``, ``Risk``,
``Action``, ``AiSystem``, ``Documentation``, ``RiskGroup``,
``RiskTaxonomy``) that validate against the umbrella schema at
``linkml/src/ai_governance_framework/schema/ai_governance_framework.yaml``
and are directly importable into upstream ai-atlas-nexus.

Outputs (paths relative to the repository root)::

  linkml/tests/data/finos/finos_ai_governance_framework_v2.yaml
      Canonical full catalogue (Container root: documents, taxonomies,
      groups, entries=Risk+AiSystem, actions=Action). One per FINOS
      Jekyll release; importable upstream as-is.

  linkml/tests/data/valid/<ClassName>-<id>.yaml
      Per-class single-instance fixtures consumed by
      ``linkml/tests/test_data.py`` (stem prefix == upstream class name).

  linkml/tests/data/invalid/<ClassName>-<reason>.yaml
      Deliberately broken fixtures exercising upstream schema
      constraints (missing required ``id``, wrong scalar type for a
      multivalued slot, list passed to single-valued ``isPartOf``).

FINOS Jekyll front-matter -> ai-risk-ontology slot mapping::

    filename id (ri-N / mi-N / uc-N)  -> id
    title                              -> name
    first body paragraph               -> description
    type: (RC/SEC/OP/GOV) on ri-*      -> Risk.isPartOf -> RiskGroup id
    type: (PREV/DET/RESP) on mi-*      -> Action.isCategorizedAs ->
                                          RiskControlGroup id (one
                                          ``RiskControlGroup`` emitted
                                          per kind actually used)
    mitigates: on mi-*                 -> Action.hasRelatedRisk
    related_risks: on uc-*             -> AiSystem.hasRelatedRisk
    end_user: on uc-*                  -> AiSystem.hasStakeholder ->
                                          one ``Stakeholder`` per
                                          comma-separated role in
                                          ``Container.stakeholders:``
    data_handling_aspects: on uc-*     -> AiSystem.isCategorizedAs ->
                                          per-aspect Documentation
                                          children of
                                          ``deployment-data-handling``
                                          parent
    further_reading[*].name            -> Documentation.name
    further_reading[*].url             -> Documentation.url
    further_reading[*].source          -> Documentation.author
    <framework>_references[*]          -> Documentation per cited section
                                          (name/url/author from
                                          docs/_data/<framework>.yml;
                                          isCategorizedAs links to the
                                          framework's parent Documentation)
    data_classifications[*].name       -> Term per classification under
                                          taxonomy ``finos-ai-governance-
                                          framework-v2``
                                          (description/url from
                                          docs/_data/data_classification.yml;
                                          isCategorizedAs links to a
                                          ``sensitivity-<tier>`` Term under
                                          the ``finos-data-sensitivity-tiers``
                                          Vocabulary)
    regulatory_concerns[*]             -> inline Documentation per concern

The script is reproducible: rerunning it overwrites the generated files
byte-for-byte. Only the FINOS Jekyll corpus is consulted; nothing is
downloaded.

Usage::

    python linkml/scripts/build_finos_data.py [--repo-root PATH] [--output PATH]

Dependencies: ``PyYAML`` (front-matter parsing), ``ruamel.yaml`` (block-style
emission with consistent indentation).
"""

from __future__ import annotations

import argparse
from datetime import date
import io
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml
from ruamel.yaml import YAML as _RUAMEL_YAML
from ruamel.yaml.scalarstring import FoldedScalarString, LiteralScalarString

# -----------------
# Constants
# -----------------

DEFAULT_REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Front-matter delimiter used by Jekyll.
_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# Extract the leading id (``ri-1``, ``mi-12``, ``uc-2``) from filenames such
# as ``ri-1_information-leaked-to-hosted-model.md``.
_ID_RE = re.compile(r"^(?P<id>(?:ri|mi|uc)-\d+)(?:_|\.)")

# Permitted RiskKind tokens. Each token must have a corresponding RiskGroup
# instance in the emitted catalogue; FINOS ``Risk.isPartOf`` then references
# that group id. This is the structural replacement for an enum
# (`equals_string_in:`) on the schema side.
VALID_RISK_TYPES = {"RC", "SEC", "OP", "GOV"}

# Permitted ActionKind tokens for mitigations (front-matter ``type:`` on
# ``mi-*.md``). Mirrors the Risk taxonomy treatment: each token used in the
# corpus materialises a ``RiskControlGroup`` instance, and every Action gets
# ``isCategorizedAs: [<control-group-id>]`` linking it to its group.
# (Upstream ``Action`` has no ``isPartOf`` slot, so ``isCategorizedAs`` —
# which ``Entity`` carries and ``range: Any`` accepts — is the correct
# vehicle for the relationship; a future upstream fix to add
# ``Action.isPartOf: range RiskControlGroup`` would let this swap to
# ``isPartOf`` without restructuring the catalogue.)
VALID_ACTION_KINDS = {"PREV", "DET", "RESP"}

# Catalogue-level identity.
TAXONOMY_ID = "finos-ai-governance-framework-v2"
TAXONOMY_NAME = "FINOS AI Governance Framework v2"
TAXONOMY_URL = "https://air-governance-framework.finos.org/"
TAXONOMY_DESCRIPTION = (
    "Financial-services-focused AI risk taxonomy and control catalogue "
    "published by the FINOS AI Readiness project. Covers AI risks, "
    "mitigations and use cases relevant to regulated financial institutions."
)

# Human-readable expansions of the FINOS RiskKind tokens.
RISK_KIND_LABELS: dict[str, str] = {
    "RC": "Regulatory & Compliance",
    "SEC": "Security",
    "OP": "Operational",
    "GOV": "Governance",
}

# Human-readable expansions of the FINOS ActionKind tokens (mitigation
# ``type:`` front-matter values; mirrored in ``docs/index.md``'s
# ``mitigation_order:`` for rendering).
ACTION_KIND_LABELS: dict[str, str] = {
    "PREV": "Preventive",
    "DET": "Detective",
    "RESP": "Responsive",
}

# Human-readable labels for the four FINOS data-classification sensitivity
# tiers (``docs/_data/data_classification.yml``). Each tier materialises one
# ``Term`` (id: ``sensitivity-<tier>``) under the
# ``finos-data-sensitivity-tiers`` ``Vocabulary``; data-classification
# Terms reference it via ``isCategorizedAs``. Modelled as ``Term`` rather
# than ``Documentation`` because a sensitivity tier is a classification
# concept (skos:Concept), not a documented standard.
SENSITIVITY_LABELS: dict[str, str] = {
    "Critical": "Critical sensitivity",
    "High": "High sensitivity",
    "Medium": "Medium sensitivity",
    "Low": "Low sensitivity",
}

# Human-readable labels for jurisdictions cited in
# ``docs/_data/data_classification.yml`` reference entries.
# Authoritative source: ``docs/_data/finos-jurisdictions.yml``
# (loaded lazily by :meth:`DocRegistry.ensure_jurisdiction`); this
# constant is kept as a fallback label map (and for static lookups
# in description text) so legacy rows render even if the YAML is
# absent.
#
# Each cited code materialises:
#   - one ``Term`` (id: ``jurisdiction-<code-slug>``) under the
#     ``finos-jurisdictions`` ``Vocabulary`` (skos:Concept in a
#     skos:ConceptScheme), and
#   - a typed ``hasJurisdiction: [<code>]`` slot on the regulatory-
#     reference ``Documentation`` row (FINOS-local extension of the
#     ai-atlas-nexus ``Jurisdiction`` enum + slot; see
#     ISSUE-nexus.md G29 for the upstream proposal).
#
# The Term-on-Vocabulary view supports human navigation; the typed
# slot supports machine-readable cross-jurisdiction filtering and
# graph queries. The two views must stay in lock-step.
JURISDICTION_LABELS: dict[str, str] = {
    "US": "United States",
    "EU": "European Union",
    "UK": "United Kingdom",
    "International": "International",
}

# Vocabulary ids for the FINOS classification-concept vocabularies
# emitted alongside ``finos-ai-governance-framework-v2``.
#
# * ``finos-data-sensitivity-tiers`` — closed enum of the four
#   sensitivity tiers (Critical / High / Medium / Low) from
#   ``docs/_data/data_classification.yml``. Each tier materialises
#   one ``Term`` via :meth:`DocRegistry.ensure_sensitivity_tier`.
#
# * ``finos-jurisdictions`` — closed enum of the four legal/political
#   jurisdictions cited in regulatory ``references[*].jurisdiction:``
#   entries, sourced from ``docs/_data/finos-jurisdictions.yml``.
#   Each code materialises one ``Term`` via
#   :meth:`DocRegistry.ensure_jurisdiction`.
SENSITIVITY_VOCAB_ID = "finos-data-sensitivity-tiers"
JURISDICTION_VOCAB_ID = "finos-jurisdictions"

# Sentinel id prefixes for one-per-code Term rows.
SENSITIVITY_PARENT_PREFIX = "sensitivity"
JURISDICTION_PARENT_PREFIX = "jurisdiction"

# FINOS AI Deployment Model — sourced from
# ``docs/_data/ai_deployment_model.yml``. One ``RiskTaxonomy``
# umbrella, one ``RiskGroup`` per axis (7 axes), and one ``Term``
# per leaf (38 leaves). Use-case ``data_handling_aspects:``
# front-matter resolves to the ``data_handling`` axis Term ids
# (replacing the pre-2026-06 ``deployment-data-handling-*``
# Documentation hack).
DEPLOYMENT_TAXONOMY_ID = "finos-ai-deployment-model"
DEPLOYMENT_TAXONOMY_NAME = "FINOS AI Deployment Model"
DEPLOYMENT_TAXONOMY_DESCRIPTION = (
    "FINOS-published seven-axis facet taxonomy for classifying AI "
    "deployments across financial services. The axes are: AI type, "
    "architecture pattern, deployment type, data handling, regulatory "
    "alignment, operational model, and integration pattern."
)
DEPLOYMENT_TAXONOMY_URL = (
    "https://github.com/finos/ai-governance-framework/"
    "blob/main/docs/_data/ai_deployment_model.yml"
)
# Front-matter slot name on use-case markdown files cited as a
# back-compat alias for the ``data_handling`` axis of the
# deployment model. Each cited token resolves to a deployment-model
# Term id under the ``data_handling`` axis.
DEPLOYMENT_DATA_HANDLING_AXIS = "data_handling"

FINOS_DOC_ID = "finos-ai-governance-framework-site"

# Stable id for the FINOS AI use-case taxonomy (sourced from
# ``docs/_data/ai_use_cases.yml``). One ``AiTaskTaxonomy`` row +
# one ``AiTaskDomain`` per Level-1 sector + one ``AiTaskGroup`` per
# Level-2 subcategory + one ``AiTask`` per Level-3 leaf. The full
# three-level hierarchy is materialised as proper grouping nodes
# (post ai-atlas-nexus #190 / G30); the leaf ``AiTask`` rows
# additionally keep the breadcrumb in ``description`` for human
# readability.
AI_UC_TAXONOMY_ID = "finos-ai-use-cases-v1"

# Stable id for the FINOS cross-cutting AI capabilities taxonomy.
# Sourced from the ``cross_cutting_capabilities:`` list in
# ``docs/_data/ai_use_cases.yml``. One ``CapabilityTaxonomy`` + one
# ``CapabilityGroup`` + one ``Capability`` per item.
AI_CAPS_TAXONOMY_ID = "finos-ai-capabilities-v1"
AI_CAPS_CROSSCUTTING_GROUP_ID = "finos-cross-cutting-capabilities"

# Pre-G28 the ``category:`` slot on uc-*.md front-matter was wired
# into the AiSystem via ``isCategorizedAs: [<AI_UC_TAXONOMY_ID>]``
# (a lightweight anchor to the use-case taxonomy). Now (post
# ai-atlas-nexus #188 / G28) each ``category:`` materialises a
# proper ``Domain`` Entry (id: ``domain-<slug>``) and the AiSystem
# carries it via ``isAppliedWithinDomain``. The constant is kept
# only as a backwards-compatibility alias for any out-of-tree
# callers; the builder itself no longer uses it.
CATEGORY_TAXONOMY_ID = AI_UC_TAXONOMY_ID

# NIST SP 800-53 Rev. 5 native-AIRO controls catalogue. Emitted as a
# standalone Container-shaped file (``linkml/tests/data/finos/
# nist_sp_800_53_r5.yaml``) alongside the FINOS catalogue: 1
# ``RiskControlGroupTaxonomy`` + 1 ``Documentation`` + one
# ``RiskControl`` per row in ``docs/_data/nist-sp-800-53r5.yml``.
# Independent of the FINOS-side ``ref-nist-sp-800-53r5-*``
# ``Documentation`` rows emitted via ``_FRAMEWORK_REGISTRY`` —
# cross-walks between the two are owned by the SSSOM TSV at
# ``linkml/src/ai_governance_framework/mappings/
# finos_to_nist_sp_800_53r5.sssom.tsv``.
NIST_SP_800_53R5_TAXONOMY_ID = "nist-sp-800-53r5"
NIST_SP_800_53R5_TAXONOMY_NAME = "NIST Special Publication 800-53 Revision 5"
NIST_SP_800_53R5_TAXONOMY_DESCRIPTION = (
    "Security and Privacy Controls for Information Systems and Organizations"
)
NIST_SP_800_53R5_TAXONOMY_URL = "https://doi.org/10.6028/NIST.SP.800-53r5"
NIST_SP_800_53R5_TAXONOMY_VERSION = "1"
# Document id is suffixed with ``-doc`` to avoid colliding with the
# taxonomy id (the ai-atlas-nexus loader merges records globally by id).
NIST_SP_800_53R5_DOC_ID = "nist-sp-800-53r5-doc"
NIST_SP_800_53R5_DOC_NAME = "SP 800-53 Controls"
NIST_SP_800_53R5_DOC_DESCRIPTION = (
    "SP 800-53 Controls and SP 800-53B Control Baselines Resources for "
    "Implementers"
)
NIST_SP_800_53R5_DOC_URL = (
    "https://csrc.nist.gov/projects/risk-management/sp800-53-controls"
)
NIST_SP_800_53R5_OSCAL_DOC_ID = "nist-sp-800-53r5-oscal-catalog"
NIST_SP_800_53R5_OSCAL_DOC_NAME = (
    "Electronic (OSCAL) Version of NIST SP 800-53 Rev 5.2.0 Controls and "
    "SP 800-53A Rev 5.2.0 Assessment Procedures"
)
NIST_SP_800_53R5_OSCAL_DOC_DESCRIPTION = (
    "NIST is maintaining OSCAL content for multiple revisions of the NIST "
    "Special Publication (SP) 800-53. The XML, JSON, and YAML versions of "
    "SP800-53 given here are derived from the NIST publications. The OSCAL "
    "XML, JSON, and YAML variants are all equivalent in their information "
    "content and are provided to support tooling on different "
    "format-specific implementation stacks. These OSCAL files are intended "
    "to faithfully represent the control-related content from the published "
    "documents in machine-readable formats."
)
NIST_SP_800_53R5_OSCAL_DOC_URL = (
    "https://github.com/usnistgov/oscal-content/tree/release-1.4/"
    "nist.gov/SP800-53/rev5"
)

# Small words lowercased after the leading prefix is stripped from a
# NIST control title (``AC-1 Policy And Procedures`` ->
# ``Policy and Procedures``). Source titles are derived from PDF
# bookmarks and use uppercase ``And``/``Or``/etc.
_TITLE_SMALL_WORDS = frozenset({
    "a", "an", "and", "at", "by", "for", "from", "in", "of",
    "on", "or", "the", "to", "with",
})


# -----------------
# External-standard reference catalogues
# -----------------
# Seven external standards cited in FINOS front-matter ``<key>_references:``
# slots are emitted as standalone ai-risk-ontology Container files alongside
# the FINOS catalogue, mirroring the existing NIST SP 800-53r5 pattern. Each
# file is independent of the FINOS-side ``ref-<key>-*`` ``Documentation``
# rows; cross-walks are owned by the SSSOM TSVs under
# ``linkml/src/ai_governance_framework/mappings/``.
#
# Outputs (under ``linkml/tests/data/finos/``):
#   * ``eu_ai_act.yaml``
#   * ``ffiec_it_handbook.yaml``
#   * ``iso_42001.yaml``
#   * ``nist_ai_600_1.yaml``
#   * ``owasp_llm_top_10.yaml``
#   * ``owasp_ml_top_10.yaml``
#   * ``sr_11_7.yaml``
#
# Purpose:
#   1. test data for ``just test`` (round-trips through the umbrella schema)
#   2. candidates for upstream contribution into
#      ``IBM/ai-atlas-nexus/src/ai_atlas_nexus/data/knowledge_graph/``
#      as native reference data.

# --- EU AI Act ---
EU_AI_ACT_TAXONOMY_ID = "eu-ai-act"
EU_AI_ACT_TAXONOMY_NAME = (
    "Regulation (EU) 2024/1689 (EU Artificial Intelligence Act)"
)
EU_AI_ACT_TAXONOMY_DESCRIPTION = (
    "Regulation of the European Parliament and of the Council laying down "
    "harmonised rules on artificial intelligence (Artificial Intelligence "
    "Act). Indexed by article via the AI Act Explorer."
)
EU_AI_ACT_TAXONOMY_VERSION = "2024"
EU_AI_ACT_DOC_ID = "eu-ai-act-explorer"
EU_AI_ACT_DOC_NAME = "EU AI Act Explorer"
EU_AI_ACT_DOC_DESCRIPTION = (
    "Searchable, article-by-article index of Regulation (EU) 2024/1689 "
    "(EU AI Act) maintained by the Future of Life Institute."
)
EU_AI_ACT_DOC_URL = "https://artificialintelligenceact.eu/"

# --- FFIEC IT Examination Handbook ---
FFIEC_IT_TAXONOMY_ID = "ffiec-it-handbook"
FFIEC_IT_TAXONOMY_NAME = "FFIEC Information Technology Examination Handbook"
FFIEC_IT_TAXONOMY_DESCRIPTION = (
    "Federal Financial Institutions Examination Council Information "
    "Technology Examination Handbook, organised into topical booklets "
    "(Architecture/Infrastructure/Operations, Management, Audit, Business "
    "Continuity Management, Development & Acquisition, Outsourcing, Retail "
    "Payment Systems, Information Security, Supervision of Technology "
    "Service Providers, Wholesale Payment Systems)."
)
FFIEC_IT_TAXONOMY_VERSION = "current"
FFIEC_IT_DOC_ID = "ffiec-it-handbook-landing"
FFIEC_IT_DOC_NAME = "FFIEC IT Examination Handbook"
FFIEC_IT_DOC_DESCRIPTION = (
    "Landing page for the FFIEC Information Technology Examination "
    "Handbook, listing all booklets."
)
FFIEC_IT_DOC_URL = "https://ithandbook.ffiec.gov/"

# --- ISO/IEC 42001:2023 ---
ISO_42001_TAXONOMY_ID = "iso-42001"
ISO_42001_TAXONOMY_NAME = (
    "ISO/IEC 42001:2023 \u2014 Artificial Intelligence Management Systems"
)
ISO_42001_TAXONOMY_DESCRIPTION = (
    "International standard specifying requirements for establishing, "
    "implementing, maintaining and continually improving an AI Management "
    "System (AIMS) within organizations. Indexed by Annex A control."
)
ISO_42001_TAXONOMY_VERSION = "2023"
ISO_42001_DOC_ID = "iso-42001-landing"
ISO_42001_DOC_NAME = "ISO/IEC 42001:2023 standard page"
ISO_42001_DOC_DESCRIPTION = (
    "ISO catalogue landing page for ISO/IEC 42001:2023 \u2014 Information "
    "technology \u2014 Artificial intelligence \u2014 Management system."
)
ISO_42001_DOC_URL = "https://www.iso.org/standard/81230.html"

# --- NIST AI 600-1 (Generative AI Profile) ---
# Canonical URL per upstream guidance: DOI redirect rather than the
# nvlpubs.nist.gov PDF deep-link.
NIST_AI_600_1_TAXONOMY_ID = "nist-ai-600-1"
NIST_AI_600_1_TAXONOMY_NAME = (
    "NIST AI 600-1: Artificial Intelligence Risk Management Framework \u2014 "
    "Generative Artificial Intelligence Profile"
)
NIST_AI_600_1_TAXONOMY_DESCRIPTION = (
    "Companion profile to the NIST AI Risk Management Framework (AI RMF "
    "1.0) addressing generative AI-specific risks. Enumerates a closed list "
    "of generative-AI risks with cross-references to AI RMF functions."
)
NIST_AI_600_1_TAXONOMY_VERSION = "1.0"
# Document id is suffixed with ``-doc`` to avoid colliding with the
# taxonomy id (the ai-atlas-nexus loader merges records globally by id).
NIST_AI_600_1_DOC_ID = "nist-ai-600-1-doc"
NIST_AI_600_1_DOC_NAME = "NIST AI 600-1 (Generative AI Profile)"
NIST_AI_600_1_DOC_DESCRIPTION = (
    "Canonical DOI landing page for NIST AI 600-1, the Generative AI "
    "Profile of the NIST AI Risk Management Framework."
)
NIST_AI_600_1_DOC_URL = "https://doi.org/10.6028/NIST.AI.600-1"

# --- OWASP Top 10 for LLM Applications (2025) ---
OWASP_LLM_TAXONOMY_ID = "owasp-llm-top-10-2025"
OWASP_LLM_TAXONOMY_NAME = "OWASP Top 10 for LLM Applications (2025)"
OWASP_LLM_TAXONOMY_DESCRIPTION = (
    "OWASP-published top-10 list of the most critical security risks "
    "facing applications that use large language models, 2025 edition."
)
OWASP_LLM_TAXONOMY_VERSION = "2025"
OWASP_LLM_DOC_ID = "owasp-llm-top-10"
OWASP_LLM_DOC_NAME = "OWASP Gen AI Security Project"
OWASP_LLM_DOC_DESCRIPTION = (
    "OWASP Generative AI Security Project landing page, host of the Top "
    "10 for LLM Applications risk list."
)
OWASP_LLM_DOC_URL = "https://genai.owasp.org/"

# --- OWASP Machine Learning Security Top 10 (2023) ---
OWASP_ML_TAXONOMY_ID = "owasp-ml-top-10-2023"
OWASP_ML_TAXONOMY_NAME = "OWASP Machine Learning Security Top 10 (2023)"
OWASP_ML_TAXONOMY_DESCRIPTION = (
    "OWASP-published top-10 list of the most critical security risks "
    "facing machine-learning systems, 2023 edition."
)
OWASP_ML_TAXONOMY_VERSION = "2023"
OWASP_ML_DOC_ID = "owasp-ml-top-10"
OWASP_ML_DOC_NAME = "OWASP Machine Learning Security Top 10 project"
OWASP_ML_DOC_DESCRIPTION = (
    "OWASP Machine Learning Security Top 10 project landing page."
)
OWASP_ML_DOC_URL = (
    "https://owasp.org/www-project-machine-learning-security-top-10/"
)

# --- Federal Reserve / OCC SR 11-7 ---
SR_11_7_TAXONOMY_ID = "sr-11-7"
SR_11_7_TAXONOMY_NAME = (
    "SR 11-7: Supervisory Guidance on Model Risk Management"
)
SR_11_7_TAXONOMY_DESCRIPTION = (
    "Federal Reserve Supervisory Letter SR 11-7 / OCC Bulletin 2011-12, "
    "supervisory guidance on model risk management for banks regulated by "
    "the Federal Reserve System and the OCC, April 2011."
)
SR_11_7_TAXONOMY_VERSION = "2011-04"
SR_11_7_DOC_ID = "sr-11-7-letter"
SR_11_7_DOC_NAME = "SR 11-7 Supervisory Letter (landing)"
SR_11_7_DOC_DESCRIPTION = (
    "Federal Reserve Supervisory Letter SR 11-7 landing page."
)
SR_11_7_DOC_URL = (
    "https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm"
)
SR_11_7_ATTACHMENT_DOC_ID = "sr-11-7-attachment"
SR_11_7_ATTACHMENT_DOC_NAME = (
    "SR 11-7 Attachment: Guidance on Model Risk Management"
)
SR_11_7_ATTACHMENT_DOC_DESCRIPTION = (
    "PDF attachment to SR 11-7 containing the full text of the supervisory "
    "guidance on model risk management."
)
SR_11_7_ATTACHMENT_DOC_URL = (
    "https://www.federalreserve.gov/supervisionreg/srletters/sr1107a1.pdf"
)


def parse_front_matter(md_path: Path) -> dict[str, Any]:
    """Return the YAML front-matter block of a Jekyll markdown file."""
    text = md_path.read_text(encoding="utf-8")
    match = _FRONT_MATTER_RE.match(text)
    if not match:
        raise ValueError(f"No YAML front-matter found in {md_path}")
    fm = yaml.safe_load(match.group(1)) or {}
    if not isinstance(fm, dict):
        raise ValueError(f"Front-matter in {md_path} is not a mapping")
    body = text[match.end():].strip()
    fm.setdefault("_body", body)
    return fm


def extract_id(md_path: Path) -> str:
    """Return the legacy filename id (``ri-1``, ``mi-12``, ``uc-2``).

    Retained as the canonical key used in cross-reference front-matter
    slots (``mitigates:``, ``related_risks:``). The emitted entry ids
    are computed separately by :func:`build_id_map` from these legacy
    ids plus the post's ``type:`` and numeric sequence, mirroring the
    Jekyll templates ``docs/_includes/{risk,mitigation,usecase}-id.html``.
    """
    match = _ID_RE.match(md_path.name)
    if not match:
        raise ValueError(f"Cannot extract id from filename {md_path.name}")
    return match.group("id")


def _extract_sequence(legacy_id: str) -> int:
    """Return the numeric sequence from a legacy id like ``ri-12`` -> ``12``."""
    return int(legacy_id.split("-", 1)[1])


def _air_risk_id(fm_type: str, sequence: int) -> str:
    """Build the AIR-style id for a Risk: ``AIR-<TYPE>-<NNN>``.

    Mirrors ``docs/_includes/risk-id.html``:
    ``AIR-{{ include.risk.type }}-{{ padded_number }}`` where
    ``padded_number`` is the sequence zero-padded to three digits.
    """
    return f"AIR-{fm_type}-{sequence:03d}"


def _air_mitigation_id(fm_type: str, sequence: int) -> str:
    """Build the AIR-style id for a Mitigation: ``AIR-<TYPE>-<NNN>``.

    Mirrors ``docs/_includes/mitigation-id.html``:
    ``AIR-{{ include.mitigation.type }}-{{ padded_number }}``.
    """
    return f"AIR-{fm_type}-{sequence:03d}"


def _air_usecase_id(sequence: int) -> str:
    """Build the AIR-style id for a Use case: ``UC-<NNN>``.

    Mirrors ``docs/_includes/usecase-id.html``:
    ``UC-{{ padded_number }}`` (no ``AIR-`` prefix and no type segment).
    """
    return f"UC-{sequence:03d}"


def build_id_map(
    risk_files: list[Path],
    mit_files: list[Path],
    uc_files: list[Path],
) -> dict[str, str]:
    """Return ``{legacy_id: air_id}`` for every Risk / Mitigation / Use case.

    The legacy ids (``ri-N``, ``mi-N``, ``uc-N``) remain the canonical
    keys used in front-matter cross-reference slots; the AIR-style ids
    (``AIR-OP-001``, ``AIR-PREV-015``, ``UC-002``) are what the emitted
    catalogue uses for ``id`` slots and cross-references after
    translation.
    """
    id_map: dict[str, str] = {}
    for path in risk_files:
        legacy = extract_id(path)
        fm = parse_front_matter(path)
        risk_type = (fm.get("type") or "").strip()
        if risk_type not in VALID_RISK_TYPES:
            raise ValueError(
                f"{path.name}: risk type {risk_type!r} not in {VALID_RISK_TYPES}"
            )
        id_map[legacy] = _air_risk_id(risk_type, _extract_sequence(legacy))
    for path in mit_files:
        legacy = extract_id(path)
        fm = parse_front_matter(path)
        action_type = (fm.get("type") or "").strip()
        if action_type not in VALID_ACTION_KINDS:
            raise ValueError(
                f"{path.name}: mitigation type {action_type!r} not in "
                f"{VALID_ACTION_KINDS}"
            )
        id_map[legacy] = _air_mitigation_id(
            action_type, _extract_sequence(legacy)
        )
    for path in uc_files:
        legacy = extract_id(path)
        id_map[legacy] = _air_usecase_id(_extract_sequence(legacy))
    return id_map


def _translate_refs(
    refs: list[str], id_map: dict[str, str]
) -> list[str]:
    """Map legacy ``ri-N``/``mi-N``/``uc-N`` refs to their AIR-style ids.

    Unknown refs are passed through unchanged (matches the existing
    dangling-citation leniency — ``scripts/lint-check`` is the right
    place to enforce closure on this enum).
    """
    return [id_map.get(r, r) for r in refs]


# -----------------
# Cross-reference index
# -----------------
#
# Subset of build_sssom_mappings.FRAMEWORK_SSSOM_REGISTRY needed here to
# translate front-matter ``<key>_references:`` slots to the normalised
# ids that land in the standalone Container dumps under
# ``linkml/tests/data/finos/<dump_stem>.yaml``. Keep in sync with
# :mod:`build_sssom_mappings` (small enough to duplicate without
# coupling the two scripts via import).
_FRAMEWORK_REF_REGISTRY: tuple[tuple[str, str], ...] = (
    # (front-matter key suffix, id_prefix used in the standalone dump)
    ("iso-42001", "iso-42001"),
    ("nist-ai-600-1", "nist-ai-600-1"),
    ("nist-sp-800-53r5", ""),
    ("eu-ai-act", "eu-ai-act"),
    ("sr11-7", "sr-11-7"),
    ("ffiec-itbooklets", "ffiec-itbook"),
    ("owasp-llm", "owasp-llm-top-10-2025"),
    ("owasp-ml", "owasp-ml-top-10-2023"),
)


def _compose_framework_ref_id(id_prefix: str, src_id: str) -> str:
    """Compose a normalised dump record id from a source citation.

    Mirrors the forward composition performed by
    :func:`_build_external_standard_container` and consumed by
    :mod:`build_sssom_mappings`. When ``id_prefix`` is empty the source
    id is used verbatim (NIST SP 800-53 controls).
    """
    src_id = src_id.strip()
    if not id_prefix:
        return src_id
    return f"{id_prefix}-{src_id}"


class CrossRefIndex:
    """Two-pass cross-reference index for FINOS Risks and Mitigations.

    Phase 1 (``populate``): walks every ``docs/_risks/ri-*.md`` and
    ``docs/_mitigations/mi-*.md`` to collect raw citation ids and the
    canonical class each mitigation lands on (Action for ``type: PREV``,
    RiskControl for ``type: DET``).

    Phase 2 (lookup methods): consumed by :func:`build_risk_entries`,
    :func:`build_action_entries`, and :func:`build_riskcontrol_entries`
    to populate ``related_mappings`` (skos:relatedMatch), reverse
    ``hasRelatedAction`` / ``isDetectedBy`` links on Risk, and forward
    ``hasRelatedRisk`` / ``detectsRiskConcept`` links on Action /
    RiskControl.

    Mitigation-class decision:

    * ``DET`` -> ``RiskControl`` (`detectsRiskConcept` is the canonical
      slot upstream — see Granite Guardian ``gg-*-detection`` entries
      in ``upstream-releases/ai-atlas-nexus/.../granite_guardian_dimensions.yaml``).
    * ``PREV`` -> ``Action`` (`hasRelatedRisk` semantics).
    * ``RESP`` -> ``Action`` (no FINOS rows currently, kept for symmetry).
    """

    # Mapping from mitigation ``type:`` to the emitted upstream class.
    _MITIGATION_CLASS: dict[str, str] = {
        "DET": "RiskControl",
        "PREV": "Action",
        "RESP": "Action",
    }

    def __init__(self, id_map: dict[str, str]) -> None:
        self._id_map = id_map
        # legacy_id (ri-N / mi-N / uc-N) -> AIR-style id
        self.legacy_to_air: dict[str, str] = dict(id_map)
        # mitigation legacy id -> "Action" | "RiskControl"
        self.mitigation_class: dict[str, str] = {}
        # mitigation legacy id -> list of risk AIR ids it targets
        self.mitigation_targets: dict[str, list[str]] = {}
        # risk AIR id -> list of Action AIR ids that mitigate it (PREV)
        self.risk_to_actions: dict[str, list[str]] = {}
        # risk AIR id -> list of RiskControl AIR ids that detect it (DET)
        self.risk_to_controls: dict[str, list[str]] = {}

    @classmethod
    def build(
        cls,
        id_map: dict[str, str],
        risk_files: list[Path],
        mit_files: list[Path],
    ) -> "CrossRefIndex":
        """Pre-processing pass: walk source files and populate the index."""
        idx = cls(id_map)
        # Risk pass: nothing to harvest beyond what id_map already has;
        # reverse links from risks are populated by the mitigation pass
        # below (each mitigation declares the risks it covers).
        for path in risk_files:
            _ = extract_id(path)  # touch for side-effect / future use
        # Mitigation pass: classify by ``type:`` and harvest the
        # ``mitigates:`` list so risk entries can later receive reverse
        # ``hasRelatedAction`` / ``isDetectedBy`` links.
        for path in mit_files:
            legacy = extract_id(path)
            fm = parse_front_matter(path)
            mtype = (fm.get("type") or "").strip()
            cls_name = cls._MITIGATION_CLASS.get(mtype, "Action")
            idx.mitigation_class[legacy] = cls_name
            mid = idx.legacy_to_air.get(legacy)
            if not mid:
                continue
            targets: list[str] = []
            for raw in fm.get("mitigates") or []:
                if not isinstance(raw, str):
                    continue
                tgt = idx.legacy_to_air.get(raw.strip())
                if tgt and tgt not in targets:
                    targets.append(tgt)
            if targets:
                idx.mitigation_targets[legacy] = targets
            reverse = (
                idx.risk_to_controls if cls_name == "RiskControl"
                else idx.risk_to_actions
            )
            for risk_air_id in targets:
                bucket = reverse.setdefault(risk_air_id, [])
                if mid not in bucket:
                    bucket.append(mid)
        return idx

    # --- Lookup helpers used by the second-pass builders ---

    def mitigation_air_id(self, legacy: str) -> str | None:
        return self.legacy_to_air.get(legacy)

    def mitigation_emitted_as(self, legacy: str) -> str:
        """Return ``"Action"`` or ``"RiskControl"`` for a mitigation id."""
        return self.mitigation_class.get(legacy, "Action")

    def actions_for_risk(self, risk_air_id: str) -> list[str]:
        return list(self.risk_to_actions.get(risk_air_id, ()))

    def controls_for_risk(self, risk_air_id: str) -> list[str]:
        return list(self.risk_to_controls.get(risk_air_id, ()))

    def framework_refs(self, fm: dict[str, Any]) -> list[str]:
        """Return cross-walk ids from a post's ``<key>_references:`` slots.

        Each cited section is normalised to the corresponding record id
        in the standalone Container dump under
        ``linkml/tests/data/finos/<dump_stem>.yaml`` (composed from the
        per-framework ``id_prefix`` plus the source id). Suitable for
        ``related_mappings`` (skos:relatedMatch) on the originating
        Risk / Action / RiskControl entry.
        """
        out: list[str] = []
        for key, id_prefix in _FRAMEWORK_REF_REGISTRY:
            slot = f"{key}_references"
            cited = fm.get(slot)
            if not isinstance(cited, list):
                continue
            for raw in cited:
                if not isinstance(raw, str):
                    continue
                norm = _compose_framework_ref_id(id_prefix, raw)
                if norm and norm not in out:
                    out.append(norm)
        return out


def first_paragraph(body: str) -> str:
    """Return the first non-empty paragraph of a markdown body, plain text."""
    for chunk in body.split("\n\n"):
        chunk = chunk.strip()
        if not chunk or chunk.startswith("#"):
            continue
        chunk = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", chunk)
        chunk = re.sub(r"[*_`]+", "", chunk)
        return chunk
    return ""


def _first_url_from_links_section(body: str) -> str | None:
    """Return the first URL in a markdown heading that contains "Links".

    Scans ``body`` for a heading like ``## Links`` or
    ``### Links to Research and Tools`` and returns the first markdown-link
    target ``(https://...)`` found in that section. The section ends when the
    next markdown heading starts.
    """
    if not body:
        return None
    in_links_section = False
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        # Enter/leave sections on markdown headings.
        m = re.match(r"^#{1,6}\s+(.+)$", line)
        if m:
            heading = m.group(1).strip().lower()
            in_links_section = "links" in heading
            continue
        if not in_links_section:
            continue
        link_match = re.search(r"\[[^\]]+\]\((https?://[^)\s]+)\)", line)
        if link_match:
            return link_match.group(1)
    return None


# -----------------
# YAML writer (matches nexus block style)
# -----------------


def _folded(text: str) -> FoldedScalarString:
    """Return a folded YAML scalar (>-) from plain text.

    ruamel.yaml word-wraps folded scalars at _ruamel.width, accounting for
    indentation, so no pre-wrapping is needed here.  Injecting \\n chars
    into the text would produce blank lines (paragraph separators), which
    is the wrong behaviour for flowing prose.
    """
    return FoldedScalarString(text)


def _format_url(url: str) -> str:
    """Return ``url`` as a plain scalar (single line on output).

    Long URLs are kept on one line by :func:`_unwrap_id_url`, which
    post-processes the emitted YAML to rejoin any line wrapping that
    ruamel inserts for ``id`` / ``url`` values exceeding ``_ruamel.width``.
    Returning a ``LiteralScalarString`` (``|-``) would not work: when the
    value fits beside the key, ruamel emits ``url: |- https://...`` which
    is invalid YAML (``|-`` is a block-header marker; the value must
    begin on the next line).
    """
    return url


def _extract_author_from_url(url: str) -> str:
    """Extract author name from URL hostname.
    
    Extracts the first part of the hostname, strips www. prefix if present,
    and returns it uppercased. Returns empty string if URL is invalid or
    cannot be parsed.
    
    Examples:
        https://www.bis.org/publ/bcbs239.htm -> BIS
        https://www.accenture.com/us-en/insights -> ACCENTURE
        https://gdpr-info.eu/art-4-gdpr/ -> GDPR
    """
    if not url or not isinstance(url, str):
        return ""
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        if not hostname:
            return ""
        # Remove 'www.' prefix if present
        if hostname.startswith("www."):
            hostname = hostname[4:]
        # Get the first part before the first dot
        first_part = hostname.split(".")[0]
        # Uppercase and return
        return first_part.upper()
    except Exception:
        return ""


_ruamel = _RUAMEL_YAML()
_ruamel.default_flow_style = False
_ruamel.allow_unicode = True
_ruamel.width = 78  # Folded scalars (name, description) wrap at this width
_ruamel.indent(mapping=2, sequence=4, offset=2)
_ruamel.preserve_quotes = False

_HEADER = (
    "# AUTOGENERATED by linkml/scripts/build_finos_data.py.\n"
    "# Source: docs/_risks/, docs/_mitigations/, docs/_usecases/\n"
    "# Format: ai-atlas-nexus knowledge_graph YAML (importable upstream).\n"
)


# Matches the first line of a list-of-mappings item, e.g. ``  - id: foo`` or
# ``    - name: bar`` at any indentation. Used by :func:`_space_out` to insert
# a blank line between sibling mapping-shaped list entries while leaving
# plain scalar lists (e.g. ``- doc-bar``) packed together.
_LIST_MAPPING_RE = re.compile(r"^(\s*)- [A-Za-z_][\w-]*:")


def _space_out(text: str) -> str:
    """Insert blank lines between sibling entries for human readability.

    * Two blank lines before each top-level mapping key after the first
      (``documents:``, ``taxonomies:``, ``groups:``, ...).
    * One blank line before each sibling list-of-mappings entry at any
      depth (detected by ``- key:`` start plus a previous content line at
      a deeper indent, which is the signature of a closing sibling).
    Within ``yamllint`` defaults (``empty-lines.max: 2``).
    """
    lines = text.split("\n")
    out: list[str] = []
    prev_indent = -1
    seen_top_key = False
    for line in lines:
        stripped = line.lstrip(" ")
        indent = len(line) - len(stripped)
        is_blank = not stripped
        is_top_key = (
            indent == 0
            and stripped
            and not stripped.startswith("#")
            and not stripped.startswith("- ")
        )
        is_list_mapping = bool(_LIST_MAPPING_RE.match(line))

        if is_top_key:
            if seen_top_key:
                while out and out[-1] == "":
                    out.pop()
                out.append("")
                out.append("")
            seen_top_key = True
        elif is_list_mapping and prev_indent > indent:
            if out and out[-1] != "":
                out.append("")

        out.append(line)
        if not is_blank:
            prev_indent = indent
    return "\n".join(out)


# Keys whose long string values should be emitted as folded scalars (>-)
# so prose wraps at _ruamel.width. Short values (≤ _FOLD_THRESHOLD chars)
# are left as plain scalars so they stay on a single line.
_FOLD_KEYS = frozenset({"name", "description"})
_FOLD_THRESHOLD = 78

# Collection keys that identify a Container-shaped root mapping.
_CONTAINER_COLLECTION_KEYS = frozenset({
    "documents",
    "taxonomies",
    "vocabularies",
    "groups",
    "entries",
    "actions",
    "aitasks",
    "stakeholders",
    "controls",
})


def _is_container_root(node: dict[str, Any]) -> bool:
    """Return True if ``node`` looks like a Container root mapping."""
    return any(key in node for key in _CONTAINER_COLLECTION_KEYS)


def _inject_date_created(node: Any, value: str) -> Any:
    """Recursively set ``dateCreated`` on emitted record mappings.

    Rules:

    * Container root mappings are traversed but do not receive
      ``dateCreated``.
    * Any non-container mapping receives ``dateCreated`` when missing.
    * Existing ``dateCreated`` values are preserved.
    """
    if isinstance(node, list):
        for item in node:
            _inject_date_created(item, value)
        return node
    if isinstance(node, dict):
        if _is_container_root(node):
            for child in node.values():
                _inject_date_created(child, value)
            return node
        node.setdefault("dateCreated", value)
        for child in node.values():
            _inject_date_created(child, value)
    return node


def _force_folded_keys(node: Any) -> Any:
    """Recursively coerce long values under _FOLD_KEYS to FoldedScalarString.

    Walks dict/list structures in-place; leaves non-string values untouched.
    Only strings longer than ``_FOLD_THRESHOLD`` characters are converted to
    block-folded scalars (``>-``); shorter values remain plain scalars on a
    single line.
    """
    if isinstance(node, dict):
        for k, v in list(node.items()):
            if (
                k in _FOLD_KEYS
                and isinstance(v, str)
                and not isinstance(v, (FoldedScalarString, LiteralScalarString))
                and len(v) > _FOLD_THRESHOLD
            ):
                node[k] = FoldedScalarString(v)
            else:
                _force_folded_keys(v)
    elif isinstance(node, list):
        for item in node:
            _force_folded_keys(item)
    return node


# Matches a wrapped plain scalar continuation line: a line indented deeper
# than its key line with no ``key:`` mapping. Used to rejoin id/url values
# that the emitter split across lines because they exceeded width.
_ID_URL_KEY_RE = re.compile(r"^(\s*)(?:- )?(id|url):\s*(\S.*)?$")


def _unwrap_id_url(body: str) -> str:
    """Post-process YAML to keep id and url values on single lines.

    ruamel.yaml may wrap long plain scalars by inserting a continuation
    line indented past the key column. This walks the emitted text and
    rejoins those continuations into a single line for ``id`` and ``url``
    keys only.
    """
    lines = body.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = _ID_URL_KEY_RE.match(line)
        if m:
            key_indent = len(m.group(1))
            value = (m.group(3) or "").rstrip()
            # Collect continuation lines indented strictly deeper than the key
            j = i + 1
            while j < len(lines):
                cont = lines[j]
                stripped = cont.lstrip()
                if not stripped:
                    break
                cont_indent = len(cont) - len(stripped)
                if cont_indent <= key_indent:
                    break
                # A continuation line is plain text (no ``key:`` mapping)
                if re.match(r"^[A-Za-z_][\w-]*:\s", stripped) or stripped.startswith("- "):
                    break
                value = (value + " " + stripped.rstrip()).strip()
                j += 1
            if j > i + 1:
                # Rebuild the line with the joined value
                prefix = line[: line.index(m.group(2))]
                out.append(f"{prefix}{m.group(2)}: {value}")
                i = j
                continue
        out.append(line)
        i += 1
    return "\n".join(out)


_CONTAINER_ID_COLLECTIONS = (
    "taxonomies",
    "documents",
    "vocabularies",
    "groups",
    "entries",
    "controls",
    "actions",
    "aitasks",
    "stakeholders",
)


def _check_id_collisions(path: Path, data: Any) -> None:
    """Fail fast if a Container dump reuses an ``id`` across collections.

    The ai-atlas-nexus loader (``load_yamls_to_container``) merges records
    globally by ``id``, so a collision between e.g. a Taxonomy and a
    Documentation silently corrupts both records and surfaces later as
    Pydantic ``extra_forbidden`` / ``literal_error`` validation errors.
    """
    if not isinstance(data, dict):
        return
    seen: dict[str, str] = {}
    for coll in _CONTAINER_ID_COLLECTIONS:
        for rec in data.get(coll) or []:
            if not isinstance(rec, dict):
                continue
            rid = rec.get("id")
            if rid is None:
                continue
            if rid in seen:
                raise ValueError(
                    f"ID collision in {path.name}: '{rid}' appears in both "
                    f"'{seen[rid]}' and '{coll}'. The ai-atlas-nexus loader "
                    f"merges records globally by id; use a distinct suffix "
                    f"(e.g. '-doc') for one of them."
                )
            seen[rid] = coll


def _dump(path: Path, data: Any, header: str = _HEADER) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    _inject_date_created(data, date.today().isoformat())
    _check_id_collisions(path, data)
    _force_folded_keys(data)
    buf = io.StringIO()
    _ruamel.dump(data, buf)
    body = "\n".join(line.rstrip() for line in buf.getvalue().splitlines())
    body = _space_out(body)
    body = _unwrap_id_url(body)
    path.write_text(header + body + "\n", encoding="utf-8")


# -----------------
# Helpers
# -----------------


def _numeric_md_files(directory: Path, prefix: str) -> list[Path]:
    items = [
        p for p in directory.glob(f"{prefix}-*.md")
        if re.match(rf"^{prefix}-\d+(_|\.)", p.name)
    ]
    return sorted(
        items,
        key=lambda p: int(re.match(rf"^{prefix}-(\d+)", p.name).group(1)),
    )


def _group_id(kind_token: str) -> str:
    return f"{TAXONOMY_ID}-{kind_token.lower()}"


def _control_group_id(kind_token: str) -> str:
    """Stable id for a ``RiskControlGroup`` corresponding to a mitigation kind.

    Distinct namespace from :func:`_group_id` (which is risk-kinds) so the
    two taxonomies cannot collide even if a token were ever shared.
    """
    return f"{TAXONOMY_ID}-control-{kind_token.lower()}"


def _doc_id_slug(*parts: str) -> str:
    """Build a stable Documentation id from one or more raw segments."""
    joined = "-".join(parts)
    s = re.sub(r"[^A-Za-z0-9]+", "-", joined.lower()).strip("-")
    return s or "doc"


def _deployment_axis_group_id(axis: str) -> str:
    """Stable ``RiskGroup`` id for one axis of the deployment model."""
    return _doc_id_slug("ai-deployment-group", axis)


def _deployment_term_id(axis: str, leaf: str) -> str:
    """Stable ``Term`` id for one leaf of the deployment model.

    Axis-prefixed because some leaf labels repeat across axes
    (e.g. ``Generative_AI`` under both ``ai_type`` and
    ``architecture_pattern``; ``Federated`` under ``data_handling``
    vs ``Federated_Learning`` under ``architecture_pattern``).
    """
    return _doc_id_slug("ai-deployment", axis, leaf)


_NIST_SP_800_53R5_CONTROL_URL_BASE = (
    "https://csrc.nist.gov/projects/cprt/catalog#/cprt/framework/version/"
    "SP_800_53_5_2_0/home?element="
)


def _nist_control_url(control_id: str) -> str:
    """Build the CPRT catalogue URL for a NIST SP 800-53 Rev. 5 control.

    Converts ``ac-1`` to
    ``https://…SP_800_53_5_2_0/home?element=AC-01``.
    The family prefix is uppercased and the numeric suffix is
    zero-padded to two digits.
    """
    parts = control_id.upper().split("-", 1)
    if len(parts) == 2 and parts[1].isdigit():
        element = f"{parts[0]}-{int(parts[1]):02d}"
    else:
        element = control_id.upper()
    return _NIST_SP_800_53R5_CONTROL_URL_BASE + element


def _normalise_control_name(raw_title: str, control_id: str) -> str:
    """Strip the leading ``<ID> `` from a control title and lowercase small words.

    Source titles in ``docs/_data/nist-sp-800-53r5.yml`` come from PDF
    bookmarks and look like ``AC-1 Policy And Procedures``. The bookmark
    extractor uppercases every word; this helper strips the leading
    identifier prefix and restores conventional title-case spacing.
    """
    prefix = f"{control_id.upper()} "
    body = raw_title[len(prefix):] if raw_title.startswith(prefix) else raw_title
    words = body.split()
    out: list[str] = []
    for i, w in enumerate(words):
        if i > 0 and w.lower() in _TITLE_SMALL_WORDS:
            out.append(w.lower())
        else:
            out.append(w)
    return " ".join(out)


def _load_data_yaml(repo_root: Path, stem: str) -> dict[str, Any]:
    """Load ``docs/_data/<stem>.yml`` as a plain mapping."""
    path = repo_root / "docs" / "_data" / f"{stem}.yml"
    if not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return loaded if isinstance(loaded, dict) else {}


class DocRegistry:
    """Accumulates Documentation and Term rows with deduplication.

    Holds the master ``documents`` list emitted under
    ``Container.documents`` plus a parallel ``terms`` list for ``Term``
    instances (sourced from ``docs/_data/data_classification.yml``
    rows; each Term carries ``type: Term`` and lands in
    ``Container.entries`` alongside Risks and AiSystems). Builders call
    ``ensure(doc)`` / ``ensure_term(term)`` to register a new row and
    receive its id; ``ensure_data_classification(name)`` is a convenience
    helper that consults the loaded ``docs/_data/`` registry.
    """

    def __init__(
        self,
        repo_root: Path,
        documents: list[dict[str, Any]],
    ) -> None:
        self.documents = documents
        self.terms: list[dict[str, Any]] = []
        self.repo_root = repo_root
        self._by_id: dict[str, dict[str, Any]] = {
            d["id"]: d for d in documents
        }
        self._terms_by_id: dict[str, dict[str, Any]] = {}
        self._data_classification_index: dict[str, dict[str, Any]] | None = None
        self._deployment_data_handling_leaves: set[str] | None = None
        self._jurisdictions_index: dict[str, dict[str, Any]] | None = None

    def ensure(self, doc: dict[str, Any]) -> str:
        """Register ``doc`` (or merge into existing) and return its id."""
        doc_id = doc["id"]
        existing = self._by_id.get(doc_id)
        if existing is None:
            self.documents.append(doc)
            self._by_id[doc_id] = doc
            return doc_id
        # Merge: prefer existing values, fill in any missing scalars.
        for k, v in doc.items():
            existing.setdefault(k, v)
        # Union isCategorizedAs lists when both sides provide one.
        new_cats = doc.get("isCategorizedAs") or []
        if new_cats:
            cats = existing.setdefault("isCategorizedAs", [])
            for c in new_cats:
                if c not in cats:
                    cats.append(c)
        return doc_id

    def ensure_term(self, term: dict[str, Any]) -> str:
        """Register ``term`` (or merge into existing) and return its id.

        Mirrors :meth:`ensure` for ``Term`` rows, which land in
        ``Container.entries`` (range ``Entry``) carrying
        ``type: Term``.
        """
        term_id = term["id"]
        existing = self._terms_by_id.get(term_id)
        if existing is None:
            self.terms.append(term)
            self._terms_by_id[term_id] = term
            return term_id
        for k, v in term.items():
            existing.setdefault(k, v)
        new_cats = term.get("isCategorizedAs") or []
        if new_cats:
            cats = existing.setdefault("isCategorizedAs", [])
            for c in new_cats:
                if c not in cats:
                    cats.append(c)
        return term_id

    def _data_classification_lookup(self) -> dict[str, dict[str, Any]]:
        if self._data_classification_index is None:
            raw = _load_data_yaml(self.repo_root, "data_classification")
            items = raw.get("financial_data_classification") or []
            self._data_classification_index = {
                str(item.get("name", "")).strip(): item
                for item in items
                if isinstance(item, dict) and item.get("name")
            }
        return self._data_classification_index

    def ensure_data_classification(self, name: str) -> str | None:
        """Materialise (idempotent) a ``Term`` for one data-classification row.

        Each row of ``docs/_data/data_classification.yml`` becomes one
        ``Term`` instance landing in ``Container.entries`` (carrying
        ``type: Term`` and ``isDefinedByTaxonomy: <TAXONOMY_ID>``). The
        term's ``description`` folds the source row's ``description``,
        ``storage_location``, ``regulations`` and ``examples`` into
        prose; ``isCategorizedAs`` points at the relevant
        sensitivity-tier Documentation parent.

        Each ``references[*]`` entry is emitted as a child
        ``Documentation`` row carrying ``isCategorizedAs: [<term_id>]``
        so consumers can filter by the parent term. The reference's
        ``jurisdiction:`` is folded into the Documentation's
        ``description`` text (pre-G29 it was a second
        ``isCategorizedAs`` ref to a ``jurisdiction-<code>`` Term —
        see the module-level ``JURISDICTION_LABELS`` note).
        """
        index = self._data_classification_lookup()
        item = index.get(name)
        if not item:
            return None
        term_id = _doc_id_slug("data-classification", name)
        desc_raw = (item.get("description") or "").strip().replace("\n", " ")
        sensitivity = (item.get("sensitivity") or "").strip()
        storage = (item.get("storage_location") or "").strip()
        regulations = (item.get("regulations") or "").strip()
        examples_raw = item.get("examples") or []

        desc_parts: list[str] = []
        if sensitivity:
            desc_parts.append(
                f"FINOS data classification (sensitivity: {sensitivity})."
            )
        if desc_raw:
            desc_parts.append(desc_raw)
        if storage:
            desc_parts.append(f"Storage location: {storage}.")
        if regulations:
            desc_parts.append(f"Regulations: {regulations}.")
        if examples_raw:
            sample = "; ".join(
                str(e).strip() for e in examples_raw if isinstance(e, str)
            )
            if sample:
                desc_parts.append(f"Examples: {sample}.")

        categories: list[str] = []
        if sensitivity:
            tier_id = self.ensure_sensitivity_tier(sensitivity)
            if tier_id:
                categories.append(tier_id)

        term: dict[str, Any] = {
            "id": term_id,
            "name": name.replace("_", " "),
            "description": " ".join(desc_parts).strip(),
            "type": "Term",
            "isDefinedByTaxonomy": TAXONOMY_ID,
        }
        if categories:
            term["isCategorizedAs"] = categories
        self.ensure_term(term)

        # Emit each regulatory reference from the classification row as a
        # Documentation child row. ``isCategorizedAs`` points at the parent
        # Term plus the jurisdiction Term (Vocabulary navigation view).
        # ``hasJurisdiction`` carries the typed enum value
        # (graph/cross-walk view). The two are kept in lock-step by
        # :meth:`ensure_jurisdiction`. The jurisdiction text is also
        # folded into the Documentation's ``description`` for human
        # reading.
        for ref in item.get("references") or []:
            if not isinstance(ref, dict):
                continue
            ref_name = str(ref.get("name", "")).strip()
            if not ref_name:
                continue
            ref_id = _doc_id_slug("data-classification-ref", name, ref_name)
            ref_cats: list[str] = [term_id]
            jurisdiction = str(ref.get("jurisdiction", "")).strip()
            ref_desc_parts: list[str] = []
            ref_jurisdictions: list[str] = []
            if jurisdiction:
                jur_label = JURISDICTION_LABELS.get(jurisdiction, jurisdiction)
                ref_desc_parts.append(
                    f"Jurisdiction: {jur_label} ({jurisdiction})."
                )
                jur_term_id = self.ensure_jurisdiction(jurisdiction)
                if jur_term_id and jur_term_id not in ref_cats:
                    ref_cats.append(jur_term_id)
                ref_jurisdictions.append(jurisdiction)
            ref_url = str(ref.get("url", "")).strip() if ref.get("url") else None
            ref_author = _extract_author_from_url(ref_url) if ref_url else ""
            ref_doc: dict[str, Any] = {
                "id": ref_id,
                "name": ref_name,
                "isCategorizedAs": ref_cats,
            }
            if ref_jurisdictions:
                ref_doc["hasJurisdiction"] = ref_jurisdictions
            if ref_desc_parts:
                ref_doc["description"] = " ".join(ref_desc_parts)
            if ref_author:
                ref_doc["author"] = ref_author
            if ref_url:
                ref_doc["url"] = ref_url
            self.ensure(ref_doc)
        return term_id

    def ensure_sensitivity_tier(self, tier: str) -> str | None:
        """Materialise (idempotent) a sensitivity-tier ``Term``.

        Each tier (Critical / High / Medium / Low) becomes one ``Term``
        row landing in ``Container.entries`` (type ``Term``,
        ``isDefinedByVocabulary: finos-data-sensitivity-tiers``)
        referenced by ``isCategorizedAs`` from any data-classification
        Term carrying that tier. Surfaces the sensitivity badge rendered
        by ``docs/_layouts/usecase.html``.

        Previously emitted as ``Documentation``; corrected to ``Term``
        because a sensitivity tier is a classification concept
        (skos:Concept), not a documented standard.
        """
        tier = (tier or "").strip()
        if not tier:
            return None
        term_id = _doc_id_slug(SENSITIVITY_PARENT_PREFIX, tier)
        if term_id in self._terms_by_id:
            return term_id
        label = SENSITIVITY_LABELS.get(tier, f"{tier} sensitivity")
        self.ensure_term({
            "id": term_id,
            "name": label,
            "description": (
                f"FINOS financial data sensitivity tier: {tier}."
            ),
            "type": "Term",
            "isDefinedByVocabulary": SENSITIVITY_VOCAB_ID,
        })
        return term_id

    def _jurisdictions_lookup(self) -> dict[str, dict[str, Any]]:
        """Lazy-load and index ``docs/_data/finos-jurisdictions.yml``.

        Returns a ``{code: row}`` index. Missing or malformed YAML
        yields an empty index — callers fall back to
        :data:`JURISDICTION_LABELS` for the label and emit the Term
        with description text only.
        """
        if self._jurisdictions_index is None:
            raw = _load_data_yaml(self.repo_root, "finos-jurisdictions")
            items = raw.get("finos_jurisdictions") or []
            self._jurisdictions_index = {
                str(item.get("code", "")).strip(): item
                for item in items
                if isinstance(item, dict) and item.get("code")
            }
        return self._jurisdictions_index

    def ensure_jurisdiction(self, code: str) -> str | None:
        """Materialise (idempotent) a ``Term`` for one jurisdiction code.

        Each distinct ``code`` cited in
        ``docs/_data/data_classification.yml`` (or other source data)
        becomes one ``Term`` row in ``Container.entries`` (type
        ``Term``, ``isDefinedByVocabulary: finos-jurisdictions``).
        Description text is built from the matching row of
        ``docs/_data/finos-jurisdictions.yml`` when available, with
        :data:`JURISDICTION_LABELS` as fallback.

        The Term is the human-navigable view; the canonical typed
        linkage is the ``hasJurisdiction: [<code>]`` slot on the
        regulatory-reference ``Documentation`` row (slot range:
        ``Jurisdiction`` enum, FINOS-local extension of the vendored
        ai-atlas-nexus schema — see ISSUE-nexus.md G29).
        """
        code = (code or "").strip()
        if not code:
            return None
        term_id = _doc_id_slug(JURISDICTION_PARENT_PREFIX, code)
        if term_id in self._terms_by_id:
            return term_id
        index = self._jurisdictions_lookup()
        row = index.get(code) or {}
        label = (
            str(row.get("name", "")).strip()
            or JURISDICTION_LABELS.get(code, code)
        )
        desc = (str(row.get("description", "")).strip()
                or f"FINOS jurisdiction: {label} ({code}).")
        term: dict[str, Any] = {
            "id": term_id,
            "name": label,
            "description": desc,
            "type": "Term",
            "isDefinedByVocabulary": JURISDICTION_VOCAB_ID,
        }
        iso = row.get("iso_3166_1_alpha_2")
        if isinstance(iso, str) and iso.strip():
            term["exact_mappings"] = [f"iso_3166_1_alpha_2:{iso.strip()}"]
        self.ensure_term(term)
        return term_id

    def emit_all_jurisdictions(self) -> None:
        """Eagerly materialise every row of ``finos-jurisdictions.yml``.

        Cited codes are materialised lazily by
        :meth:`ensure_jurisdiction` when reg-ref Documentation rows
        are emitted; this method backfills any codes not currently
        cited so the full FINOS-published jurisdiction registry is
        always present in the dump.
        """
        for code in self._jurisdictions_lookup():
            self.ensure_jurisdiction(code)

    def ensure_data_handling_aspect(self, aspect: str) -> str | None:
        """Resolve a ``data_handling_aspects:`` token to its Term id.

        Each token (e.g. ``Centralized``, ``Privacy_Preserving``)
        maps to one leaf of the ``data_handling`` axis of the FINOS
        AI Deployment Model. The corresponding ``Term`` row is
        emitted by :func:`build_ai_deployment_model_taxonomy`; this
        method only computes the deterministic id (the term row is
        guaranteed to land in ``Container.entries`` provided the
        front-matter token names a leaf actually present in
        ``docs/_data/ai_deployment_model.yml``). Unknown tokens
        return ``None`` and the caller silently drops them —
        matches the dangling-section-id leniency elsewhere in this
        builder; FINOS [`scripts/lint-check`] is the right place to
        enforce closure on this enum.
        """
        aspect = (aspect or "").strip()
        if not aspect:
            return None
        if not self._is_known_deployment_data_handling_leaf(aspect):
            return None
        return _deployment_term_id(DEPLOYMENT_DATA_HANDLING_AXIS, aspect)

    def _is_known_deployment_data_handling_leaf(self, aspect: str) -> bool:
        """Return True iff ``aspect`` names a ``data_handling`` axis leaf.

        Lazy-loads ``docs/_data/ai_deployment_model.yml`` on first
        call and caches the set of leaf labels under the
        ``data_handling`` axis.
        """
        if self._deployment_data_handling_leaves is None:
            raw = _load_data_yaml(self.repo_root, "ai_deployment_model")
            leaves: set[str] = set()
            for axis_wrapper in raw.get(
                "ai_deployment_model_taxonomy"
            ) or []:
                if (
                    not isinstance(axis_wrapper, dict)
                    or len(axis_wrapper) != 1
                ):
                    continue
                axis_name, axis_leaves = next(iter(axis_wrapper.items()))
                if (
                    axis_name != DEPLOYMENT_DATA_HANDLING_AXIS
                    or not isinstance(axis_leaves, list)
                ):
                    continue
                for leaf_wrapper in axis_leaves:
                    if (
                        not isinstance(leaf_wrapper, dict)
                        or len(leaf_wrapper) != 1
                    ):
                        continue
                    leaf_name = next(iter(leaf_wrapper.keys()))
                    if isinstance(leaf_name, str) and leaf_name.strip():
                        leaves.add(leaf_name.strip())
            self._deployment_data_handling_leaves = leaves
        return aspect in self._deployment_data_handling_leaves

    def emit_all_data_classifications(self) -> None:
        """Eagerly materialise every row of ``data_classification.yml``.

        Cited rows are materialised lazily by
        :meth:`ensure_data_classification` from
        ``data_classifications:`` front-matter on use-case posts; this
        method backfills any rows not currently cited so the full
        FINOS-published data-classification registry is always in the
        dump (these are FINOS-authored data, not site presentation).
        Also force-emits all four sensitivity tiers so the parent rows
        are always present even if a tier is currently uncited.
        """
        index = self._data_classification_lookup()
        for name in index:
            self.ensure_data_classification(name)
        for tier in SENSITIVITY_LABELS:
            self.ensure_sensitivity_tier(tier)

    def ensure_stakeholder(
        self, name: str, stakeholders: list[dict[str, Any]]
    ) -> str | None:
        """Materialise (idempotent) a ``Stakeholder`` instance.

        Appends to the caller-supplied ``stakeholders`` list so the
        emitted ``Container.stakeholders:`` collection stays in
        deterministic insertion order. Returns the stakeholder id (a
        slugified form of ``name``), or ``None`` for empty input.
        """
        name = (name or "").strip()
        if not name:
            return None
        sid = _doc_id_slug("stakeholder", name)
        for existing in stakeholders:
            if existing.get("id") == sid:
                return sid
        stakeholders.append({
            "id": sid,
            "name": name,
            "description": f"Stakeholder role: {name}.",
            "isDefinedByTaxonomy": TAXONOMY_ID,
        })
        return sid

    def ensure_regulatory_concern(self, item: dict[str, Any]) -> str | None:
        name = str(item.get("name", "")).strip()
        if not name:
            return None
        doc_id = _doc_id_slug("reg-concern", name)
        desc_parts: list[str] = [f"Regulatory concern: {name}."]
        jurisdiction = str(item.get("jurisdiction", "")).strip()
        if jurisdiction:
            desc_parts.append(f"Jurisdiction: {jurisdiction}.")
        url = str(item.get("url", "")).strip() if item.get("url") else None
        author = _extract_author_from_url(url) if url else ""
        doc: dict[str, Any] = {
            "id": doc_id,
            "name": name,
            "description": " ".join(desc_parts),
        }
        if author:
            doc["author"] = author
        if url:
            doc["url"] = url
        return self.ensure(doc)

    def collect_front_matter_refs(
        self, fm: dict[str, Any]
    ) -> tuple[list[str], list[str]]:
        """Return ``(documentation_ids, term_ids)`` from a post's front-matter.

        Walks ``regulatory_concerns`` (-> ``Documentation``) and
        ``data_classifications`` (-> ``Term`` instances under
        ``Container.entries``), materialising any missing rows as a
        side-effect. Callers wire the returned documentation ids into
        ``hasDocumentation`` and the term ids into ``isCategorizedAs``
        on the originating entry.
        """
        doc_refs: list[str] = []
        term_refs: list[str] = []
        for dc in fm.get("data_classifications") or []:
            if isinstance(dc, dict):
                name = str(dc.get("name", "")).strip()
            elif isinstance(dc, str):
                name = dc.strip()
            else:
                continue
            if not name:
                continue
            term_id = self.ensure_data_classification(name)
            if term_id is not None and term_id not in term_refs:
                term_refs.append(term_id)
        for rc in fm.get("regulatory_concerns") or []:
            if not isinstance(rc, dict):
                continue
            doc_id = self.ensure_regulatory_concern(rc)
            if doc_id is not None and doc_id not in doc_refs:
                doc_refs.append(doc_id)
        return doc_refs, term_refs


# -----------------
# Builders
# -----------------


def build_organizations() -> list[dict[str, Any]]:
    """Return the FINOS organization entry."""
    return [
        {
            "id": "finos",
            "name": "FINOS",
            "description": (
                "FINOS is the Fintech Open Source Foundation, a nonprofit "
                "organization that fosters open collaboration and innovation "
                "in financial services technology. FINOS provides a neutral "
                "forum for industry participants to develop and share open "
                "source software, standards, and best practices that drive "
                "digital transformation across the financial ecosystem."
            ),
            "url": "https://w3id.org/finos",
        }
    ]


def build_documents() -> list[dict[str, Any]]:
    return [
        {
            "id": FINOS_DOC_ID,
            "name": "FINOS AI Governance Framework — Project Site",
            "description": (
                "Canonical publication of the FINOS AI Governance Framework, "
                "including the risk register, mitigation catalogue and "
                "use-case library for AI in financial services."
            ),
            "url": TAXONOMY_URL,
        }
    ]


def build_taxonomy() -> dict[str, Any]:
    return {
        "id": TAXONOMY_ID,
        "name": TAXONOMY_NAME,
        "type": "RiskTaxonomy",
        "description": TAXONOMY_DESCRIPTION,
        "url": TAXONOMY_URL,
        "version": "v2",
        "hasDocumentation": [FINOS_DOC_ID],
    }


def build_vocabularies() -> list[dict[str, Any]]:
    """Return the FINOS classification-concept ``Vocabulary`` rows.

    * ``finos-data-sensitivity-tiers`` — closed enum of four
      sensitivity tiers (Critical / High / Medium / Low) sourced from
      the ``sensitivity:`` slot of every row of
      ``docs/_data/data_classification.yml``. Each tier materialises
      one ``Term`` (id: ``sensitivity-<tier>``) under this vocabulary,
      emitted lazily by
      :meth:`DocRegistry.ensure_sensitivity_tier`.

    * ``finos-jurisdictions`` — closed enum of the four FINOS
      jurisdiction codes (US / EU / UK / International) sourced from
      ``docs/_data/finos-jurisdictions.yml``. Each code materialises
      one ``Term`` (id: ``jurisdiction-<code-slug>``) under this
      vocabulary, emitted lazily by
      :meth:`DocRegistry.ensure_jurisdiction`. The Term view is the
      human-navigable index; the typed-graph view is the
      ``hasJurisdiction:`` slot on reg-ref ``Documentation`` rows
      (FINOS-local extension of the vendored ai-atlas-nexus schema —
      see ISSUE-nexus.md G29 for the upstream proposal).
    """
    return [
        {
            "id": SENSITIVITY_VOCAB_ID,
            "name": "FINOS Data Sensitivity Tiers",
            "description": (
                "Closed enum of four data sensitivity tiers (Critical, "
                "High, Medium, Low) used to grade FINOS financial data "
                "classifications."
            ),
            "type": "Vocabulary",
            "hasDocumentation": [FINOS_DOC_ID],
        },
        {
            "id": JURISDICTION_VOCAB_ID,
            "name": "FINOS Jurisdictions",
            "description": (
                "Closed enum of legal/political jurisdictions cited by "
                "regulatory references across the FINOS AI Governance "
                "Framework catalogue. Source: "
                "docs/_data/finos-jurisdictions.yml."
            ),
            "type": "Vocabulary",
            "hasDocumentation": [FINOS_DOC_ID],
        },
    ]


def build_groups(used_kinds: set[str]) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    for token in ("RC", "SEC", "OP", "GOV"):
        if token not in used_kinds:
            continue
        groups.append(
            {
                "id": _group_id(token),
                "name": RISK_KIND_LABELS[token],
                "type": "RiskGroup",
                "description": (
                    f"FINOS {RISK_KIND_LABELS[token]} risk grouping."
                ),
                "isDefinedByTaxonomy": TAXONOMY_ID,
            }
        )
    return groups


def build_control_groups(used_kinds: set[str]) -> list[dict[str, Any]]:
    """Emit one ``RiskControlGroup`` per mitigation ``type:`` actually used.

    Mirrors :func:`build_groups` for risks. Each Action references its
    control group via ``isCategorizedAs: [<group-id>]`` (since upstream
    ``Action`` has no ``isPartOf`` slot). The reverse-direction
    ``hasPart:`` collection is intentionally omitted to avoid duplicating
    the wire — see the module-level note on ``VALID_ACTION_KINDS``.
    """
    groups: list[dict[str, Any]] = []
    for token in ("PREV", "DET", "RESP"):
        if token not in used_kinds:
            continue
        groups.append(
            {
                "id": _control_group_id(token),
                "name": f"{ACTION_KIND_LABELS[token]} controls",
                "type": "RiskControlGroup",
                "description": (
                    f"FINOS {ACTION_KIND_LABELS[token]} mitigation grouping."
                ),
                "isDefinedByTaxonomy": TAXONOMY_ID,
            }
        )
    return groups


def build_ai_use_cases_taxonomy(
    repo_root: Path,
) -> tuple[
    dict[str, Any],        # AiTaskTaxonomy row -> Container.taxonomies
    list[dict[str, Any]],  # AiTaskDomain rows  -> Container.groups
    list[dict[str, Any]],  # AiTaskGroup rows   -> Container.groups
    list[dict[str, Any]],  # AiTask leaf rows   -> Container.aitasks
]:
    """Build the FINOS AI use-case taxonomy from ``docs/_data/ai_use_cases.yml``.

    Emits the full three-level hierarchy as native ai-atlas-nexus rows
    (ai-atlas-nexus #190 / gap G30):

    * One ``AiTaskTaxonomy`` row (``Container.taxonomies``).
    * One ``AiTaskDomain`` per Level-1 sector
      (``Container.groups``, ``type: AiTaskDomain``), with ``hasPart``
      enumerating its child ``AiTaskGroup`` ids.
    * One ``AiTaskGroup`` per Level-2 subcategory
      (``Container.groups``, ``type: AiTaskGroup``), with
      ``isPartOf: <domain-id>`` and ``hasPart`` enumerating its child
      ``AiTask`` ids.
    * One ``AiTask`` per Level-3 leaf (``Container.aitasks``), with
      ``isPartOf: <group-id>``.

    Replaces the pre-G30 flat emission (one ``RiskTaxonomy`` + leaf
    ``AiTask`` rows only) — the Level-1 and Level-2 structure is now
    materialised as proper grouping nodes instead of being implied by
    breadcrumb strings in ``AiTask.description``.

    ``cross_cutting_capabilities`` are handled by
    :func:`build_cross_cutting_capabilities` (they map to
    ``Capability``, not ``AiTask``).
    """
    raw = _load_data_yaml(repo_root, "ai_use_cases")
    taxonomy: dict[str, Any] = {
        "id": AI_UC_TAXONOMY_ID,
        "name": "FINOS AI Use-Cases Taxonomy (Financial Services)",
        "type": "AiTaskTaxonomy",
        "description": (
            "FINOS-published taxonomy of AI use cases relevant to "
            "financial services. Organised into five top-level sector "
            "domains (AiTaskDomain), subcategories (AiTaskGroup), and "
            "leaf AI tasks (AiTask)."
        ),
        "url": TAXONOMY_URL,
        "version": "v1",
        "hasDocumentation": [FINOS_DOC_ID],
    }
    domains: list[dict[str, Any]] = []
    groups: list[dict[str, Any]] = []
    ai_tasks: list[dict[str, Any]] = []

    for cat_wrapper in raw.get("AI_use_cases") or []:
        if not isinstance(cat_wrapper, dict) or len(cat_wrapper) != 1:
            continue
        cat_name, subs = next(iter(cat_wrapper.items()))
        if not isinstance(subs, list):
            continue
        domain_id = _doc_id_slug(AI_UC_TAXONOMY_ID, "domain", str(cat_name))
        domain_name = str(cat_name).replace("_", " ")
        group_ids_for_domain: list[str] = []
        for sub_wrapper in subs:
            if not isinstance(sub_wrapper, dict) or len(sub_wrapper) != 1:
                continue
            sub_name, leaves = next(iter(sub_wrapper.items()))
            if not isinstance(leaves, list):
                continue
            group_id = _doc_id_slug(
                AI_UC_TAXONOMY_ID, "group", str(cat_name), str(sub_name)
            )
            group_name = str(sub_name).replace("_", " ")
            task_ids_for_group: list[str] = []
            for leaf in leaves:
                if not isinstance(leaf, str) or not leaf.strip():
                    continue
                task_id = _doc_id_slug(AI_UC_TAXONOMY_ID, "task", str(leaf))
                ai_tasks.append({
                    "id": task_id,
                    "name": str(leaf).replace("_", " "),
                    "description": (
                        f"FINOS AI task: {str(leaf).replace('_', ' ')} "
                        f"(domain: {domain_name}, "
                        f"subcategory: {group_name})."
                    ),
                    "isDefinedByTaxonomy": AI_UC_TAXONOMY_ID,
                    "isPartOf": group_id,
                })
                task_ids_for_group.append(task_id)
            group_row: dict[str, Any] = {
                "id": group_id,
                "name": group_name,
                "type": "AiTaskGroup",
                "description": (
                    f"FINOS AI use-case subcategory: {group_name} "
                    f"(domain: {domain_name})."
                ),
                "isDefinedByTaxonomy": AI_UC_TAXONOMY_ID,
                "isPartOf": domain_id,
            }
            if task_ids_for_group:
                group_row["hasPart"] = task_ids_for_group
            groups.append(group_row)
            group_ids_for_domain.append(group_id)
        domain_row: dict[str, Any] = {
            "id": domain_id,
            "name": domain_name,
            "type": "AiTaskDomain",
            "description": (
                f"FINOS AI use-case sector domain: {domain_name}."
            ),
            "isDefinedByTaxonomy": AI_UC_TAXONOMY_ID,
        }
        if group_ids_for_domain:
            domain_row["hasPart"] = group_ids_for_domain
        domains.append(domain_row)
    return taxonomy, domains, groups, ai_tasks


def build_cross_cutting_capabilities(
    repo_root: Path,
) -> tuple[
    dict[str, Any],        # CapabilityTaxonomy row -> Container.taxonomies
    dict[str, Any],        # CapabilityGroup row -> Container.groups
    list[dict[str, Any]],  # Capability rows -> Container.entries
]:
    """Build the FINOS cross-cutting AI capabilities from
    ``docs/_data/ai_use_cases.yml``.

    Emits:
    * One ``CapabilityTaxonomy`` row (``Container.taxonomies``).
    * One ``CapabilityGroup`` row (``Container.groups``) anchoring all
      cross-cutting capabilities under the capability taxonomy.
    * One ``Capability`` row per item in the
      ``cross_cutting_capabilities:`` list (``Container.entries``),
      each with ``type: Capability`` and ``isPartOf: <group-id>``.

    No ``CapabilityDomain`` is emitted—the source data is a flat list,
    not a nested domain/group/capability hierarchy.
    """
    raw = _load_data_yaml(repo_root, "ai_use_cases")
    taxonomy: dict[str, Any] = {
        "id": AI_CAPS_TAXONOMY_ID,
        "name": "FINOS AI Capabilities (Financial Services)",
        "type": "CapabilityTaxonomy",
        "description": (
            "FINOS-published cross-cutting AI capabilities applicable "
            "across financial services use cases, covering foundational "
            "engineering, operational, and governance concerns."
        ),
        "url": TAXONOMY_URL,
        "version": "v1",
        "hasDocumentation": [FINOS_DOC_ID],
    }
    group: dict[str, Any] = {
        "id": AI_CAPS_CROSSCUTTING_GROUP_ID,
        "name": "Cross-Cutting Capabilities",
        "type": "CapabilityGroup",
        "description": (
            "AI capabilities that cut across multiple FINOS use-case "
            "domains, including data engineering, MLOps, privacy, "
            "security, and monitoring."
        ),
        "isDefinedByTaxonomy": AI_CAPS_TAXONOMY_ID,
    }
    capabilities: list[dict[str, Any]] = []
    for cap in raw.get("cross_cutting_capabilities") or []:
        if not isinstance(cap, str) or not cap.strip():
            continue
        cap = cap.strip()
        cap_id = _doc_id_slug(AI_CAPS_TAXONOMY_ID, "cap", cap)
        capabilities.append({
            "id": cap_id,
            "name": cap.replace("_", " "),
            "description": (
                f"FINOS cross-cutting AI capability: "
                f"{cap.replace('_', ' ')}."
            ),
            "type": "Capability",
            "isDefinedByTaxonomy": AI_CAPS_TAXONOMY_ID,
            "isPartOf": AI_CAPS_CROSSCUTTING_GROUP_ID,
        })
    return taxonomy, group, capabilities


def build_ai_deployment_model_taxonomy(
    repo_root: Path,
) -> tuple[
    dict[str, Any],        # RiskTaxonomy row -> Container.taxonomies
    list[dict[str, Any]],  # axis RiskGroup rows -> Container.groups
    list[dict[str, Any]],  # leaf Term rows -> Container.entries
]:
    """Build the FINOS AI Deployment Model from
    ``docs/_data/ai_deployment_model.yml``.

    Mirrors the ``hf_ml_tasks.yaml`` shape (Taxonomy + Groups + leaf
    entries with ``isPartOf``) and the FINOS data-classification Term
    treatment. Emits exactly one ``RiskTaxonomy`` umbrella, one
    ``RiskGroup`` per axis, and one ``Term`` per leaf. No local
    schema additions.

    The source file structures the taxonomy as a list of
    single-key dicts under ``ai_deployment_model_taxonomy:``; each
    dict's key names an axis (``ai_type``, ``architecture_pattern``,
    ``deployment_type``, ``data_handling``, ``regulatory_alignment``,
    ``operational_model``, ``integration_pattern``) and its value
    is a list of leaf-label dicts with ``description:`` strings.
    """
    raw = _load_data_yaml(repo_root, "ai_deployment_model")
    taxonomy: dict[str, Any] = {
        "id": DEPLOYMENT_TAXONOMY_ID,
        "name": DEPLOYMENT_TAXONOMY_NAME,
        "type": "RiskTaxonomy",
        "description": DEPLOYMENT_TAXONOMY_DESCRIPTION,
        "url": DEPLOYMENT_TAXONOMY_URL,
        "version": "v1",
    }
    groups: list[dict[str, Any]] = []
    terms: list[dict[str, Any]] = []
    seen_term_ids: set[str] = set()

    for axis_wrapper in raw.get("ai_deployment_model_taxonomy") or []:
        if not isinstance(axis_wrapper, dict) or len(axis_wrapper) != 1:
            continue
        axis_name, leaves = next(iter(axis_wrapper.items()))
        if not isinstance(axis_name, str) or not isinstance(leaves, list):
            continue
        axis_name = axis_name.strip()
        if not axis_name:
            continue
        group_id = _deployment_axis_group_id(axis_name)
        groups.append({
            "id": group_id,
            "name": axis_name.replace("_", " "),
            "type": "RiskGroup",
            "description": (
                f"FINOS AI Deployment Model axis: "
                f"{axis_name.replace('_', ' ')}."
            ),
            "isDefinedByTaxonomy": DEPLOYMENT_TAXONOMY_ID,
        })
        for leaf_wrapper in leaves:
            if not isinstance(leaf_wrapper, dict) or len(leaf_wrapper) != 1:
                continue
            leaf_name, leaf_meta = next(iter(leaf_wrapper.items()))
            if not isinstance(leaf_name, str):
                continue
            leaf_name = leaf_name.strip()
            if not leaf_name:
                continue
            term_id = _deployment_term_id(axis_name, leaf_name)
            if term_id in seen_term_ids:
                continue
            seen_term_ids.add(term_id)
            description = ""
            if isinstance(leaf_meta, dict):
                description = str(leaf_meta.get("description", "")).strip()
            description = " ".join(description.split())  # collapse whitespace
            terms.append({
                "id": term_id,
                "name": leaf_name.replace("_", " "),
                "description": (
                    f"FINOS AI Deployment Model facet "
                    f"({axis_name.replace('_', ' ')}): {description}"
                    if description
                    else (
                        f"FINOS AI Deployment Model facet "
                        f"({axis_name.replace('_', ' ')})."
                    )
                ),
                "type": "Term",
                "isDefinedByTaxonomy": DEPLOYMENT_TAXONOMY_ID,
                "isPartOf": group_id,
            })
    return taxonomy, groups, terms


def build_nist_sp_800_53r5_controls_dataset(repo_root: Path) -> dict[str, Any]:
    """Build the standalone NIST SP 800-53 Rev. 5 native-AIRO catalogue.

    Emits a ``Container``-shaped dict with one ``RiskControlGroupTaxonomy``
    (``taxonomies:``), one ``Documentation`` row for the SP 800-53 Controls
    landing page (``documents:``), and one ``RiskControl`` per row of
    ``docs/_data/nist-sp-800-53r5.yml`` (``controls:``). The source file
    is a flat mapping of ``<control-id>: { title, url }`` rows produced
    by ``scripts/dl_nist-pdfs.py`` from PDF bookmarks.

    Cross-walks between FINOS catalogue entries and these controls are
    owned by ``linkml/src/ai_governance_framework/mappings/
    finos_to_nist_sp_800_53r5.sssom.tsv``; the per-citation
    ``ref-nist-sp-800-53r5-*`` ``Documentation`` rows emitted into the
    main FINOS catalogue via ``_FRAMEWORK_REGISTRY`` are independent
    of this file.
    """
    raw = _load_data_yaml(repo_root, "nist-sp-800-53r5")
    taxonomy: dict[str, Any] = {
        "id": NIST_SP_800_53R5_TAXONOMY_ID,
        "name": NIST_SP_800_53R5_TAXONOMY_NAME,
        "description": _folded(NIST_SP_800_53R5_TAXONOMY_DESCRIPTION),
        "type": "RiskControlGroupTaxonomy",
        "url": _format_url(NIST_SP_800_53R5_TAXONOMY_URL),
        "version": NIST_SP_800_53R5_TAXONOMY_VERSION,
        "hasDocumentation": [NIST_SP_800_53R5_DOC_ID],
    }
    document: dict[str, Any] = {
        "id": NIST_SP_800_53R5_DOC_ID,
        "name": NIST_SP_800_53R5_DOC_NAME,
        "description": _folded(NIST_SP_800_53R5_DOC_DESCRIPTION),
        "author": "NIST",
        "url": _format_url(NIST_SP_800_53R5_DOC_URL),
    }
    oscal_document: dict[str, Any] = {
        "id": NIST_SP_800_53R5_OSCAL_DOC_ID,
        "name": _folded(NIST_SP_800_53R5_OSCAL_DOC_NAME),
        "description": _folded(NIST_SP_800_53R5_OSCAL_DOC_DESCRIPTION),
        "author": "NIST",
        "url": _format_url(NIST_SP_800_53R5_OSCAL_DOC_URL),
    }
    controls: list[dict[str, Any]] = []
    for control_id, meta in raw.items():
        if not isinstance(control_id, str) or not isinstance(meta, dict):
            continue
        raw_title = str(meta.get("title", control_id)).strip()
        control_url = _nist_control_url(control_id)
        control: dict[str, Any] = {
            "id": control_id,
            "name": _normalise_control_name(raw_title, control_id),
            "type": "RiskControl",
            "detectsRiskConcept": [],
            "isDefinedByTaxonomy": NIST_SP_800_53R5_TAXONOMY_ID,
            "hasDocumentation": [NIST_SP_800_53R5_DOC_ID, NIST_SP_800_53R5_OSCAL_DOC_ID],
            "url": _format_url(control_url),
        }
        controls.append(control)
    return {
        "taxonomies": [taxonomy],
        "documents": [document, oscal_document],
        "controls": controls,
    }


# -----------------
# Generic external-standard dump helper
# -----------------


def _build_external_standard_container(
    repo_root: Path,
    *,
    source_stem: str,
    taxonomy_id: str,
    taxonomy_name: str,
    taxonomy_description: str,
    taxonomy_class: str,
    taxonomy_version: str,
    taxonomy_author: str,
    landing_doc_id: str,
    landing_doc_name: str,
    landing_doc_description: str,
    landing_doc_url: str,
    landing_doc_author: str,
    item_class: str,
    container_slot: str,
    id_prefix: str,
    description_prefix: str,
    omit_per_entry_url: bool = False,
    include_item_documentation: bool = True,
    extra_documents: list[dict[str, Any]] | None = None,
    per_entry_doc_resolver: Any = None,
) -> dict[str, Any]:
    """Emit a Container-shaped dump for one external reference standard.

    Mirrors the shape of :func:`build_nist_sp_800_53r5_controls_dataset`:
    one taxonomy + one or more parent ``Documentation`` rows + one row per
    source entry. The source file is expected to be a flat mapping of
    ``<src_id>: { title, url, ... }`` (the shape produced by the
    download scripts under ``scripts/dl_*.py``).

    Parameters:
        ``omit_per_entry_url`` \u2014 set when every source row repeats the
            same URL (e.g. ISO 42001 cites the same standard page for every
            Annex A row); the per-entry ``url`` is dropped and consumers
            follow ``hasDocumentation`` to the parent.
        ``per_entry_doc_resolver`` \u2014 optional callable
            ``(src_id, meta) -> str | None`` returning an additional
            Documentation id to append to ``hasDocumentation`` (used by SR
            11-7 to route entries to either the htm landing or the pdf
            attachment).
    """
    raw = _load_data_yaml(repo_root, source_stem)
    taxonomy: dict[str, Any] = {
        "id": taxonomy_id,
        "name": taxonomy_name,
        "description": _folded(taxonomy_description),
        "type": taxonomy_class,
        "url": _format_url(landing_doc_url),
        "version": taxonomy_version,
        "hasDocumentation": [landing_doc_id],
    }
    landing_doc: dict[str, Any] = {
        "id": landing_doc_id,
        "name": landing_doc_name,
        "description": _folded(landing_doc_description),
        "author": landing_doc_author,
        "url": _format_url(landing_doc_url),
    }
    documents: list[dict[str, Any]] = [landing_doc]
    if extra_documents:
        documents.extend(extra_documents)

    items: list[dict[str, Any]] = []
    for src_id, meta in raw.items():
        if not isinstance(src_id, str) or not isinstance(meta, dict):
            continue
        title = str(meta.get("title", src_id)).strip()
        url = str(meta.get("url", "")).strip() if meta.get("url") else ""
        item_id = f"{id_prefix}-{src_id}"
        doc_ids: list[str] = [landing_doc_id]
        if per_entry_doc_resolver is not None:
            extra_doc = per_entry_doc_resolver(src_id, meta)
            if extra_doc and extra_doc not in doc_ids:
                doc_ids.append(extra_doc)
        item: dict[str, Any] = {
            "id": item_id,
            "name": title,
            "description": f"{description_prefix}: {title}.",
            "type": item_class,
            "isDefinedByTaxonomy": taxonomy_id,
        }
        if include_item_documentation and doc_ids:
            item["hasDocumentation"] = doc_ids
        if url and not omit_per_entry_url:
            item["url"] = _format_url(url)
        items.append(item)
    return {
        "taxonomies": [taxonomy],
        "documents": documents,
        container_slot: items,
    }


def build_eu_ai_act_dataset(repo_root: Path) -> dict[str, Any]:
    """Standalone Container dump for EU AI Act obligations/requirements.

    FINOS cites article/section references from Regulation (EU) 2024/1689;
    these are normative legal duties and are modelled as concrete
    ``Requirement`` rows under ``Container.rules`` (not ``Risk`` entries).
    """
    return _build_external_standard_container(
        repo_root,
        source_stem="eu-ai-act",
        taxonomy_id=EU_AI_ACT_TAXONOMY_ID,
        taxonomy_name=EU_AI_ACT_TAXONOMY_NAME,
        taxonomy_description=EU_AI_ACT_TAXONOMY_DESCRIPTION,
        taxonomy_class="Taxonomy",
        taxonomy_version=EU_AI_ACT_TAXONOMY_VERSION,
        taxonomy_author="European Union",
        landing_doc_id=EU_AI_ACT_DOC_ID,
        landing_doc_name=EU_AI_ACT_DOC_NAME,
        landing_doc_description=EU_AI_ACT_DOC_DESCRIPTION,
        landing_doc_url=EU_AI_ACT_DOC_URL,
        landing_doc_author="Future of Life Institute",
        item_class="Requirement",
        container_slot="rules",
        id_prefix=EU_AI_ACT_TAXONOMY_ID,
        description_prefix="EU AI Act requirement",
        include_item_documentation=False,
    )


def build_iso_42001_dataset(repo_root: Path) -> dict[str, Any]:
    """Standalone Container dump for ISO/IEC 42001 Annex A controls.

    Every source row repeats the same standard-page URL, so per-entry
    ``url`` is dropped and consumers follow ``hasDocumentation`` to the
    parent.
    """
    return _build_external_standard_container(
        repo_root,
        source_stem="iso-42001",
        taxonomy_id=ISO_42001_TAXONOMY_ID,
        taxonomy_name=ISO_42001_TAXONOMY_NAME,
        taxonomy_description=ISO_42001_TAXONOMY_DESCRIPTION,
        taxonomy_class="RiskControlGroupTaxonomy",
        taxonomy_version=ISO_42001_TAXONOMY_VERSION,
        taxonomy_author="ISO/IEC",
        landing_doc_id=ISO_42001_DOC_ID,
        landing_doc_name=ISO_42001_DOC_NAME,
        landing_doc_description=ISO_42001_DOC_DESCRIPTION,
        landing_doc_url=ISO_42001_DOC_URL,
        landing_doc_author="ISO/IEC",
        item_class="RiskControl",
        container_slot="controls",
        id_prefix=ISO_42001_TAXONOMY_ID,
        description_prefix="ISO/IEC 42001:2023 Annex A control",
        omit_per_entry_url=True,
    )


def build_nist_ai_600_1_dataset(repo_root: Path) -> dict[str, Any]:
    """Standalone Container dump for NIST AI 600-1 generative-AI risks.

    Source rows carry per-section PDF anchor URLs; the canonical
    persistent identifier is the DOI redirect. Per-entry anchor URLs are
    dropped and consumers follow ``hasDocumentation`` to the canonical
    DOI landing page.
    """
    return _build_external_standard_container(
        repo_root,
        source_stem="nist-ai-600-1",
        taxonomy_id=NIST_AI_600_1_TAXONOMY_ID,
        taxonomy_name=NIST_AI_600_1_TAXONOMY_NAME,
        taxonomy_description=NIST_AI_600_1_TAXONOMY_DESCRIPTION,
        taxonomy_class="RiskTaxonomy",
        taxonomy_version=NIST_AI_600_1_TAXONOMY_VERSION,
        taxonomy_author="NIST",
        landing_doc_id=NIST_AI_600_1_DOC_ID,
        landing_doc_name=NIST_AI_600_1_DOC_NAME,
        landing_doc_description=NIST_AI_600_1_DOC_DESCRIPTION,
        landing_doc_url=NIST_AI_600_1_DOC_URL,
        landing_doc_author="NIST",
        item_class="Risk",
        container_slot="entries",
        id_prefix=NIST_AI_600_1_TAXONOMY_ID,
        description_prefix="NIST AI 600-1 generative AI risk",
        omit_per_entry_url=True,
    )


def build_owasp_llm_dataset(repo_root: Path) -> dict[str, Any]:
    """Standalone Container dump for the OWASP Top 10 for LLM Apps (2025)."""
    return _build_external_standard_container(
        repo_root,
        source_stem="owasp-llm",
        taxonomy_id=OWASP_LLM_TAXONOMY_ID,
        taxonomy_name=OWASP_LLM_TAXONOMY_NAME,
        taxonomy_description=OWASP_LLM_TAXONOMY_DESCRIPTION,
        taxonomy_class="RiskTaxonomy",
        taxonomy_version=OWASP_LLM_TAXONOMY_VERSION,
        taxonomy_author="OWASP",
        landing_doc_id=OWASP_LLM_DOC_ID,
        landing_doc_name=OWASP_LLM_DOC_NAME,
        landing_doc_description=OWASP_LLM_DOC_DESCRIPTION,
        landing_doc_url=OWASP_LLM_DOC_URL,
        landing_doc_author="OWASP",
        item_class="Risk",
        container_slot="entries",
        id_prefix=OWASP_LLM_TAXONOMY_ID,
        description_prefix="OWASP Top 10 for LLM Applications risk",
    )


def build_owasp_ml_dataset(repo_root: Path) -> dict[str, Any]:
    """Standalone Container dump for the OWASP ML Security Top 10 (2023)."""
    return _build_external_standard_container(
        repo_root,
        source_stem="owasp-ml",
        taxonomy_id=OWASP_ML_TAXONOMY_ID,
        taxonomy_name=OWASP_ML_TAXONOMY_NAME,
        taxonomy_description=OWASP_ML_TAXONOMY_DESCRIPTION,
        taxonomy_class="RiskTaxonomy",
        taxonomy_version=OWASP_ML_TAXONOMY_VERSION,
        taxonomy_author="OWASP",
        landing_doc_id=OWASP_ML_DOC_ID,
        landing_doc_name=OWASP_ML_DOC_NAME,
        landing_doc_description=OWASP_ML_DOC_DESCRIPTION,
        landing_doc_url=OWASP_ML_DOC_URL,
        landing_doc_author="OWASP",
        item_class="Risk",
        container_slot="entries",
        id_prefix=OWASP_ML_TAXONOMY_ID,
        description_prefix="OWASP ML Security Top 10 risk",
    )


def build_sr_11_7_dataset(repo_root: Path) -> dict[str, Any]:
    """Standalone Container dump for Federal Reserve / OCC SR 11-7 sections.

    Source rows split across two URLs (the htm landing page and the pdf
    attachment containing the full guidance text). Both are emitted as
    Documentation rows; each entry references whichever Documentation
    matches its source URL via ``hasDocumentation``.
    """
    attachment_doc: dict[str, Any] = {
        "id": SR_11_7_ATTACHMENT_DOC_ID,
        "name": SR_11_7_ATTACHMENT_DOC_NAME,
        "description": _folded(SR_11_7_ATTACHMENT_DOC_DESCRIPTION),
        "author": "Federal Reserve / OCC",
        "url": _format_url(SR_11_7_ATTACHMENT_DOC_URL),
    }

    def _resolver(src_id: str, meta: dict[str, Any]) -> str | None:
        url = str(meta.get("url", "")).strip()
        if url == SR_11_7_ATTACHMENT_DOC_URL:
            return SR_11_7_ATTACHMENT_DOC_ID
        return None

    return _build_external_standard_container(
        repo_root,
        source_stem="sr11-7",
        taxonomy_id=SR_11_7_TAXONOMY_ID,
        taxonomy_name=SR_11_7_TAXONOMY_NAME,
        taxonomy_description=SR_11_7_TAXONOMY_DESCRIPTION,
        taxonomy_class="RiskTaxonomy",
        taxonomy_version=SR_11_7_TAXONOMY_VERSION,
        taxonomy_author="Federal Reserve / OCC",
        landing_doc_id=SR_11_7_DOC_ID,
        landing_doc_name=SR_11_7_DOC_NAME,
        landing_doc_description=SR_11_7_DOC_DESCRIPTION,
        landing_doc_url=SR_11_7_DOC_URL,
        landing_doc_author="Federal Reserve / OCC",
        item_class="Risk",
        container_slot="entries",
        id_prefix=SR_11_7_TAXONOMY_ID,
        description_prefix="SR 11-7 guidance section",
        extra_documents=[attachment_doc],
        per_entry_doc_resolver=_resolver,
    )


def build_ffiec_it_handbook_dataset(repo_root: Path) -> dict[str, Any]:
    """Standalone Container dump for the FFIEC IT Examination Handbook.

    Each row in ``ffiec-itbooklets.yml`` carries a ``booklet_abbrev``
    grouping marker. The 11 distinct booklets are emitted as ``Group``
    rows (``Container.groups``); each booklet's root row supplies the
    booklet's landing-page Documentation and the remaining rows are
    section Documentation children referencing the group via
    ``isCategorizedAs``.
    """
    raw = _load_data_yaml(repo_root, "ffiec-itbooklets")

    # Split rows into booklet-root rows (id == booklet_abbrev) and
    # per-section rows. Preserve source order.
    booklet_roots: dict[str, dict[str, Any]] = {}
    section_rows: list[tuple[str, dict[str, Any]]] = []
    for src_id, meta in raw.items():
        if not isinstance(src_id, str) or not isinstance(meta, dict):
            continue
        abbrev = str(meta.get("booklet_abbrev", "")).strip()
        if not abbrev:
            continue
        if src_id == abbrev:
            booklet_roots[abbrev] = meta
        else:
            section_rows.append((src_id, meta))

    taxonomy: dict[str, Any] = {
        "id": FFIEC_IT_TAXONOMY_ID,
        "name": FFIEC_IT_TAXONOMY_NAME,
        "description": _folded(FFIEC_IT_TAXONOMY_DESCRIPTION),
        "url": _format_url(FFIEC_IT_DOC_URL),
        "version": FFIEC_IT_TAXONOMY_VERSION,
        "hasDocumentation": [FFIEC_IT_DOC_ID],
    }
    landing_doc: dict[str, Any] = {
        "id": FFIEC_IT_DOC_ID,
        "name": FFIEC_IT_DOC_NAME,
        "description": _folded(FFIEC_IT_DOC_DESCRIPTION),
        "author": "FFIEC",
        "url": _format_url(FFIEC_IT_DOC_URL),
    }

    documents: list[dict[str, Any]] = [landing_doc]
    groups: list[dict[str, Any]] = []

    # One Documentation per booklet root + one Group per booklet.
    for abbrev, meta in booklet_roots.items():
        booklet_doc_id = f"ffiec-itbook-{abbrev}"
        booklet_group_id = f"ffiec-it-group-{abbrev}"
        booklet_title = str(meta.get("title", abbrev)).strip()
        booklet_url = str(meta.get("url", "")).strip()
        documents.append({
            "id": booklet_doc_id,
            "name": booklet_title,
            "description": (
                f"FFIEC IT Examination Handbook booklet: {booklet_title}."
            ),
            "author": "FFIEC",
            "url": _format_url(booklet_url),
        })
        groups.append({
            "id": booklet_group_id,
            "name": booklet_title,
            "description": (
                f"FFIEC IT Examination Handbook booklet grouping: "
                f"{booklet_title}."
            ),
            "hasDocumentation": [booklet_doc_id],
        })

    # One Documentation per section, referencing its booklet group.
    for src_id, meta in section_rows:
        abbrev = str(meta.get("booklet_abbrev", "")).strip()
        section_doc_id = f"ffiec-itbook-{src_id}"
        section_url = str(meta.get("url", "")).strip()
        documents.append({
            "id": section_doc_id,
            "name": str(meta.get("title", src_id)).strip(),
            "author": "FFIEC",
            "url": _format_url(section_url),
            "isCategorizedAs": [f"ffiec-it-group-{abbrev}"],
        })

    return {
        "taxonomies": [taxonomy],
        "documents": documents,
        "groups": groups,
    }


def build_risk_entries(
    md_paths: list[Path],
    registry: DocRegistry,
    id_map: dict[str, str],
    xrefs: "CrossRefIndex",
) -> tuple[list[dict[str, Any]], set[str]]:
    """Build Risk entries with cross-references resolved via ``xrefs``.

    Cross-reference wiring (all populated from the front-matter +
    pre-processed :class:`CrossRefIndex`):

    * ``related_mappings`` — union of intra-FINOS related risks
      (``related_risks:``, translated to AIR ids) and normalised
      external-framework section ids derived from
      ``<framework>_references:`` slots. Mapped under ``skos:relatedMatch``
      semantics (no slot value is more specific than that today).
    * ``hasRelatedAction`` — reverse map: every PREV mitigation whose
      ``mitigates:`` list cites this risk (Action target class).
    * ``isDetectedBy`` — reverse map: every DET mitigation whose
      ``mitigates:`` list cites this risk (RiskControl target class).
    """
    entries: list[dict[str, Any]] = []
    used_kinds: set[str] = set()
    for path in md_paths:
        fm = parse_front_matter(path)
        legacy_id = extract_id(path)
        rid = id_map[legacy_id]
        risk_type = (fm.get("type") or "").strip()
        if risk_type not in VALID_RISK_TYPES:
            raise ValueError(
                f"{path.name}: risk type {risk_type!r} not in {VALID_RISK_TYPES}"
            )
        used_kinds.add(risk_type)
        doc_refs: list[str] = [FINOS_DOC_ID]
        fm_doc_ids, fm_term_ids = registry.collect_front_matter_refs(fm)
        for doc_id in fm_doc_ids:
            if doc_id not in doc_refs:
                doc_refs.append(doc_id)
        # related_mappings: intra-FINOS related_risks + external framework refs.
        related: list[str] = []
        for raw in fm.get("related_risks") or []:
            if not isinstance(raw, str):
                continue
            air = id_map.get(raw.strip())
            if air and air != rid and air not in related:
                related.append(air)
        for fid in xrefs.framework_refs(fm):
            if fid not in related:
                related.append(fid)
        entry: dict[str, Any] = {
            "id": rid,
            "name": str(fm.get("title", rid)).strip(),
            "description": first_paragraph(fm.get("_body", "")),
            "type": "Risk",
            "isDefinedByTaxonomy": TAXONOMY_ID,
            "isPartOf": _group_id(risk_type),
            "hasDocumentation": doc_refs,
        }
        first_links_url = _first_url_from_links_section(fm.get("_body", ""))
        if first_links_url:
            entry["url"] = _format_url(first_links_url)
        if fm_term_ids:
            entry["isCategorizedAs"] = list(fm_term_ids)
        if related:
            entry["related_mappings"] = related
        actions_for = xrefs.actions_for_risk(rid)
        if actions_for:
            entry["hasRelatedAction"] = actions_for
        controls_for = xrefs.controls_for_risk(rid)
        if controls_for:
            entry["isDetectedBy"] = controls_for
        entries.append(entry)
    return entries, used_kinds


def build_action_entries(
    md_paths: list[Path],
    registry: DocRegistry,
    id_map: dict[str, str],
    xrefs: "CrossRefIndex",
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], set[str]]:
    """Build Action + RiskControl entries from mitigation markdown files.

    The FINOS ``type:`` enum (``PREV``, ``DET``, ``RESP``) is split
    across two upstream classes:

    * ``DET`` rows land as ``RiskControl`` instances under the
      ``controls:`` collection (canonical slot is ``detectsRiskConcept``,
      matching upstream Granite Guardian detection rows in
      ``upstream-releases/ai-atlas-nexus/.../granite_guardian_dimensions.yaml``).
    * ``PREV`` / ``RESP`` rows land as ``Action`` instances under the
      ``actions:`` collection (slot is ``hasRelatedRisk``).

    Returns ``(actions, controls, used_action_kinds)`` so the
    orchestrator can emit one ``RiskControlGroup`` per kind actually
    referenced. Cross-references populated:

    * Mitigation ``mitigates:`` -> ``hasRelatedRisk`` (Action) or
      ``detectsRiskConcept`` (RiskControl), AIR-id translated.
    * Mitigation ``related_mitigations:`` + ``<framework>_references:``
      -> ``related_mappings`` (skos:relatedMatch).
    """
    actions: list[dict[str, Any]] = []
    controls: list[dict[str, Any]] = []
    used_action_kinds: set[str] = set()
    for path in md_paths:
        fm = parse_front_matter(path)
        legacy_id = extract_id(path)
        mid = id_map[legacy_id]
        action_type = (fm.get("type") or "").strip()
        if action_type not in VALID_ACTION_KINDS:
            raise ValueError(
                f"{path.name}: mitigation type {action_type!r} not in "
                f"{VALID_ACTION_KINDS}"
            )
        used_action_kinds.add(action_type)
        mitigates = _translate_refs(
            [r for r in (fm.get("mitigates") or []) if isinstance(r, str)],
            id_map,
        )
        doc_refs: list[str] = [FINOS_DOC_ID]
        fm_doc_ids, fm_term_ids = registry.collect_front_matter_refs(fm)
        for doc_id in fm_doc_ids:
            if doc_id not in doc_refs:
                doc_refs.append(doc_id)
        categories: list[str] = [_control_group_id(action_type)]
        for tid in fm_term_ids:
            if tid not in categories:
                categories.append(tid)
        # related_mappings: sibling mitigations + framework refs.
        related: list[str] = []
        for raw in fm.get("related_mitigations") or []:
            if not isinstance(raw, str):
                continue
            air = id_map.get(raw.strip())
            if air and air != mid and air not in related:
                related.append(air)
        for fid in xrefs.framework_refs(fm):
            if fid not in related:
                related.append(fid)
        record: dict[str, Any] = {
            "id": mid,
            "name": str(fm.get("title", mid)).strip(),
            "description": first_paragraph(fm.get("_body", "")),
            "isDefinedByTaxonomy": TAXONOMY_ID,
            "isCategorizedAs": categories,
            "hasDocumentation": doc_refs,
        }
        first_links_url = _first_url_from_links_section(fm.get("_body", ""))
        if first_links_url:
            record["url"] = _format_url(first_links_url)
        if related:
            record["related_mappings"] = related
        emitted_as = xrefs.mitigation_emitted_as(legacy_id)
        if emitted_as == "RiskControl":
            # ``Container.controls`` has abstract range ``Control``; the
            # ``type:`` discriminator (designates_type: true on Control)
            # tells the LinkML loader to instantiate the concrete
            # subclass.
            record["type"] = "RiskControl"
            if mitigates:
                record["detectsRiskConcept"] = mitigates
            controls.append(record)
        else:
            if mitigates:
                record["hasRelatedRisk"] = mitigates
            actions.append(record)
    return actions, controls, used_action_kinds


def build_usecase_entries(
    md_paths: list[Path],
    registry: DocRegistry,
    stakeholders: list[dict[str, Any]],
    id_map: dict[str, str],
) -> tuple[
    list[dict[str, Any]],  # AiSystem entries
    list[dict[str, Any]],  # Purpose entries (one per use-case w/ business_value)
    list[dict[str, Any]],  # Domain entries (one per distinct category)
]:
    """Build AiSystem entries from use-case markdown files.

    Side effects:

    * Appends one deduplicated ``Documentation`` per ``further_reading``
      link (via :class:`DocRegistry`) plus any framework-citation /
      data-classification / regulatory-concern / data-handling-aspect
      Documentation rows implied by the post's front-matter, and wires
      the entry's ``hasDocumentation`` to the resulting ids.
    * Appends one ``Stakeholder`` instance per comma-separated role
      named in ``end_user:`` (deduplicated across the whole corpus)
      into the caller-supplied ``stakeholders`` list, and wires the
      entry's ``hasStakeholder`` to the resulting ids.
    * Wires ``isCategorizedAs`` to the Documentation rows materialised
      for ``data_handling_aspects:`` tokens (e.g. ``Centralized``).
    * Materialises one ``Purpose`` entry per use-case with a
      non-empty ``business_value:`` (id: ``purpose-<uc-uid>``) and
      wires it via ``hasPurpose``.
    * Materialises one ``Domain`` entry per distinct ``category:``
      value (id: ``domain-<slug>``) under the AI use-cases taxonomy
      and wires it via ``isAppliedWithinDomain``. Replaces the
      pre-G28 ``isCategorizedAs: [<AI_UC_TAXONOMY_ID>]`` anchor.
    """
    entries: list[dict[str, Any]] = []
    purposes: list[dict[str, Any]] = []
    domains: list[dict[str, Any]] = []
    domains_by_id: dict[str, dict[str, Any]] = {}
    for path in md_paths:
        fm = parse_front_matter(path)
        legacy_id = extract_id(path)
        uid = id_map[legacy_id]
        related_risks = _translate_refs(
            [
                r for r in (fm.get("related_risks") or [])
                if isinstance(r, str)
            ],
            id_map,
        )
        doc_refs: list[str] = [FINOS_DOC_ID]
        for fr in fm.get("further_reading") or []:
            if not isinstance(fr, dict) or not fr.get("name"):
                continue
            url = str(fr.get("url", "")).strip() if fr.get("url") else None
            # Prefer explicit source, then try URL extraction
            author = str(fr.get("source", "")).strip() if fr.get("source") else ""
            if not author and url:
                author = _extract_author_from_url(url)
            doc: dict[str, Any] = {
                "id": _doc_id_slug("doc", str(fr["name"])),
                "name": str(fr["name"]).strip(),
            }
            if author:
                doc["author"] = author
            if url:
                doc["url"] = url
            doc_id = registry.ensure(doc)
            if doc_id not in doc_refs:
                doc_refs.append(doc_id)
        fm_doc_ids, fm_term_ids = registry.collect_front_matter_refs(fm)
        for doc_id in fm_doc_ids:
            if doc_id not in doc_refs:
                doc_refs.append(doc_id)

        # data_handling_aspects -> Documentation rows + isCategorizedAs
        # on the AiSystem.
        categories: list[str] = []
        for aspect in fm.get("data_handling_aspects") or []:
            if not isinstance(aspect, str):
                continue
            doc_id = registry.ensure_data_handling_aspect(aspect)
            if doc_id and doc_id not in categories:
                categories.append(doc_id)

        # category: -> Domain entry + isAppliedWithinDomain on the
        # AiSystem (G28, ai-atlas-nexus #188). The Domain row is
        # deduplicated by slug across the whole corpus and pinned to
        # the AI use-cases taxonomy (Level-1 sectors).
        cat_raw = (fm.get("category") or "").strip()
        domain_ids: list[str] = []
        if cat_raw:
            domain_id = _doc_id_slug("domain", cat_raw)
            if domain_id not in domains_by_id:
                domain_row: dict[str, Any] = {
                    "id": domain_id,
                    "name": cat_raw.replace("_", " "),
                    "description": (
                        f"FINOS AI use-case domain: "
                        f"{cat_raw.replace('_', ' ')}."
                    ),
                    "type": "Domain",
                    "isDefinedByTaxonomy": AI_UC_TAXONOMY_ID,
                }
                domains_by_id[domain_id] = domain_row
                domains.append(domain_row)
            domain_ids.append(domain_id)

        # business_value: -> Purpose entry + hasPurpose on the AiSystem
        # (G28, ai-atlas-nexus #188). One Purpose row per use-case
        # (the text is freeform per system), id: ``purpose-<uc-uid>``.
        purpose_ids: list[str] = []
        bv_raw = (fm.get("business_value") or "").strip()
        if bv_raw:
            purpose_id = _doc_id_slug("purpose", uid)
            purposes.append({
                "id": purpose_id,
                "name": f"{str(fm.get('title', uid)).strip()} — business value",
                "description": bv_raw,
                "type": "Purpose",
                "isDefinedByTaxonomy": AI_UC_TAXONOMY_ID,
            })
            purpose_ids.append(purpose_id)

        # data_classifications -> Term ids on isCategorizedAs.
        for tid in fm_term_ids:
            if tid not in categories:
                categories.append(tid)

        # end_user -> Stakeholder instances + hasStakeholder on the
        # AiSystem. The raw string is comma-separated free-text.
        stakeholder_ids: list[str] = []
        end_user = (fm.get("end_user") or "").strip()
        if end_user:
            for raw in end_user.split(","):
                sid = registry.ensure_stakeholder(raw.strip(), stakeholders)
                if sid and sid not in stakeholder_ids:
                    stakeholder_ids.append(sid)

        entry: dict[str, Any] = {
            "id": uid,
            "name": str(fm.get("title", uid)).strip(),
            "description": str(
                fm.get("description") or first_paragraph(fm.get("_body", ""))
            ).strip(),
            "type": "AiSystem",
            "hasDocumentation": doc_refs,
        }
        if related_risks:
            entry["hasRelatedRisk"] = related_risks
        if stakeholder_ids:
            entry["hasStakeholder"] = stakeholder_ids
        if domain_ids:
            entry["isAppliedWithinDomain"] = domain_ids
        if purpose_ids:
            entry["hasPurpose"] = purpose_ids
        if categories:
            entry["isCategorizedAs"] = categories
        entries.append(entry)
    return entries, purposes, domains


# -----------------
# Orchestration
# -----------------


def build_dataset(repo_root: Path) -> dict[str, Any]:
    docs_root = repo_root / "docs"
    risk_files = _numeric_md_files(docs_root / "_risks", "ri")
    mit_files = _numeric_md_files(docs_root / "_mitigations", "mi")
    uc_files = _numeric_md_files(docs_root / "_usecases", "uc")

    documents = build_documents()
    registry = DocRegistry(repo_root, documents)
    stakeholders: list[dict[str, Any]] = []
    # Build the legacy-id -> AIR-style-id map up-front so cross-references
    # in `mitigates:` / `related_risks:` can be translated consistently.
    id_map = build_id_map(risk_files, mit_files, uc_files)
    # Pre-processing pass: classify each mitigation as Action vs
    # RiskControl and build reverse-lookup tables so risk entries can
    # later carry ``hasRelatedAction`` / ``isDetectedBy`` without a
    # second I/O pass over the markdown files.
    xrefs = CrossRefIndex.build(id_map, risk_files, mit_files)
    risk_entries, used_kinds = build_risk_entries(
        risk_files, registry, id_map, xrefs
    )
    groups = build_groups(used_kinds)
    actions, controls, used_action_kinds = build_action_entries(
        mit_files, registry, id_map, xrefs
    )
    groups.extend(build_control_groups(used_action_kinds))
    usecase_entries, purpose_entries, domain_entries = build_usecase_entries(
        uc_files, registry, stakeholders, id_map
    )

    # AI use-case taxonomy (ai-atlas-nexus #190 / G30): one
    # AiTaskTaxonomy + AiTaskDomain per Level-1 sector + AiTaskGroup
    # per Level-2 subcategory + AiTask per Level-3 leaf, all sourced
    # from docs/_data/ai_use_cases.yml.
    uc_taxonomy, uc_task_domains, uc_task_groups, uc_ai_tasks = (
        build_ai_use_cases_taxonomy(repo_root)
    )
    groups.extend(uc_task_domains)
    groups.extend(uc_task_groups)

    # Cross-cutting AI capabilities: 1 CapabilityTaxonomy + 1 CapabilityGroup
    # + 5 Capability entries. Sourced from the ``cross_cutting_capabilities:``
    # list in docs/_data/ai_use_cases.yml.
    caps_taxonomy, caps_group, cap_entries = build_cross_cutting_capabilities(
        repo_root
    )
    groups.append(caps_group)

    # FINOS AI Deployment Model: 1 RiskTaxonomy + 7 RiskGroups (one per
    # axis) + 38 Term entries (one per leaf). Sourced from
    # docs/_data/ai_deployment_model.yml. Use-case ``data_handling_aspects:``
    # front-matter resolves to Term ids under the ``data_handling`` axis.
    dep_taxonomy, dep_groups, dep_terms = (
        build_ai_deployment_model_taxonomy(repo_root)
    )
    groups.extend(dep_groups)

    # Lossless ``data_classification.yml`` backfill. Cited classifications
    # are materialised lazily by ``ensure_data_classification`` during the
    # use-case pass; this fills in any rows not currently cited so the
    # full FINOS-authored registry is in the dump. External-framework
    # section registries (ISO Annex A, NIST controls, EU AI Act articles,
    # etc.) are deliberately NOT eagerly emitted here — they are external
    # standards' content, not FINOS data, and cross-walks live in the
    # SSSOM TSVs (see linkml/scripts/build_sssom_mappings.py).
    registry.emit_all_data_classifications()
    registry.emit_all_jurisdictions()

    organizations = build_organizations()

    container: dict[str, Any] = {
        "organizations": organizations,
        "documents": documents,
        "taxonomies": [build_taxonomy(), uc_taxonomy, caps_taxonomy, dep_taxonomy],
        "vocabularies": build_vocabularies(),
        "groups": groups,
        "entries": (
            risk_entries + usecase_entries + cap_entries
            + purpose_entries + domain_entries
            + registry.terms + dep_terms
        ),
        "actions": actions,
        "aitasks": uc_ai_tasks,
    }
    if stakeholders:
        container["stakeholders"] = stakeholders
    if controls:
        container["controls"] = controls
    return container


# -----------------
# Test-fixture emission
# -----------------


def _strip_type(row: dict[str, Any]) -> dict[str, Any]:
    """Drop the polymorphic ``type:`` discriminator from a copy of the row.

    The discriminator is required when the row appears under
    ``Container.entries`` (which has abstract range ``Entry``). When a row
    is loaded standalone with ``target_class=Risk`` / ``AiSystem``, the
    loader rejects a ``type`` slot that the concrete class does not declare.
    """
    return {k: v for k, v in row.items() if k != "type"}


def emit_valid_fixtures(
    repo_root: Path, dataset: dict[str, Any]
) -> list[Path]:
    """Emit one per-class single-instance fixture under tests/data/valid/.

    Filenames use upstream class names so ``linkml/tests/test_data.py``
    (which splits the stem on ``-``) can look them up directly in the
    generated ``ai_governance_framework.datamodel`` module.
    """
    valid = repo_root / "linkml" / "tests" / "data" / "valid"
    valid.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    risks = [e for e in dataset["entries"] if e.get("type") == "Risk"]
    aisystems = [e for e in dataset["entries"] if e.get("type") == "AiSystem"]
    terms = [e for e in dataset["entries"] if e.get("type") == "Term"]
    caps = [e for e in dataset["entries"] if e.get("type") == "Capability"]
    purposes = [e for e in dataset["entries"] if e.get("type") == "Purpose"]
    domains = [e for e in dataset["entries"] if e.get("type") == "Domain"]
    actions = dataset["actions"]
    controls = dataset.get("controls", [])
    documents = dataset["documents"]
    taxonomies = dataset["taxonomies"]
    groups = dataset["groups"]
    ai_task_taxonomies = [t for t in taxonomies if t.get("type") == "AiTaskTaxonomy"]
    ai_task_domains = [g for g in groups if g.get("type") == "AiTaskDomain"]
    ai_task_groups = [g for g in groups if g.get("type") == "AiTaskGroup"]

    if risks:
        p = valid / f"Risk-{risks[0]['id']}.yaml"
        _dump(p, _strip_type(risks[0]))
        written.append(p)
    if actions:
        p = valid / f"Action-{actions[0]['id']}.yaml"
        _dump(p, actions[0])
        written.append(p)
    if controls:
        p = valid / f"RiskControl-{controls[0]['id']}.yaml"
        _dump(p, _strip_type(controls[0]))
        written.append(p)
    if aisystems:
        p = valid / f"AiSystem-{aisystems[0]['id']}.yaml"
        _dump(p, _strip_type(aisystems[0]))
        written.append(p)
    if terms:
        p = valid / f"Term-{terms[0]['id']}.yaml"
        _dump(p, _strip_type(terms[0]))
        written.append(p)
    if documents:
        p = valid / f"Documentation-{documents[0]['id']}.yaml"
        _dump(p, documents[0])
        written.append(p)
    if taxonomies:
        p = valid / f"RiskTaxonomy-{taxonomies[0]['id']}.yaml"
        _dump(p, _strip_type(taxonomies[0]))
        written.append(p)
    if groups:
        p = valid / f"RiskGroup-{groups[0]['id']}.yaml"
        _dump(p, _strip_type(groups[0]))
        written.append(p)
    if caps:
        p = valid / f"Capability-{caps[0]['id']}.yaml"
        _dump(p, _strip_type(caps[0]))
        written.append(p)
    if purposes:
        p = valid / f"Purpose-{purposes[0]['id']}.yaml"
        _dump(p, _strip_type(purposes[0]))
        written.append(p)
    if domains:
        p = valid / f"Domain-{domains[0]['id']}.yaml"
        _dump(p, _strip_type(domains[0]))
        written.append(p)
    if ai_task_taxonomies:
        p = valid / f"AiTaskTaxonomy-{ai_task_taxonomies[0]['id']}.yaml"
        _dump(p, _strip_type(ai_task_taxonomies[0]))
        written.append(p)
    if ai_task_domains:
        p = valid / f"AiTaskDomain-{ai_task_domains[0]['id']}.yaml"
        _dump(p, _strip_type(ai_task_domains[0]))
        written.append(p)
    if ai_task_groups:
        p = valid / f"AiTaskGroup-{ai_task_groups[0]['id']}.yaml"
        _dump(p, _strip_type(ai_task_groups[0]))
        written.append(p)

    # A slim Container fixture: one of each row, keeping the polymorphic
    # `type:` discriminator on entries.
    slim_container: dict[str, Any] = {
        "documents": documents[:1],
        "taxonomies": taxonomies[:1],
        "groups": groups[:1],
        "entries": (
            risks[:1] + aisystems[:1] + purposes[:1] + domains[:1]
        ),
        "actions": actions[:1],
    }
    if controls:
        slim_container["controls"] = controls[:1]
    p = valid / "Container-sample.yaml"
    _dump(p, slim_container)
    written.append(p)

    return written


def emit_invalid_fixtures(repo_root: Path) -> list[Path]:
    """Emit deliberately-broken fixtures exercising upstream constraints.

    These are documentation-grade exemplars; ``tests/test_data.py`` does
    not currently parametrize over them but they ship alongside the valid
    set as recipe references.
    """
    invalid = repo_root / "linkml" / "tests" / "data" / "invalid"
    invalid.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    # Risk missing the required `id`.
    p = invalid / "Risk-missing-id.yaml"
    _dump(p, {
        "name": "Missing identifier",
        "description": (
            "Every Entity-derived class requires an `id`; loader rejects "
            "this row."
        ),
        "isPartOf": _group_id("RC"),
    })
    written.append(p)

    # Action with hasRelatedRisk as a scalar (must be a list).
    p = invalid / "Action-bad-related-risk.yaml"
    _dump(p, {
        "id": "mi-invalid-1",
        "name": "Bad hasRelatedRisk shape",
        "description": "hasRelatedRisk is multivalued; scalar is rejected.",
        "hasRelatedRisk": 42,
    })
    written.append(p)

    # Risk with a list-shaped `isPartOf`. Upstream defines the slot as
    # single-valued (range: RiskGroup), so a sequence fails JSON Schema
    # validation. (Referential integrity for unknown group ids is a
    # build-time concern handled by build_groups()/used_kinds; jsonschema
    # alone cannot catch dangling cross-references.)
    p = invalid / "Risk-bad-group-shape.yaml"
    _dump(p, {
        "id": "ri-invalid-1",
        "name": "Bad isPartOf shape",
        "description": (
            "isPartOf is single-valued; a list is rejected by the schema."
        ),
        "isPartOf": [_group_id("RC"), _group_id("SEC")],
    })
    written.append(p)

    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help="Repository root (defaults to two levels above this script).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=(
            "Catalogue output file (defaults to "
            "linkml/tests/data/finos/finos_ai_governance_framework_v2.yaml)."
        ),
    )
    parser.add_argument(
        "--nist-sp-800-53r5-output",
        type=Path,
        default=None,
        help=(
            "NIST SP 800-53 Rev. 5 controls-catalogue output file (defaults "
            "to linkml/tests/data/finos/nist_sp_800_53_r5.yaml)."
        ),
    )
    parser.add_argument(
        "--eu-ai-act-output",
        type=Path,
        default=None,
        help=(
            "EU AI Act standalone Container dump (defaults to "
            "linkml/tests/data/finos/eu_ai_act.yaml)."
        ),
    )
    parser.add_argument(
        "--ffiec-it-handbook-output",
        type=Path,
        default=None,
        help=(
            "FFIEC IT Examination Handbook standalone Container dump "
            "(defaults to linkml/tests/data/finos/ffiec_it_handbook.yaml)."
        ),
    )
    parser.add_argument(
        "--iso-42001-output",
        type=Path,
        default=None,
        help=(
            "ISO/IEC 42001:2023 standalone Container dump (defaults to "
            "linkml/tests/data/finos/iso_42001.yaml)."
        ),
    )
    parser.add_argument(
        "--nist-ai-600-1-output",
        type=Path,
        default=None,
        help=(
            "NIST AI 600-1 (Generative AI Profile) standalone Container "
            "dump (defaults to linkml/tests/data/finos/nist_ai_600_1.yaml)."
        ),
    )
    parser.add_argument(
        "--owasp-llm-output",
        type=Path,
        default=None,
        help=(
            "OWASP Top 10 for LLM Applications standalone Container dump "
            "(defaults to linkml/tests/data/finos/owasp_llm_top_10.yaml)."
        ),
    )
    parser.add_argument(
        "--owasp-ml-output",
        type=Path,
        default=None,
        help=(
            "OWASP ML Security Top 10 standalone Container dump (defaults "
            "to linkml/tests/data/finos/owasp_ml_top_10.yaml)."
        ),
    )
    parser.add_argument(
        "--sr-11-7-output",
        type=Path,
        default=None,
        help=(
            "Federal Reserve SR 11-7 standalone Container dump (defaults "
            "to linkml/tests/data/finos/sr_11_7.yaml)."
        ),
    )
    args = parser.parse_args(argv)

    repo_root: Path = args.repo_root.resolve()
    output: Path = (
        args.output
        if args.output is not None
        else repo_root
        / "linkml"
        / "tests"
        / "data"
        / "finos"
        / "finos_ai_governance_framework_v2.yaml"
    )
    nist_output: Path = (
        args.nist_sp_800_53r5_output
        if args.nist_sp_800_53r5_output is not None
        else repo_root
        / "linkml"
        / "tests"
        / "data"
        / "finos"
        / "nist_sp_800_53_r5.yaml"
    )

    def _default_finos_output(filename: str) -> Path:
        return (
            repo_root / "linkml" / "tests" / "data" / "finos" / filename
        )

    external_outputs: dict[str, Path] = {
        "eu_ai_act": (
            args.eu_ai_act_output
            if args.eu_ai_act_output is not None
            else _default_finos_output("eu_ai_act.yaml")
        ),
        "ffiec_it_handbook": (
            args.ffiec_it_handbook_output
            if args.ffiec_it_handbook_output is not None
            else _default_finos_output("ffiec_it_handbook.yaml")
        ),
        "iso_42001": (
            args.iso_42001_output
            if args.iso_42001_output is not None
            else _default_finos_output("iso_42001.yaml")
        ),
        "nist_ai_600_1": (
            args.nist_ai_600_1_output
            if args.nist_ai_600_1_output is not None
            else _default_finos_output("nist_ai_600_1.yaml")
        ),
        "owasp_llm": (
            args.owasp_llm_output
            if args.owasp_llm_output is not None
            else _default_finos_output("owasp_llm_top_10.yaml")
        ),
        "owasp_ml": (
            args.owasp_ml_output
            if args.owasp_ml_output is not None
            else _default_finos_output("owasp_ml_top_10.yaml")
        ),
        "sr_11_7": (
            args.sr_11_7_output
            if args.sr_11_7_output is not None
            else _default_finos_output("sr_11_7.yaml")
        ),
    }

    dataset = build_dataset(repo_root)
    _dump(output, dataset)
    nist_dataset = build_nist_sp_800_53r5_controls_dataset(repo_root)
    _dump(
        nist_output,
        nist_dataset,
        header=(
            "# AUTOGENERATED by linkml/scripts/build_finos_data.py.\n"
            "# Source: docs/_data/nist-sp-800-53r5.yml\n"
            "# Format: ai-atlas-nexus Container YAML (RiskControlGroupTaxonomy"
            " + RiskControl rows).\n"
        ),
    )

    external_specs: list[tuple[str, str, str, str, Any]] = [
        (
            "eu_ai_act",
            "docs/_data/eu-ai-act.yml",
            "Taxonomy + Requirement rows (per article).",
            "rules",
            build_eu_ai_act_dataset,
        ),
        (
            "ffiec_it_handbook",
            "docs/_data/ffiec-itbooklets.yml",
            "Taxonomy + Group rows (per booklet) + Documentation rows "
            "(per section).",
            "groups",
            build_ffiec_it_handbook_dataset,
        ),
        (
            "iso_42001",
            "docs/_data/iso-42001.yml",
            "RiskControlGroupTaxonomy + RiskControl rows (Annex A).",
            "controls",
            build_iso_42001_dataset,
        ),
        (
            "nist_ai_600_1",
            "docs/_data/nist-ai-600-1.yml",
            "RiskTaxonomy + Risk rows (generative-AI profile).",
            "entries",
            build_nist_ai_600_1_dataset,
        ),
        (
            "owasp_llm",
            "docs/_data/owasp-llm.yml",
            "RiskTaxonomy + Risk rows (OWASP Top 10 for LLM Apps).",
            "entries",
            build_owasp_llm_dataset,
        ),
        (
            "owasp_ml",
            "docs/_data/owasp-ml.yml",
            "RiskTaxonomy + Risk rows (OWASP ML Security Top 10).",
            "entries",
            build_owasp_ml_dataset,
        ),
        (
            "sr_11_7",
            "docs/_data/sr11-7.yml",
            "RiskTaxonomy + Risk rows (SR 11-7 supervisory letter).",
            "entries",
            build_sr_11_7_dataset,
        ),
    ]
    external_datasets: dict[str, dict[str, Any]] = {}
    for key, source, shape, _slot, builder in external_specs:
        ds = builder(repo_root)
        external_datasets[key] = ds
        _dump(
            external_outputs[key],
            ds,
            header=(
                "# AUTOGENERATED by linkml/scripts/build_finos_data.py.\n"
                f"# Source: {source}\n"
                f"# Format: ai-atlas-nexus Container YAML ({shape})\n"
            ),
        )

    valid_paths = emit_valid_fixtures(repo_root, dataset)
    invalid_paths = emit_invalid_fixtures(repo_root)

    caps_count = sum(1 for e in dataset["entries"] if e.get("type") == "Capability")
    print(
        f"Wrote {output.relative_to(repo_root)}: "
        f"{len(dataset['documents'])} documents, "
        f"{len(dataset['taxonomies'])} taxonomies, "
        f"{len(dataset['vocabularies'])} vocabularies, "
        f"{len(dataset['groups'])} groups, "
        f"{len(dataset['entries'])} entries "
        f"({caps_count} capabilities), "
        f"{len(dataset['actions'])} actions, "
        f"{len(dataset.get('controls', []))} controls."
    )
    print(
        f"Wrote {nist_output.relative_to(repo_root)}: "
        f"{len(nist_dataset['taxonomies'])} taxonomies, "
        f"{len(nist_dataset['documents'])} documents, "
        f"{len(nist_dataset['controls'])} controls."
    )
    for key, _src, _shape, slot, _builder in external_specs:
        ds = external_datasets[key]
        out_path = external_outputs[key]
        bits = [
            f"{len(ds.get('taxonomies', []))} taxonomies",
            f"{len(ds.get('documents', []))} documents",
        ]
        if ds.get("groups") and slot != "groups":
            bits.append(f"{len(ds['groups'])} groups")
        bits.append(f"{len(ds.get(slot, []))} {slot}")
        print(
            f"Wrote {out_path.relative_to(repo_root)}: " + ", ".join(bits) + "."
        )
    print(
        f"Wrote {len(valid_paths)} valid + {len(invalid_paths)} invalid "
        f"per-class fixtures under linkml/tests/data/."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
