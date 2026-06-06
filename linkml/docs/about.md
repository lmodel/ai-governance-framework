# FINOS AI Governance Framework — LinkML Schema

A LinkML profile expressing the FINOS AI Governance Framework catalogue (risks, mitigations, use cases) as native data over the [IBM ai-atlas-nexus](https://github.com/IBM/ai-atlas-nexus) `ai-risk-ontology` schema, with cross-walks to ISO 42001 / NIST AI 600-1 / NIST SP 800-53r5 / EU AI Act / SR 11-7 / FFIEC IT / OWASP LLM / OWASP ML published as SSSOM TSVs.

---

## Architecture

```ascii
┌────────────────────────────────────────────────────────────┐
│   FINOS AI Governance Framework - LinkML Schema            │
│     Nominal schema + compliant data + cross-walks only     │
└────────────────────┬─────────────────────┬─────────────────┘
                     │                     │
            ┌────────▼─────────┐   ┌────────▼─────────┐
            │  ai-atlas-nexus  │   │  SSSOM cross-    │
            │ (vendored 0.5.0) │   │  walks (8 TSVs)  │
            └──────────────────┘   └──────────────────┘
```

The FINOS AI Governance Framework LinkML schema is import-only; everything FINOS-specific
exists in generated data files plus the SSSOM cross-walk files.

---

## Module layout

```
linkml/src/ai_governance_framework/
  schema/
    ai_governance_framework.yaml      # umbrella — imports only (~45 lines)
    ai_risk_ontology/                 # vendored ai-atlas-nexus 0.5.0
  mappings/
    finos_to_nist_sp_800_53r5.sssom.tsv  # 181 rows
    finos_to_eu_ai_act.sssom.tsv      # 67 rows
    finos_to_ffiec_it.sssom.tsv       # 56 rows
    finos_to_iso42001.sssom.tsv       # 49 rows
    finos_to_owasp_llm.sssom.tsv      # 22 rows
    finos_to_nist_ai_600_1.sssom.tsv  # 17 rows
    finos_to_sr_11_7.sssom.tsv        # 11 rows
    finos_to_owasp_ml.sssom.tsv       # 8 rows
    finos_to_dpv_ai.sssom.tsv         # bridge (hand-curated)
    finos_to_ibm_risk_atlas.sssom.tsv # chain hub (hand-curated)
linkml/scripts/
  build_finos_data.py                 # Jekyll + docs/_data/ -> AIRO Container exporter
  build_sssom_mappings.py             # citation-driven SSSOM generator
linkml/tests/data/
  finos/finos_ai_governance_framework_v2.yaml  # canonical dump
  finos/nist_sp_800_53_r5.yaml                 # standalone NIST SP 800-53 controls dump
  finos/eu_ai_act.yaml                         # standalone EU AI Act dump
  finos/ffiec_it_handbook.yaml                 # standalone FFIEC IT Handbook dump
  finos/iso_42001.yaml                         # standalone ISO/IEC 42001 dump
  finos/nist_ai_600_1.yaml                     # standalone NIST AI 600-1 dump
  finos/owasp_llm_top_10.yaml                  # standalone OWASP LLM Top 10 dump
  finos/owasp_ml_top_10.yaml                   # standalone OWASP ML Top 10 dump
  finos/sr_11_7.yaml                           # standalone SR 11-7 dump
  valid/                              # per-class single-instance fixtures
  invalid/                            # constraint-violation fixtures
```

---

## Current state (2026-06-05)

### Schema

| Property | Value |
|---|---|
| Local LinkML classes / slots / enums | **0 / 0 / 0** |
| Total local LinkML | ~45 lines (umbrella imports only) |
| Container collections used | `documents`, `taxonomies`, `vocabularies`, `groups`, `entries`, `actions`, `aitasks`, `stakeholders` |

### Catalogue dump — `finos_ai_governance_framework_v2.yaml`

| Container collection | Count | Composition |
|---|---:|---|
| `documents` | 49 | FINOS site (1) · data-classification regulatory references (41) · regulatory concerns (~5) · further-reading (2) |
| `taxonomies` | 4 | `finos-ai-governance-framework-v2` · `finos-ai-use-cases-v1` · `finos-ai-capabilities-v1` · `finos-ai-deployment-model` |
| `vocabularies` | 2 | `finos-data-sensitivity-tiers` · `finos-jurisdictions` |
| `groups` | 13 | 3 RiskGroup (RC/SEC/OP) + 2 RiskControlGroup (PREV/DET) + 1 CapabilityGroup (cross-cutting) + 7 RiskGroup (deployment-model axes) |
| `entries` | 78 | 23 Risk · 5 Capability · 50 Term (11 data classifications + 4 sensitivity tiers + 4 jurisdictions + 31 deployment-model leaves) |
| `actions` | 23 | one per `mi-*` |
| `aitasks` | 43 | Level-3 leaves of `ai_use_cases.yml` |
| `stakeholders` | 5 | one per distinct `end_user:` role |

### Standalone external-standard dumps

Eight `Container`-shaped files emitted alongside the canonical FINOS catalogue, one per external reference standard. Each is independent of the FINOS catalogue (no shared ids), and independent of the SSSOM cross-walks. Cross-walks between FINOS catalogue entries and these standards are owned by the matching `finos_to_<std>.sssom.tsv`.

| Standalone file | Source | Taxonomy class | Items | Per-entry URL | Notes |
|---|---|---|---:|---|---|
| [nist_sp_800_53_r5.yaml](../tests/data/finos/nist_sp_800_53_r5.yaml) | `docs/_data/nist-sp-800-53r5.yml` | `RiskControlGroupTaxonomy` | 321 `RiskControl` | preserved (CPRT catalogue URL per control) | 2 `Documentation` rows (controls page + OSCAL catalog) |
| [eu_ai_act.yaml](../tests/data/finos/eu_ai_act.yaml) | `docs/_data/eu-ai-act.yml` | `RiskTaxonomy` | 306 `Risk` | preserved (AI Act Explorer per article) | 1 landing `Documentation` |
| [ffiec_it_handbook.yaml](../tests/data/finos/ffiec_it_handbook.yaml) | `docs/_data/ffiec-itbooklets.yml` | `Taxonomy` | 11 `Group` (per booklet) | preserved (per-section URL) | 110 `Documentation` rows (1 landing + 11 booklet-root docs + 98 section docs); section docs reference their booklet `Group` via `isCategorizedAs` |
| [iso_42001.yaml](../tests/data/finos/iso_42001.yaml) | `docs/_data/iso-42001.yml` | `RiskControlGroupTaxonomy` | 27 `RiskControl` | **dropped** — all rows share the same standard-page URL; consumers follow `hasDocumentation` to the parent | 1 landing `Documentation` (ISO standard page) |
| [nist_ai_600_1.yaml](../tests/data/finos/nist_ai_600_1.yaml) | `docs/_data/nist-ai-600-1.yml` | `RiskTaxonomy` | 12 `Risk` | **dropped** — canonical persistent identifier is the DOI redirect, not per-section PDF anchors | 1 landing `Documentation` with canonical DOI URL (`https://doi.org/10.6028/NIST.AI.600-1`) |
| [owasp_llm_top_10.yaml](../tests/data/finos/owasp_llm_top_10.yaml) | `docs/_data/owasp-llm.yml` | `RiskTaxonomy` | 10 `Risk` | preserved | 1 landing `Documentation` |
| [owasp_ml_top_10.yaml](../tests/data/finos/owasp_ml_top_10.yaml) | `docs/_data/owasp-ml.yml` | `RiskTaxonomy` | 10 `Risk` | preserved | 1 landing `Documentation` |
| [sr_11_7.yaml](../tests/data/finos/sr_11_7.yaml) | `docs/_data/sr11-7.yml` | `RiskTaxonomy` | 15 `Risk` | preserved (htm or pdf) | 2 `Documentation` (htm landing + pdf attachment); each entry references both letter + attachment when its source URL is the pdf |

These files serve two purposes:

1. **Test data** — round-tripped through the umbrella schema by `just test`, exercising every external-standard shape.
2. **Upstream-contribution candidates** — direct input to [IBM ai-atlas-nexus](https://github.com/IBM/ai-atlas-nexus/tree/main/src/ai_atlas_nexus/data/knowledge_graph) as native reference data, complementing the existing IBM AI Risk Atlas.

#### Use cases (AiSystem entries) — FINOS catalogue only

**Design decision:** Use-case records (AiSystem entries like "Credit Risk Analysis", "Autonomous Wealth Management") are **excluded from standalone Container dumps** and remain in the main FINOS catalogue (`finos_ai_governance_framework_v2.yaml`) only.

**Rationale:** 
- Use cases are *deployed AI system examples* specific to FINOS's financial-services domain. They carry FINOS-specific semantics (stakeholder roles, governance concerns, data classifications, capabilities) and depend on FINOS-authored taxonomies (`finos-ai-use-cases-v1`, etc.).
- Standalone dumps are designed to be **framework-neutral reference containers** — each holds one external standard's native content (NIST controls, ISO provisions, OWASP entries, etc.) independent of the FINOS catalogue.
- Container schema has no `aisystems` slot; AiSystem records can only land in `entries`, but `entries` are semantically for framework-neutral entities (Risk, Capability, Term), not deployment-specific systems.
- Upstream `ai-atlas-nexus` does not define a native collection for deployed systems; such extension would couple FINOS's schema to ai-atlas-nexus, violating the "data not schema" principle.

**Implication:** Use-case records remain available in `finos_ai_governance_framework_v2.yaml` and are wired to external frameworks via the SSSOM cross-walks (8 TSVs), providing complete FINOS->framework traceability. They simply do not appear in the eight standalone dumps, which preserve the separation of concerns between FINOS deployments and external standards' reference data.

### SSSOM cross-walks

**411 citation-driven mapping rows** across 8 TSVs (one per cited framework) plus 2 hand-curated bridges:

| TSV | Rows |
|---|---:|
| `finos_to_nist_sp_800_53r5.sssom.tsv` | 181 |
| `finos_to_eu_ai_act.sssom.tsv` | 67 |
| `finos_to_ffiec_it.sssom.tsv` | 56 |
| `finos_to_iso42001.sssom.tsv` | 49 |
| `finos_to_owasp_llm.sssom.tsv` | 22 |
| `finos_to_nist_ai_600_1.sssom.tsv` | 17 |
| `finos_to_sr_11_7.sssom.tsv` | 11 |
| `finos_to_owasp_ml.sssom.tsv` | 8 |
| `finos_to_dpv_ai.sssom.tsv` | hand-curated bridge |
| `finos_to_ibm_risk_atlas.sssom.tsv` | hand-curated bridge (chain hub) |

Predicate `skos:relatedMatch`; justification `semapv:ManualMappingCuration`. The two hand-curated bridges feed transitive coverage through the [vendored IBM mapping sets](../../linkml/upstream-releases/ai-atlas-nexus/src/ai_atlas_nexus/data/mappings/).

### Gates

| Gate | Status |
|---|---|
| `python linkml/scripts/build_finos_data.py` | ✅ exit 0 |
| `python linkml/scripts/build_sssom_mappings.py` | ✅ exit 0 (411 rows / 8 TSVs) |
| `python -m pytest linkml/tests/` | ✅ 13/13 |
| `just gen-project` | ✅ exit 0 (with workarounds — see below) |
| `linkml-lint` (umbrella) | ⚠️ upstream-only warnings — no FINOS-authored errors |

---

## FINOS -> `ai-risk-ontology` field mapping

The exporter in [linkml/scripts/build_finos_data.py](../scripts/build_finos_data.py) applies this mapping deterministically. Polymorphic entries (Risk / AiSystem / Term) co-exist under `Container.entries` distinguished by `type:` (the `Entry.type` attribute is declared `designates_type: true` upstream).

| FINOS Jekyll front-matter | `ai-risk-ontology` slot | Source |
|---|---|---|
| filename id (`ri-N` / `mi-N` / `uc-N`) | `id` (translated to `AIR-<TYPE>-<NNN>` / `UC-<NNN>`) | filename |
| `title` | `name` | front-matter |
| first body paragraph | `description` | body |
| Risk `type:` ∈ {RC, SEC, OP, GOV} | `Risk.isPartOf` -> `RiskGroup` id | `_risks/*.md` |
| Mitigation `type:` ∈ {PREV, DET, RESP} | `Action.isCategorizedAs[0]` -> `RiskControlGroup` id | `_mitigations/*.md` |
| `mitigates:` (on `mi-*`) | `Action.hasRelatedRisk` | `_mitigations/*.md` |
| `related_risks:` (on `uc-*`) | `AiSystem.hasRelatedRisk` | `_usecases/*.md` |
| `<key>_references:` (8 frameworks) | one `Documentation` per cited section, parented under the framework `Documentation` via `isCategorizedAs:` | `docs/_data/<key>.yml` |
| `data_classifications[*].name` | one `Term` row (`type: Term`, `isDefinedByTaxonomy: finos-ai-governance-framework-v2`, `isCategorizedAs: [<sensitivity-tier>]`); `description` folds source `description` + `storage_location` + `regulations` + `examples` | `docs/_data/data_classification.yml` |
| `data_classifications[*].references[*]` | one child `Documentation` with `isCategorizedAs: [<term-id>, <jurisdiction-id>]` | `docs/_data/data_classification.yml` |
| `data_classifications[*].references[*].jurisdiction` | one `Term` per distinct jurisdiction under the `finos-jurisdictions` vocabulary | `docs/_data/data_classification.yml` |
| `data_classifications[*].sensitivity` | one `Term` per tier under the `finos-data-sensitivity-tiers` vocabulary | `docs/_data/data_classification.yml` |
| `data_handling_aspects[*]` | `AiSystem.isCategorizedAs` -> deployment-model `Term` ids under the `data_handling` axis | `docs/_data/ai_deployment_model.yml` |
| `category:` (on `uc-*`) | `AiSystem.isCategorizedAs` -> `finos-ai-use-cases-v1` taxonomy anchor | front-matter |
| `end_user:` (on `uc-*`) | one `Stakeholder` per comma-separated role; `AiSystem.hasStakeholder` | front-matter |
| `regulatory_concerns[*]` | one `Documentation` per concern; `name` / `url` / jurisdiction folded into `description` | front-matter |
| `further_reading[*]` | one `Documentation` per link (`name` / `url` / `author`) | front-matter |
| `docs/_data/ai_use_cases.yml` (Level-3 leaves) | one `AiTask` row per leaf in `Container.aitasks` under `finos-ai-use-cases-v1` | data file |
| `docs/_data/ai_use_cases.yml` (`cross_cutting_capabilities` list) | 1 `CapabilityTaxonomy` (`finos-ai-capabilities-v1`) + 1 `CapabilityGroup` (`finos-cross-cutting-capabilities`) + 5 `Capability` in `Container.entries` | data file |
| `docs/_data/ai_deployment_model.yml` | 1 `RiskTaxonomy` + 7 `RiskGroup` (one per axis) + 31 `Term` (one per leaf, axis-prefixed ids) | data file |
| `docs/_data/nist-sp-800-53r5.yml` | standalone Container: 1 `RiskControlGroupTaxonomy` + 2 `Documentation` + 321 `RiskControl` | data file |
| `docs/_data/eu-ai-act.yml` | standalone Container: 1 `RiskTaxonomy` + 1 `Documentation` + 306 `Risk` | data file |
| `docs/_data/ffiec-itbooklets.yml` | standalone Container: 1 `Taxonomy` + 110 `Documentation` (1 landing + 11 booklet roots + 98 sections) + 11 `Group` (one per booklet) | data file |
| `docs/_data/iso-42001.yml` | standalone Container: 1 `RiskControlGroupTaxonomy` + 1 `Documentation` + 27 `RiskControl` (per-entry URL dropped — see [Standalone external-standard dumps](#standalone-external-standard-dumps)) | data file |
| `docs/_data/nist-ai-600-1.yml` | standalone Container: 1 `RiskTaxonomy` + 1 `Documentation` (canonical DOI) + 12 `Risk` (per-entry PDF anchors dropped) | data file |
| `docs/_data/owasp-llm.yml` | standalone Container: 1 `RiskTaxonomy` + 1 `Documentation` + 10 `Risk` | data file |
| `docs/_data/owasp-ml.yml` | standalone Container: 1 `RiskTaxonomy` + 1 `Documentation` + 10 `Risk` | data file |
| `docs/_data/sr11-7.yml` | standalone Container: 1 `RiskTaxonomy` + 2 `Documentation` (htm + pdf) + 15 `Risk` | data file |

### Front-matter coverage detail (48 catalogue posts)

| Front-matter key | Posts using | Mapped to | Status |
|---|---:|---|---|
| `layout`, `sequence`, `title`, `description` | 48 | `name`, body or `description` | ✅ |
| `type` (risk + mitigation) | 46 | `Risk.isPartOf` / `Action.isCategorizedAs` | ✅ |
| `mitigates` | 23 | `Action.hasRelatedRisk` | ✅ |
| `related_risks` / `related_mitigations` | 25 / 25 | `AiSystem.hasRelatedRisk` (`related_mitigations` is derivable from `Action.hasRelatedRisk`) | ✅ |
| `<key>_references` (×8 frameworks) | 23–24 each | one `Documentation` per cited section | ✅ |
| `data_classifications` | 2 | `Term` (`Container.entries`) + reference children | ✅ |
| `data_handling_aspects` | 2 | deployment-model `Term` ids in `isCategorizedAs` | ✅ |
| `regulatory_concerns` | 2 | `Documentation` rows | ⚠️ jurisdiction is opaque label (G29) |
| `further_reading` | 2 | `Documentation` rows | ✅ |
| `end_user` | 2 | `Stakeholder` rows | ✅ |
| `category` | 2 | `AiSystem.isCategorizedAs` (taxonomy anchor only) | ⚠️ partial (G28) |
| `business_value` | 2 | — | ❌ blocked on G28 |
| `doc-status` | 48 | — | ❌ blocked on G27 |
| `external_risks` (mitigation template) | 0 | — | N/A — template slot, not currently used |

---

## Source data inventory — `docs/_data/`

The FINOS Jekyll site ships eleven authoritative YAML files under [docs/_data/](../../docs/_data/). They split into three groups by how (and whether) the LinkML pipeline currently consumes them.

### Group A — FINOS-authored data (emitted as native AIRO instances)

Processed by [build_finos_data.py](../scripts/build_finos_data.py); every row lands in the canonical dump.

| File | Lines | Status | Emitted as | Notes |
|---|---:|---|---|---|
| [data_classification.yml](../../docs/_data/data_classification.yml) | 295 | ✅ Complete | 11 `Term` (one per classification) + per-reference `Documentation` children + 4 `Term` (sensitivity tiers) + 4 `Term` (jurisdictions) + 2 `Vocabulary` (`finos-data-sensitivity-tiers`, `finos-jurisdictions`) | Backfilled lossless via `emit_all_data_classifications()` — every row is in the dump even if no use case currently cites it. `references[*].jurisdiction` and `sensitivity` are wired through `isCategorizedAs`. |
| [ai_deployment_model.yml](../../docs/_data/ai_deployment_model.yml) | 112 | ✅ Complete | 1 `RiskTaxonomy` (`finos-ai-deployment-model`) + 7 `RiskGroup` (one per axis) + 31 `Term` (one per leaf) | All seven axes (`ai_type`, `architecture_pattern`, `deployment_type`, `data_handling`, `regulatory_alignment`, `operational_model`, `integration_pattern`) and every leaf descriptor are emitted. Use-case `data_handling_aspects:` resolve to leaves of the `data_handling` axis. |
| [ai_use_cases.yml](../../docs/_data/ai_use_cases.yml) | 71 | ⚠️ Partial | 1 `RiskTaxonomy` (`finos-ai-use-cases-v1`) + 43 `AiTask` (Level-3 leaves) + 1 `CapabilityTaxonomy` (`finos-ai-capabilities-v1`) + 1 `CapabilityGroup` + 5 `Capability` (cross-cutting capabilities) | Level-1 sector domains and Level-2 subcategories are not yet emitted as native data; their hierarchy is preserved only as a breadcrumb in each `AiTask.description`. Blocked on upstream Nexus [G30](../../ISSUE-nexus.md#g30) (`AiTaskGroup` / `AiTaskDomain` classes). Cross-cutting capabilities are fully emitted. |
| [nist-sp-800-53r5.yml](../../docs/_data/nist-sp-800-53r5.yml) | 966 | ✅ Complete (separate output) | 1 `RiskControlGroupTaxonomy` + 2 `Documentation` + 321 `RiskControl` in [nist_sp_800_53_r5.yaml](../tests/data/finos/nist_sp_800_53_r5.yaml) | Emitted as a standalone Container file rather than merged into the FINOS catalogue, because it represents an *external* standard's content. Per-row URLs computed via the CPRT catalogue template; titles normalised from PDF-bookmark casing. |

### Group B — External-framework reference data (cross-walks + standalone native dumps)

Consumed by [build_sssom_mappings.py](../scripts/build_sssom_mappings.py) to look up the `name` / `url` of cited sections when assembling SSSOM rows, and **also** emitted as standalone Container dumps by [build_finos_data.py](../scripts/build_finos_data.py) under [linkml/tests/data/finos/](../tests/data/finos/) — one file per external standard, deliberately kept separate from the FINOS catalogue (these files represent external standards' content, not FINOS-authored data). Per-file dump shape is documented in [Standalone external-standard dumps](#standalone-external-standard-dumps) above.

| File | Lines | SSSOM rows | Standalone dump | Notes |
|---|---:|---:|---|---|
| [eu-ai-act.yml](../../docs/_data/eu-ai-act.yml) | 951 | 67 | [eu_ai_act.yaml](../tests/data/finos/eu_ai_act.yaml) (306 `Risk`) | Generated from `artificialintelligenceact.eu`; SSSOM covers articles cited by FINOS posts; standalone dump covers every article in the source file. |
| [ffiec-itbooklets.yml](../../docs/_data/ffiec-itbooklets.yml) | 442 | 56 | [ffiec_it_handbook.yaml](../tests/data/finos/ffiec_it_handbook.yaml) (11 `Group` + 110 `Documentation`) | `booklet_abbrev` rows become `Group`s; section rows become `Documentation` children via `isCategorizedAs`. |
| [iso-42001.yml](../../docs/_data/iso-42001.yml) | 82 | 49 | [iso_42001.yaml](../tests/data/finos/iso_42001.yaml) (27 `RiskControl`) | Per-entry URL dropped (all rows share the same standard page); consumers follow `hasDocumentation`. |
| [nist-ai-600-1.yml](../../docs/_data/nist-ai-600-1.yml) | 39 | 17 | [nist_ai_600_1.yaml](../tests/data/finos/nist_ai_600_1.yaml) (12 `Risk`) | Per-entry PDF anchor URLs dropped in favour of the canonical DOI redirect (`https://doi.org/10.6028/NIST.AI.600-1`). See [ISSUE-nexus.md G31](../../ISSUE-nexus.md#g31-nist-harmful-bias-or-homogenization-namesid-uses-or-should-be-and). |
| [owasp-llm.yml](../../docs/_data/owasp-llm.yml) | 30 | 22 | [owasp_llm_top_10.yaml](../tests/data/finos/owasp_llm_top_10.yaml) (10 `Risk`) | OWASP Top-10 for LLM Applications 2025. |
| [owasp-ml.yml](../../docs/_data/owasp-ml.yml) | 30 | 8 | [owasp_ml_top_10.yaml](../tests/data/finos/owasp_ml_top_10.yaml) (10 `Risk`) | OWASP Machine Learning Top-10 2023. |
| [sr11-7.yml](../../docs/_data/sr11-7.yml) | 66 | 11 | [sr_11_7.yaml](../tests/data/finos/sr_11_7.yaml) (15 `Risk`) | Federal Reserve / OCC Supervisory Letter SR 11-7; 2 `Documentation` rows (htm landing + pdf attachment), each entry routed to the matching one. |

### Open work on `docs/_data/`

1. **`ai_use_cases.yml` hierarchy (G30)** — emit Level-1 domains as `AiTaskDomain` and Level-2 subcategories as `AiTaskGroup` once upstream Nexus lands those classes. Pending [Nexus G30](../../ISSUE-nexus.md#g30).
2. ✅ **Group-B files as native dumps (landed)** — the NIST SP 800-53r5 pattern is now replicated for all seven Group-B sources. Eight standalone `Container` files (one per external standard) are emitted under [linkml/tests/data/finos/](../tests/data/finos/) by [build_finos_data.py](../scripts/build_finos_data.py); shape per file is documented in [Standalone external-standard dumps](#standalone-external-standard-dumps). These are candidates for upstream contribution into `IBM/ai-atlas-nexus`'s `knowledge_graph/` reference-data directory.
3. **Build-time provenance on emitted entries** — descriptions currently drop the source-file breadcrumb (`docs/_data/<file>`) because upstream `Entity` has no `notes:` / provenance slot. See [ISSUE-nexus.md Note A](../../ISSUE-nexus.md#note-a--no-notes--provenance-slot-on-entity) for the proposed upstream addition.

---

## Compliance against the FINOS source corpus

| Surface | Captured | Status |
|---|---|---|
| Front-matter keys (21 distinct) | 18 / 21 = **86%** | 3 blocked on upstream G27 / G28 / G29 |
| `docs/_data/<framework>.yml` (×7 external) | cited sections via SSSOM **and** every row emitted as a standalone Container dump | ✅ both surfaces complete (see [Standalone external-standard dumps](#standalone-external-standard-dumps)) |
| `docs/_data/data_classification.yml` | full (Term + references + sensitivity + jurisdiction) | ✅ 100% |
| `docs/_data/ai_use_cases.yml` | Level-3 leaves + cross-cutting capabilities | ⚠️ Level-1 / Level-2 grouping deferred on G30 |
| `docs/_data/ai_deployment_model.yml` | full (1 RiskTaxonomy + 7 RiskGroup + 31 Term) | ✅ 100% |
| `docs/_data/nist-sp-800-53r5.yml` | full (1 RiskControlGroupTaxonomy + 321 RiskControl, separate file) | ✅ 100% |

The 3 unmapped front-matter keys (`doc-status`, `business_value`, regulatory `jurisdiction`) all require upstream schema extensions; **no FINOS-local schema additions are needed to close them.** See [Gaps and upstream dependencies](#gaps-and-upstream-dependencies) below for the gap-by-gap blocker map.

---

## Gaps and upstream dependencies

All gaps are tracked authoritatively in:

- [ISSUE-nexus.md](../../ISSUE-nexus.md) — gaps in `ai-atlas-nexus` (`ai-risk-ontology`), G6–G30
- [ISSUE-linkml.md](../../ISSUE-linkml.md) — LinkML runtime / generator bugs, LMB-1 / LMB-2 / LMB-3

Summary by status:

| Status | Count | Gap IDs |
|---|---:|---|
| ✅ Closed (no longer a gap) | 8 | G1–G5, G7, G8 (covered by `lmodel/dpv` / DPV 2.3) |
| ✅ Local fix applied | 8 | G11, G13, G14, G15, G16, G18, G19, LMB-1 |
| 📋 Filed upstream | 3 | G6 ([Nexus #179](https://github.com/IBM/ai-atlas-nexus/issues/179)) · G9 ([#180](https://github.com/IBM/ai-atlas-nexus/issues/180)) · G10 ([#181](https://github.com/IBM/ai-atlas-nexus/issues/181)) |
| 📋 Ready to file (proposed body in ISSUE-nexus.md) | 4 | G27, G28, G29, G30 |
| 📋 Ready to file (LinkML) | 2 | LMB-1, LMB-2 (G12 / G25 / etc. are sub-cases) |
| ⏳ Active blocker on data compliance | 4 | G27 (`doc-status`) · G28 (`business_value`, `category` typing) · G29 (jurisdiction) · G30 (use-case taxonomy hierarchy) |

### Active blockers — workaround detail

| ID | Front-matter blocked | Upstream ask | Workaround |
|---|---|---|---|
| **G27** | `doc-status:` (mandatory on all 48 posts) | `lifecycle_status` slot on `Entity` | currently dropped; can emit as opaque label via `isCategorizedAs: [doc-status-<value>]` (range `Any` accepts it) |
| **G28** | `business_value:` (2 posts); `category:` typed as `Domain` (2 posts) | `Container.purposes:` and `Container.domains:` collection slots | `business_value` dropped; `category` reduced to taxonomy anchor only |
| **G29** | `regulatory_concerns[*].jurisdiction:` typed | `Jurisdiction` enum + `jurisdiction:` slot on `Concept` | jurisdiction wired through `isCategorizedAs` to a `Term` under the `finos-jurisdictions` vocabulary instead of being a typed scalar |
| **G30** | `ai_use_cases.yml` Level-1 / Level-2 grouping | `AiTaskDomain` and `AiTaskGroup` classes (mirror `RiskGroup`) | flat emission of Level-3 leaves only; hierarchy preserved in `AiTask.description` breadcrumb |
| **LMB-1** | none directly — affects `gen-project` modular merge | `SchemaLoader` nested-import resolution | `merge_modules: false` |
| **LMB-2** | none directly — affects SHACL output | `shaclgen` `KeyError` fix | `excludes: [shacl]` |

**No FINOS-authored schema additions are required to close any of these gaps.** They are pure upstream surface-area extensions.

### Next steps

1. File the four ready-to-file Nexus issues (G27, G28, G29, G30) — proposed issue bodies are in [ISSUE-nexus.md](../../ISSUE-nexus.md).
2. File the two LinkML generator bugs (LMB-1, LMB-2) — repros in [ISSUE-linkml.md](../../ISSUE-linkml.md).
3. Backfill open `docs/_data/` work items listed in [Open work on `docs/_data/`](#open-work-on-docs_data) above.
4. Track an upstream `notes:` / provenance slot on `Entity` so the build script can re-attach source-file breadcrumbs to generated descriptions — see [ISSUE-nexus.md Note A](../../ISSUE-nexus.md#note-a--no-notes--provenance-slot-on-entity).

---

## Validation surface

The umbrella schema enforces:

- **Reference integrity** — `Risk.isPartOf` / `Term.isPartOf` resolve to existing `RiskGroup` ids; `AiSystem.hasStakeholder` to a `Stakeholder`; etc.
- **Required identifiers** — every entity row carries an `id`.
- **Cardinality** — multivalued slots (`hasRelatedRisk`, `hasDocumentation`, `mitigates`, `isCategorizedAs`) reject scalars.
- **Type discriminator** — `Container.entries` rows must carry `type: Risk | AiSystem | Term | Capability` (`designates_type: true` on `Entry.type`).
- **Container shape** — only the slots declared on `Container` may appear at top level.

Build-time guards in [linkml/scripts/build_finos_data.py](../../linkml/scripts/build_finos_data.py) additionally enforce `VALID_RISK_TYPES = {RC, SEC, OP, GOV}` and `VALID_ACTION_KINDS = {PREV, DET, RESP}` on Jekyll front-matter before the data file is written.

---

## `gen-project` workarounds

Active flags (set in [linkml/gen-project.yaml](../gen-project.yaml) and [linkml/config.yaml](../config.yaml)):

| Flag | Reason | Tracking |
|---|---|---|
| `gen_project.merge_modules: false` | `SchemaLoader` loses directory context resolving nested relative imports during merge | [ISSUE-linkml.md LMB-1](../../ISSUE-linkml.md#lmb-1) |
| `excludes: [shacl, markdown]` | `shaclgen` raises `KeyError` on imported module names when `mergeimports=True` | [ISSUE-linkml.md LMB-2](../../ISSUE-linkml.md#lmb-2) |

`gen-project` produces: Python dataclasses, Pydantic models, GraphQL schema, JSON Schema, JSON-LD context, OWL/Turtle, TypeScript, Java, Protobuf. SHACL is excluded pending LMB-2.

---

## Reproduction

```bash
# install (one-time)
cd linkml && python -m venv .venv && source .venv/bin/activate && pip install -e .

# regenerate everything
python linkml/scripts/build_finos_data.py
python linkml/scripts/build_sssom_mappings.py
python -m pytest linkml/tests/ -q
just gen-project
```

All four commands are idempotent.

---

## Further reading

- [ISSUE-nexus.md](../../ISSUE-nexus.md) — upstream gap registry (G1–G31, plus informational notes)
- [ISSUE-linkml.md](../../ISSUE-linkml.md) — LinkML runtime / generator bugs (LMB-1 / LMB-2 / LMB-3)
- [linkml/src/ai_governance_framework/mappings/README.md](../src/ai_governance_framework/mappings/README.md) — SSSOM cross-walk inventory and conventions
