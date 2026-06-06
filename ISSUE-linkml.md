# LinkML runtime / generator gaps surfaced by FINOS

> Bugs and feature gaps in [`linkml/linkml`](https://github.com/linkml/linkml) (and adjacent generators) hit while building [FINOS AI Governance Framework](https://github.com/finos/ai-governance-framework) on top of `ai-atlas-nexus`. Upstream-Nexus gaps live in [ISSUE-nexus.md](ISSUE-nexus.md); design rationale in [linkml/docs/about.md](linkml/docs/about.md).
>
> - **LinkML version inspected**: 1.6+ (`pip show linkml` in `linkml/.venv`)
> - **Generators inspected**: `genget`, `gen-project`, `gen-shacl`, `gen-typescript`, `gen-graphql`, `PythonGenerator` (in-process for `linkml-run-examples`)

---

## Status table

| ID | Title | Status | Workaround | Active blocker? |
|---|---|---|---|---|
| **LMB-1** | `SchemaLoader` loses directory context resolving nested relative imports during merge | 📋 Ready to file (candidate dup of [linkml/linkml#2054](https://github.com/linkml/linkml/issues/2054)) | `gen_project.merge_modules: false` in [linkml/gen-project.yaml](linkml/gen-project.yaml) | No — `just gen-project` exits 0 |
| **LMB-2** | `shaclgen` raises `KeyError` on imported module name when `mergeimports=True` | 📋 Ready to file | `excludes: [shacl]` in [linkml/config.yaml](linkml/config.yaml) | No — SHACL excluded |
| **LMB-3** | Granular / namespace-aware imports missing | 🔵 Tracked at [LinkML discussion #1739](https://github.com/orgs/linkml/discussions/1739) | Vendor + locally patch upstream modules | No — vendoring works |
| **LMB-4** | LinkML `data_utils` global-ID merging silently corrupts multi-class Containers | 📋 Ready to file (upstream-Nexus behavior) | Add `-doc` suffix to Documentation IDs that collide with non-Document entity IDs; defensive `_check_id_collisions()` at generation time | No — workaround landed in [build_finos_data.py](linkml/scripts/build_finos_data.py) |
| **LMB-5** | `gen-rust` `RustStructOrSubtypeEnum.type_designators` annotation mismatch (`dict[str, str]` vs `dict[str, list[str]]`) crashes on `designates_type` hierarchies | 📋 Ready to file | Monkey-patch wrapper [linkml/scripts/issues/gen_rust_patched.py](linkml/scripts/issues/gen_rust_patched.py); recipe in [linkml/project.justfile](linkml/project.justfile) `gen-rust-artifact` | No — `just gen-rust-artifact` produces a Cargo crate |
| **LMB-6** | `linkml-run-examples` (`ExampleRunner._load_from_dict`) crashes with `AttributeError: 'list' object has no attribute 'items'` on list-valued inline multivalued slots | 📋 Ready to file | Monkey-patch in [linkml/scripts/issues/run_examples_patched.py](linkml/scripts/issues/run_examples_patched.py); `_test-examples` recipe uses wrapper | No — `just test` exits 0 |
| **LMB-7** | `PythonGenerator` emits one "mangled name already exists" warning per slot for every slot that appears more than once in a merged schema | ⚠️ Noise (not an error); upstream schema design gap | None needed — warnings are spurious | No |
| **LMB-8** | Standard prefixes `xsd` and `shex` are "Unrecognized" after mergeimports — generator doesn't treat W3C/ShEx built-ins as implicitly declared | 📋 Ready to file | None needed — warnings are informational | No |

No active blockers on FINOS data compliance. LMB-1, LMB-2, LMB-4, LMB-5, and LMB-6 have working idempotent workarounds; LMB-3 is a long-term ergonomics improvement.

---

## LMB-1 — `SchemaLoader` loses directory context resolving nested relative imports during merge

**Status**: 📋 Ready to file (probable duplicate of [linkml/linkml#2054](https://github.com/linkml/linkml/issues/2054)) · **FINOS impact**: none (workaround active)

### Observation

`gen-project --merge_modules=true` resolves nested `./`-prefixed imports against the *root schema directory* rather than the *importing module's directory*. For ai-atlas-nexus (where `ai-risk-ontology.yaml` imports `./common`, and `common.yaml` imports `./ai_system`, etc.) this raises `FileNotFoundError` during merge:

```
FileNotFoundError: [Errno 2] No such file or directory:
  '/…/ai-risk-ontology/ai_system.yaml'   <- should be …/ai_system.yaml resolved from common.yaml's dir
```

### Reproducer

```bash
cd linkml
.venv/bin/python -c "
from linkml_runtime.utils.schemaview import SchemaView
sv = SchemaView('src/ai_governance_framework/schema/ai_governance_framework.yaml',
                merge_imports=True)
sv.materialize_derived_schema()
"
# -> FileNotFoundError on nested ./-prefixed import
```

### Workaround (active)

`merge_modules: false` in [linkml/gen-project.yaml](linkml/gen-project.yaml) plus per-generator imports preserved as separate files. `just gen-project` exits 0; some monolithic generator outputs (merged GraphQL schema, single-file OWL) are consequently incomplete but the per-module outputs are intact.

### Suggested fix (LinkML)

In `SchemaLoader._merge_imports()`, resolve `./`-prefixed imports against the *importing schema's source path* rather than the loader's root. Mirrors the resolution already correct in non-merge mode.

### Proposed upstream issue body

> **Title**: `gen-project --merge_modules=true` fails on nested relative imports — directory context lost
>
> **Body**: `SchemaLoader` in merge mode resolves `./`-prefixed imports against the root schema directory rather than the importing module's directory. For schemas with multi-level relative imports (e.g. `ai-atlas-nexus`: `ai-risk-ontology.yaml` -> `./common` -> `./ai_system`), this raises `FileNotFoundError`. Non-merge resolution is correct; only merge mode breaks.
>
> Repro: see https://github.com/finos/ai-governance-framework/blob/main/ISSUE-linkml.md#lmb-1
>
> Probable duplicate of [#2054](https://github.com/linkml/linkml/issues/2054). Suggested fix: resolve relative imports against the importing schema's source path.

---

## LMB-2 — `shaclgen` `KeyError` on imported module name when `mergeimports=True`

**Status**: 📋 Ready to file · **FINOS impact**: none (SHACL generator excluded)

### Observation LMB-2

`gen-shacl --mergeimports=True` raises `KeyError: 'common'` (or any imported module name) when the source schema imports modules using bare names. The generator looks up the module by its bare key in `schema.imports` rather than by its resolved path, and the post-merge `SchemaView` no longer carries the bare-key form.

### Reproducer LMB-2

```bash
cd linkml
.venv/bin/python -m linkml.generators.shaclgen \
  src/ai_governance_framework/schema/ai_governance_framework.yaml \
  --mergeimports
# -> KeyError: 'common'
```

### Workaround (active)

[`linkml/config.yaml`](linkml/config.yaml) carries:

```yaml
generators:
  excludes:
    - shacl
    - markdown
```

`gen-project` produces all other artefacts (Pydantic, GraphQL, JSON Schema, JSON-LD context, OWL, TypeScript, Java, Protobuf) successfully.

### Suggested fix (LinkML)

In `ShaclGenerator._iter_modules()`, look up imported modules via `SchemaView.imports_closure()` rather than direct `schema.imports[key]` access.

### Proposed upstream issue body

> **Title**: `gen-shacl --mergeimports` raises `KeyError` on imported module name
>
> **Body**: With `mergeimports=True`, `shaclgen` raises `KeyError: '<module_name>'` for any imported module looked up by bare key after merge has rewritten the schema. SHACL-from-merged-schemas is therefore unusable for any multi-module schema.
>
> Repro: https://github.com/finos/ai-governance-framework/blob/main/ISSUE-linkml.md#lmb-2
>
> Suggested fix: `ShaclGenerator` should iterate imports via `SchemaView.imports_closure()` rather than direct `schema.imports[key]` access.

---

## LMB-3 — Granular / namespace-aware imports missing

**Status**: 🔵 Tracked at [LinkML discussion #1739](https://github.com/orgs/linkml/discussions/1739) · **FINOS impact**: none

### Observation

LinkML imports are all-or-nothing — there is no way to:

1. Import a *subset* of classes / slots / enums from a module (`imports: { common: [Entity, Documentation] }` style).
2. Alias an imported class (`imports: { dpv: { PersonalData: as: DPVPersonalData } }`) to avoid collisions.
3. Re-export a vendored module under a local namespace (`imports: { dpv: namespace: lmodel/dpv }`).

This makes G14-style duplicate-slot collisions (across modules that legitimately need both) hard to resolve without forking the schema.

### Effect on FINOS

Mitigated by Plan C (zero local schema additions). The FINOS umbrella now has 1 import only ([`ai_governance_framework.yaml`](linkml/src/ai_governance_framework/schema/ai_governance_framework.yaml) -> `ai-risk-ontology`) so collision risk is minimal.

### Tracked at

[LinkML discussion #1739 — granular imports](https://github.com/orgs/linkml/discussions/1739) (existing community discussion). No separate issue needed from FINOS.

---

## LMB-4 — LinkML `data_utils` global-ID merging silently corrupts multi-class Containers

**Status**: 📋 Ready to file (upstream-Nexus / LinkML-runtime gap) · **FINOS impact**: none (workaround active)

### Observation

The ai-atlas-nexus `load_yamls_to_container()` function (and underlying LinkML `data_utils`) merges records by `id` *globally across all collections* in a Container, rather than per-class. When a Taxonomy and a Documentation record share the same `id` (e.g., `nist-ai-600-1`), the loader silently overwrites one with the other during deserialization. Later, when Pydantic validates the Container:

1. The merged record carries fields from both classes (e.g., `author: NIST` on a Taxonomy)
2. Pydantic rejects the record as violating slot constraints (`extra_forbidden`, `literal_error`)
3. Error trace references wrong indices / wrong class names (because the record is corrupted, not missing)

This makes the error source very hard to diagnose.

### Reproducer (FINOS)

In [linkml/tests/data/finos/](linkml/tests/data/finos/):

- `nist_ai_600_1.yaml`: Taxonomy `id: nist-ai-600-1` + Documentation `id: nist-ai-600-1` (collision) -> Pydantic error: `taxonomies.22.RiskTaxonomy.author: Extra inputs are not permitted`
- `nist_sp_800_53_r5.yaml`: Taxonomy `id: nist-sp-800-53r5` + Documentation `id: nist-sp-800-53r5` (collision) -> Pydantic error: `taxonomies.X.RiskControlGroupTaxonomy.author: Extra inputs are not permitted`

**Pre-fix proof**:

```bash
cd linkml
python3 << 'EOF'
import yaml, glob
for f in sorted(glob.glob('tests/data/finos/*.yaml')):
    data = yaml.safe_load(open(f))
    all_ids = {}
    for coll in ['taxonomies', 'documents', 'entries', 'groups', 'vocabularies', 'controls']:
        for r in data.get(coll, []):
            rid = r.get('id')
            if rid in all_ids:
                print(f"COLLISION in {f.split('/')[-1]}: '{rid}' in {all_ids[rid]} AND {coll}")
            else:
                all_ids[rid] = coll
EOF
# Output (pre-fix):
# COLLISION in nist_ai_600_1.yaml: 'nist-ai-600-1' in taxonomies AND documents
# COLLISION in nist_sp_800_53_r5.yaml: 'nist-sp-800-53r5' in taxonomies AND documents
```

### Workaround (active)

In [`linkml/scripts/build_finos_data.py`](linkml/scripts/build_finos_data.py):

1. **Rename colliding Documentation IDs** with `-doc` suffix:
   - `nist-ai-600-1` -> `nist-ai-600-1-doc`
   - `nist-sp-800-53r5` -> `nist-sp-800-53r5-doc`

2. **Defensive collision detection** added to `_dump()`:
   - Function `_check_id_collisions(path: Path, data: Any)` inspects every Container dump at generation time
   - Fails fast with a clear message if any `id` appears in multiple collections
   - Prevents future regressions from similar conflicts

**Impact on referential integrity**: SSSOM generator only references Taxonomy `id`s (not Documentation), so the rename is safe. `hasDocumentation: [nist-ai-600-1-doc]` correctly resolves in the flattened Container.

### Suggested fix (LinkML / ai-atlas-nexus)

At the ai-atlas-nexus level (not LinkML proper):

1. **Document the constraint**: Clarify that `load_yamls_to_container()` requires unique IDs across all collections in a Container. Add a runtime check (like our `_check_id_collisions()`) to fail early with a clear message instead of silently corrupting records.

2. **Or**: Scope merging per-class collection instead of globally. This would be more aligned with standard Container semantics (where `id` is unique within its class, not across the entire data space).

### Proposed upstream issue body

> **Title**: `load_yamls_to_container()` global-ID merging silently corrupts multi-class records
>
> **Body**: When two records from different collections (e.g., Taxonomy and Documentation) share the same `id`, `load_yamls_to_container()` silently overwrites one during merge. The corrupted record later fails Pydantic validation with cryptic `extra_forbidden`/`literal_error` errors that don't clearly point to the ID collision.
>
> **Reproducer**: Create a Container YAML with `taxonomies[0].id = 'X'` and `documents[0].id = 'X'`. Load via `load_yamls_to_container()` and validate. The resulting record carries fields from both classes, violating Pydantic constraints.
>
> **Suggested fix**: 
> - Add a runtime `_check_id_collisions()` validation in `load_yamls_to_container()` that fails fast with a clear message
> - Or: scope merging per-class instead of globally (more semantically correct)
> - Document the constraint if the current behavior is intentional

---

## LMB-5 — `gen-rust` `RustStructOrSubtypeEnum.type_designators` annotation mismatch crashes on `designates_type` hierarchies

**Status**: 📋 Ready to file · **FINOS impact**: none (monkey-patch wrapper active) · **LinkML version**: 1.9.4

### Observation LMB-5

The Pydantic template model `RustStructOrSubtypeEnum` (in `linkml/generators/rustgen/template.py`) annotates the `type_designators` field as `dict[str, str]`, but:

- The producer code in `linkml/generators/rustgen/rustgen.py` populates it with `dict[str, list[str]]` via [`get_accepted_type_designator_values()`](https://github.com/linkml/linkml/blob/main/linkml/generators/common/type_designators.py) (which always returns a `list[str]` of accepted CURIE/URI/native forms per LinkML issue [#945](https://github.com/linkml/linkml/issues/945)).
- The Jinja template `templates/struct_or_subtype_enum.rs.jinja` consumes it as a list (`tds[0]`, `tds[1:]`).

Under Pydantic v2's strict validation the producer-side mismatch trips:

```
pydantic_core._pydantic_core.ValidationError: 3 validation errors for RustStructOrSubtypeEnum
type_designators.RiskTaxonomy
  Input should be a valid string [type=string_type, input_value=['RiskTaxonomy'], input_type=list]
type_designators.RiskControlGroupTaxonomy
  Input should be a valid string [type=string_type, input_value=['RiskControlGroupTaxonomy'], input_type=list]
type_designators.CapabilityTaxonomy
  Input should be a valid string [type=string_type, input_value=['CapabilityTaxonomy'], input_type=list]
```

This fires for any class hierarchy that has descendants AND a `designates_type: true` slot — in our case the three concrete descendants of ai-atlas-nexus `Taxonomy` (whose `taxonomy__type` slot is the type designator).

### Reproducer LMB-5

```bash
cd linkml
.venv/bin/python -m linkml.generators.rustgen.cli \
  --mergeimports --force -o /tmp/rust-out \
  tmp/ai_governance_framework.yaml
# -> ValidationError: 3 validation errors for RustStructOrSubtypeEnum
#     type_designators.RiskTaxonomy ... input_type=list
```

Minimum schema to reproduce: any LinkML schema with a parent class whose slot has `designates_type: true` and ≥1 concrete subclass.

### Workaround (active)

[`linkml/scripts/issues/gen_rust_patched.py`](linkml/scripts/issues/gen_rust_patched.py) rebuilds the Pydantic model with the corrected annotation before delegating to the upstream click CLI:

```python
from linkml.generators.rustgen import template as _rust_template
from linkml.generators.rustgen.cli import cli as _gen_rust_cli

_field = _rust_template.RustStructOrSubtypeEnum.model_fields["type_designators"]
_field.annotation = dict[str, list[str]]
_rust_template.RustStructOrSubtypeEnum.model_rebuild(force=True)

if __name__ == "__main__":
    sys.exit(_gen_rust_cli())
```

Wired into [`linkml/project.justfile`](linkml/project.justfile) as `gen-rust-artifact`. `just gen-rust-artifact` now produces `project/rust/` containing `Cargo.toml`, `pyproject.toml`, and `src/{lib.rs,poly.rs,poly_containers.rs,serde_utils.rs,stub_utils.rs}`.

### Suggested fix (LinkML)

One-line annotation fix in `linkml/generators/rustgen/template.py`:

```diff
 class RustStructOrSubtypeEnum(RustTemplateModel):
     template: ClassVar[str] = "struct_or_subtype_enum.rs.jinja"
     enum_name: str
     struct_names: list[str]
     as_key_value: bool = False
     type_designator_field: str | None = None
-    type_designators: dict[str, str]
+    type_designators: dict[str, list[str]]
     key_property_type: str = "String"
```

This matches both the producer (`rustgen.py: td_mapping[d] = get_accepted_type_designator_values(...)`) and the consumer (`struct_or_subtype_enum.rs.jinja: tds[0]`, `{% for t in tds[1:] %}`).

### Proposed upstream issue body

> **Title**: `gen-rust` crashes with Pydantic `ValidationError` on schemas using `designates_type` — `RustStructOrSubtypeEnum.type_designators` annotated as `dict[str, str]` but populated as `dict[str, list[str]]`
>
> **Body**: `linkml/generators/rustgen/template.py` declares `RustStructOrSubtypeEnum.type_designators: dict[str, str]`, but the producer in `rustgen.py:gen_struct_or_subtype_enum()` fills it from `get_accepted_type_designator_values()` (which always returns `list[str]`), and the Jinja template `struct_or_subtype_enum.rs.jinja` indexes it as a list (`tds[0]`, `tds[1:]`). Under Pydantic v2 strict validation this raises `ValidationError: Input should be a valid string ... input_type=list` for every descendant of a class with a type-designator slot.
>
> Repro: any LinkML schema with a class hierarchy whose parent has a `designates_type: true` slot — e.g. ai-atlas-nexus `Taxonomy` -> `RiskTaxonomy` / `RiskControlGroupTaxonomy` / `CapabilityTaxonomy`. See https://github.com/finos/ai-governance-framework/blob/main/ISSUE-linkml.md#lmb-5
>
> **Suggested fix**: change `type_designators: dict[str, str]` -> `dict[str, list[str]]` in `RustStructOrSubtypeEnum` (one line in `template.py`). Verified produces a clean crate against a merged schema with 4 type-designator hierarchies.
>
> Inspected in linkml 1.9.4.

---

## LMB-6 — `linkml-run-examples` `ExampleRunner._load_from_dict` crashes on list-valued inline multivalued slots

**Status**: 📋 Ready to file · **FINOS impact**: none (monkey-patch wrapper active) · **LinkML version**: 1.9.4

### Observation LMB-6

(note: check https://github.com/linkml/linkml/issues/2415)

`ExampleRunner._load_from_dict` (in `linkml/workspaces/example_runner.py`) handles inline multivalued slots by calling `v.items()` unconditionally on the slot value. For the case where `inlined=True` and `inlined_as_list` is not explicitly set but the YAML payload provides the value as a list, this raises:

```
AttributeError: 'list' object has no attribute 'items'
```

This is a type-narrowing error: the method only handles the dict-keyed inline form, but YAML examples legitimately supply inline multivalued associations as plain lists of IDs or inline objects. The crash propagates through `process_examples_from_list` as `ValueError: Example … failed validation: 'list' object has no attribute 'items'`.

A second related failure on `hasStakeholder` (`'stakeholder-risk-analyst' is not valid under any of the given schemas in /hasStakeholder/0`) was a local schema gap — the slot lacked `multivalued: true` and `inlined: false` — but was revealed by the same example runner exercising the schema.

### Reproducer LMB-6

```bash
cd linkml
# Generate per-class valid fixtures and run the example runner against them
uv run linkml-run-examples \
  --input-formats yaml \
  --output-formats json \
  --input-directory tests/data/valid \
  --output-directory /tmp/ex-out \
  --schema tmp/ai_governance_framework.yaml
# -> AttributeError: 'list' object has no attribute 'items'
# Via: ExampleRunner._load_from_dict, line 263
```

Minimum schema to reproduce: a schema with any class that has a slot where `multivalued: true` and `inlined: true` (or defaulted), and a valid YAML example supplying that slot as a list.

### Workaround (active)

[`linkml/scripts/issues/run_examples_patched.py`](linkml/scripts/issues/run_examples_patched.py) monkey-patches `ExampleRunner._load_from_dict` to guard the `v.items()` call:

```python
if islot.multivalued and islot.inlined and not islot.inlined_as_list:
    if isinstance(v, list):
        # Slot is multivalued+inlined but value is already a list — process directly
        v2 = self._load_from_dict(v, target_class=islot.range)
    else:
        # Original dict-keyed inline handling
        (range_id_slot, range_simple_dict_value_slot, _) = get_range_associated_slots(...)
        for ik, iv in v.items():
            ...
```

Wired into [linkml/justfile](linkml/justfile) `_test-examples` recipe:

```
uv run python scripts/issues/run_examples_patched.py ...
```

`just test` exits 0 after this fix plus the `hasStakeholder` schema correction (`multivalued: true`, `inlined: false` in [linkml/src/ai_governance_framework/schema/ai_risk_ontology/ai_system.yaml](linkml/src/ai_governance_framework/schema/ai_risk_ontology/ai_system.yaml)).

### Suggested fix (LinkML)

In `ExampleRunner._load_from_dict` (`linkml/workspaces/example_runner.py`), guard the `inlined_as_list`-false branch with an `isinstance(v, list)` check:

```diff
             if islot.multivalued and islot.inlined and not islot.inlined_as_list:
+                if isinstance(v, list):
+                    v2 = self._load_from_dict(v, target_class=islot.range)
+                else:
                 (range_id_slot, range_simple_dict_value_slot, _) = get_range_associated_slots(
                     self.schemaview, islot.range
                 )
                 v_as_list = []
                 for ik, iv in v.items():
                     ...
```

This makes the method robust to both dict-keyed inline form (the existing path) and list-form (the new guard), consistent with how `isinstance(dict_obj, list)` is already handled at the outer level of the same method.

### Proposed upstream issue body

> **Title**: `linkml-run-examples` crashes with `AttributeError: 'list' object has no attribute 'items'` when a valid example supplies an inline multivalued slot as a list
>
> **Body**: `ExampleRunner._load_from_dict` (in `linkml/workspaces/example_runner.py`) unconditionally calls `v.items()` for slots where `multivalued and inlined and not inlined_as_list`. When a valid YAML example provides such a slot as a list rather than a keyed dict (which is valid YAML — the spec doesn't mandate the keyed form for association slots), this raises `AttributeError: 'list' object has no attribute 'items'`, wrapped as `ValueError: Example … failed validation: …`.
>
> Repro: any schema with an inline multivalued association slot and a valid example providing that slot as a list. See https://github.com/finos/ai-governance-framework/blob/main/ISSUE-linkml.md#lmb-6
>
> **Suggested fix**: guard the `v.items()` path with `isinstance(v, list)` and short-circuit to `self._load_from_dict(v, ...)` for the list case. One-line change in `example_runner.py:263`. Patch verified against merged ai-atlas-nexus schema (linkml 1.9.4).

---

## LMB-7 — `PythonGenerator` emits spurious "mangled name already exists" warnings for every slot duplicated in a merged schema

**Status**: ⚠️ Noise warning (not an error); upstream schema design gap · **FINOS impact**: none (no action needed) · **LinkML version**: 1.9.4

### Observation LMB-7

When `PythonGenerator` processes a merged schema (produced by `mergeimports=True` or `scripts/linkml_import_tools.py merge`), it emits one warning per slot for every slot name that was defined in more than one constituent module:

```
Class: "Container" attribute "organizations" - mangled name: container__organizations already exists
Class: "Container" attribute "taxonomies" - mangled name: container__taxonomies already exists
... (80+ lines for ai_governance_framework.yaml)
```

**Why it happens**: LinkML merges all slots from all transitive imports into a single flat namespace in the merged YAML. Slots that appear in both an upstream module and the root schema (e.g. every `Container` slot defined in `common.yaml` and echoed in the root schema that imports it) get their mangled form (`ClassName__slotname`) registered twice. On the second registration the generator warns.

**Impact**: None. The first definition wins and the module compiles correctly. The warnings are purely cosmetic noise.

**Volume**: ~80 lines for the ai-governance-framework merged schema. They dominate `just test` stderr and obscure genuinely actionable messages.

### Workaround

None required — build succeeds. Suppress with `2>/dev/null` or a log-level filter if noise is a problem in CI.

### Suggested fix (LinkML)

In `PythonGenerator._mangled_name()` (or the slot-registration loop), detect duplicates silently or demote the log level to `DEBUG`:

```diff
- logger.warning(f'Class: "{cls.name}" attribute "{slot.name}" - mangled name: {mangled} already exists')
+ logger.debug(f'Class: "{cls.name}" attribute "{slot.name}" - mangled name: {mangled} already exists (merged schema duplicate — expected)')
```

Or: emit the warning at most once per slot name across all classes (deduplicate before logging).

---

## LMB-8 — Standard prefixes `xsd` and `shex` treated as "Unrecognized" after mergeimports

**Status**: 📋 Ready to file · **FINOS impact**: none (informational warning only) · **LinkML version**: 1.9.4

### Observation LMB-8

When any generator loads the merged schema, the LinkML schema validator emits:

```
File "ai_governance_framework.yaml", line 65, col 10: Unrecognized prefix: xsd
File "ai_governance_framework.yaml", line 261, col 10: Unrecognized prefix: shex
```

`xsd` (W3C XML Schema datatypes) and `shex` (W3C Shape Expressions) are universally recognised W3C standards. They are referenced in the ai-atlas-nexus vendored schema (in `prefixes:` or as type/slot URIs) but their canonical URIs are not echoed into the merged schema's `prefixes:` block after the merge step.

LinkML's generator does not treat any prefix as implicitly declared — every prefix used must appear in the active schema's `prefixes:` map. Because the merge step flattens imports but does not guarantee that all transitively-required prefixes are propagated into the root `prefixes:` map, these two standard prefixes are lost.

Note: `tech`, `dpv`, `dqv`, `ai` unrecognized prefix warnings come from the same root cause but originate in the upstream ai-atlas-nexus schema (tracked as G32 in [ISSUE-nexus.md](ISSUE-nexus.md)).

### Workaround

None needed — these are warnings, not errors. The generated artefacts (Python, Pydantic, JSON Schema, etc.) are correct.

### Suggested fix (LinkML)

Two complementary options:

1. **Merge-step fix**: `scripts/linkml_import_tools.py merge` (or LinkML's native merge) should copy all `prefixes:` entries from every imported module into the merged output's root `prefixes:` block.

2. **Validator fix**: Treat `xsd`, `shex`, `rdf`, `rdfs`, `owl`, `skos`, and `linkml` as always-declared built-in prefixes and suppress the "Unrecognized prefix" warning for them.

### Proposed upstream issue body

> **Title**: `mergeimports` drops transitively-imported prefix declarations, causing spurious "Unrecognized prefix" warnings for `xsd`, `shex`, and other standard prefixes
>
> **Body**: After merging a multi-module schema, any prefix declared only in an imported module (not the root schema) is absent from the merged output's `prefixes:` block. The generator then warns "Unrecognized prefix: xsd" (and `shex`, and any others from imports). `xsd` and `shex` are W3C standards and should be either implicitly known or faithfully propagated during merge.
>
> Repro: `scripts/linkml_import_tools.py merge` on any schema that imports ai-atlas-nexus. Check merged YAML for `xsd:` in `prefixes:`; it will be absent, and every downstream generator warns.
>
> **Suggested fix**: propagate all `prefixes:` from every merged module into the root block (collision-free), or treat standard W3C prefixes as implicitly declared. See https://github.com/finos/ai-governance-framework/blob/main/ISSUE-linkml.md#lmb-8

| Step | LMB-1 | LMB-2 | LMB-3 | LMB-4 | LMB-5 | LMB-6 | LMB-7 | LMB-8 |
|---|---|---|---|---|---|---|---|---|
| Reproducer captured | ✅ | ✅ | n/a | ✅ | ✅ | ✅ | ✅ | ✅ |
| Workaround documented | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Suggested fix drafted | ✅ | ✅ | n/a | ✅ | ✅ | ✅ | ✅ | ✅ |
| Upstream-issue body drafted | ✅ | ✅ | n/a | ✅ | ✅ | ✅ | ✔️ (no body; noise only) | ✅ |
| Filed | ⏳ | ⏳ | ✅ (community) | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |

---

## References

- **LinkML discussion #1739** — https://github.com/orgs/linkml/discussions/1739 (granular imports)
- **Candidate duplicate for LMB-1** — [linkml/linkml#2054](https://github.com/linkml/linkml/issues/2054)
- **LinkML issue #945** — https://github.com/linkml/linkml/issues/945 (type-designator accepted-values semantics, LMB-5 context)
- **FINOS adoption state** — [linkml/docs/about.md](linkml/docs/about.md)
- **Upstream-Nexus gaps** — [ISSUE-nexus.md](ISSUE-nexus.md)
