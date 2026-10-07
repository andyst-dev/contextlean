# ContextLean v0.3.1 — Packaging and distribution readiness

This patch release delivers the completed repository cleanup and Codex/Claude Code
distribution work. The product remains dependency-free and skills-only.

- Cleaner active repository structure, with historical documentation separated
  from current installation and developer documentation.
- Completed Old-vs-Balanced comparison tooling removed from active maintenance;
  legacy Bootstrap compatibility machinery retained as historical test support,
  outside the packaged Skill.
- Simpler contributor guidance and clearer installation, update and uninstall flows.
- Native Codex and Claude Code packaging and four-Skill discovery support.
- Deterministic distribution ZIP export from the canonical shared Skills.
- Offline validation of fresh installation, discovery, relocation, updates and
  uninstall safety, including preservation of customized project guidance.
- Listing metadata and a shared icon prepared for separate platform submissions.

Balanced runtime guidance is unchanged. There are no new Skills, no Skill behavior
changes and no benchmark rerun. The optional measurement helper changes only its
reported product version. Published benchmark evidence is unchanged; historical
v0.2.1 performance results are not v0.3.1 performance claims.

Update through the existing native plugin commands in the
[installation guide](https://github.com/andyst-dev/contextlean/blob/v0.3.1/docs/installation.md).
The version bump enables normal updates from 0.3.0 without modifying generated
project guidance. Public-directory submissions are not part of this release.

## Validation and artifact

- 139 offline tests passed, including native Codex/Claude installation lifecycle
  tests; no model sessions were run.
- Plugin/Skill validators, Ruff lint/format, Markdown links/anchors, version and
  package hygiene checks passed. Claude retains the documented catalog-policy warning.
- All 14 historical checksum ledgers (3,363 entries) and eight historical
  fingerprints passed. Published evidence changed files: **zero**.
- All four `SKILL.md` files and Balanced runtime guidance are byte-identical to
  distribution commit `b107a96c679f517e5ef0724fcaa879d8934ab85b`. Representative
  generated guidance remains **4,752 bytes**.

Release asset: `contextlean-0.3.1.zip` — **22 files, 33,470 bytes**.
Its companion `contextlean-0.3.1.sha256` records SHA-256:

```text
28cf9489e9fe7c93d22e7b34a993b3badfb1bdd67767268be2e471483e66eff3
```
