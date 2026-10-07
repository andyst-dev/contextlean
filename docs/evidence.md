# Evidence provenance

ContextLean v0.3.0 uses the Balanced contract. Product-change validation and historical
performance studies answer different questions; they must not be pooled.

## Current release: v0.3.0 Balanced

[Balanced product-change validation](../benchmarks/results/2026-10-06-balanced-product-change/README.md)
compares Old `ae8653b123bdb4c686ee36825c80db851c8595ea` with Balanced
`1a6e67fb9e5c3d5a91ca89a9f5466d2fa037ea52`: six Refactor sessions, all six fully
graded solutions passing, with no material retained-contract regression observed.
This is behavioral validation, not general performance evidence or proof of
complex-refactor equivalence. The [release verification](release-v0.3.0-verification.md)
records deterministic release checks.

The comparison adapter is completed historical tooling. Reproduction uses frozen
adapter commit `43972cb610755dde7a2866595a8e1f34f2b2d907` and matching inputs;
see its [dated record](history/product-comparison-adapter.md). It is no longer
maintained as an active runner extension. Published source and outcomes remain unchanged.

## Historical performance and investigations

- [v0.2.1 performance study](../benchmarks/results/2026-10-02-harness-v4-repeated-performance/README.md):
  30 harness-v4 sessions at `ae8653b123bdb4c686ee36825c80db851c8595ea`, descriptive
  aggregate **8.96% fewer tokens**, with mixed task-level outcomes. This is not a
  v0.3.0 performance result.
- [Earlier evidence index](../benchmarks/results/README.md): frozen earlier products,
  preliminary release studies and diagnostic datasets; their original caveats apply.
- [Preparation root-cause investigation](../benchmarks/analysis/2026-09-30-final-0.2.0/README.md)
  explains the invalid diagnostic batch. Its evidence-linked location is preserved.
- [Historical/design records](history/README.md) include bootstrap migration,
  implementation verification and the harness sandbox diagnosis.

Neither three-pair study supports statistical-significance claims. Cache state,
service load and stochastic behavior limit performance interpretation. No model
sessions were run for the v0.3.0 release preparation.

## Publication integrity

The 30-session archive was already complete locally before this release and is now
included unchanged. All 1,393 pre-existing files retain their hashes, including its
original checksum ledgers. Its methodology referenced a missing companion file;
`sandbox-composition.md` was added verbatim from the study's frozen revision to
resolve that link. This is an additive documentation repair, not a changed result.
The companion's SHA-256 is
`3ad9448e2b486f9f3074f6efdb6ea4e8e883ee53f63fe69d397ecae95c5d2fb6`;
it is outside the original checksum ledger. Generic system/tool installation paths
in the immutable historical receipts are retained; private user paths are absent.

Balanced publication preserves reports, statistics, exposed traces, receipts,
solutions, grading and provenance hashes. Host-specific tool installation prefixes
are replaced with role placeholders; user/session roots were already normalized.
Its publication record retains the pre-sanitization checksum ledgers and per-file
before/after hashes. Updated export checksums cover the sanitized files. Recorded
runtime/source digests continue to identify the measured originals, not sanitized
re-executions. Private byte-exact originals remain local and are not committed.
