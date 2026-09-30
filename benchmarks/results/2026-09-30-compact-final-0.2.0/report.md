# Final compact-context 0.2.0 validation

Frozen product: `90ed9a4a049af519a40c36424ed1ff8b6acefe48`. `gpt-5.6-terra`, low reasoning, one run per condition per task.

Preliminary validation for the tested configuration only; no statistical-confidence or universal token-savings claim.

| Task | Vanilla total | ContextLean total | Difference | V time | C time | Commands (V/C) | Success |
|---|---:|---:|---:|---:|---:|---:|---|
| navigation | 65,119 | 28,236 | -56.64% | 16.01s | 15.41s | 3/1 | Both pass |
| bug-fix | 87,323 | 74,680 | -14.48% | 33.85s | 28.10s | 3/3 | Both pass |
| feature | 93,977 | 93,484 | -0.52% | 47.17s | 50.34s | 3/4 | Both pass |
| refactor | 84,972 | 104,772 | +23.30% | 30.21s | 32.26s | 3/5 | Both pass |
| documentation-config | 103,502 | 60,478 | -41.57% | 40.56s | 31.68s | 3/5 | Both pass |

| Aggregate | Vanilla | ContextLean | Difference |
|---|---:|---:|---:|
| input_tokens | 428,936.00 | 356,321.00 | -16.93% |
| cached_input_tokens | 319,744.00 | 266,240.00 | -16.73% |
| output_tokens | 5,957.00 | 5,329.00 | -10.54% |
| total_tokens | 434,893.00 | 361,650.00 | -16.84% |
| duration_seconds | 167.80 | 157.79 | -5.97% |
| command_calls | 15.00 | 18.00 | +20.00% |

Success: vanilla 5/5, contextlean 5/5.

## Unfavorable task results

- **feature**: duration_seconds +3.17 (+6.72%); command_calls +1.00 (+33.33%).
- **refactor**: total_tokens +19800.00 (+23.30%); duration_seconds +2.05 (+6.77%); command_calls +2.00 (+66.67%).
- **documentation-config**: command_calls +2.00 (+66.67%).

## Separate comparison with the previous clean-final batch

Previous ContextLean vs Vanilla: tokens +9.86%, time +17.67%.
Compact ContextLean vs Vanilla: tokens -16.84%, time -5.97%.
ContextLean old to compact: tokens -14.59%, time -6.96%, commands +20.00%.
Datasets are not pooled. These observations do not establish causality or statistical confidence.

## Dated credit-equivalents

Eight new calls: 12.47162. Existing Bug Fix pair: 3.80775. Complete compact batch: 16.27937.
ChatGPT standard-speed card dated 2026-09-30: uncached input 50, cached input 5, output 300 credit-equivalents per million tokens. Cached input is a subset of input; reasoning is a subset of output. Actual credits spent are unavailable.

[Measurement review](measurement-review.json) · [methodology](methodology.md) · [all raw numeric records](summary.json) · [offline regrading](offline-regrade) · [previous comparison](comparison.json).
