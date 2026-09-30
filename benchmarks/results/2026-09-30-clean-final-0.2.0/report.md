# ContextLean benchmark validation batch

Validation only. Not a published performance benchmark.

Model: `gpt-5.6-terra` · reasoning: `low` · repeats: 1
Completed runs: 10/10

| Task | Condition | Task success | Regression tests | Input | Cached | Output | Total | Commands | Seconds |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| navigation | vanilla | pass | pass | 47777 | 37120 | 322 | 48099 | 2 | 12.94 |
| navigation | contextlean | pass | pass | 43547 | 27136 | 381 | 43928 | 2 | 19.23 |
| bug-fix | contextlean | pass | pass | 92794 | 73472 | 1232 | 94026 | 3 | 35.67 |
| bug-fix | vanilla | pass | pass | 70058 | 64256 | 963 | 71021 | 3 | 28.86 |
| feature | vanilla | pass | pass | 92956 | 71424 | 1869 | 94825 | 4 | 46.85 |
| feature | contextlean | pass | pass | 96738 | 90624 | 2424 | 99162 | 3 | 54.36 |
| refactor | contextlean | pass | pass | 109630 | 101632 | 1409 | 111039 | 4 | 38.46 |
| refactor | vanilla | pass | pass | 87393 | 68352 | 1073 | 88466 | 4 | 29.83 |
| documentation-config | vanilla | pass | pass | 82137 | 70400 | 881 | 83018 | 3 | 25.65 |
| documentation-config | contextlean | pass | pass | 74548 | 68352 | 712 | 75260 | 3 | 21.88 |

All tasks passed; this validation batch is eligible for measurement review, not a performance claim.

## Per-task medians and ranges

Every run is retained, including incorrect solutions and failed executions.

| Task | Condition | Successes / runs | Total tokens median [min, max] | Seconds median [min, max] |
|---|---|---:|---:|---:|
| navigation | vanilla | 1/1 | 48099.00 [48099.00, 48099.00] | 12.94 [12.94, 12.94] |
| navigation | contextlean | 1/1 | 43928.00 [43928.00, 43928.00] | 19.23 [19.23, 19.23] |
| bug-fix | vanilla | 1/1 | 71021.00 [71021.00, 71021.00] | 28.86 [28.86, 28.86] |
| bug-fix | contextlean | 1/1 | 94026.00 [94026.00, 94026.00] | 35.67 [35.67, 35.67] |
| feature | vanilla | 1/1 | 94825.00 [94825.00, 94825.00] | 46.85 [46.85, 46.85] |
| feature | contextlean | 1/1 | 99162.00 [99162.00, 99162.00] | 54.36 [54.36, 54.36] |
| refactor | vanilla | 1/1 | 88466.00 [88466.00, 88466.00] | 29.83 [29.83, 29.83] |
| refactor | contextlean | 1/1 | 111039.00 [111039.00, 111039.00] | 38.46 [38.46, 38.46] |
| documentation-config | vanilla | 1/1 | 83018.00 [83018.00, 83018.00] | 25.65 [25.65, 25.65] |
| documentation-config | contextlean | 1/1 | 75260.00 [75260.00, 75260.00] | 21.88 [21.88, 21.88] |

File reads, unique files inspected and total tool calls: unavailable from the current CLI event contract.
Command calls are unique command_execution events, not all tool calls. No inferred file counts are presented.
Cached input is a subset of input. Total is input + output. Missing reasoning-token fields remain null.
One repetition cannot establish variance or statistical confidence.
