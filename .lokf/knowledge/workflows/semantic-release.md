---
type: Service
id: https://w3id.org/lmodel/ai-governance-framework/knowledge/workflows/semantic-release
genre: reference
title: Semantic release (semantic-release.yml)
description: "The release workflow: it previews each pull request, and on `main` it promotes `.linkml/CHANGELOG.md`, tags the commit, publishes the release and dispatches the knowledge release."
resource: .github/workflows/semantic-release.yml
sources:
  - id: semantic-release.yml
    resource: .github/workflows/semantic-release.yml
  - resource: .releaserc.json
generated:
  by: process:ktl-librarian
  at: "2026-11-05T21:48:14Z"
  revision: cde50310ebeec25edc8ec55b83e4402e9f6b2ac4
status: draft
---

# Semantic release (semantic-release.yml)

A merge of FINOS's main brings FINOS's commits into the range this job reads, and some carry a `feat` or `fix` type.[^semantic-release.yml] The tags FINOS writes, `v1` and `v2`, are not versions this job reads.[^semantic-release.yml]

[^semantic-release.yml]: .github/workflows/semantic-release.yml
