# ContextLean benchmark validation batch

Harness v4 · performance. No statistical significance claim.

Model: `gpt-5.6-sol` · reasoning: `high` · repeats: 3
Completed runs: 6/6

| Task | Condition | Task success | Regression tests | Input | Cached | Output | Total | Commands | Seconds |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| refactor | vanilla | pass | pass | 91239 | 79360 | 1951 | 93190 | 5 | 88.59 |
| refactor | contextlean | pass | pass | 80074 | 72448 | 1578 | 81652 | 5 | 76.29 |
| refactor | contextlean | pass | pass | 81323 | 73472 | 1802 | 83125 | 4 | 80.20 |
| refactor | vanilla | pass | pass | 81760 | 73856 | 1544 | 83304 | 4 | 85.62 |
| refactor | vanilla | pass | pass | 91609 | 78336 | 1508 | 93117 | 5 | 51.72 |
| refactor | contextlean | pass | pass | 65800 | 58624 | 1457 | 67257 | 3 | 54.13 |

All observations retained; no statistical significance or universal gain claim.

## Per-task medians and ranges

Every run is retained, including incorrect solutions and failed executions.

| Task | Condition | Successes / runs | Total tokens median [min, max] | Seconds median [min, max] |
|---|---|---:|---:|---:|
| refactor | vanilla | 3/3 | 93117.00 [83304.00, 93190.00] | 85.62 [51.72, 88.59] |
| refactor | contextlean | 3/3 | 81652.00 [67257.00, 83125.00] | 76.29 [54.13, 80.20] |

All exposed tool attempts, coverage identities and output sizes are in execution.json; hidden actions remain unavailable.
Command calls count unique Bash/command_execution attempts, including denials. No inferred file counts are presented.
Cached input is a subset of input. Total is input + output. Missing reasoning-token fields remain null.
One repetition cannot establish variance or statistical confidence.

## Token statistics

| Task | Condition | Mean | Sample SD | Range |
|---|---|---:|---:|---:|
| refactor | vanilla | 89870.33 | 5686.73 | 9886 |
| refactor | contextlean | 77344.67 | 8767.17 | 15868 |

Paired differences (ContextLean minus Vanilla):

- refactor: observations [-11538, -179, -25860]; mean -12525.67; median -11538.00; range 25681; sample SD 12868.957002544275