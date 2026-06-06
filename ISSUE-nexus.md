# Upstream gaps — `ai-atlas-nexus` (`ai-risk-ontology`)

> Authoritative registry of gaps surfaced while building [FINOS AI Governance Framework](https://github.com/finos/ai-governance-framework) on top of `ai-atlas-nexus`. See [linkml/docs/about.md](linkml/docs/about.md) for the current FINOS adoption state and [ISSUE-linkml.md](ISSUE-linkml.md) for LinkML runtime / generator bugs.
>
> - **Repository**: https://github.com/IBM/ai-atlas-nexus
> - **Schema inspected**: vendored at [linkml/upstream-releases/ai-atlas-nexus/src/ai_atlas_nexus/ai_risk_ontology/schema/](linkml/upstream-releases/ai-atlas-nexus/src/ai_atlas_nexus/ai_risk_ontology/schema/) (release 0.5.0)

---

## Gap status (G1–G30)

| Gap | Type | Status | Effect on FINOS data compliance |
|---|---|---|---|
| **G1–G5, G7, G8** | Nexus | ✅ Closed | Covered by `lmodel/dpv` (W3C DPV 2.3) and existing Nexus modules (eu_ai_act etc.) |
| **G6** Framework taxonomy modules (OWASP / SR 11-7 / FFIEC) | Nexus | 📋 Filed [#179](https://github.com/IBM/ai-atlas-nexus/issues/179) | None — cited sections emit as `Documentation` rows |
| **G9** ISO 42001 / NIST AI 600-1 reference modules | Nexus | 📋 Filed [#180](https://github.com/IBM/ai-atlas-nexus/issues/180) | None — cross-walks live in SSSOM TSVs |
| **G10** No concrete `ExternalReference` subclass of `Entry` | Nexus | 📋 Filed [#181](https://github.com/IBM/ai-atlas-nexus/issues/181) (Option C: `aliases: [ExternalReference]` on `Documentation`) | None — using `Documentation` directly |
| **G11** Prefix mismatches (`skos`, `dpv`, `ai`) prevent merge | Nexus / FINOS | ✅ Local fix in vendored copy | None |
| **G12** Bare vs `./`-prefixed import paths | LinkML | 📋 To file | None — local fix in vendored copy |
| **G13** `gen-project` nested relative-import resolution | LinkML | ✅ Worked around (`merge_modules: false`) — see [ISSUE-linkml.md LMB-1](ISSUE-linkml.md#lmb-1) | None |
| **G14** Duplicate `implementsCapability` slot | FINOS | ✅ Local fix in vendored copy | None |
| **G15** Invalid `settings.strict: False` form | Nexus | 📋 To file | None — `linkml-lint` warning only |
| **G16** Bare-string `permissible_values` | Nexus | 📋 To file | None — `linkml-lint` warning only |
| **G17** Undeclared DPV ranges (`Notice`, `PersonalData`) | FINOS | ✅ Resolved by Plan C (FINOS schema deleted) | None |
| **G18** Non-canonical prefixes (`risk`, `loc`, `dct`) | Nexus / FINOS | ⚠️ Lint warning; intentional | None |
| **G19** `camelCase` slot naming | Nexus / LinkML | ⚠️ Intentional upstream | None |
| **G20** Inverse slot domain/range mismatches | Nexus | 📋 To file | None |
| **G21** Ambiguous OWL attribute URIs | Nexus | 📋 To file | None — `gen-owl` warning only |
| **G22** DPV `Incident` class URI lacks prefix | Nexus | 📋 To file | None |
| **G23** Ambiguous OWL type for `isAppliedWithinDomain` | FINOS | ✅ Resolved by Plan C | None |
| **G24** Enum value `X-LORA` invalid in GraphQL | Nexus | 📋 To file | None — workaround via excluded generator |
| **G25** `typescriptgen` lacks `datetime` / `uri` base mappings | LinkML | 📋 To file | None — workaround via excluded generator |
| **G26** Nexus `common.yaml` re-declares DPV classes (blocks `lmodel/dpv` import) | Nexus | 📋 To file | None — Plan C does not import `lmodel/dpv` |
| **G27** No `lifecycle_status` slot on `Entity` | Nexus | 📋 Ready to file | ⛔ Blocks `doc-status:` (mandatory on all 48 posts) |
| **G28** No `Container.purposes:` / `Container.domains:` collection slots | Nexus | 📋 Ready to file | ⛔ Blocks `business_value:` and typed `category:` (use cases) |
| **G29** No `Jurisdiction` enum / `jurisdiction:` slot on `Concept` | Nexus | 📋 Ready to file | ⛔ Blocks typed `regulatory_concerns[*].jurisdiction:` |
| **G30** No `AiTaskGroup` / `AiTaskDomain` classes | Nexus | 📋 Ready to file | ⚠️ Blocks Level-1 / Level-2 grouping of `ai_use_cases.yml` |
| **G31** `nist-harmful-bias-or-homogenization` uses "or" (should be "and") | Nexus | 📋 To file | ⚠️ Name/ID mismatch vs NIST AI 600-1 § 2.6 breaks cross-walk matching |
| **G32** Prefixes `tech`, `dqv` used in schema CURIEs but undeclared in any module `prefixes:` block | Nexus | 📋 To file | None — warning only |

**Active data-compliance blockers: 4** (G27, G28, G29, G30). Everything else is either closed, locally worked around, or filed upstream with no current FINOS impact.

---

## G11 Prefix mismatches (`skos`, `dpv`, `ai`) prevent merge

vi ./ai_risk_ontology/ai_eval.yaml

Comment out lines:
 397a398  in common .yaml
>     inverse: implementedByAdapter

 129a130,138 in ai_capability.yaml
>     inverse: implementsCapability
129a130,138
>     inverse: implementsCapability
> 
>   implementsCapability:
>     description: Indicates that this intrinsic implements a specific capability
>     domain: LLMIntrinsic
>     range: Capability
>     multivalued: true
>     inlined: false
>     inverse: implementedByIntrinsic

ValueError: Conflicting URIs (https://ibm.github.io/ai-atlas-nexus/ontology/ai_capability, https://ibm.github.io/ai-atlas-nexus/ontology/common) for item: implementsCapability

No namespace defined for URI: https://w3id.org/dpv/risk#Incident
vi ai_risk.yaml
add line 14
  risk: https://w3id.org/dpv/risk#

## G6 — No taxonomy modules for OWASP LLM / OWASP ML / SR 11-7 / FFIEC IT

**Filed**: [Nexus #179](https://github.com/IBM/ai-atlas-nexus/issues/179) · **Status**: 🟡 Awaiting upstream · **FINOS impact**: none

### Observation

Nexus ships [`schema/eu_ai_act.yaml`](linkml/upstream-releases/ai-atlas-nexus/src/ai_atlas_nexus/ai_risk_ontology/schema/eu_ai_act.yaml) (one regulatory framework). There is no equivalent module for OWASP Top-10 for LLM Applications, OWASP ML Top-10, Federal Reserve SR 11-7, or FFIEC IT Examination Handbook — all four cited from FINOS catalogue posts via `<key>_references:` arrays.

### FINOS resolution

Each cited section emits as one `Documentation` row in `Container.documents:` with a per-framework parent linked via `isCategorizedAs:`. No local schema needed. See [linkml/scripts/build_finos_data.py](linkml/scripts/build_finos_data.py) `_FRAMEWORK_REGISTRY`.

### Suggested upstream change

Ship one mini-module per framework mirroring `eu_ai_act.yaml`. Optional — FINOS is no longer blocked.

---

## G9 — No reference modules for ISO 42001 or NIST AI 600-1

**Filed**: [Nexus #180](https://github.com/IBM/ai-atlas-nexus/issues/180) · **Status**: 🟡 Awaiting upstream · **FINOS impact**: none

### Observation

Same shape as G6 — Nexus has no `iso_42001.yaml` / `nist_ai_600_1.yaml` modules. Both are heavily cited by FINOS catalogue posts.

### FINOS resolution

Cross-walks live in SSSOM TSVs ([`finos_to_iso42001.sssom.tsv`](linkml/src/ai_governance_framework/mappings/finos_to_iso42001.sssom.tsv) — 49 rows; [`finos_to_nist_ai_600_1.sssom.tsv`](linkml/src/ai_governance_framework/mappings/finos_to_nist_ai_600_1.sssom.tsv) — 17 rows). Plan C principle: **cross-walks live in SSSOM, not in schema.**

### Revised upstream ask

Two options preferred over the original "ship full reference modules":

**Option 1 (preferred) — ship `*.sssom.tsv` mapping sets** alongside the schema modules. SSSOM is the W3C-recommended exchange format for cross-vocabulary mappings.

**Option 2 — register CURIE-prefix aliases** (`iso42001:`, `nist_ai_600_1:`) in `ai-risk-ontology.yaml` `prefixes:` resolving to `https://w3id.org/lmodel/iso42001/` and `https://w3id.org/lmodel/nist-ai-600-1/`. Zero new classes / slots / enums.

**Option 3 (original) — ship full reference-module schemas.** Lowest-value option for what most downstream consumers actually need (the data, not the classes).

---

## G10 — `Entry` is abstract but lacks a concrete `ExternalReference` subclass

**Filed**: [Nexus #181](https://github.com/IBM/ai-atlas-nexus/issues/181) · **Status**: 🟡 Awaiting upstream (Option C preferred) · **FINOS impact**: none

### Observation

[`common.yaml`](linkml/upstream-releases/ai-atlas-nexus/src/ai_atlas_nexus/ai_risk_ontology/schema/common.yaml) declares `Entry` abstract; the only concrete subclasses are `Term` (terminology) and `Principle` (ethical principles). There is no concrete subclass for the "thin pointer to one section of one external standard" pattern.

### FINOS resolution

Plan C uses upstream `Documentation` directly (it already carries `name`, `url`, `author`, `description`). 197 cited framework sections + 4 regulatory concerns + 2 further-reading entries are emitted as plain `Documentation` rows.

### Suggested upstream change — Option C (preferred)

Add `aliases: [ExternalReference]` to the existing `Documentation` class. Two-line additive change:

```yaml
# common.yaml
Documentation:
  aliases:
    - ExternalReference          # ← single-line addition
  is_a: Entity
  class_uri: airo:Documentation
  ...
```

Rejected alternatives: (B) introduce a parallel `ExternalReference(is_a: Entry)` — duplicates `airo:Documentation`; (A) status quo — forces every consumer to choose between hand-rolling or using `Documentation` informally.

---

## G11 — Namespace prefix inconsistencies prevent schema merging

**Status**: ✅ Local fix in vendored copy · **FINOS impact**: none

### Observation

Nexus modules defined `skos`, `dpv` with conflicting URIs (some with trailing `#`, some without; some pointing at `w3id.org/dpv#`, others at `w3id.org/lmodel/dpv/`). `gen-project` merge fails with `ValueError: Prefix: skos mismatch`.

### Local fix

Three modules patched in the vendored copy:
- `ai_eval.yaml`: `skos: http://www.w3.org/2004/02/skos/core/` -> `skos: http://www.w3.org/2004/02/skos/core#`
- `ai_intrinsic.yaml`: `dpv: https://w3id.org/dpv#` -> `dpv: https://w3id.org/lmodel/dpv/`
- `ai_aiuc.yaml`: same as above

### Suggested upstream change

Audit all modules in `schema/` and align to canonical W3C URIs (`skos: …skos/core#`, `dpv: https://w3id.org/lmodel/dpv/`).

---

## G12 — Import paths inconsistent: bare vs relative

**Status**: 📋 To file (LinkML) · **FINOS impact**: none

### Observation

Modules within `ai-risk-ontology/` mix bare imports (`ai_system`) and relative imports (`./ai_system`). Bare imports fail in nested resolution scenarios.

### Suggested upstream change (LinkML)

Mandate `./` prefix for same-directory imports. Adopting this convention in Nexus would model best practice.

---

## G13 — `gen-project` fails resolving nested relative imports

**Status**: ✅ Worked around · **FINOS impact**: none

### Observation

`SchemaLoader` resolves nested `./`-prefixed imports against the root schema directory, not the importing module's directory. Triggers `FileNotFoundError` during merge.

### Local workaround

[`linkml/gen-project.yaml`](linkml/gen-project.yaml) sets `gen_project.merge_modules: false`. `just gen-project` exits 0; some monolithic generator outputs (GraphQL merged schema) are consequently incomplete.

### Tracked at

[ISSUE-linkml.md LMB-1](ISSUE-linkml.md#lmb-1) — full repro and proposed fix.

---

## G14 — Duplicate `implementsCapability` slot definitions

**Status**: ✅ Local fix in vendored copy · **FINOS impact**: none

### Observation

`common.yaml` and `ai_capability.yaml` both define `implementsCapability` with conflicting `inverse:` targets. LinkML rejects with a duplicate-definition error.

### Local fix

Removed the conflicting `inverse: implementsCapability` from `implementedByIntrinsic` in `ai_capability.yaml`; canonical slot kept in `common.yaml`.

### Long-term ideal

Granular imports / namespace aliasing — tracked at [LinkML discussion #1739](https://github.com/orgs/linkml/discussions/1739) and as [ISSUE-linkml.md LMB-3](ISSUE-linkml.md#lmb-3).

---

## G15 — Invalid `settings.strict: False` form

**Status**: 📋 To file (Nexus) · **FINOS impact**: none

`ai-risk-ontology.yaml` declares `settings.strict: False` — rejected by the LinkML metamodel (expects string or object form). `linkml-lint` warning only; no functional impact.

---

## G16 — Bare-string `permissible_values`

**Status**: 📋 To file (Nexus) · **FINOS impact**: none

Six+ Nexus enums use `KEY: "Label"` instead of the structured `KEY: { description: "Label" }` form. `linkml-lint valid-schema` warnings; no functional impact.

---

## G17 — Undeclared DPV ranges in FINOS classes

**Status**: ✅ Resolved by Plan C · **FINOS impact**: none

FINOS `finos_catalogue.yaml` referenced `Notice` and `PersonalData` ranges before DPV imports were possible. Plan C deleted `finos_catalogue.yaml` entirely; the gap no longer exists.

---

## G18 — Non-canonical prefix mappings

**Status**: ⚠️ Lint warning; intentional · **FINOS impact**: none

`risk`, `loc`, `dct` resolve via `lmodel/*` rewrite rules rather than the canonical W3C URIs. Intentional in `lmodel/dpv` design. `dct` should arguably be renamed to `dcterms` upstream.

---

## G19 — `camelCase` slot naming convention

**Status**: ⚠️ Intentional upstream · **FINOS impact**: none

Nexus uses `camelCase` slots by design (RDF/OWL convention); LinkML's `standard_naming` rule expects `snake_case`. Lint warnings only. LinkML lacks a configurable `naming_convention` knob — see G19 sibling on the LinkML side.

---

## G20 — Inverse slot domain/range mismatches

**Status**: 📋 To file (Nexus) · **FINOS impact**: none

Five slot pairs declare asymmetric inverses whose `range` and the inverse's `domain` do not match. `gen-owl` produces inconsistent OWL output but no schema-load error. The five pairs surfaced by `just test` stderr:

| Slot | Declared on | Inverse slot | Inconsistency |
|---|---|---|---|
| `requiredByTask` | `AiTask` | `requiresCapability` | range/domain mismatch |
| `requiresCapability` | `Capability` | `requiredByTask` | range/domain mismatch |
| `implementedByAdapter` | `Adapter` | `implementsCapability` | range/domain mismatch |
| `implementsCapability` | `Capability` | `implementedByAdapter` | range/domain mismatch |
| `possessedByAi` | `BaseAi` | `hasCapability` | range/domain mismatch |

All five are defined in `ai_system.yaml`. The LinkML generator warning message: `Range of slot 'X' (ClassA) does not line with the domain of its inverse (Y)`.

---

## G21 — Ambiguous OWL attribute URIs

**Status**: 📋 To file (Nexus) · **FINOS impact**: none

Per-class attributes (`type`, `author`, `source_type`) defined in multiple modules with conflicting class URIs. `gen-owl` warning only.

---

## G22 — W3C DPV `Incident` class URI lacks a prefix mapping

**Status**: 📋 To file (Nexus / lmodel) · **FINOS impact**: none

The full URI `https://w3id.org/dpv/risk#Incident` is referenced in the Nexus schema as the `class_uri` of a DPV risk-related class but the prefix `dpv-risk:` (or equivalent short form for `https://w3id.org/dpv/risk#`) is not declared in any module's `prefixes:` block. The LinkML generator emits:

```
No namespace defined for URI: https://w3id.org/dpv/risk#Incident
```

This is distinct from G11 (`dpv:` conflicting URIs) — here the prefix for `https://w3id.org/dpv/risk#` (the DPV **risk** sub-namespace) is entirely absent, not just inconsistent.

### Suggested upstream change

Add to the relevant module's `prefixes:` block:

```yaml
prefixes:
  dpv-risk: https://w3id.org/dpv/risk#
```

And update the `class_uri` to use the CURIE form: `class_uri: dpv-risk:Incident`.

---

## G23 — Ambiguous OWL type for `isAppliedWithinDomain`

**Status**: ✅ Resolved by Plan C · **FINOS impact**: none

Caused by FINOS `slot_usage: { range: string }` overriding upstream `range: Domain`. Plan C deleted the FINOS override; the gap no longer exists.

---

## G24 — Enum value `X-LORA` invalid in GraphQL

**Status**: 📋 To file (Nexus) · **FINOS impact**: none

The `-` is illegal in GraphQL enum names. Affects `genget gen-graphql` output for one specific value. Workaround: rename in vendored copy or exclude `genget gen-graphql` for that module.

---

## G25 — `typescriptgen` lacks `datetime` / `uri` base mappings

**Status**: 📋 To file (LinkML) · **FINOS impact**: none

`linkml.generators.typescriptgen` does not map LinkML builtin bases (`datetime`, `uri`, etc.) to TypeScript primitives. Generator emits warnings for slots ranged on these types.

---

## G26 — Nexus `common.yaml` re-declares DPV classes locally

**Status**: 📋 To file (Nexus) · **FINOS impact**: none (Plan C does not import `lmodel/dpv`)

`common.yaml` re-declares 8 DPV classes (`PersonalData`, `Notice`, etc.). Any downstream that also imports `lmodel/dpv` hits `Conflicting URIs` `ValueError`. Plan C avoided this by *not* importing `lmodel/dpv` (the schema no longer depends on DPV; SSSOM TSVs replace cross-walk decoration).

---

## G27 — No `lifecycle_status` slot on `Entity` for editorial workflow

**Status**: 📋 Ready to file (Nexus) · **FINOS impact**: ⛔ blocks `doc-status:` on all 48 posts

### Observation

Every FINOS post under [docs/_risks/](docs/_risks/), [docs/_mitigations/](docs/_mitigations/), [docs/_usecases/](docs/_usecases/) carries a mandatory `doc-status:` front-matter key (one of `Approved-Specification`, `Draft`, `Review`, plus FINOS-specific tags). [`scripts/lint-check`](scripts/lint-check) enforces it.

Upstream carries no equivalent slot on `Entity`, `Entry`, or `Documentation`. The closest neighbour, `lifecycleState` on `AiSystem`, is scoped to runtime AI lifecycle (`development` / `testing` / `production`), not editorial state.

### Suggested upstream change

Add `lifecycle_status` slot on `Entity` (range new `LifecycleStatus` enum: `DRAFT`, `REVIEW`, `APPROVED`, `DEPRECATED`, `WITHDRAWN`).

### Local workaround

Currently dropped. Could emit as opaque label via `isCategorizedAs: [doc-status-<value>]` (range `Any` accepts it) without schema change — bounded to build-script.

### Proposed upstream issue body

> **Title**: Add `lifecycle_status` slot on `Entity` for editorial workflow
>
> **Body**: Catalogued entities need editorial-state annotation (draft / review / approved). Current schema has no slot for this; `lifecycleState` on `AiSystem` is scoped to runtime AI lifecycle, not editorial workflow.
>
> Downstream evidence: FINOS AI Governance Framework requires `doc-status:` on all 48 posts ([scripts/lint-check](https://github.com/finos/ai-governance-framework/blob/main/scripts/lint-check)).
>
> **Proposal**: add `lifecycle_status` to `Entity` (range new `LifecycleStatus` enum with `DRAFT`, `REVIEW`, `APPROVED`, `DEPRECATED`, `WITHDRAWN`).

---

## G28 — `Container` has no `purposes` / `domains` collection slots

**Status**: 📋 Ready to file (Nexus) · **FINOS impact**: ⛔ blocks `business_value:` and typed `category:` (use cases)

### Observation

`Container` declares collections for `stakeholders`, `concepts`, `taxonomies`, `aimodels`, `aisystems`, `risks`, `actions`, `entries`, etc. but no `purposes:` and no `domains:`. Meanwhile inverse-direction slots `hasPurpose` (range `Purpose`) and `isAppliedWithinDomain` (range `Domain`) already exist on `AiSystem` and `Risk`.

Result: `Purpose` and `Domain` instances cannot live in a native AIRO data file — there is nowhere to put them.

### Suggested upstream change

Two-line additive change to `ai-risk-ontology.yaml` mirroring `Container.stakeholders:`:

```yaml
classes:
  Container:
    attributes:
      purposes:
        range: Purpose
        multivalued: true
        inlined: true
        inlined_as_list: true
      domains:
        range: Domain
        multivalued: true
        inlined: true
        inlined_as_list: true
```

### Local workaround

`business_value:` currently dropped. `category:` reduced to a taxonomy anchor in `AiSystem.isCategorizedAs` rather than a typed `Domain` reference.

### Proposed upstream issue body

> **Title**: Add `Container.purposes:` and `Container.domains:` collection slots
>
> **Body**: `Container` already holds typed collections for `stakeholders`, `concepts`, `aisystems`, etc., but has no slot for the existing `Purpose` and `Domain` classes — even though `hasPurpose` (range `Purpose`) and `isAppliedWithinDomain` (range `Domain`) are first-class slots used by `AiSystem` and `Risk`. Without container slots, downstreams cannot populate the slots: the referenced ids have no home.
>
> Downstream evidence: FINOS drops use-case `business_value:` and `category:` for exactly this reason (see [linkml/docs/about.md](https://github.com/finos/ai-governance-framework/blob/main/linkml/docs/about.md#active-blockers--workaround-detail) §"Active blockers — workaround detail").
>
> **Proposal**: add `purposes:` and `domains:` collection slots on `Container`, mirroring `stakeholders:`. Two-line additive change.

---

## G29 — No `Jurisdiction` enum / `jurisdiction:` slot on `Concept`

**Status**: 📋 Ready to file (Nexus) · **FINOS impact**: ⛔ blocks typed `regulatory_concerns[*].jurisdiction:`

### Observation

FINOS `regulatory_concerns[*].jurisdiction:` carries `US` / `EU` / `UK` / `International`. The closest upstream neighbour, `isAppliedWithinDomain` (range `Domain`), is the *application sector* (Finance / Healthcare), not the *legal jurisdiction*. Orthogonal: GDPR has Domain=Generic and Jurisdiction=EU; GLBA has Domain=Finance and Jurisdiction=US.

### Suggested upstream change

Add a `Jurisdiction` enum (ISO 3166-1 alpha-2 plus `EU`, `INTL`, `GLOBAL`) and a `jurisdiction:` slot on `Concept` (range `Jurisdiction`, multivalued).

### Local workaround

Currently emitted as opaque `Documentation` rows (`jurisdiction-us`, `-eu`, `-uk`, `-international`) referenced via `isCategorizedAs:` on the regulatory-concern Documentation. Loses enum validation but preserves the data round-trip.

### Proposed upstream issue body

> **Title**: Add `Jurisdiction` enum + `jurisdiction:` slot on `Concept` for regulatory cross-walk
>
> **Body**: AIRO has no first-class way to express the legal jurisdiction of a regulatory `Concept`. The closest existing slot, `isAppliedWithinDomain`, is the *application sector*, not the *legal jurisdiction* — orthogonal axes.
>
> Downstream evidence: FINOS tags every `regulatory_concerns[*]` entry with `jurisdiction: {US, EU, International, …}` (rendered as a badge by [docs/_layouts/usecase.html](https://github.com/finos/ai-governance-framework/blob/main/docs/_layouts/usecase.html)).
>
> **Proposal**: add `Jurisdiction` enum (ISO 3166-1 alpha-2 + `EU`, `INTL`, `GLOBAL`) and `jurisdiction:` slot on `Concept` (range `Jurisdiction`, multivalued).

---

## G30 — No `AiTaskGroup` / `AiTaskDomain` classes for use-case taxonomy hierarchy

**Status**: 📋 Ready to file (Nexus) · **FINOS impact**: ⚠️ blocks Level-1 / Level-2 grouping of `ai_use_cases.yml`

### Observation

`AiTask` (in `ai_system.yaml`) is concrete for leaf instances. There is no `AiTaskGroup` (subcategory) or `AiTaskDomain` (sector domain) — the structural counterpart of the existing `RiskGroup` / `RiskControlGroup` pair for the risk taxonomy.

FINOS [docs/_data/ai_use_cases.yml](docs/_data/ai_use_cases.yml) has a three-level hierarchy:

```
Level 1 (sector domain):   Risk_and_Compliance
  Level 2 (subcategory):   Fraud_Detection_and_Prevention
    Level 3 (leaf task):   Transaction_Anomaly_Detection   ← AiTask
```

### Suggested upstream change

Add to `ai_system.yaml` (or a new `ai_task_taxonomy.yaml` module):

```yaml
classes:
  AiTaskTaxonomy:
    is_a: Taxonomy

  AiTaskDomain:
    is_a: Group
    class_uri: nexus:AiTaskDomain
    slot_usage:
      hasPart: { range: AiTaskGroup }
    slots: [isDefinedByTaxonomy, hasPart]

  AiTaskGroup:
    is_a: Group
    class_uri: nexus:AiTaskGroup
    slot_usage:
      hasPart: { range: AiTask }
      isPartOf: { range: AiTaskDomain }
    slots: [isDefinedByTaxonomy, hasPart, isPartOf]
```

Plus `Container.aitaskdomains:` and `Container.aitaskgroups:` collection slots mirroring `Container.aitasks:`. Mirrors the existing `RiskGroup` / `RiskControlGroup` / `RiskTaxonomy` pattern.

### Local workaround (current)

Flat emission: only the 43 Level-3 leaves emit as `AiTask` instances under `Container.aitasks`. Hierarchy preserved as a breadcrumb in each task's `description`. `AiSystem` entries reference the taxonomy via `isCategorizedAs: [finos-ai-use-cases-v1]`.

### Proposed upstream issue body

> **Title**: Add `AiTaskGroup` and `AiTaskDomain` classes to support use-case taxonomy hierarchy
>
> **Body**: `AiTask` works for leaf task instances, but there is no structural counterpart to `RiskGroup` / `RiskControlGroup` for grouping tasks into subcategories and sector domains. Downstream catalogues with three-level hierarchies must omit grouping nodes or type them incorrectly.
>
> **Proposal**: add `AiTaskDomain` (is_a Group, hasPart->AiTaskGroup) and `AiTaskGroup` (is_a Group, hasPart->AiTask, isPartOf->AiTaskDomain) to `ai_system.yaml`, plus `Container.aitaskdomains:` and `Container.aitaskgroups:` collection slots. Mirrors existing `RiskGroup` / `RiskControlGroup` pattern. Downstream evidence: [FINOS docs/_data/ai_use_cases.yml](https://github.com/finos/ai-governance-framework/blob/main/docs/_data/ai_use_cases.yml).

---

## G31 — `nist-harmful-bias-or-homogenization` name/ID uses "or" (should be "and")

**Status**: 📋 To file (Nexus) · **FINOS impact**: ⚠️ cross-walk name matching

### Observation

In `nist_ai_rmf_data.yaml` the entry for NIST AI 600-1 § 2.6 is:

```yaml
id: nist-harmful-bias-or-homogenization
name: Harmful Bias or Homogenization
```

NIST AI 600-1 § 2.6 is titled **"Harmful Bias and Homogenization"** (conjunction "and"). The upstream knowledge graph uses "or" in both `id` and `name`.

### FINOS evidence

`docs/_data/nist-ai-600-1.yml` key `2-6`:

```yaml
2-6:
  title: 2.6. Harmful Bias and Homogenization
```

### Impact

Any cross-walk or mapping that matches by name or slug will silently resolve to the wrong upstream entry. FINOS SSSOM TSV `finos_to_nist_ai_600_1.sssom.tsv` uses the FINOS-side title; consumers joining on the upstream slug will miss the match.

### Suggested upstream change

Correct the upstream `nist_ai_rmf_data.yaml` entry:

```yaml
id: nist-harmful-bias-and-homogenization
name: Harmful Bias and Homogenization
```

---

## Notes (informational observations)

> Non-blocking observations about the upstream schema surfaced while building FINOS data. Distinct from the numbered gaps above — these do not warrant a filed ticket on their own but are recorded here for reference and to inform future upstream conversations.

### Note A — No `notes:` / provenance slot on `Entity`

**Status**: 📝 Observation only · **FINOS impact**: minor (lossy provenance)

#### Observation

`Entity` (in [linkml/upstream-releases/ai-atlas-nexus/src/ai_atlas_nexus/ai_risk_ontology/schema/common.yaml](linkml/upstream-releases/ai-atlas-nexus/src/ai_atlas_nexus/ai_risk_ontology/schema/common.yaml)) carries `id`, `name`, `description`, `url`, `dateCreated`, `dateModified`, the `*_mappings` family, and `isCategorizedAs`. It does **not** carry a `notes:` / `comments:` / `editorial_notes:` / `annotations:` data slot.

LinkML's `notes:` and `annotations:` are *metamodel* slots (they live on schema-element definitions, not data instances), so they cannot be used on emitted data without first being declared as ordinary slots on `Entity`.

#### FINOS evidence

The generator at [linkml/scripts/build_finos_data.py](linkml/scripts/build_finos_data.py) derives ~75 entries (Terms, Stakeholders, RiskGroups, etc.) from FINOS Jekyll YAML / front-matter. Each entry has a natural provenance breadcrumb — e.g. `docs/_data/data_classification.yml` for sensitivity tiers, `docs/_data/ai_deployment_model.yml` for deployment axes. With no `notes:` slot available, these can only be:

1. Embedded inside `description:` (rejected — descriptions should be domain content, not implementation/repo paths).
2. Stored on the single-valued `url:` slot (rejected — `url:` is the canonical resource URI, not a list of contributing source files).
3. Dropped entirely (current state — lossy).

#### Suggested upstream change

Add an optional, multivalued, free-text slot on `Entity` (or a new `Annotatable` mixin) for build-time provenance and editorial notes:

```yaml
# common.yaml
slots:
  notes:
    slot_uri: skos:note
    multivalued: true
    recommended: false
    description: >-
      Free-text editorial notes, source breadcrumbs, or build-time provenance
      that do not belong in the user-facing description. Opaque to consumers.

classes:
  Entity:
    slots:
      # ... existing slots ...
      - notes
```

`skos:note` is the SKOS-canonical predicate for this purpose and is already used downstream by SKOS-aware consumers. Alternative: separate `skos:editorialNote` / `skos:scopeNote` if finer-grained provenance categories are wanted.

#### Local workaround

None — provenance currently dropped. If/when upstream lands a `notes:` slot, [linkml/scripts/build_finos_data.py](linkml/scripts/build_finos_data.py) can re-attach the stripped source paths (e.g. `notes: ["docs/_data/data_classification.yml"]`) on each generated `Term` / `RiskGroup` / `Stakeholder`.

---

## G32 — Prefixes `tech` and `dqv` used in schema CURIEs but never declared

**Status**: 📋 To file (Nexus) · **FINOS impact**: none (warnings only)

### Observation G32

When any LinkML generator loads the merged schema, it emits:

```
File "ai_governance_framework.yaml", line 743, col 15: Unrecognized prefix: tech
File "ai_governance_framework.yaml", line 878, col 15: Unrecognized prefix: dpv
File "ai_governance_framework.yaml", line 1662, col 15: Unrecognized prefix: dqv
File "ai_governance_framework.yaml", line 5180, col 16: Unrecognized prefix: ai
```

- `tech:` — Dublin Core Terms Technology (or similar) used in CURIE references in the Nexus schema; no `tech:` entry in any module's `prefixes:` block.
- `dqv:` — W3C Data Quality Vocabulary (`https://www.w3.org/ns/dqv#`); referenced but undeclared.
- `dpv:` and `ai:` — partially addressed in G11 (local vendor fix), but post-merge the warnings resurface because the vendor patch affects the source modules, not the merged output.

Note: `xsd:` and `shex:` unrecognised prefix warnings come from the same merge-step prefix loss but are a LinkML generator issue (tracked as LMB-8 in [ISSUE-linkml.md](ISSUE-linkml.md)).

### Suggested upstream change

Add to the relevant modules' `prefixes:` blocks:

```yaml
prefixes:
  tech: https://w3id.org/linkml/tech/   # or whichever canonical URI
  dqv: https://www.w3.org/ns/dqv#
```

And audit all modules to ensure every CURIE prefix used in `class_uri`, `slot_uri`, or `*_mappings` is declared in that module's own `prefixes:` block (not relying on transitive prefix inheritance, which LinkML's merge step does not reliably propagate).

## References

- **Filed Nexus tickets**: [#179](https://github.com/IBM/ai-atlas-nexus/issues/179) · [#180](https://github.com/IBM/ai-atlas-nexus/issues/180) · [#181](https://github.com/IBM/ai-atlas-nexus/issues/181)
- **LinkML discussion**: [#1739](https://github.com/orgs/linkml/discussions/1739) (granular imports)
- **FINOS adoption state**: [linkml/docs/about.md](linkml/docs/about.md)
- **LinkML runtime / generator bugs**: [ISSUE-linkml.md](ISSUE-linkml.md)
- **Public design doc**: [linkml/docs/about.md](linkml/docs/about.md)
