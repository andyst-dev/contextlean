# Reproducing ContextLean measurements

[Final 0.2.0 candidate validation](results/2026-09-30-final-0.2.0/README.md):
ten new live runs against commit `52a2c34c091f9720076cc9685fb858347d9f6dcf`,
with five freshly bootstrapped fixture preparations. All task checks pass, but
ContextLean uses more aggregate tokens/time/commands and the generated map has a
known config-path error. Retain this as diagnostic evidence, not a clean bootstrap
release validation. No further live runs are authorized.

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

```sh
python3 benchmarks/run_benchmark.py \
  --model gpt-5.6-terra --reasoning low --repeat 1 \
  --output-dir .contextlean/validation/first-batch
```

This starts **10 live runs** and consumes model usage. Ordinary unit tests never
start a model. Use an empty output directory; existing results are not overwritten.
Provider/CLI failures stop the batch rather than repeatedly spending usage on a
broken setup. Wrong solutions remain recorded and do not stop other tasks.

Both batches are complete. Additional runs require separate approval. After approval,
`--repeat 2` in a **new** directory adds those 20 runs; combine all 30 only when prompts, fixture,
evaluator, model/configuration and environment still match. Never replace or discard
the first batch. A corrected setup is a separate series. A fresh `--repeat 3` means 30 new runs.
Every result retains its repetition and sequence; do not select favorable repetitions.

The committed sample map remains the historical example. To reproduce the final
candidate context, use the frozen source archive linked in its result set, or
prepare fresh guidance with the specified bootstrap revision before a separately
authorized run. The generic command above does not regenerate guidance.

## Conditions and fairness

- **Vanilla:** sample repository with its `AGENTS.md` and `CLAUDE.md` removed.
- **ContextLean:** the same sample with a frozen map created using the bootstrap procedure.
- Only those two instruction files differ initially. Non-instruction hashes are checked.
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
