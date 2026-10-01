# Reproducing ContextLean measurements

[Release-aligned v0.2.0 validation](results/2026-09-30-release-aligned-0.2.0/README.md):
exactly ten fresh calls at `86043499d5a375cc6a3b295bc7c03b0999eb458c`, one per condition
per existing task, all independently regraded and passing. This is the current README
headline: ContextLean -29.12% tokens, -29.19% time, 18→16 commands. Bug Fix uses more
output tokens/commands; Navigation has a higher dated credit-equivalent. Preliminary
validation only, no statistical-confidence or universal token-savings claim.
All earlier batches are preserved separately. No additional calls are authorized.

[Final compact-context 0.2.0 validation](results/2026-09-30-compact-final-0.2.0/README.md):
the completed frozen-commit Bug Fix pair plus exactly eight new calls, one per
condition for each remaining task, against `90ed9a4`. All ten pass independent offline
grading. ContextLean uses 16.84% fewer aggregate tokens, 5.97% less time and 20% more
commands. Feature regresses in time/commands, Refactor in tokens/time/commands, and
Documentation/config in commands. This is historical preliminary evidence,
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

## Future graded runs: harness v2

The development runner now uses stronger session isolation and versioned evidence.
Historical datasets above and their frozen runners remain unchanged. Read
[methodology v2](methodology-v2.md) for controls, receipt definitions and limitations.
The packaged ContextLean product and generic diagnostic A/B runner are unchanged.

Five independent tasks use the standard-library expense-report fixture:

| Task | Acceptance |
|---|---|
| navigation | Source/test ownership paths and executed sample output |
| bug-fix | Mixed-case, whitespace-padded category queries |
| feature | Inclusive decimal minimum-amount filter combined with category |
| refactor | One shared normalization function; behavior/imports preserved |
| documentation-config | EUR default in configuration, README and execution; override preserved |

[Prompts](tasks/suite.json) · [fixture](fixtures/expense-report) ·
[unchanged acceptance rules](evaluate.py) · [runner](run_benchmark.py)

Prepare fresh guidance in a disposable candidate checkout, review its map and
freeze the fixture with the existing offline preparation command:

```sh
python3 benchmarks/prepare_fixture.py \
  --baseline /path/to/baseline \
  --prepared /path/to/bootstrapped-copy \
  --review /path/to/responsibility-review.json \
  --output benchmarks/fixtures/expense-report \
  --record .contextlean/preparation.json
```

The review attests semantic responsibility, with exact path/source evidence. See
[review examples](analysis/2026-09-30-final-0.2.0/corrected-preparation.json).
Invalid maps and stale hashes fail preparation. No guidance is automatically
created by the runner. Do not use the historical diagnostic fixture as a fresh
headline comparison.

Python 3.11+, Git, rg, an authenticated provider CLI and a working native filesystem
boundary are required. macOS uses sandbox-exec; Linux requires Bubblewrap. Other
hosts and nested sandboxes that cannot enforce the boundary fail closed. Runtime
paths/hashes/versions are pinned and receipts are checked across conditions.

Run deterministic gates without model calls:

```sh
python3 benchmarks/run_benchmark.py \
  --provider codex --model MODEL --reasoning EFFORT \
  --preflight-only --experiment-kind performance --repeat 3 \
  --preparation-record .contextlean/preparation.json \
  --output-dir .contextlean/validation/preflight-v2
```

This executes canonical tests, Git and permission probes and CLI version checks,
not models. Use a new output directory. An offline preflight does not authorize
future live execution. Reliable quota checking is currently unavailable and is
recorded as unknown.

Only after a separate explicit live authorization, replace `--preflight-only` with
`--live` and choose another new output directory. Five tasks × three repetitions ×
two conditions means **30 model calls**; five repetitions means **50**. Claude uses
`--provider claude --claude CLI --model MODEL --reasoning EFFORT`. No model calls are
authorized by this documentation or performed in ordinary tests.

Use `--experiment-kind compatibility-smoke --repeat 1` for compatibility only.
Performance mode requires at least three independent repetitions, preferably five.
The schedule is saved before execution and alternates pair order. Every result is
retained, including unfavorable measurements. No silent retries, replacements or
favorable-result stopping are allowed. Provider/quota, harness and grader errors
stop an incomplete campaign; task assertion failures remain recorded and allow the
schedule to continue. Incomplete pairs cannot produce token comparison aggregates.

Each session has its own disposable repo/tmp/cache/artifacts/receipts root and real,
clean deterministic Git baseline. Only declared guidance (AGENTS.md, CLAUDE.md and
optional PROJECT_REFERENCE.md) differs between conditions. Product/test bytes and
exact prompts match. Policy permits session-local writes and prevents shared-parent
scratch files and access to prior exported evidence. The whole root is removed and
cleanup is verified before the next session.

## Future v2 evidence

```text
summary.json                   # schema/harness v2, all observations, descriptive/paired statistics
schedule.json                  # deterministic plan saved before calls
fixture-manifest.json          # exhaustive condition hashes/sizes, task prompt identities
preparation.json               # frozen offline map/source attestation
preflight/                     # every planned session's deterministic gates
fixtures/, source/             # sanitized input exports
raw/<task>-<repeat>-<condition>/
  events.jsonl, events.stderr.txt # sanitized chronological provider evidence
  execution.json               # exposed tools, coverage, primary/helper usage, sizes
  session.json, post-run.json   # runtime/env/provider/Git/permission and contamination receipts
  evaluation.txt, run.json, solution/
checksums.json                 # public export integrity, excludes private originals
private/                       # NEVER publish: exact raw streams, inputs, receipts and solutions
```

Primary input/cached/uncached/output tokens, turns and helper usage are reported
only where exposed. Claude helpers remain separate from primary usage. Codex's
merged command output has no invented stdout/stderr split. Equal complete test-list
digests detect duplicate verification coverage, with observable intervening changes.
Missing fields remain null. No per-action token-cost estimates are produced.

Summaries include individual observations, means, medians, ranges, sample standard
deviations and paired differences. Failed or incomplete comparisons suppress gain
claims. Provider cache state remains uncontrolled; order, timestamps and exposed
identifiers are saved. No statistical significance or universal savings claim is
made. Review sanitized evidence before publication; never include private originals.
No upload happens automatically. Keep local runs under `.contextlean/`.

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
