---
type: Explanation
id: https://w3id.org/lmodel/ai-governance-framework/knowledge/explanations/what-is-left-out
genre: explanation
title: What the model leaves out
description: "What the schema and the catalogue do not hold: the pages' prose, the display settings of `docs/_config.yml` other than the lenses, reference entries' titles, and a mapping to lmodel/iso42001, which has no release yet."
resource: .linkml/docs/about.md
about:
  - https://w3id.org/lmodel/ai-governance-framework/knowledge/datasets/catalogue
sources:
  - id: about.md
    resource: .linkml/docs/about.md
    title: What is left out
generated:
  by: process:ktl-librarian
  at: "2026-11-05T21:48:14Z"
  revision: cde50310ebeec25edc8ec55b83e4402e9f6b2ac4
status: draft
---

# What the model leaves out

The pages' prose stays in FINOS's files, which `source_file` names. Most display settings of `docs/_config.yml` stay out, such as the domain icons and the use case order.[^about.md]

There is no mapping to lmodel/iso42001, which has no release. A row of `finos_to_iso_42001.sssom.tsv` names FINOS's key.[^about.md]

[^about.md]: .linkml/docs/about.md, What is left out
