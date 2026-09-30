# Reproducing ContextLean measurements

[Final compact-context 0.2.0 validation](results/2026-09-30-compact-final-0.2.0/README.md):
the completed frozen-commit Bug Fix pair plus exactly eight new calls, one per
condition for each remaining task, against `90ed9a4`. All ten pass independent offline
grading. ContextLean uses 16.84% fewer aggregate tokens, 5.97% less time and 20% more
commands. Feature regresses in time/commands, Refactor in tokens/time/commands, and
Documentation/config in commands. This is the current preliminary README evidence,
for the tested configuration only, with no confidence or universal savings claim.
The [methodology](results/2026-09-30-compact-final-0.2.0/methodology.md) records fresh
preparation, conditional-reference handling and the explicitly requested pair order.
No additional model calls are authorized.

[Previous clean-final 0.2.0 validation](results/2026-09-30-clean-final-0.2.0/README.md):
ten fresh runs, one per condition per task, using the pinned final product and repaired
harness. Preparation and all grading checks pass. ContextLean uses 9.9% more total
tokens, 17.7% more time and one fewer command call; all regressions are disclosed.
Preliminary validation only, no confidence or universal savings claim. No further
live calls are authorized. Historical and invalid diagnostic evidence remain separate.

[Final 0.2.0 candidate validation](results/2026-09-30-final-0.2.0/README.md):
ten new live runs against commit `52a2c34c091f9720076cc9685fb858347d9f6dcf`,
with five freshly bootstrapped fixture preparations. All task checks pass, but
ContextLean uses more aggregate tokens/time/commands and the generated map has a
known config-path error. Retain this as diagnostic evidence, not a clean bootstrap
release validation. This diagnostic batch is invalid for headline comparison.

[Offline root-cause analysis](analysis/2026-09-30-final-0.2.0/README.md) classifies the
bad map as a manual preparation error. Product behavior remains unchanged. The runner
now requires a validated offline preparation record before any model call; the
diagnostic result folder remains immutable and invalid for headline comparison.

[2026-09-30 preliminary validation](results/2026-09-30-validation/README.md):
all ten live runs, one per condition for each of five tasks. Both conditions passed
all task checks. Two task pairs used more total tokens with ContextLean. This checks
the runner and grading; it is not a statistically robust final benchmark.
The separately authorized final-candidate series above retains new evidence without
overwriting this historical batch. No further repetitions are authorized.

## Graded sample suite

Run from a local ContextLean checkout with Python 3.11+ and an authenticated Codex
CLI. There are five independent tasks in the small expense-report repository:

| Task | Category | Acceptance check |
|---|---|---|
| navigation | Understanding/navigation | Correct source/test paths and executed example output |
| bug-fix | Small bug fix | Mixed-case, whitespace-padded category queries work |
| feature | Small feature | Inclusive decimal minimum-amount filter, combined with category |
| refactor | Localized refactor | One shared normalization function; imports and behavior preserved |
| documentation-config | Documentation/configuration | EUR default in configuration, README and execution; override preserved |

[Exact prompts](tasks/suite.json) · [sample repository](fixtures/expense-report) ·
[independent evaluator](evaluate.py) · [runner](run_benchmark.py)

The sample has five regression tests. The evaluator runs the submitted tests, restores
the original five in a separate copy, and adds two independent acceptance checks per
task. It does not accept the agent's statement that tests passed. Acceptance tests are
outside the measured repository, and their paths/rubrics are not added to either condition.
The prompts describe the requested behavior, equally for both conditions.

### Optional future live reproduction

Before a future authorized run, apply the pinned Bootstrap procedure to a fresh
fixture copy. Review every project-map path and responsibility against the actual
source, then freeze it using the offline preparation command below. Do not copy
guidance from the diagnostic batch or reduce valid permanent rules to improve scores.

Use a **disposable candidate checkout**: move its original expense-report fixture to
a separate baseline directory, bootstrap a fresh copy of that baseline, and freeze
the reviewed copy back into the vacated fixture path. The output and record must be
new paths outside both preparation inputs. This command itself makes no model calls:

```sh
python3 benchmarks/prepare_fixture.py \
  --baseline /path/to/baseline \
  --prepared /path/to/bootstrapped-copy \
  --review /path/to/responsibility-review.json \
  --output benchmarks/fixtures/expense-report \
  --record .contextlean/preparation.json
```

The review is explicit human/agent evidence, not automatically inferred ownership:
`semantics_reviewed: true`, with `entries` keyed by every map path. Each entry has
the exact map `responsibility` and an `evidence` list of `{ "path": "relative-file",
"contains": "reviewed exact source excerpt" }`. Evidence must reside in the mapped
owner. See the [complete corrected review examples](analysis/2026-09-30-final-0.2.0/corrected-preparation.json).
The root map must have a `## Project map` section using explicit
`` `relative/path`: responsibility `` entries, and `CLAUDE.md` must import `AGENTS.md`.
Unsupported syntax fails closed; future generic Skill paths outside the map section
are not mistaken for existing project-map entries. The checker verifies paths,
evidence and hashes; natural-language meaning still requires the preparing agent's
source review.

The live runner requires that receipt and checks it before CLI probing/snapshotting,
after snapshotting, and before each fresh run. A nonexistent path, stale map/review,
incorrect wrapper or changed product state blocks execution. It retains the receipt
as `preparation.json` beside the results. Prompts, grading and token/timing logic are
unchanged. For a future separately authorized run only:

```sh
python3 benchmarks/run_benchmark.py \
  --model gpt-5.6-terra --reasoning low --repeat 1 \
  --preparation-record .contextlean/preparation.json \
  --output-dir .contextlean/validation/first-batch
```

This starts **10 live runs** and consumes model usage. Ordinary unit tests never
start a model. Use an empty output directory; existing results are not overwritten.
Provider/CLI failures stop the batch rather than repeatedly spending usage on a
broken setup. Wrong solutions remain recorded and do not stop other tasks.

All recorded batches are complete. Additional runs require separate approval. After approval,
`--repeat 2` in a **new** directory adds those 20 runs; combine all 30 only when prompts, fixture,
evaluator, model/configuration and environment still match. Never replace or discard
the first batch. A corrected setup is a separate series. A fresh `--repeat 3` means 30 new runs.
Every result retains its repetition and sequence; do not select favorable repetitions.

The committed sample map remains the historical example. The diagnostic source
archive retains its invalid map for forensic reproduction only; do not use it for a
new headline validation. Prepare fresh guidance with the pinned implementation and
the offline checks above before any separately authorized run. Neither command
automatically authors guidance.

## Conditions and fairness

- **Vanilla:** sample repository with its `AGENTS.md` and `CLAUDE.md` removed.
- **ContextLean:** the same sample with a frozen map created using the bootstrap procedure.
- Only those two instruction files differ initially. Non-instruction hashes are checked.
- The compact-final series uses a documented local adapter to additionally remove
  the optional `PROJECT_REFERENCE.md` from Vanilla and exclude it from product-state
  hashes. Automatic startup discovery, task prompts, grading and metric logic are
  unchanged. This adapter is retained with its evidence; the frozen runner is unchanged.
- Each task/condition/repetition starts from a fresh copy. No edits or conversation
  carry over. Both conditions use the same temporary workspace path.
- Prompt, model, reasoning, configured provider, sandbox and evaluator are identical
  within each pair. Navigation is read-only; edit tasks use `workspace-write`.
- Codex runs are ephemeral, ignore user configuration and exec rules, disable web
  search, and set approval policy to never. No full-access sandbox is used.
- Neither condition loads the ContextLean plugin. This isolates generated repository
  guidance; it does not measure skill discovery or the cost of bootstrap itself.
- Order alternates by task/repetition. With five tasks and one repetition, the
  first position cannot be perfectly balanced. Caching/service load are uncontrolled.
- For compact-final, the owner explicitly requested Vanilla first for all eight new
  calls; its existing Bug Fix pair was ContextLean first. This ordering is disclosed
  and the previous dataset is never pooled with compact-final.
- Sample copies omit Git metadata, so agent `git diff` checks cannot work. Any setup
  change to address this requires a separate, clearly identified measurement series.
- The same Git HEAD is recorded for both conditions. Before an authorized commit,
  HEAD does not identify the candidate changes: the complete candidate snapshot,
  fixture digest, prompts and evaluator digest are retained too. Repeat from that
  snapshot, or use a committed revision when publishing the final benchmark.

The fixture is intentionally small and synthetic. It includes an ordinary filter
bug and a duplicated helper so each requested task has a verifiable outcome.
The map describes ownership and commands, not bug solutions or evaluator answers.
These results cannot establish performance on large projects or other languages.

## Metrics and success

| Metric | Evidence / availability |
|---|---|
| Input, cached input, output | Exact `turn.completed.usage` fields; null if unavailable |
| Total tokens | Input + output; cached input is already included in input |
| Reasoning output | Optional provider field; null when absent, never double-counted |
| Command calls | Unique `command_execution` event ids; not all tool calls |
| Wall time | Local monotonic duration of Codex execution; evaluator time excluded |
| All tool calls, file reads, unique files inspected | Unavailable; no guesses from shell text |
| Tests passing | Original regression suite plus independent checks; logs retained |
| Task success | Valid execution and usage, tests and acceptance pass, protected inputs/guidance preserved |
| Estimated cost | Null in the suite unless supported separately by authentication and dated rates |

Every individual run appears in `summary.json` and `report.md`, including failures.
Per task and condition, the summary gives median, mean, minimum and maximum for
available metrics. A single run has no meaningful variance estimate.
An incorrect or incomplete comparison cannot support a gain claim. Regressions
must be reported alongside improvements; repeated runs are not automatically
statistically significant. Inspect success rates before comparing resource usage.

## Raw artifacts and publication

Each output directory contains:

```text
summary.json                   # configuration, prompts, hashes, all outcomes and summaries
report.md                      # human-readable tables
candidate/                     # exact candidate source used before a release commit
raw/<task>-<repeat>-<condition>/
  events.jsonl                 # Codex events, including final answer and reported usage
  events.stderr.txt            # CLI diagnostic output
  evaluation.txt               # submitted tests, original tests, acceptance checks
  run.json                     # metrics, pass/fail, order and relative artifact paths
  solution/                    # resulting repository, including unsuccessful edits
```

Logs replace temporary workspace and home prefixes for sharing. This is path
redaction, not a general secret scrubber. Review all raw material before publishing;
use only the public sample for public claims. No upload happens automatically.

Keep validation output locally under `.contextlean/`. The reviewed preliminary batch is included under
[results/](results/README.md), with every run and compact source/solution archives.
Future datasets must retain all outcomes, exact configuration and raw evidence.
No final repeated benchmark has been published.

## Existing measurement modes

The plugin's `benchmark estimate` remains offline:

```sh
python3 skills/benchmark/scripts/benchmark.py estimate --repo .
```

It reports an inventory of instruction files and a byte-based token estimate, not
actual automatically loaded context or model savings. A missing bootstrap baseline
means only the current state can be shown.

The generic `ab` runner remains a read-only navigation experiment:

```sh
python3 skills/benchmark/scripts/benchmark.py ab \
  --repo . --model gpt-5.6-terra --reasoning low --repeat 1
```

Its completion flags mean execution completed with valid usage. It has no answer
grader and suppresses gain claims. Use the graded suite for task-success evidence.
See the [measurement reference](../skills/benchmark/references/methodology.md).
