# Clean final ContextLean 0.2.0 validation — 2026-09-30

**Preliminary validation: one fresh run per condition per task, ten runs total.**
All preparation and offline grading gates pass. This record is suitable for an honest
v0.2.0 README/release-note description of this tested configuration, including the
regressions below. It makes **no statistical-confidence or universal savings claim**.

Product commit: `52a2c34c091f9720076cc9685fb858347d9f6dcf`.
Repaired harness commit: `c58b0d6` (full SHA in preparation evidence).
Model: `gpt-5.6-terra`; reasoning: `low`; Codex CLI 0.147.0; Python 3.14.4;
Darwin arm64. No repetitions beyond these ten calls were started.

## Task pairs

| Task | Vanilla tokens | ContextLean tokens | Token difference | Vanilla / ContextLean seconds | Time difference | Vanilla / ContextLean commands | Command difference | Success |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Navigation | 48,099 | 43,928 | -8.7% | 12.94 / 19.23 | +48.6% | 2 / 2 | +0 | Both pass |
| Bug fix | 71,021 | 94,026 | +32.4% | 28.86 / 35.67 | +23.6% | 3 / 3 | +0 | Both pass |
| Feature | 94,825 | 99,162 | +4.6% | 46.85 / 54.36 | +16.0% | 4 / 3 | -1 | Both pass |
| Refactor | 88,466 | 111,039 | +25.5% | 29.83 / 38.46 | +28.9% | 4 / 4 | +0 | Both pass |
| Documentation/config | 83,018 | 75,260 | -9.3% | 25.65 / 21.88 | -14.7% | 3 / 3 | +0 | Both pass |

## Aggregate

| Metric | Vanilla | ContextLean | Difference |
|---|---:|---:|---:|
| Input tokens | 380,321 | 417,257 | +9.7% |
| Cached input tokens (included in input) | 311,552 | 361,216 | +15.9% |
| Output tokens | 5,108 | 6,158 | +20.6% |
| Total tokens | 385,429 | 423,415 | +9.9% |
| Wall time (s) | 144.12 | 169.59 | +17.7% |
| Command calls | 16 | 15 | -6.2% |
| Task / acceptance / regression / submitted-test success | 5/5 each | 5/5 each | Same |

ContextLean uses **9.9% more aggregate tokens** and **17.7% more wall time**,
with **one fewer command call**. Bug fix, Feature and Refactor use more tokens and
more time. Navigation uses fewer tokens but more time. Documentation/config uses
fewer tokens and less time. **No task uses more command calls**; Feature uses one fewer.
All ten runs pass acceptance, restored original regression tests, submitted tests,
protected inputs and guidance checks, including the navigation read-only check.

## Every run

| Sequence | Task | Condition | Input | Cached input | Output | Total | Seconds | Commands | Acceptance / regression / submitted tests |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | [Navigation](raw/navigation-1-vanilla/run.json) | vanilla | 47,777 | 37,120 | 322 | 48,099 | 12.94 | 2 | Pass / pass / pass |
| 2 | [Navigation](raw/navigation-1-contextlean/run.json) | contextlean | 43,547 | 27,136 | 381 | 43,928 | 19.23 | 2 | Pass / pass / pass |
| 3 | [Bug fix](raw/bug-fix-1-contextlean/run.json) | contextlean | 92,794 | 73,472 | 1,232 | 94,026 | 35.67 | 3 | Pass / pass / pass |
| 4 | [Bug fix](raw/bug-fix-1-vanilla/run.json) | vanilla | 70,058 | 64,256 | 963 | 71,021 | 28.86 | 3 | Pass / pass / pass |
| 5 | [Feature](raw/feature-1-vanilla/run.json) | vanilla | 92,956 | 71,424 | 1,869 | 94,825 | 46.85 | 4 | Pass / pass / pass |
| 6 | [Feature](raw/feature-1-contextlean/run.json) | contextlean | 96,738 | 90,624 | 2,424 | 99,162 | 54.36 | 3 | Pass / pass / pass |
| 7 | [Refactor](raw/refactor-1-contextlean/run.json) | contextlean | 109,630 | 101,632 | 1,409 | 111,039 | 38.46 | 4 | Pass / pass / pass |
| 8 | [Refactor](raw/refactor-1-vanilla/run.json) | vanilla | 87,393 | 68,352 | 1,073 | 88,466 | 29.83 | 4 | Pass / pass / pass |
| 9 | [Documentation/config](raw/documentation-config-1-vanilla/run.json) | vanilla | 82,137 | 70,400 | 881 | 83,018 | 25.65 | 3 | Pass / pass / pass |
| 10 | [Documentation/config](raw/documentation-config-1-contextlean/run.json) | contextlean | 74,548 | 68,352 | 712 | 75,260 | 21.88 | 3 | Pass / pass / pass |

Cached input is a subset of input; total tokens equal input plus output.
Reported reasoning output remains part of output and is not added again.
File reads, unique files inspected and total tool calls are unavailable. Command counts
are unique command-execution event IDs. Wall time measures model execution, excluding
preparation and grading. Raw JSON retains the unrounded measured values.

## Comparison with earlier batches

Batches remain separate; no old or diagnostic run is used in this result set.
The diagnostic batch has an invalid generated path and is **invalid for headline
performance comparison**, even though its submitted solutions pass grading.

| Batch | Condition | Input | Cached | Output | Total | Seconds | Commands | Success |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Historical 0.1.0 guidance | contextlean | 350,329 | 279,296 | 4,978 | 355,307 | 149.85 | 13 | 5/5 |
| Historical 0.1.0 guidance | vanilla | 396,727 | 294,400 | 6,645 | 403,372 | 188.28 | 15 | 5/5 |
| Invalid diagnostic 0.2.0 guidance | contextlean | 463,316 | 383,488 | 7,043 | 470,359 | 200.41 | 19 | 5/5 |
| Invalid diagnostic 0.2.0 guidance | vanilla | 378,295 | 299,520 | 4,951 | 383,246 | 165.78 | 16 | 5/5 |
| Clean final 0.2.0 guidance | contextlean | 417,257 | 361,216 | 6,158 | 423,415 | 169.59 | 15 | 5/5 |
| Clean final 0.2.0 guidance | vanilla | 380,321 | 311,552 | 5,108 | 385,429 | 144.12 | 16 | 5/5 |

Compared with historical ContextLean: total tokens increase by **68,108 (+19.2%)**,
wall time increases by **19.73 s (+13.2%)**, and commands increase by **2**.
Historical Vanilla also changes: tokens −4.4%, time −23.5%, commands +1.
The historical paired aggregate token difference was −11.9%; the clean final
paired difference is +9.9%. Historical Bug fix and Feature token improvements
become regressions; Refactor remains a token regression, while Documentation/config
becomes an improvement. Navigation remains a token improvement, with a time regression.

Compared with invalid diagnostic ContextLean (descriptive only): total tokens decrease
by **46,944 (−10.0%)**, time by **30.83 s (−15.4%)**, and commands by **4**.
Its paired token difference was +22.7%. These between-batch changes do not establish
causality: bootstrap context, stochastic choices, caching and load vary. They do not
prove the repair caused the resource differences.

[Machine-readable comparison, all metrics and per-task deltas](comparison.json) ·
[historical evidence](../2026-09-30-validation/README.md) ·
[invalid diagnostic evidence](../2026-09-30-final-0.2.0/README.md) ·
[preparation root-cause analysis](../../analysis/2026-09-30-final-0.2.0/README.md).

## Preparation and fairness

All five Vanilla and five ContextLean fixtures were prepared before any call.
Each ContextLean copy was bootstrapped from pristine product code using the final
committed specification and permanent rules, with a fresh baseline and newly authored
map. No earlier generated guidance or run was reused. Every map has eight reviewed
existing paths, including root `config.json`; all responsibilities have exact source
anchors, and all 71 permanent facets have reviewed hashed durable destinations.
CLAUDE.md is exactly `@AGENTS.md`. Code, tests, prompts and evaluator match the pinned
candidate. Only the two guidance files differ between conditions.

All five independently validated/frozen contexts are byte-identical. The runner uses
one of those verified sources and creates fresh workspaces for each run, checking
its immutable receipt before probing, after snapshotting and before each copy.
The preparation evidence was rechecked after the batch. Natural-language responsibility
and facet review was performed by the preparing agent; hash/path checks bind that
review to the actual files, rather than proving semantic meaning automatically.

See [methodology](methodology.md), [preparation evidence](preparation-evidence.json),
[runner preparation receipt](preparation.json), and [sanitized preparation recipe](preparation-procedure.py.txt).
The recipe uses placeholders for private directories. Bootstrap reports and transfer
ledgers are evidence only, excluded from measured startup context.

## Measurement review and limits

Provider cache state and service load are uncontrolled. Temporary samples omit Git
metadata in both conditions; navigation and all edit ContextLean runs attempt an
initial Git status that fails, while Vanilla Feature/Refactor also attempt failing
Git diff checks and Vanilla documentation/config has a failing Git status.
The failed commands and subsequent recovery remain visible in raw events.
CLI model-cache and state-database warnings remain in stderr; a navigation tool-cache
pathname was redacted. No individual failed command is assigned a causal token cost.
One run cannot separate instruction effects from stochastic/tool/cache differences.

Standard-speed **credit-equivalent: 12.98414** across ten runs
(Vanilla 6.52861; ContextLean 6.45553).
ChatGPT login was confirmed. Official rates, verified 2026-09-30, are 50 / 5 / 300
credits per million uncached input / cached input / output tokens.
Formula: `(input − cached) × 50/M + cached × 5/M + output × 300/M`.
[Official Codex pricing](https://learn.chatgpt.com/docs/pricing).
This is **not actual credits charged or subscription allowance consumed**; those
figures are unavailable for these calls. Bootstrap and offline checks are not charged
model runs.

## Complete evidence

- [summary.json](summary.json): exact metrics, configuration, prompts, ordering and every outcome.
- [report.md](report.md): generated run tables.
- [raw runs](raw): events, stderr, original grading logs and per-run JSON; none omitted.
- [offline grading logs](offline-regrade): all ten saved solutions regraded with the frozen evaluator.
- [source snapshot](source-snapshot.zip) and [selection/hashes](source-selection.json): final product plus repaired harness and measured context.
- [saved solutions](solutions.zip): all ten complete submitted repositories.
- [measurement review](measurement-review.json): totals, negative cases, credit-equivalent and regrading results.
- [publication review](publication-review.json): hygiene, reconciliation and preservation checks.
- [quality checks](quality-checks.json): offline tests, validators, links and scans.
- [checksums](checksums.json): all evidence except this index and the checksum file itself.

Historical and diagnostic artifacts are preserved byte-for-byte. Only generated Python
cache files created by offline imports are omitted from the public source archive;
they are listed in source-selection.json and excluded from the candidate tree digest.
No measured numeric result was changed by publication. No tag or release was created.
