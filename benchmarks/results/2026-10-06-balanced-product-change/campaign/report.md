# ContextLean benchmark validation batch

Harness v4 · product-change-validation. No statistical significance claim.

Model: `gpt-5.6-sol` · reasoning: `high` · repeats: 3
Completed runs: 6/6

| Task | Condition | Task success | Regression tests | Input | Cached | Output | Total | Commands | Seconds |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| refactor | old | pass | pass | 82241 | 66432 | 1561 | 83802 | 4 | 41.48 |
| refactor | balanced | pass | pass | 81767 | 69632 | 1553 | 83320 | 4 | 40.70 |
| refactor | balanced | pass | pass | 99125 | 85888 | 2233 | 101358 | 9 | 56.21 |
| refactor | old | pass | pass | 99146 | 90368 | 2050 | 101196 | 5 | 52.32 |
| refactor | old | pass | pass | 114255 | 105216 | 1961 | 116216 | 6 | 55.00 |
| refactor | balanced | pass | pass | 80848 | 69120 | 1233 | 82081 | 4 | 36.72 |

All observations retained; no statistical significance or universal gain claim.

## Per-task medians and ranges

Every run is retained, including incorrect solutions and failed executions.

| Task | Condition | Successes / runs | Total tokens median [min, max] | Seconds median [min, max] |
|---|---|---:|---:|---:|
| refactor | old | 3/3 | 101196.00 [83802.00, 116216.00] | 52.32 [41.48, 55.00] |
| refactor | balanced | 3/3 | 83320.00 [82081.00, 101358.00] | 40.70 [36.72, 56.21] |

All exposed tool attempts, coverage identities and output sizes are in execution.json; hidden actions remain unavailable.
Command calls count unique Bash/command_execution attempts, including denials. No inferred file counts are presented.
Cached input is a subset of input. Total is input + output. Missing reasoning-token fields remain null.
One repetition cannot establish variance or statistical confidence.

## Token statistics

| Task | Condition | Mean | Sample SD | Range |
|---|---|---:|---:|---:|
| refactor | old | 100404.67 | 16221.48 | 32414 |
| refactor | balanced | 88919.67 | 10789.71 | 19277 |

Paired differences (Balanced minus Old):

- refactor: observations [-482, 162, -34135]; mean -11485.00; median -482.00; range 34297; sample SD 19618.118130952316