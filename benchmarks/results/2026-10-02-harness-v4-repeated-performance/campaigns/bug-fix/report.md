# ContextLean benchmark validation batch

Harness v4 · performance. No statistical significance claim.

Model: `gpt-5.6-sol` · reasoning: `high` · repeats: 3
Completed runs: 6/6

| Task | Condition | Task success | Regression tests | Input | Cached | Output | Total | Commands | Seconds |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| bug-fix | vanilla | pass | pass | 76997 | 64896 | 1214 | 78211 | 4 | 64.88 |
| bug-fix | contextlean | pass | pass | 78982 | 67328 | 1385 | 80367 | 5 | 45.99 |
| bug-fix | contextlean | pass | pass | 80106 | 72832 | 1124 | 81230 | 4 | 63.56 |
| bug-fix | vanilla | pass | pass | 62516 | 56320 | 1072 | 63588 | 3 | 63.96 |
| bug-fix | vanilla | pass | pass | 90982 | 75520 | 1553 | 92535 | 6 | 47.61 |
| bug-fix | contextlean | pass | pass | 79110 | 71936 | 1305 | 80415 | 5 | 49.16 |

All observations retained; no statistical significance or universal gain claim.

## Per-task medians and ranges

Every run is retained, including incorrect solutions and failed executions.

| Task | Condition | Successes / runs | Total tokens median [min, max] | Seconds median [min, max] |
|---|---|---:|---:|---:|
| bug-fix | vanilla | 3/3 | 78211.00 [63588.00, 92535.00] | 63.96 [47.61, 64.88] |
| bug-fix | contextlean | 3/3 | 80415.00 [80367.00, 81230.00] | 49.16 [45.99, 63.56] |

All exposed tool attempts, coverage identities and output sizes are in execution.json; hidden actions remain unavailable.
Command calls count unique Bash/command_execution attempts, including denials. No inferred file counts are presented.
Cached input is a subset of input. Total is input + output. Missing reasoning-token fields remain null.
One repetition cannot establish variance or statistical confidence.

## Token statistics

| Task | Condition | Mean | Sample SD | Range |
|---|---|---:|---:|---:|
| bug-fix | vanilla | 78111.33 | 14473.76 | 28947 |
| bug-fix | contextlean | 80670.67 | 484.99 | 863 |

Paired differences (ContextLean minus Vanilla):

- bug-fix: observations [2156, 17642, -12120]; mean 2559.33; median 2156.00; range 29762; sample SD 14885.098902369891