## Add your own just recipes here. This is imported by the main justfile.

# Overriding recipes from the root justfile by adding a recipe with the same
# name in this file is not possible until a known issue in just is fixed,
# https://github.com/casey/just/issues/2540

# ============== Schema / Test fixture recipes ==============

# Regenerate the FINOS catalogue (native ai-risk-ontology shape) and
# the per-class test fixtures under tests/data/{valid,invalid}/.
# Reads docs/_risks/, docs/_mitigations/, docs/_usecases/ — see linkml/docs/about.md.
[group('model development')]
gen-data: && gen-mappings
    uv run python ./scripts/build_finos_data.py

[group('model development')]
gen-mappings:
    uv run python ./scripts/build_sssom_mappings.py

# Apply curated SSSOM mapping TSVs to the generated LinkML schema YAMLs.
# Merges SKOS exact/close/broad/narrow/related matches into the matching
# class / enum / type bodies and declares any referenced object-side prefixes.
# Idempotent: re-running on a clean tree produces no further changes.
# Merge curated SSSOM mappings into the generated LinkML schemas.
[group('model development')]
apply-sssom-overlay:
  uv run python scripts/sssom_mappings.py overlay \
    --schema-dir src/ai_governance_framework/schema \
    --mappings-dir src/ai_governance_framework/mappings

# ============== Hidden internal recipes ==============

# Materialise an absolute-path import map at `tmp/importmap.json`.
# Source of truth is the committed `importmap.json` (relative paths). At
# build time we rewrite its string values to absolute paths because
# `SchemaLoader` joins importmap values with the importing schema's
# directory; absolute values short-circuit that join.
_importmap:
    #!{{shebang}}
    import json
    import os
    from pathlib import Path
    repo_root = Path.cwd().resolve()
    src_path = repo_root / "importmap.json"
    if not src_path.exists():
        raise SystemExit(f"Missing {src_path}")
    data = json.loads(src_path.read_text())
    abs_data = {
        k: (str(repo_root / v) + os.sep if isinstance(v, str) and not os.path.isabs(v) else v)
        for k, v in data.items()
    }
    dest = repo_root / "tmp" / "importmap.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(abs_data, indent=2) + "\n")
    print(f"Wrote {dest}")


# Materialise a self-contained merged schema at `{{merged_schema_path}}`.
# Required because `gen-project`'s SchemaLoader-based sub-generators
# (python/sqltable/excel) construct a secondary SchemaView from the merged
# schema *without* propagating `--importmap`, so any unresolved URI imports
# in the merged schema's `imports:` list get HTTP-fetched and fail.
# `scripts/linkml_import_tools.py merge` resolves imports up-front and strips them.
# Depends on `apply-sssom-overlay` so the source schemas exist (and carry
# the curated mappings) before we try to flatten them.
_merged-schema: _importmap apply-sssom-overlay
  uv run python scripts/linkml_import_tools.py merge {{source_schema_path}} \
    --importmap {{import_map_path}} \
    --output {{merged_schema_path}}

# ============== Supplemental generator recipes (beyond gen-project defaults) ==============
#
# gen-project already covers: graphql, jsonldcontext, jsonld, jsonschema, owl,
# prefixmap, proto, python, shex, shacl, sqlddl, excel, typescript.
# Explicit in main justfile: java, typescript (dup), owl (dup), pydantic (-> datamodel/).
# The recipes below cover the remaining available generators.
# Run all at once with: just gen-project-extended

# ---- Schema / metadata formats ----

# NOTE: recipe named gen-merged-schema to avoid conflict with CDM's gen-linkml recipe
# Generate a single self-contained merged LinkML YAML with all imports resolved.
#
# We feed `gen-linkml` the pre-merged schema (`tmp/ai_governance_framework.yaml`) rather than
# the source `src/ai_governance_framework/schema/ai_governance_framework.yaml` because `gen-linkml` builds an
# internal `SchemaView` without honouring `--importmap` for URI-style
# imports (see ISSUE.md §8/§9 - same upstream bug as `gen-doc`). Feeding
# the merged YAML sidesteps the broken import resolution entirely.
[group('model development - extended')]
gen-merged-schema: _merged-schema
  mkdir -p {{dest}}/linkml
  uv run gen-linkml --mergeimports -o {{dest}}/linkml/{{schema_name}}.merged.linkml.yaml {{merged_schema_path}}

# gen-yaml CLI hits the linkml-runtime 1.11.0 RepresenterError (JsonObj missing SafeDumper representer).
# Use the same patched script as _gen-yaml until linkml-runtime > 1.11.0 lands.
# Generate resolved YAML schema (patched yamlgen).
#
# Feed the pre-merged schema (`tmp/ai_governance_framework.yaml`) so URI imports like
# `ai_governance_framework:schema/ai_governance_framework_common` are already resolved - `gen-yaml` underneath
# `gen_yaml_patched.py` also drops `--importmap` for URI imports and
# would 404 on the w3id IRI (see ISSUE.md §8/§9).
[group('model development - extended')]
gen-yaml-artifact: _merged-schema
  mkdir -p {{dest}}/yaml
  uv run python scripts/issues/gen_yaml_patched.py {{merged_schema_path}} > {{dest}}/yaml/{{schema_name}}.yaml

# Generate SSSOM mapping TSV from schema slot_uri / mappings
[group('model development - extended')]
gen-sssom-artifact: _merged-schema
  mkdir -p {{dest}}/sssom
  uv run gen-sssom --mergeimports -o {{dest}}/sssom/{{schema_name}}.sssom.tsv {{merged_schema_path}}

# Generate Python namespace manager for all prefixes in the schema
[group('model development - extended')]
gen-namespaces-artifact: _merged-schema
  mkdir -p {{dest}}/namespaces
  uv run gen-namespaces --mergeimports {{merged_schema_path}} > {{dest}}/namespaces/{{schema_name}}.namespaces.py

# Generate TSV summary (classes, slots, counts - useful in spreadsheets)
[group('model development - extended')]
gen-summary-artifact: _merged-schema
  mkdir -p {{dest}}/summary
  uv run gen-summary --mergeimports {{merged_schema_path}} > {{dest}}/summary/{{schema_name}}.summary.tsv

# ---- Visualization / diagram formats ----

# Generate a single combined Graphviz DOT graph of the schema
[group('model development - extended')]
gen-graphviz-artifact: _merged-schema
  mkdir -p {{dest}}/graphviz
  uv run gen-graphviz --mergeimports -f dot -o {{dest}}/graphviz/{{schema_name}}.dot {{merged_schema_path}}

# Generate per-class Mermaid class diagram Markdown files (one .md per class)
[group('model development - extended')]
gen-mermaid-artifact: _merged-schema
  mkdir -p {{dest}}/mermaid
  uv run gen-mermaid-class-diagram --mergeimports -d {{dest}}/mermaid {{merged_schema_path}}

# Generate Mermaid ER diagram (single file, mermaid format)
[group('model development - extended')]
gen-erdiagram-artifact: _merged-schema
  mkdir -p {{dest}}/erdiagram
  uv run gen-erdiagram --mergeimports -f mermaid {{merged_schema_path}} > {{dest}}/erdiagram/{{schema_name}}.er.md

# Generate PlantUML diagram (stdout -> single file)
[group('model development - extended')]
gen-plantuml-artifact: _merged-schema
  mkdir -p {{dest}}/plantuml
  uv run gen-plantuml --mergeimports {{merged_schema_path}} > {{dest}}/plantuml/{{schema_name}}.plantuml

# ---- Data / query formats ----

# gen-rdf embeds ./cdm_*.context.jsonld refs that rdflib resolves against the
# schema @base URL (https://w3id.org/lmodel/…), returning HTTP 404. Patched
# script strips those refs; all prefix bindings are in the merged context.
# Generate RDF/Turtle representation of the schema
[group('model development - extended')]
gen-rdf-artifact: _merged-schema
  mkdir -p {{dest}}/rdf
  uv run python scripts/issues/gen_rdf_patched.py --mergeimports -o {{dest}}/rdf/{{schema_name}}.ttl {{merged_schema_path}}

# Generate a directory of SPARQL validation queries (one query per constraint)
[group('model development - extended')]
gen-sparql-artifact: _merged-schema
  mkdir -p {{dest}}/sparql
  uv run gen-sparql --mergeimports -d {{dest}}/sparql {{merged_schema_path}}

# Generate CSV data dictionary of classes and slots
[group('model development - extended')]
gen-csv-artifact: _merged-schema
  mkdir -p {{dest}}/csv
  uv run gen-csv --mergeimports {{merged_schema_path}} > {{dest}}/csv/{{schema_name}}.csv

# ---- Database formats ----

# Generate DBML (Database Markup Language) for schema visualization tools (DBDiagram etc.)
[group('model development - extended')]
gen-dbml-artifact: _merged-schema
  mkdir -p {{dest}}/dbml
  uv run python3 scripts/issues/gen_dbml_patched.py -s {{merged_schema_path}} -o {{dest}}/dbml/{{schema_name}}.dbml

# Generate SQLAlchemy ORM models
[group('model development - extended')]
gen-sqla-artifact: _merged-schema
  mkdir -p {{dest}}/sqla
  uv run gen-sqla --mergeimports {{merged_schema_path}} > {{dest}}/sqla/{{schema_name}}_sqlalchemy.py

# Generate SQL validation queries
[group('model development - extended')]
gen-sqlvalidation-artifact: _merged-schema
  mkdir -p {{dest}}/sqlvalidation
  uv run gen-sqlvalidation --mergeimports {{merged_schema_path}} > {{dest}}/sqlvalidation/{{schema_name}}.sql

# Generate TerminusDB JSON-LD schema
[group('model development - extended')]
gen-terminusdb-artifact: _merged-schema
  mkdir -p {{dest}}/terminusdb
  uv run gen-terminusdb --mergeimports {{merged_schema_path}} > {{dest}}/terminusdb/{{schema_name}}.json

# Generate TypeDB TypeQL schema definitions
[group('model development - extended')]
gen-typedb-artifact: _merged-schema
  mkdir -p {{dest}}/typedb
  uv run gen-typedb --mergeimports {{merged_schema_path}} > {{dest}}/typedb/{{schema_name}}.tql

# ---- Language bindings ----

# Generate Go structs (stdout -> single file)
[group('model development - extended')]
gen-golang-artifact: _merged-schema
  mkdir -p {{dest}}/golang
  uv run gen-golang --mergeimports {{merged_schema_path}} > {{dest}}/golang/{{schema_name}}.go

# Generate Rust crate (directory with Cargo.toml + src/)
# NOTE: uses scripts/issues/gen_rust_patched.py to monkey-patch an upstream
# annotation bug: RustStructOrSubtypeEnum.type_designators is typed as
# dict[str, str] but is populated/consumed as dict[str, list[str]], which
# trips Pydantic v2 strict validation on schemas with `designates_type`
# class hierarchies (e.g. Taxonomy -> RiskTaxonomy/CapabilityTaxonomy/...).
[group('model development - extended')]
gen-rust-artifact: _merged-schema
  mkdir -p {{dest}}/rust
  uv run python3 scripts/issues/gen_rust_patched.py --mergeimports --force -o {{dest}}/rust {{merged_schema_path}}

# Generate C++17 header file
[group('model development - extended')]
gen-cpp-artifact: _merged-schema
  mkdir -p {{dest}}/cpp
  uv run gen-cpp-header --mergeimports {{merged_schema_path}} > {{dest}}/cpp/{{schema_name}}.h

# Generate Pandera dataframe validation schemas
[group('model development - extended')]
gen-pandera-artifact: _merged-schema
  mkdir -p {{dest}}/pandera
  uv run python3 scripts/issues/gen_pandera_patched.py {{merged_schema_path}} > {{dest}}/pandera/{{schema_name}}_pandera.py

# Generate Markdown data dictionary (single combined file)
# NOTE Bug 12: gen-markdown-datadict creates a new ERDiagramGenerator (and
# therefore re-loads the full CDM schema) for every one of the 2500+ CDM
# classes, hanging indefinitely.  scripts/gen_markdown_datadict_patched.py
# overrides _generate_class_diagram to cache one ERDiagramGenerator instance.
[group('model development - extended')]
gen-markdown-datadict-artifact: _merged-schema
  mkdir -p {{dest}}/markdown-datadict
  uv run python3 scripts/issues/gen_markdown_datadict_patched.py --mergeimports {{merged_schema_path}} > {{dest}}/markdown-datadict/{{schema_name}}.md

# Generate GOLR (SOLR) view configurations (one JSON per class)
[group('model development - extended')]
gen-golr-artifact: _merged-schema
  mkdir -p {{dest}}/golr
  uv run gen-golr-views --mergeimports -d {{dest}}/golr {{merged_schema_path}}

# ---- Aggregate ----

# Usage: just gen-project && just gen-project-extended
# Run all supplemental generators (those not already covered by gen-project)
[group('model development - extended')]
gen-project-extended: \
  gen-merged-schema \
  gen-yaml-artifact \
  gen-sssom-artifact \
  gen-namespaces-artifact \
  gen-summary-artifact \
  gen-graphviz-artifact \
  gen-mermaid-artifact \
  gen-erdiagram-artifact \
  gen-plantuml-artifact \
  gen-rdf-artifact \
  gen-sparql-artifact \
  gen-csv-artifact \
  gen-dbml-artifact \
  gen-sqla-artifact \
  gen-sqlvalidation-artifact \
  gen-terminusdb-artifact \
  gen-typedb-artifact \
  gen-golang-artifact \
  gen-rust-artifact \
  gen-cpp-artifact \
  gen-pandera-artifact \
  gen-markdown-datadict-artifact \
  gen-golr-artifact
