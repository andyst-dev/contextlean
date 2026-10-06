# ContextLean benchmark validation batch

Harness v4 · performance. No statistical significance claim.

Model: `gpt-5.6-sol` · reasoning: `high` · repeats: 3
Completed runs: 6/6

| Task | Condition | Task success | Regression tests | Input | Cached | Output | Total | Commands | Seconds |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| navigation | vanilla | pass | pass | 50361 | 40064 | 549 | 50910 | 3 | 44.57 |
| navigation | contextlean | pass | pass | 24058 | 19584 | 300 | 24358 | 1 | 19.17 |
| navigation | contextlean | pass | pass | 24078 | 0 | 255 | 24333 | 1 | 14.69 |
| navigation | vanilla | pass | pass | 37353 | 23552 | 503 | 37856 | 2 | 32.61 |
| navigation | vanilla | pass | pass | 37395 | 27264 | 478 | 37873 | 2 | 37.00 |
| navigation | contextlean | pass | pass | 24192 | 19584 | 364 | 24556 | 1 | 22.97 |

All observations retained; no statistical significance or universal gain claim.

## Per-task medians and ranges

Every run is retained, including incorrect solutions and failed executions.

| Task | Condition | Successes / runs | Total tokens median [min, max] | Seconds median [min, max] |
|---|---|---:|---:|---:|
| navigation | vanilla | 3/3 | 37873.00 [37856.00, 50910.00] | 37.00 [32.61, 44.57] |
| navigation | contextlean | 3/3 | 24358.00 [24333.00, 24556.00] | 19.17 [14.69, 22.97] |

All exposed tool attempts, coverage identities and output sizes are in execution.json; hidden actions remain unavailable.
Command calls count unique Bash/command_execution attempts, including denials. No inferred file counts are presented.
Cached input is a subset of input. Total is input + output. Missing reasoning-token fields remain null.
One repetition cannot establish variance or statistical confidence.

## Token statistics

| Task | Condition | Mean | Sample SD | Range |
|---|---|---:|---:|---:|
| navigation | vanilla | 42213.00 | 7531.83 | 13054 |
| navigation | contextlean | 24415.67 | 122.17 | 223 |

Paired differences (ContextLean minus Vanilla):

- navigation: observations [-26552, -13523, -13317]; mean -17797.33; median -13523.00; range 13235; sample SD 7582.463342036896