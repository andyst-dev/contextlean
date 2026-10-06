# Evidence provenance

ContextLean v0.3.0 uses the Balanced contract. Product-change validation and historical
performance studies answer different questions; they must not be pooled.

| Evidence | Product and scope | Interpretation |
|---|---|---|
| [Balanced product-change validation](../benchmarks/results/2026-10-06-balanced-product-change/README.md) | Old `ae8653b123bdb4c686ee36825c80db851c8595ea` versus Balanced `1a6e67fb9e5c3d5a91ca89a9f5466d2fa037ea52`; six Refactor sessions; adapter `43972cb610755dde7a2866595a8e1f34f2b2d907` | Behavioral validation: 6/6 fully graded solutions pass, no material retained-contract regression observed. Not general performance evidence or complex-refactor equivalence. |
| [Historical v0.2.1 performance study](../benchmarks/results/2026-10-02-harness-v4-repeated-performance/README.md) | Previous v0.2.1 contract at `ae8653b123bdb4c686ee36825c80db851c8595ea`; harness v4; 30 sessions | Historical descriptive aggregate −8.96% tokens, mixed task-level behavior. Not a v0.3.0 result. |
| [Earlier evidence index](../benchmarks/results/README.md) | Frozen earlier products, including v0.2.0 and v0.2.1 | Original scope and caveats apply; the frozen index and evidence are unchanged. |

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
