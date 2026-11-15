---
type: Service
id: https://w3id.org/lmodel/ai-governance-framework/knowledge/services/documentation-site
genre: reference
title: Documentation site
description: The knowledge website in `website/`, a Hugo site that the Knowledge website workflow builds. It shows `.linkml/README.md`, `.linkml/docs/`, the changelog, the schema's pages and the bundle, and leaves FINOS's own site alone.
resource: website
sources:
  - id: site.toml
    resource: website/site.toml
    title: the site's address, title and redirects
  - resource: website/README.md
dependsOn:
  - https://w3id.org/lmodel/ai-governance-framework/knowledge/datasets/ai-governance-framework-linkml-schema
generated:
  by: process:ktl-librarian
  at: "2026-11-15T03:27:32Z"
status: draft
---

# Documentation site

`website/site.toml` names what the site shows. The home page is `.linkml/README.md`, the docs are `.linkml/docs/`, and the changelog is `.linkml/CHANGELOG.md`.[^site.toml]

The site's schema pages come from `just --justfile .linkml/justfile gen-doc`.[^site.toml] FINOS's Jekyll `docs/` stays out.[^site.toml]

[^site.toml]: website/site.toml, the site's address, title and redirects
