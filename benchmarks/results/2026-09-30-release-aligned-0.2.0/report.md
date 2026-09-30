# Release-aligned v0.2.0 validation

Frozen product: `86043499d5a375cc6a3b295bc7c03b0999eb458c`. `gpt-5.6-terra`, low reasoning.
One fresh run per condition per task: exactly ten new calls. Preliminary validation, no statistical-confidence or universal token-savings claim.

| Task | Vanilla total | ContextLean total | Difference | V time | C time | Commands V/C | Success |
|---|---:|---:|---:|---:|---:|---:|---|
| navigation | 55,054 | 50,553 | -8.18% | 17.88s | 15.29s | 3/3 | Both pass |
| bug-fix | 88,459 | 78,423 | -11.35% | 29.18s | 28.50s | 3/5 | Both pass |
| feature | 94,876 | 77,823 | -17.97% | 60.41s | 39.68s | 3/3 | Both pass |
| refactor | 99,049 | 75,257 | -24.02% | 37.17s | 28.18s | 5/3 | Both pass |
| documentation-config | 144,586 | 59,620 | -58.77% | 45.33s | 22.88s | 4/2 | Both pass |

| Aggregate | Vanilla | ContextLean | Difference |
|---|---:|---:|---:|
| input_tokens | 475,198 | 337,007 | -29.08% |
| cached_input_tokens | 369,920 | 257,280 | -30.45% |
| output_tokens | 6,826 | 4,669 | -31.60% |
| total_tokens | 482,024 | 341,676 | -29.12% |
| duration_seconds | 189.97 | 134.52 | -29.19% |
| command_calls | 18 | 16 | -11.11% |
| Acceptance / original regression / submitted-test success | 5/5 each | 5/5 each | Same |

## Unfavorable results

- **navigation**: dated credit-equivalent +59.93%.
- **bug-fix**: output_tokens +3.35%; command_calls +66.67%.

## Credit-equivalents

Vanilla: 9.16130; ContextLean: 6.67345; all ten calls: 15.83475.
Dated standard-speed ChatGPT card (2026-09-30): uncached input 50, cached input 5, output 300 credit-equivalents per million tokens. Cached input is included in input; reasoning tokens are included in output. Actual credits charged are unavailable. Cache composition can reverse token-versus-credit comparisons.

## Behavior and limitations

Refactor trace interpretation is recorded in behavior-review.md; raw commands and patch events remain in trace-review.json. All unfavorable observations are retained. Datasets are separate; no result is reused or pooled. One batch cannot establish causality, statistical confidence or universal savings.

[Summary and every run](summary.json) · [measurement review](measurement-review.json) · [methodology](methodology.md) · [behavior review](behavior-review.md) · [raw traces](raw) · [offline grading](offline-regrade) · [checksums](checksums.json).
