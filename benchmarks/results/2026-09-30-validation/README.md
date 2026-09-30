# Preliminary validation — 2026-09-30

**Ten live runs; one run per condition per task. This is not a statistically robust
final benchmark.** All ten passed submitted tests, original regression tests and
independent acceptance checks. Two tasks used more total tokens with ContextLean.
Additional repeated trials are needed for stronger conclusions; no further model
runs are authorized for this release preparation.

## Configuration and frozen state

- Exact model: `gpt-5.6-terra`; reasoning: `low`.
- Run window: 2026-09-30, 07:46:22–07:52:04 UTC.
- Codex CLI: `0.147.0`; environment: Darwin, arm64, Python `3.14.4`.
- Base repository commit: `a7939df879f7b48a2f65c39270a0e7d3f157bded`.
  **The candidate was uncommitted. This SHA alone does not reproduce the batch.**
- Historical ContextLean version: `0.1.0`. The batch predates the 0.2.0 release
  preparation; neither the numbers nor the recorded version have been relabelled.
- [Frozen candidate source archive](source-snapshot.zip), including the fixture,
  both maps, prompts, runner and evaluator. Archive entries are relative paths;
  timestamps are normalized. Contents retain the historical documentation/version.
  Finder metadata and linter caches are excluded; [selection manifest](source-selection.json)
  records every retained file hash, omitted generated file hash and public tree hash.
  The original whole-candidate hash below includes those omitted files and cannot
  be recomputed from the curated archive. Fixture/task/evaluator hashes still match.
- [Original summary](summary.json) records complete prompts, order, hashes,
  configuration, raw metrics and task outcomes. [Artifact checksums](checksums.json).

| State | SHA-256 |
|---|---|
| Candidate tree | `6b51e8ab4e6c59571325c30afb932b49c9bf21ff9f01a7bd2463dd8dd6d9252b` |
| Fixture tree | `7642a99b1020d72fd33f9f6e23f53ed42d1f1b26bdb9a24d9b08ed25e8899dbe` |
| Task suite bytes | `bc40082c4e77dc11a268b5593f313d6b1b4b51062c3818effb64bfe03a744c62` |
| Evaluator bytes | `3200e20da7522c1a063cda247433efcdcaf2e6f945c7cdf951dee35e624fd686` |

The tree digest hashes sorted relative paths, a NUL separator, content and another
NUL separator, using the frozen runner's `tree_digest`. It excludes generated directories.
All pairs have the same non-instruction tree digest:
`361ede5431a41c0e1fcba8b5cecca598d3090eb5d775a25c4e128cbf0a1a12f2`.

## Conditions and fairness

**Vanilla:** fresh expense-report fixture with `AGENTS.md` and `CLAUDE.md` removed.
**ContextLean:** the same fixture retaining its frozen compact map and one-line
Claude import. The map was created by the current agent following the bootstrap
procedure before the batch; it gives ownership/commands/rules, not task solutions.

Only those two instruction files differ initially. Every run starts from a new
copy at the same temporary workspace path, with no inherited edits or conversation.
Both conditions use the same task prompt, model, reasoning, starting source,
sandbox and evaluator. The acceptance evaluator is outside the measured workspace.

Commands use `codex exec --json --ephemeral --ignore-user-config --ignore-rules
--strict-config --skip-git-repo-check`, with explicit model/reasoning, approval
policy `never` and web search `disabled`. Navigation uses `read-only`; edit tasks
use `workspace-write`. Service tier was left at the CLI default. Provider caching,
service load and model nondeterminism are uncontrolled. User configuration/rules
are ignored; this does not imply every provider or machine state is reset.
Neither condition loads the plugin: this isolates generated guidance and excludes
bootstrap cost, skill discovery and workflow invocation. Direct consumption of
AGENTS.md in the system prompt was not independently instrumented.

Execution order: navigation V→C, bug fix C→V, feature V→C, refactor C→V,
documentation/config V→C. Alternation limits order bias but five pairs cannot
perfectly balance which condition runs first. V = Vanilla; C = ContextLean.

## Exact tasks and grading

Every prompt has this identical prefix:

> Work only in this local sample repository. Do not use network services, install
> dependencies or change agent guidance. Use the existing standard-library tests.

The exact task bodies follow (also in `summary.json` and the source archive).

### navigation — repository understanding/navigation

Inspect this expense report repository without changing files. Identify the function that loads CSV amounts, the function that produces category totals, and the test file covering the CLI. Run the CLI on data/sample.csv. Return only a JSON object with keys loader (relative source path), reporter (relative source path), cli_tests (relative test path), total (string), count (integer), and currency (string). Verify from code and execution, not only guidance.

### bug-fix — small bug fix

Fix category filtering so --category accepts mixed case and surrounding whitespace, just as stored category names do. For example --category ' FOOD ' must select both food expenses from data/sample.csv and produce total 20.00. Preserve unfiltered reports, decimal arithmetic and currency overrides. Add a regression test and run the tests.

### feature — small feature

Add optional --min-amount to the expense report CLI. Keep only expenses whose individual amount is greater than or equal to that decimal threshold before producing the report. It must combine with --category and leave existing behavior unchanged when omitted. With data/sample.csv, --min-amount 10 yields count 2 and total 32.50; --category food --min-amount 10 yields count 1 and total 12.50. Add tests and run them.

### refactor — localized refactor

Consolidate the duplicated normalize_category functions into one shared implementation used by filtering and category grouping. Preserve behavior, including current category filter query semantics; this task is not a bug fix. Keep the normalize_category names importable from both existing modules for compatibility. Do not add dependencies or unrelated abstractions. Run the existing tests.

### documentation-config — documentation/configuration

Change the configured default currency from USD to EUR and update the README to match. --currency GBP must still override the default. Keep expense amounts and grouping behavior unchanged. Verify the documented example commands and run the tests.

The frozen evaluator runs each submitted test suite, restores the original five
tests in a separate copy, then runs two independent acceptance tests per task:

| Task | Task acceptance | Preserved behavior |
|---|---|---|
| Navigation | Exact source/test paths and executed JSON result: 40.00, three rows, USD | GBP override, three rows, total 40 |
| Bug fix | Four case/space queries select two rows/20; missing category selects zero | GBP override, three rows, total 40 |
| Feature | Inclusive thresholds 10, 12.50, 0, 100 and category combination | GBP override, three rows, total 40 |
| Refactor | One function definition, identity through both imports, grouping and original query semantics | GBP override, three rows, total 40 |
| Documentation/config | EUR in config, README and execution; USD removed from README | GBP override, three rows, total 40 |

Success also requires valid execution/usage, unchanged sample data and guidance,
and no edits for navigation. Agent claims alone do not establish success. Both
bug-fix and feature solutions added requested regression tests. Tests cover these
specific contracts, not every possible input or production behavior.

## Every raw result

Cached input is a **subset of input**, already included in the total. Total = input + output; optional reasoning usage is included in output, never added again.
Command calls count unique `command_execution` item ids, including unsuccessful
commands; they do not count every tool invocation. Seconds measure local monotonic
Codex process duration, excluding independent evaluator time. Duration is not
recoverable from JSONL alone; the full precision remains in each run record.

| Task | Condition | Input | Cached input | Output | Total | Commands | Seconds | Task success | Raw evidence |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| navigation | vanilla | 47,765 | 29,184 | 391 | 48,156 | 2 | 17.15889 | PASS | [events](raw/navigation-1-vanilla/events.jsonl), [diagnostics](raw/navigation-1-vanilla/events.stderr.txt), [grading](raw/navigation-1-vanilla/evaluation.txt), [record](raw/navigation-1-vanilla/run.json) |
| navigation | contextlean | 26,175 | 12,032 | 266 | 26,441 | 1 | 10.16185 | PASS | [events](raw/navigation-1-contextlean/events.jsonl), [diagnostics](raw/navigation-1-contextlean/events.stderr.txt), [grading](raw/navigation-1-contextlean/evaluation.txt), [record](raw/navigation-1-contextlean/run.json) |
| bug-fix | contextlean | 58,315 | 34,048 | 891 | 59,206 | 2 | 24.49146 | PASS | [events](raw/bug-fix-1-contextlean/events.jsonl), [diagnostics](raw/bug-fix-1-contextlean/events.stderr.txt), [grading](raw/bug-fix-1-contextlean/evaluation.txt), [record](raw/bug-fix-1-contextlean/run.json) |
| bug-fix | vanilla | 87,093 | 67,328 | 1,311 | 88,404 | 3 | 36.41088 | PASS | [events](raw/bug-fix-1-vanilla/events.jsonl), [diagnostics](raw/bug-fix-1-vanilla/events.stderr.txt), [grading](raw/bug-fix-1-vanilla/evaluation.txt), [record](raw/bug-fix-1-vanilla/run.json) |
| feature | vanilla | 106,627 | 83,456 | 2,790 | 109,417 | 4 | 66.08335 | PASS | [events](raw/feature-1-vanilla/events.jsonl), [diagnostics](raw/feature-1-vanilla/events.stderr.txt), [grading](raw/feature-1-vanilla/evaluation.txt), [record](raw/feature-1-vanilla/run.json) |
| feature | contextlean | 95,357 | 84,480 | 1,757 | 97,114 | 3 | 44.39200 | PASS | [events](raw/feature-1-contextlean/events.jsonl), [diagnostics](raw/feature-1-contextlean/events.stderr.txt), [grading](raw/feature-1-contextlean/evaluation.txt), [record](raw/feature-1-contextlean/run.json) |
| refactor | contextlean | 83,116 | 70,400 | 1,014 | 84,130 | 3 | 38.03595 | PASS | [events](raw/refactor-1-contextlean/events.jsonl), [diagnostics](raw/refactor-1-contextlean/events.stderr.txt), [grading](raw/refactor-1-contextlean/evaluation.txt), [record](raw/refactor-1-contextlean/run.json) |
| refactor | vanilla | 71,274 | 52,224 | 1,102 | 72,376 | 3 | 33.34189 | PASS | [events](raw/refactor-1-vanilla/events.jsonl), [diagnostics](raw/refactor-1-vanilla/events.stderr.txt), [grading](raw/refactor-1-vanilla/evaluation.txt), [record](raw/refactor-1-vanilla/run.json) |
| documentation-config | vanilla | 83,968 | 62,208 | 1,051 | 85,019 | 3 | 35.28769 | PASS | [events](raw/documentation-config-1-vanilla/events.jsonl), [diagnostics](raw/documentation-config-1-vanilla/events.stderr.txt), [grading](raw/documentation-config-1-vanilla/evaluation.txt), [record](raw/documentation-config-1-vanilla/run.json) |
| documentation-config | contextlean | 87,366 | 78,336 | 1,050 | 88,416 | 4 | 32.77296 | PASS | [events](raw/documentation-config-1-contextlean/events.jsonl), [diagnostics](raw/documentation-config-1-contextlean/events.stderr.txt), [grading](raw/documentation-config-1-contextlean/evaluation.txt), [record](raw/documentation-config-1-contextlean/run.json) |

All resulting repositories, including tests and guidance, are in
[solutions.zip](solutions.zip), under `<task>-1-<condition>/solution/`.
No run was dropped. The raw event logs include commands, outputs, final answers and
usage; stderr retains warnings and recovered errors.

## Aggregate calculations

Sum all five runs **within each condition**, then compute
`100 × (ContextLean − Vanilla) / Vanilla`. Negative means lower usage/time;
positive means higher. This is a weighted aggregate, not a mean of task percentages.
Round only for display; `summary.json` retains the measured values.

| Metric | Vanilla sum | ContextLean sum | Difference |
|---|---:|---:|---:|
| Total tokens | 403,372 | 355,307 | -11.92% |
| Input tokens | 396,727 | 350,329 | -11.70% |
| Cached input tokens | 294,400 | 279,296 | -5.13% |
| Output tokens | 6,645 | 4,978 | -25.09% |
| Wall time (seconds) | 188.28271 | 149.85422 | -20.41% |
| Command calls | 15 | 13 | -13.33% |
| Task success | 5/5 | 5/5 | Same |

In this 10-run validation batch, total tokens were **11.92% lower in aggregate**.
Refactor used **16.24% more total tokens** and took **14.08% longer** (33.34189 →
38.03595 s). Documentation/config used **4.00% more total tokens** and **one extra
command** (3 → 4). These are observed outcomes, not guaranteed effects.

## Measurement limitations and possible bias

| Limitation / observation | Consequence and possible bias |
|---|---|
| One observation per task/condition | No within-task variance, confidence interval or statistical significance. Random model choices can favor either condition. |
| Small synthetic Python fixture, selected tasks, one model/reasoning setting | Task-selection bias; results cannot establish behavior across repositories, languages, agents or models. |
| File-read counts / unique inspected files unavailable | Cannot claim measured exploration reduction. Parsing shell text would be incomplete and could favor either condition. Fields remain null, not zero. |
| Total tool-call counts unavailable | Reported 15→13 is command calls only. Patch attempts are excluded, so it cannot substantiate overall tool efficiency. |
| Recovered patch rejections in Vanilla bug fix, feature and documentation/config | CLI stderr says writing outside the project was rejected by approval settings; each later completed successfully. Recovery can inflate Vanilla tokens/time, making ContextLean's aggregate advantage look larger. Failed attempt details are not fully represented in JSONL; diagnostics are preserved. |
| Model-cache schema warnings: navigation Vanilla and refactor ContextLean at startup; feature and documentation/config ContextLean during TTL renewal | Missing `supports_parallel_tool_calls` errors introduce uneven environment noise. They may affect setup/time or behavior; direction/size cannot be isolated. They do not prove a provider cache hit or miss. |
| State-database reconciliation warnings in all ten runs | Shared CLI environment noise may add overhead; equal bias cannot be assumed. |
| Failed Git checks in non-Git copies | Git checks failed in both bug-fix runs, both feature runs, Vanilla refactor and both documentation/config runs. The fixture lacks `.git`; these are failed verification attempts, not passing Git checks. Uneven extra commands/output can bias tokens/time in either direction. |
| Documentation/config ContextLean diff commands returned 1 | Outside Git, `git diff -- config.json README.md` compared two unrelated files as a no-index diff. Its nonzero difference status short-circuited later checks and led to more checking. This can inflate ContextLean command/time/token usage; all outputs remain visible. |
| Uncontrolled provider caching, service load, default tier, imperfect first-run balance | Cache/time effects and order may favor either condition. Report cached input separately; no actual spending or provider-independent cost claim. |
| Plugin excluded, bootstrap cost excluded, guidance loading not directly instrumented | Measures this frozen-guidance comparison; cannot prove independent skill invocation or full workflow benefit. |
| Candidate uncommitted and historical version 0.1.0 | The base SHA alone is insufficient. Use the preserved archive/hashes, not the evolving 0.2.0 checkout, for exact source reproduction. |

This batch validates the measurement plumbing and these task outcomes. It is
insufficient for a clean final efficiency claim. Future repeats require approval;
if the environment changes to address warnings/Git setup, publish a separate series
rather than silently combining unlike runs. Neither failures nor regressions should
be discarded.

## Public evidence and offline audit

The public selection retains the original summary, four raw files for each run,
the frozen candidate source files and all ten resulting solutions. No user configuration,
authentication files, caches, generated bytecode or local bootstrap reports are included.
Workspace/home prefixes were replaced by `<workspace>` / `<home>` when logs were
captured. An additional scan found no personal paths, usernames or credential
patterns in the selected evidence, including archive contents. No measured numbers
were changed. Retained source and solution contents are preserved; ZIP metadata
(timestamps/permissions) is normalized. The whole evidence directory is under 0.4 MB.

From the current checkout, this command checks archive safety/checksums, reconciles
all usage/command counts and totals, verifies selected-source and original fixture/task/evaluator hashes and regrades all ten
saved solutions **without calling Codex or a model**:

```sh
python3 -m unittest discover -s tests -p test_public_validation.py -v
```

For exact source inspection, extract `source-snapshot.zip` into an empty directory.
The frozen `benchmarks/tasks/suite.json`, `benchmarks/evaluate.py`, fixture and runner
are the source of this batch. Re-running that live runner consumes ten new model
runs and requires separate authorization; offline verification is sufficient to
audit the preserved outcomes. Numeric equality across new stochastic runs is not expected.
