# ContextLean benchmark validation batch

Harness v4 · performance. No statistical significance claim.

Model: `gpt-5.6-sol` · reasoning: `high` · repeats: 3
Completed runs: 6/6

| Task | Condition | Task success | Regression tests | Input | Cached | Output | Total | Commands | Seconds |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| documentation-config | vanilla | pass | pass | 77296 | 54656 | 1291 | 78587 | 6 | 48.32 |
| documentation-config | contextlean | pass | pass | 80261 | 67328 | 1594 | 81855 | 6 | 58.84 |
| documentation-config | contextlean | pass | pass | 79692 | 55040 | 1268 | 80960 | 6 | 48.61 |
| documentation-config | vanilla | pass | pass | 61993 | 51840 | 1025 | 63018 | 3 | 40.21 |
| documentation-config | vanilla | pass | pass | 90332 | 62592 | 1418 | 91750 | 7 | 60.39 |
| documentation-config | contextlean | pass | pass | 67031 | 53888 | 1410 | 68441 | 7 | 48.54 |

All observations retained; no statistical significance or universal gain claim.

## Per-task medians and ranges

Every run is retained, including incorrect solutions and failed executions.

| Task | Condition | Successes / runs | Total tokens median [min, max] | Seconds median [min, max] |
|---|---|---:|---:|---:|
| documentation-config | vanilla | 3/3 | 78587.00 [63018.00, 91750.00] | 48.32 [40.21, 60.39] |
| documentation-config | contextlean | 3/3 | 80960.00 [68441.00, 81855.00] | 48.61 [48.54, 58.84] |

All exposed tool attempts, coverage identities and output sizes are in execution.json; hidden actions remain unavailable.
Command calls count unique Bash/command_execution attempts, including denials. No inferred file counts are presented.
Cached input is a subset of input. Total is input + output. Missing reasoning-token fields remain null.
One repetition cannot establish variance or statistical confidence.

## Token statistics

| Task | Condition | Mean | Sample SD | Range |
|---|---|---:|---:|---:|
| documentation-config | vanilla | 77785.00 | 14382.78 | 28732 |
| documentation-config | contextlean | 77085.33 | 7499.58 | 13414 |

Paired differences (ContextLean minus Vanilla):

- documentation-config: observations [3268, 17942, -23309]; mean -699.67; median 3268.00; range 41251; sample SD 20909.759308354875