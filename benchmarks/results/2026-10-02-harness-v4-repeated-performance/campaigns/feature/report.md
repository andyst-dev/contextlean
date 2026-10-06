# ContextLean benchmark validation batch

Harness v4 · performance. No statistical significance claim.

Model: `gpt-5.6-sol` · reasoning: `high` · repeats: 3
Completed runs: 6/6

| Task | Condition | Task success | Regression tests | Input | Cached | Output | Total | Commands | Seconds |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| feature | vanilla | pass | pass | 96787 | 83200 | 2335 | 99122 | 5 | 91.53 |
| feature | contextlean | pass | pass | 84107 | 66688 | 2159 | 86266 | 4 | 95.67 |
| feature | contextlean | pass | pass | 104494 | 93824 | 3124 | 107618 | 4 | 78.32 |
| feature | vanilla | pass | pass | 96907 | 78976 | 2801 | 99708 | 5 | 72.93 |
| feature | vanilla | pass | pass | 80641 | 67584 | 2228 | 82869 | 4 | 56.91 |
| feature | contextlean | pass | pass | 68221 | 36736 | 2320 | 70541 | 5 | 60.02 |

All observations retained; no statistical significance or universal gain claim.

## Per-task medians and ranges

Every run is retained, including incorrect solutions and failed executions.

| Task | Condition | Successes / runs | Total tokens median [min, max] | Seconds median [min, max] |
|---|---|---:|---:|---:|
| feature | vanilla | 3/3 | 99122.00 [82869.00, 99708.00] | 72.93 [56.91, 91.53] |
| feature | contextlean | 3/3 | 86266.00 [70541.00, 107618.00] | 78.32 [60.02, 95.67] |

All exposed tool attempts, coverage identities and output sizes are in execution.json; hidden actions remain unavailable.
Command calls count unique Bash/command_execution attempts, including denials. No inferred file counts are presented.
Cached input is a subset of input. Total is input + output. Missing reasoning-token fields remain null.
One repetition cannot establish variance or statistical confidence.

## Token statistics

| Task | Condition | Mean | Sample SD | Range |
|---|---|---:|---:|---:|
| feature | vanilla | 93899.67 | 9557.33 | 16839 |
| feature | contextlean | 88141.67 | 18609.53 | 37077 |

Paired differences (ContextLean minus Vanilla):

- feature: observations [-12856, 7910, -12328]; mean -5758.00; median -12328.00; range 20766; sample SD 11839.77888307041