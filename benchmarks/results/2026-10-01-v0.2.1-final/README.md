# Final ContextLean v0.2.1 evidence campaign

Public release/tag `v0.2.1`, commit `44ee6f227dfead62406326a1306f897358f1778f`. Product unchanged. Exactly 18 fresh sessions; no reused or extra runs. All saved solutions pass submitted tests, original regressions and acceptance, independently regraded offline. Execution success is 17/18: Terra Vanilla Documentation/config failed at the provider usage limit before turn completion/usage. No retry. Main headline aggregate unavailable; README stays unchanged.

Preliminary validation: one observation per condition per task, tested configurations only. Provider caching/service conditions and stochastic behavior uncontrolled. No statistical confidence or universal token-savings claim. Never pool models or historical batches.

## Main — GPT-5.6 Terra / low (five tasks)

The full five-task token aggregate is unavailable. Vanilla has only four reported usage records; its known subtotal is 266,647 total tokens (263,147 input, 208,640 cached, 3,500 output). ContextLean has five. These unequal subtotals must not be compared as a headline. Time/commands include the failed attempt and likewise support no valid full-batch performance comparison. Higher cached-token counts alone do not imply higher cost; the negative cases below retain all raw increases without such an inference.

| Task | Vanilla tokens | ContextLean tokens | Difference | V time | C time | Commands V/C | Success |
|---|---:|---:|---:|---:|---:|---:|---|
| navigation | 39,813 | 42,994 | +7.99% | 15.27s | 13.32s | 2/3 | Both pass |
| bug-fix | 70,850 | 74,587 | +5.27% | 26.09s | 26.92s | 3/3 | Both pass |
| feature | 86,671 | 76,887 | -11.29% | 38.35s | 35.01s | 4/3 | Both pass |
| refactor | 69,313 | 72,744 | +4.95% | 27.31s | 20.46s | 3/3 | Both pass |
| documentation-config | unavailable | 57,096 | unavailable | 29.17s | 19.47s | 3/2 | V execution failed; C pass |

| Aggregate | Vanilla | ContextLean | Difference |
|---|---:|---:|---:|
| input_tokens | unavailable | 320,597 | unavailable |
| cached_input_tokens | unavailable | 242,176 | unavailable |
| uncached_input_tokens | unavailable | 78,421 | unavailable |
| output_tokens | unavailable | 3,711 | unavailable |
| total_tokens | unavailable | 324,308 | unavailable |
| duration_seconds | 136.19 | 115.18 | No valid full-batch comparison |
| command_calls | 15 | 14 | No valid full-batch comparison |
| Submitted / original regression / acceptance | 5/5 each | 5/5 each | Same |
| Execution/task success | 4/5 | 5/5 | Failed Vanilla session retained |

### Higher ContextLean measurements

- navigation: input_tokens 39,526.00 → 42,625.00 (+7.84%).
- navigation: cached_input_tokens 25,088.00 → 27,136.00 (+8.16%).
- navigation: uncached_input_tokens 14,438.00 → 15,489.00 (+7.28%).
- navigation: output_tokens 287.00 → 369.00 (+28.57%).
- navigation: total_tokens 39,813.00 → 42,994.00 (+7.99%).
- navigation: command_calls 2.00 → 3.00 (+50.00%).
- bug-fix: input_tokens 70,029.00 → 73,760.00 (+5.33%).
- bug-fix: cached_input_tokens 60,160.00 → 64,256.00 (+6.81%).
- bug-fix: output_tokens 821.00 → 827.00 (+0.73%).
- bug-fix: total_tokens 70,850.00 → 74,587.00 (+5.27%).
- bug-fix: duration_seconds 26.09 → 26.92 (+3.19%).
- refactor: input_tokens 68,463.00 → 72,114.00 (+5.33%).
- refactor: uncached_input_tokens 7,279.00 → 17,842.00 (+145.12%).
- refactor: total_tokens 69,313.00 → 72,744.00 (+4.95%).

## Claude Opus — opus[1m] / high (two tasks)

| Task | Vanilla tokens | ContextLean tokens | Difference | V time | C time | Commands V/C | Success |
|---|---:|---:|---:|---:|---:|---:|---|
| bug-fix | 113,513 | 72,981 | -35.71% | 50.26s | 33.39s | 6/2 | Both pass |
| refactor | 100,027 | 227,415 | +127.35% | 52.89s | 79.73s | 4/9 | Both pass |

| Aggregate | Vanilla | ContextLean | Difference |
|---|---:|---:|---:|
| input_tokens | 207,085 | 293,020 | +41.50% |
| cached_input_tokens | 189,283 | 266,204 | +40.64% |
| uncached_input_tokens | 17,802 | 26,816 | +50.63% |
| output_tokens | 6,455 | 7,376 | +14.27% |
| total_tokens | 213,540 | 300,396 | +40.67% |
| duration_seconds | 103.15 | 113.12 | +9.67% |
| command_calls | 10 | 11 | +10.00% |
| Submitted / original regression / acceptance | 2/2 each | 2/2 each | Same |

### Higher ContextLean measurements

- bug-fix: uncached_input_tokens 8,977.00 → 13,511.00 (+50.51%).
- refactor: input_tokens 97,079.00 → 222,374.00 (+129.06%).
- refactor: cached_input_tokens 88,254.00 → 209,069.00 (+136.89%).
- refactor: uncached_input_tokens 8,825.00 → 13,305.00 (+50.76%).
- refactor: output_tokens 2,948.00 → 5,041.00 (+71.00%).
- refactor: total_tokens 100,027.00 → 227,415.00 (+127.35%).
- refactor: duration_seconds 52.89 → 79.73 (+50.75%).
- refactor: command_calls 4.00 → 9.00 (+125.00%).

## GPT-5.6 Sol / high (two tasks)

| Task | Vanilla tokens | ContextLean tokens | Difference | V time | C time | Commands V/C | Success |
|---|---:|---:|---:|---:|---:|---:|---|
| bug-fix | 89,223 | 91,892 | +2.99% | 34.52s | 32.04s | 4/4 | Both pass |
| refactor | 85,718 | 108,817 | +26.95% | 33.73s | 45.65s | 4/5 | Both pass |

| Aggregate | Vanilla | ContextLean | Difference |
|---|---:|---:|---:|
| input_tokens | 172,672 | 197,792 | +14.55% |
| cached_input_tokens | 126,720 | 174,464 | +37.68% |
| uncached_input_tokens | 45,952 | 23,328 | -49.23% |
| output_tokens | 2,269 | 2,917 | +28.56% |
| total_tokens | 174,941 | 200,709 | +14.73% |
| duration_seconds | 68.25 | 77.69 | +13.84% |
| command_calls | 8 | 9 | +12.50% |
| Submitted / original regression / acceptance | 2/2 each | 2/2 each | Same |

### Higher ContextLean measurements

- bug-fix: input_tokens 88,171.00 → 90,770.00 (+2.95%).
- bug-fix: cached_input_tokens 71,296.00 → 77,184.00 (+8.26%).
- bug-fix: output_tokens 1,052.00 → 1,122.00 (+6.65%).
- bug-fix: total_tokens 89,223.00 → 91,892.00 (+2.99%).
- refactor: input_tokens 84,501.00 → 107,022.00 (+26.65%).
- refactor: cached_input_tokens 55,424.00 → 97,280.00 (+75.52%).
- refactor: output_tokens 1,217.00 → 1,795.00 (+47.49%).
- refactor: total_tokens 85,718.00 → 108,817.00 (+26.95%).
- refactor: duration_seconds 33.73 → 45.65 (+35.34%).
- refactor: command_calls 4.00 → 5.00 (+25.00%).

## Historical v0.2.0 comparison

All older folders remain byte-identical, separate historical observations. Different model runs, stochastic behavior, uncontrolled cache/service conditions and the new Git-backed environment prevent causal attribution or statistical confidence. The interrupted v0.2.1 main batch supplies no full five-task comparison.

| Dataset | Vanilla tokens | ContextLean tokens | Status |
|---|---:|---:|---|
| 2026-09-30-validation | 403,372 | 355,307 | historical, separate |
| 2026-09-30-final-0.2.0 | 383,246 | 470,359 | INVALID diagnostic preparation |
| 2026-09-30-clean-final-0.2.0 | 385,429 | 423,415 | historical, separate |
| 2026-09-30-compact-final-0.2.0 | 434,893 | 361,650 | historical, separate |
| 2026-09-30-release-aligned-0.2.0 | 482,024 | 341,676 | historical, separate |
| Current v0.2.1 main | unavailable | 324,308 | Incomplete Vanilla usage; no headline aggregate |

Against the release-aligned historical batch, observed Terra token differences per complete pair move from −8.18% to +7.99% (Navigation), −11.35% to +5.27% (Bug Fix), −17.97% to −11.29% (Feature), and −24.02% to +4.95% (Refactor). Documentation/config cannot be compared. These are descriptive independent observations, not evidence that a particular rule caused a change.

## Reproduction and evidence

[Machine-readable summary](summary.json) · [methodology](methodology.md) · [preparation](preparation.json) · [frozen Git fixtures](preparation.zip) · [measurement review](measurement-review.json) · [verification behavior](verification-review.md) · [all raw artifacts](raw/) · [offline grading logs](offline-regrade/) · [solutions](solutions.zip) · [frozen public source](source-snapshot.zip) · [source hashes](source-hashes.json) · [checksums](checksums.json) · [offline checker](verify_evidence.py).

[Historical comparison](historical-comparison.json) retains previous datasets separately. The invalid diagnostic batch remains invalid. The new Git-backed environment and uncontrolled runs prevent attributing differences causally to v0.2.1.

## Quality and disposition

See [quality checks](quality.json). Product unchanged, historic evidence unchanged, root README unchanged. Main headline gate did **not** pass because session 9 failed; the cross-model pairs are valid preliminary compatibility observations, with explicit regressions. No additional runs authorized or launched.

## Cost

Dated [official credit rates](https://learn.chatgpt.com/docs/pricing), verified 2026-10-01: Terra input/cache/output 50/5/300 credits per million; Sol 100/10/500. ChatGPT authentication was verified locally. These are credit-equivalents, not observed subscription deductions.

Terra: 11.06378 credits equivalent for nine usage-reported Terra sessions; tenth usage unavailable. Sol: 12.53284 for four. Known OpenAI usage subtotal only (not a complete campaign cost): 23.59662 equivalent credits. Claude's four sessions report $1.022118 USD equivalent; actual billing/credits spent unavailable. No cross-provider token/performance aggregate or currency conversion.
