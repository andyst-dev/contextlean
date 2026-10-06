# Repeated study methodology

Harness v4 at ae8653b123bdb4c686ee36825c80db851c8595ea; CI Quality run 37000975923 green on Python 3.11 and 3.14 before execution. No ContextLean or harness edits.

Five task-specific suites use the unchanged runner's supported --tasks-file option and preserve each canonical task object and exact wrapped prompt bytes. This gives the explicitly requested V→C, C→V, V→C order for every task without changing the harness's task-index schedule behavior. The complete global schedule was frozen before execution. Each suite's local sequence is mapped to global sequence by 6 × task index + local sequence. No reordering or session retries.

All thirty offline preparation slots were gated before the first model call. Live execution repeats all six preparation gates per suite and every actual session repeats its own v4 preflight. Native permission/runtime receipts and before/after Git/artifact inspection are exported. Cleanup covers the entire session root; the harness verifies absent roots and prior scratch absence, and orchestration checks roots between suites. The same model, high reasoning and 600-second session timeout apply throughout. Infrastructure/provider/quota interruptions stop the study; task failures are retained.

Independent offline regrading uses a disposable copy of each saved original solution. It runs submitted tests, restores and runs canonical original regression tests, then runs the unchanged acceptance evaluator. Saved originals are hash-checked before/after grading. Tests remain offline, and no model sessions are launched by analysis.

Usage is the exposed top-level provider turn aggregate. Cached input is a subset of input; total tokens = input + output. Unknown metrics remain null. Wall time covers the measured provider CLI execution, excluding preparation and grading. Raw provider stdout/stderr sizes use original private bytes. Tool output sizes use original exposed UTF-8 strings. Codex merged output has no fabricated stdout/stderr split. Command distribution counts shell tool calls rather than individual subcommands. Coverage parser v2 retains exact exposed test names and complete-list digests; compact output does not invent identities.

Within each task/repetition, paired difference is ContextLean minus Vanilla; paired percentage divides by Vanilla. Sample standard deviation uses n−1. Approximately neutral means absolute paired percentage difference ≤1%, specified before results. All six observations per task and all fifteen pairs are retained. Task heterogeneity is visible; overall summaries are descriptive. No significance claim is made from n=3. Provider cache/service state and model trajectories are uncontrolled.

Local private originals are excluded from public evidence. Public checksums cover sanitized exports. Existing result sets and the project README are unchanged. See harness-methodology-v4.md for unchanged v4 policy and limitations.
