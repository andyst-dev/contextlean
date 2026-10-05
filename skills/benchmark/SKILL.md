---
name: benchmark
description: Measure ContextLean's context impact with a no-Codex static estimate or a real controlled Codex A/B benchmark. Use when asked for "benchmark estimate", "benchmark ab", context/token measurements, bootstrap impact, or a reproducible baseline-versus-optimized comparison; never invent gains and always separate exact measurements, estimates, and heuristics.
---

# Benchmark ContextLean

Run only when the user requests measurement. Model runs require an explicit live
benchmark request; a static estimate request does not authorize them.

Keep every result honest: label exact measurements, estimates, and heuristics separately. Never turn an estimate into measured token savings or claim a gain when the comparison does not support it.

## Static estimate

Run:

```bash
python3 skills/benchmark/scripts/benchmark.py estimate --repo .
```

This reads `.contextlean/bootstrap-report.json` when an explicitly requested capture produced it. It never runs Codex. If the baseline is absent, report only the current state and say that no true static before/after is available.

Only when the user requests a static before/after measurement, follow
[Static capture](references/static-capture.md). Default bootstrap creates no report
and has no measurement prerequisite. Existing reports remain readable. Keep reports
local and out of automatic instruction context; never reconstruct a missing baseline.

## Codex A/B

Read `references/methodology.md` before running a live benchmark. Live runs consume model usage, so state the planned task count and repeats before executing. Never run them as part of ordinary tests.

Require an explicit model and reasoning effort:

```bash
python3 skills/benchmark/scripts/benchmark.py ab \
  --repo . \
  --model MODEL \
  --reasoning EFFORT
```

Use `--task` repeatedly or `--tasks-file` for user-supplied read-only tasks. Without either, use the generated five-task repository-navigation suite. Use `--repeat 3` to observe variance; repetitions alone do not establish statistical confidence.

The runner must retain these invariants:

- independent fresh `codex exec --json --ephemeral` conversations;
- identical model, reasoning, prompts, sandbox, options, and repository code;
- read-only sandbox, disabled web search, ignored user config and exec rules;
- temporary A/B copies only; never neutralize instructions in the working repository;
- balanced deterministic A→B / B→A ordering;
- reports written locally as Markdown and JSON;
- no hooks, telemetry, or report upload.

Report `turn.completed.usage` fields and exact event-derived command counts. Treat `cached_input_tokens` as a subset of `input_tokens`. Report reasoning tokens separately but do not add them to billed output because they are already included in `output_tokens`. Do not report file-open counts unless a future Codex event makes them directly measurable.

If authentication or a current model rate cannot be classified safely, show tokens only. Call a dated ChatGPT-rate calculation “credit-equivalent”, never actual credits spent. For API-key authentication, do not apply ChatGPT credit rates.

## Graded sample tasks

For task-success evidence, use `benchmarks/run_benchmark.py` from a source checkout.
Read `benchmarks/README.md` before running it. This development suite covers navigation,
bug fixes, features, refactors and documentation/configuration with an independent
evaluator. It uses read-only navigation and temporary writable copies for edit tasks;
the generic `ab` mode above remains read-only and does not evaluate answer correctness.

Keep preliminary validation clearly labelled, even when its artifacts are public. State the total live-run
count before executing and retain every failed or incorrect run. A completed turn is
not task success. File-read counts and total tool-call counts remain unavailable.
