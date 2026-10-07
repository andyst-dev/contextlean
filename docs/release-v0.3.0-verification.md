# ContextLean v0.3.0 release verification

Release scope: Balanced validation evidence, immutable historical-study publication,
public documentation, version metadata and deterministic release records. No product
behavior, adapter logic, harness schema or historical measured results changed.
No model sessions were run during preparation.

## Deterministic checks

- Full offline suite: **135 tests passed**, 0 failures (79.330 seconds), including
  historical evidence fingerprints, package contracts, native sandbox probes and
  relative public-document links. Mock-provider test sessions are offline fixtures.
- Whitespace: staged checks pass with a narrow `.gitattributes` exception for
  frozen solution diffs and the historical command transcript. Their 196 original
  whitespace lines (including unified-diff context markers) remain intact; source
  and other documentation keep normal whitespace checks.
- Ruff 0.15.7: lint and formatting pass (24 source/test files).
- Codex plugin ingestion validator and all four packaged Skill validators: pass.
- Claude plugin and marketplace validators: pass with the existing warnings that
  root CLAUDE.md is not injected as project context and Claude ignores the catalog
  `policy` field. Neither warning is a newly introduced failure.
- Evidence reconciliation: eight checksum ledgers and 2,719 entries verified.
  All 1,393 pre-existing 30-session study files and 655 previously tracked historical
  files/reference remain byte-identical. The frozen historical aggregate checks also
  pass in the suite. The restored companion document is recorded separately in the
  [evidence guide](evidence.md).
- Public hygiene: 1,602 evidence files reviewed; no private directory, personal
  absolute path or credential pattern found. Balanced host installation paths are
  normalized; generic system paths and immutable historical tool paths retain their
  documented meaning.
- The six published Balanced-validation solutions were regraded offline at release:
  **6/6 pass** submitted, original regression and independent acceptance tests.
  Recorded usage, summary/statistics and trace usage reconcile without changed numbers.
- Fresh deterministic representative bootstrap: AGENTS.md **4,741 bytes** plus
  CLAUDE.md **11 bytes** = **4,752 bytes**, matching the tested Balanced hashes exactly.
  Previous automatic context was **5,486 bytes**: reduction **734 bytes / 13.38%**.
  This fixture scaffolding does not claim a fresh model-driven bootstrap trial.

[Machine-readable checks](release-v0.3.0-checks.json) record the preparation results.
The comparison adapter and execution/trace/runtime/grader files remain unchanged;
the measurement helper changes only its ContextLean version metadata. Reproducing
the earlier comparison uses its exact frozen adapter revision, as described in the
[adapter documentation](history/product-comparison-adapter.md).

## Publication gate

The preparation commit must pass the existing Quality CI on Python 3.11 and 3.14
before tagging v0.3.0. GitHub Actions associates the authoritative CI receipt with
that immutable commit; the release points to the same commit. No benchmark is part
of this gate. The [release](https://github.com/andyst-dev/contextlean/releases/tag/v0.3.0)
and [Quality CI](https://github.com/andyst-dev/contextlean/actions/workflows/quality.yml)
provide the resulting publication status.
