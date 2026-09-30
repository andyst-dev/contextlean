# ContextLean benchmark validation batch

Validation only. Not a published performance benchmark.

Model: `gpt-5.6-terra` · reasoning: `low` · repeats: 1
Completed runs: 10/10

| Task | Condition | Task success | Regression tests | Input | Cached | Output | Total | Commands | Seconds |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| navigation | vanilla | pass | pass | 47525 | 14080 | 316 | 47841 | 2 | 15.13 |
| navigation | contextlean | pass | pass | 43006 | 27136 | 332 | 43338 | 2 | 14.52 |
| bug-fix | contextlean | pass | pass | 60260 | 42240 | 968 | 61228 | 4 | 29.89 |
| bug-fix | vanilla | pass | pass | 69935 | 63232 | 883 | 70818 | 3 | 32.28 |
| feature | vanilla | pass | pass | 74057 | 54272 | 1579 | 75636 | 3 | 48.57 |
| feature | contextlean | pass | pass | 130612 | 107008 | 2918 | 133530 | 4 | 74.95 |
| refactor | contextlean | pass | pass | 106944 | 95488 | 1652 | 108596 | 4 | 44.63 |
| refactor | vanilla | pass | pass | 98960 | 91648 | 1097 | 100057 | 4 | 34.07 |
| documentation-config | vanilla | pass | pass | 87818 | 76288 | 1076 | 88894 | 4 | 35.73 |
| documentation-config | contextlean | pass | pass | 122494 | 111616 | 1173 | 123667 | 5 | 36.41 |

All tasks passed; this validation batch is eligible for measurement review, not a performance claim.

## Per-task medians and ranges

Every run is retained, including incorrect solutions and failed executions.

| Task | Condition | Successes / runs | Total tokens median [min, max] | Seconds median [min, max] |
|---|---|---:|---:|---:|
| navigation | vanilla | 1/1 | 47841.00 [47841.00, 47841.00] | 15.13 [15.13, 15.13] |
| navigation | contextlean | 1/1 | 43338.00 [43338.00, 43338.00] | 14.52 [14.52, 14.52] |
| bug-fix | vanilla | 1/1 | 70818.00 [70818.00, 70818.00] | 32.28 [32.28, 32.28] |
| bug-fix | contextlean | 1/1 | 61228.00 [61228.00, 61228.00] | 29.89 [29.89, 29.89] |
| feature | vanilla | 1/1 | 75636.00 [75636.00, 75636.00] | 48.57 [48.57, 48.57] |
| feature | contextlean | 1/1 | 133530.00 [133530.00, 133530.00] | 74.95 [74.95, 74.95] |
| refactor | vanilla | 1/1 | 100057.00 [100057.00, 100057.00] | 34.07 [34.07, 34.07] |
| refactor | contextlean | 1/1 | 108596.00 [108596.00, 108596.00] | 44.63 [44.63, 44.63] |
| documentation-config | vanilla | 1/1 | 88894.00 [88894.00, 88894.00] | 35.73 [35.73, 35.73] |
| documentation-config | contextlean | 1/1 | 123667.00 [123667.00, 123667.00] | 36.41 [36.41, 36.41] |

File reads, unique files inspected and total tool calls: unavailable from the current CLI event contract.
Command calls are unique command_execution events, not all tool calls. No inferred file counts are presented.
Cached input is a subset of input. Total is input + output. Missing reasoning-token fields remain null.
One repetition cannot establish variance or statistical confidence.
