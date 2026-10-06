# Balanced product-change validation

**Recommendation: keep Balanced.** All three Balanced solutions and all three Old solutions pass submitted tests, original regression tests and acceptance tests, both in the harness and in independent post-run regrading. No material retained-contract regression or observed harness contamination was found.

This is a six-run product-change validation, not a new public headline benchmark. The historical 30-run v0.2.1 study remains unchanged. No README performance headline, product code, adapter or harness behavior was changed. No session was retried or reordered. No statistical-significance claim is made from three pairs.

## Frozen inputs

- Adapter: `43972cb610755dde7a2866595a8e1f34f2b2d907`; [Quality CI passed](https://github.com/andyst-dev/contextlean/actions/runs/37365706020).
- Old: `ae8653b123bdb4c686ee36825c80db851c8595ea`.
- Balanced: `1a6e67fb9e5c3d5a91ca89a9f5466d2fa037ea52`.
- Model: `gpt-5.6-sol`; reasoning: `high`; task: Refactor only; harness v4; adapter schema 1; coverage parser v2.
- Automatic guidance: Old 5,486 bytes; Balanced 4,752 bytes. Old also has a 3,922-byte conditional reference. Exact filenames, bytes and hashes are in [products.json](products.json).
- Six-session order was saved before the first model call: Old, Balanced, Balanced, Old, Old, Balanced.

## All observations

Input includes cached input; uncached = input − cached. Total = input + output. Reasoning output is already included in output. Wall time measures the provider session, excluding preparation and offline grading.

| Slot | Pair | Condition | Input | Cached | Uncached | Output | Total | Seconds | Commands | Nonzero exits | Denied | Grading |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1 | old | 82,241 | 66,432 | 15,809 | 1,561 | 83,802 | 41.480 | 4 | 0 | 0 | PASS / PASS / PASS |
| 2 | 1 | balanced | 81,767 | 69,632 | 12,135 | 1,553 | 83,320 | 40.700 | 4 | 1 | 0 | PASS / PASS / PASS |
| 3 | 2 | balanced | 99,125 | 85,888 | 13,237 | 2,233 | 101,358 | 56.206 | 9 | 0 | 0 | PASS / PASS / PASS |
| 4 | 2 | old | 99,146 | 90,368 | 8,778 | 2,050 | 101,196 | 52.323 | 5 | 0 | 0 | PASS / PASS / PASS |
| 5 | 3 | old | 114,255 | 105,216 | 9,039 | 1,961 | 116,216 | 54.997 | 6 | 0 | 0 | PASS / PASS / PASS |
| 6 | 3 | balanced | 80,848 | 69,120 | 11,728 | 1,233 | 82,081 | 36.723 | 4 | 0 | 0 | PASS / PASS / PASS |

Grading columns mean submitted tests / untouched original regression tests / independent acceptance tests. Slot 2’s nonzero command exit is the trailing `rg` caller search finding no matches; it is not a failed test, denied command or runtime/cache diagnostic.

## Descriptive statistics

| Condition | Mean total tokens | Median | Min | Max | Sample SD | Mean seconds | Median seconds | Commands in run order |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| old | 100,404.67 | 101,196 | 83,802 | 116,216 | 16,221.48 | 49.600 | 52.323 | [4, 5, 6] |
| balanced | 88,919.67 | 83,320 | 82,081 | 101,358 | 10,789.71 | 44.543 | 40.700 | [4, 9, 4] |

Old command count: mean 5, median 5, min/max 4/6, sample SD 1. Balanced: mean 5.667, median 4, min/max 4/9, sample SD 2.887. Full distributions are in [analysis.json](analysis.json).

## Paired differences

Balanced minus Old; percentages use that pair’s Old total tokens as denominator.

| Pair | Slots (Old / Balanced) | Total tokens | Percent | Seconds | Commands |
|---:|---|---:|---:|---:|---:|
| 1 | 1 / 2 | -482 | -0.575% | -0.781 | +0 |
| 2 | 4 / 3 | +162 | +0.160% | +3.884 | +4 |
| 3 | 5 / 6 | -34,135 | -29.372% | -18.274 | -2 |

Paired token difference: mean **-11,485**, median **-482**, minimum/maximum **-34,135 / +162**, range width **34,297**. Mean paired time difference is −5.057 seconds; mean command difference is +0.667. The third pair dominates the token average; these observations do not establish a repeatable performance gain.

## Behavior and observable trajectories

- Every run searches for the normalizer and relevant usages before reading the affected source/tests. Both duplicate implementations are removed or consolidated at their owner.
- Slots 1–5 extract `categories.py` and preserve both import paths. Slot 6 reuses the existing function from `filters.py`, changing only `report.py`. Both are valid implementations for this fixture; relative versus absolute imports are stylistic differences.
- Old command counts are 4, 5, 6. Balanced counts are 4, 9, 4. Balanced slot 3 reads and verifies files in separate commands, explaining the higher command count without implying a correctness regression.
- Old slots 4 and 5 add a persistent import-identity regression test and a query-behavior assertion. Balanced runs execute the complete existing suite and explicit compatibility assertions; slots 2 and 3 additionally check query behavior. The task adds no non-trivial new logic, so this test-persistence difference alone is not a contract failure.
- No Balanced solution introduces arbitrary splitting, speculative machinery, unjustified public-interface changes or observable behavior changes. Caller inspection and verification cover the affected surface. Detailed assessment: [behavioral-review.json](behavioral-review.json).
- No Old run reads the conditional architecture reference. This narrow duplication-removal task establishes guidance sufficiency for this task, not equivalence on complex architectural refactors or all retained guarantees in general.

## Grading and coverage

Each saved solution was independently regraded after all six model sessions ended. The shared grader first executes the submitted tests, restores the frozen original tests, then runs the independent Refactor acceptance evaluator. Logs are in [independent-grading/](independent-grading/). Submitted suites contain 5 tests for slots 1, 2, 3, 6 and 6 tests for slots 4, 5; original regression suites contain 5 tests and acceptance suites contain 2 tests in every run. All pass.

All initial and per-session preflights report the original five test identities with coverage digest `3ecb703b5031cfb650873bd0c0da23174187806cebd6330acdfa7f843155f29a`. Model-run verification identities/digests, including the expanded Old suites, are retained per observation in analysis.json and execution.json. Smoke assertions have no invented unittest identities.

## Integrity and evidence

- CI-green committed adapter; exact committed product generators; frozen guidance hashes checked before each call. All tracked source and historical archive hashes remain unchanged after the campaign.
- Six initial preparations and six measured-session preparations passed. Python 3.14.4, Git 2.54.0 and rg 15.2.0 match; normalized runtime/environment/PATH/sandbox/auth-policy receipts are identical.
- HOME, TMP, cache and configuration stay session-local. Cache probes have no diagnostics. Repo/tmp writes succeed; parent/outside writes and evidence/unrelated-session reads are denied. Six unique measured roots are absent after verified cleanup; no unexpected root entries were recorded.
- Task fixture bytes outside guidance, exact prompt, grader and Git policy match. Git commits repeat deterministically within each condition and differ between conditions only because tracked guidance differs.
- Exact task prompt SHA-256: `464e90080aad8fbba255ac27e48b7bd0faa0fc33098d3eba0a6c3473da7589e3`.
- Exact grader SHA-256: `3200e20da7522c1a063cda247433efcdcaf2e6f945c7cdf951dee35e624fd686`.
- [campaign/schedule.json](campaign/schedule.json), [campaign/fixture-manifest.json](campaign/fixture-manifest.json), [campaign/summary.json](campaign/summary.json), and the per-run directories contain the schedule, inputs, receipts, exposed traces and saved solutions.
- Public traces are sanitized exports. Byte-exact original provider stdout/stderr and private receipts/solutions remain in the local `.contextlean/validation/2026-10-06-balanced-product-change/campaign/private/` directory and are deliberately not published. Byte counts and decoded trace hashes were reconciled with the private originals.
- Original campaign checksums were verified before export. Host tool installation prefixes are normalized in this public copy; [publication.json](publication.json) retains the original export checksum ledgers and per-file before/after hashes. Standard system paths describe the sandbox policy and carry no private identity. [checksums.json](checksums.json) covers this separate sanitized bundle. Provider-internal caching, hidden activity and service load are outside the observable guarantees.

**Decision:** keep Balanced for the tested Refactor task. All three Balanced runs pass full grading; no material retained guarantee regresses in the observed task; isolation remains valid. Slightly higher tokens/time in pair 2 do not constitute failure.

Balanced runtime simplification validation complete.
