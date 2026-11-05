## Add your own just recipes here. This is imported by the main justfile.

# Overriding recipes from the root justfile by adding a recipe with the same
# name in this file is not possible until a known issue in just is fixed,
# https://github.com/casey/just/issues/2540

# ============ The catalogue and the SSSOM sets ============

# Write src/ai_governance_framework/data/aigf-v3.yaml from FINOS's files
[group('model development')]
build-catalogue:
  uv run python scripts/build_catalogue.py

# Fail when the catalogue differs from what FINOS's files give
[group('model development')]
check-catalogue:
  uv run python scripts/build_catalogue.py --check

# Write one SSSOM set for each of FINOS's reference files
[group('model development')]
build-mappings:
  uv run python scripts/build_sssom_mappings.py

# Fail when an SSSOM set differs from what FINOS's files give
[group('model development')]
check-mappings:
  uv run python scripts/build_sssom_mappings.py --check

# ============ Knowledge bundle: the adapted domain schema ============

# `../.lokf/ai-governance-framework.yaml` is the copy `lokf adapt` writes from the
# schema so that it can sit beside `../.lokf/lokf.yaml` (`lokf adapt --help` lists
# the moves). The roots are the classes a knowledge concept may use as its `type`.
# The recipes run the `lokf` the sidecar's floor pins (0.9.0 or later); LOKF_CMD runs
# another, such as a checkout:
# LOKF_CMD="uv run --project ../../lokf lokf" just lokf-adapt
lokf_cmd := env_var_or_default("LOKF_CMD", "uv run --project ../.lokf lokf")
lokf_adapt_roots := "--root AigfItem --root AigfDataClassification --prefix aigf"

# Rewrite ../.lokf/ai-governance-framework.yaml from the schema (run after every schema change)
[group('knowledge bundle')]
lokf-adapt:
  {{lokf_cmd}} adapt {{source_schema_path}} {{lokf_adapt_roots}} --lokf ../.lokf/lokf.yaml -o ../.lokf/ai-governance-framework.yaml

# Fail when ../.lokf/ai-governance-framework.yaml is stale against the schema or lokf.yaml
[group('knowledge bundle')]
lokf-adapt-check:
  {{lokf_cmd}} adapt {{source_schema_path}} {{lokf_adapt_roots}} --lokf ../.lokf/lokf.yaml -o ../.lokf/ai-governance-framework.yaml --check

# ---- linkml-sidecar: the linkml_schema doorway (kept across `just update`) ----
# The schema folder under an ordinary, visible name at the host root, for
# folder pickers and file managers that hide dot-folders. Git carries the
# link; a sync service does not, so this recipe recreates it on a machine
# where it is missing. POSIX only; on Windows run, from the host root,
# mklink /J linkml_schema .linkml\src\ai_governance_framework\schema

# Create (or recreate) the linkml_schema link at the host root, to .linkml/src/ai_governance_framework/schema
[group('sidecar')]
linkml-link:
    #!/usr/bin/env bash
    set -euo pipefail
    target=".linkml/src/{{schema_name}}/schema"
    [ -d "../$target" ] || { echo "no $target to link to" >&2; exit 1; }
    if [ -L ../linkml_schema ]; then
      if [ "$(readlink ../linkml_schema)" = "$target" ]; then echo "linkml_schema already present - nothing to link"; exit 0; fi
      echo "../linkml_schema is a link elsewhere ($(readlink ../linkml_schema)) - remove it and re-run" >&2; exit 1
    fi
    if [ -e ../linkml_schema ]; then echo "../linkml_schema exists and is not a link - leaving it alone" >&2; exit 1; fi
    ln -s "$target" ../linkml_schema && echo "linked linkml_schema -> $target"
