# Harness v4 repeated performance study

gpt-5.6-sol · high reasoning · frozen revision `ae8653b123bdb4c686ee36825c80db851c8595ea` · 30/30 model sessions.

Three independent repetitions per task and condition. All planned results are retained. No statistical significance is claimed from n=3.

## Session completion and success

Study status: complete. Classifications: {"successful-task": 30}. Failures/interruption categories: {"model-task-failure": 0, "provider-network-failure": 0, "provider-usage-limit-interruption": 0, "harness-preparation-failure": 0, "grading-failure": 0}.

Independent task successes: Vanilla 15/15; ContextLean 15/15.

## All thirty observations

| Position | Task | Rep | Condition | Input | Cached | Uncached | Output | Total | Seconds | Commands | Success |
|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | navigation | 1 | vanilla | 50361 | 40064 | 10297 | 549 | 50910 | 44.57 | 3 | True |
| 2 | navigation | 1 | contextlean | 24058 | 19584 | 4474 | 300 | 24358 | 19.17 | 1 | True |
| 3 | navigation | 2 | contextlean | 24078 | 0 | 24078 | 255 | 24333 | 14.69 | 1 | True |
| 4 | navigation | 2 | vanilla | 37353 | 23552 | 13801 | 503 | 37856 | 32.61 | 2 | True |
| 5 | navigation | 3 | vanilla | 37395 | 27264 | 10131 | 478 | 37873 | 37.00 | 2 | True |
| 6 | navigation | 3 | contextlean | 24192 | 19584 | 4608 | 364 | 24556 | 22.97 | 1 | True |
| 7 | bug-fix | 1 | vanilla | 76997 | 64896 | 12101 | 1214 | 78211 | 64.88 | 4 | True |
| 8 | bug-fix | 1 | contextlean | 78982 | 67328 | 11654 | 1385 | 80367 | 45.99 | 5 | True |
| 9 | bug-fix | 2 | contextlean | 80106 | 72832 | 7274 | 1124 | 81230 | 63.56 | 4 | True |
| 10 | bug-fix | 2 | vanilla | 62516 | 56320 | 6196 | 1072 | 63588 | 63.96 | 3 | True |
| 11 | bug-fix | 3 | vanilla | 90982 | 75520 | 15462 | 1553 | 92535 | 47.61 | 6 | True |
| 12 | bug-fix | 3 | contextlean | 79110 | 71936 | 7174 | 1305 | 80415 | 49.16 | 5 | True |
| 13 | feature | 1 | vanilla | 96787 | 83200 | 13587 | 2335 | 99122 | 91.53 | 5 | True |
| 14 | feature | 1 | contextlean | 84107 | 66688 | 17419 | 2159 | 86266 | 95.67 | 4 | True |
| 15 | feature | 2 | contextlean | 104494 | 93824 | 10670 | 3124 | 107618 | 78.32 | 4 | True |
| 16 | feature | 2 | vanilla | 96907 | 78976 | 17931 | 2801 | 99708 | 72.93 | 5 | True |
| 17 | feature | 3 | vanilla | 80641 | 67584 | 13057 | 2228 | 82869 | 56.91 | 4 | True |
| 18 | feature | 3 | contextlean | 68221 | 36736 | 31485 | 2320 | 70541 | 60.02 | 5 | True |
| 19 | refactor | 1 | vanilla | 91239 | 79360 | 11879 | 1951 | 93190 | 88.59 | 5 | True |
| 20 | refactor | 1 | contextlean | 80074 | 72448 | 7626 | 1578 | 81652 | 76.29 | 5 | True |
| 21 | refactor | 2 | contextlean | 81323 | 73472 | 7851 | 1802 | 83125 | 80.20 | 4 | True |
| 22 | refactor | 2 | vanilla | 81760 | 73856 | 7904 | 1544 | 83304 | 85.62 | 4 | True |
| 23 | refactor | 3 | vanilla | 91609 | 78336 | 13273 | 1508 | 93117 | 51.72 | 5 | True |
| 24 | refactor | 3 | contextlean | 65800 | 58624 | 7176 | 1457 | 67257 | 54.13 | 3 | True |
| 25 | documentation-config | 1 | vanilla | 77296 | 54656 | 22640 | 1291 | 78587 | 48.32 | 6 | True |
| 26 | documentation-config | 1 | contextlean | 80261 | 67328 | 12933 | 1594 | 81855 | 58.84 | 6 | True |
| 27 | documentation-config | 2 | contextlean | 79692 | 55040 | 24652 | 1268 | 80960 | 48.61 | 6 | True |
| 28 | documentation-config | 2 | vanilla | 61993 | 51840 | 10153 | 1025 | 63018 | 40.21 | 3 | True |
| 29 | documentation-config | 3 | vanilla | 90332 | 62592 | 27740 | 1418 | 91750 | 60.39 | 7 | True |
| 30 | documentation-config | 3 | contextlean | 67031 | 53888 | 13143 | 1410 | 68441 | 48.54 | 7 | True |

## Per-task condition statistics

| Task | Condition | Mean tokens | Median tokens | Min–max | Sample SD | Mean seconds | Median seconds | Commands in rep order |
|---|---|---:|---:|---:|---:|---:|---:|---|
| navigation | vanilla | 42,213.00 | 37,873.00 | 37,856–50,910 | 7,531.83 | 38.06 | 37.00 | [3, 2, 2] |
| navigation | contextlean | 24,415.67 | 24,358.00 | 24,333–24,556 | 122.17 | 18.95 | 19.17 | [1, 1, 1] |
| bug-fix | vanilla | 78,111.33 | 78,211.00 | 63,588–92,535 | 14,473.76 | 58.82 | 63.96 | [4, 3, 6] |
| bug-fix | contextlean | 80,670.67 | 80,415.00 | 80,367–81,230 | 484.99 | 52.90 | 49.16 | [5, 4, 5] |
| feature | vanilla | 93,899.67 | 99,122.00 | 82,869–99,708 | 9,557.33 | 73.79 | 72.93 | [5, 5, 4] |
| feature | contextlean | 88,141.67 | 86,266.00 | 70,541–107,618 | 18,609.53 | 78.01 | 78.32 | [4, 4, 5] |
| refactor | vanilla | 89,870.33 | 93,117.00 | 83,304–93,190 | 5,686.73 | 75.31 | 85.62 | [5, 4, 5] |
| refactor | contextlean | 77,344.67 | 81,652.00 | 67,257–83,125 | 8,767.17 | 70.21 | 76.29 | [5, 4, 3] |
| documentation-config | vanilla | 77,785.00 | 78,587.00 | 63,018–91,750 | 14,382.78 | 49.64 | 48.32 | [6, 3, 7] |
| documentation-config | contextlean | 77,085.33 | 80,960.00 | 68,441–81,855 | 7,499.58 | 52.00 | 48.61 | [6, 6, 7] |

## All fifteen paired differences

Every difference is ContextLean minus Vanilla within the same task and repetition. Negative values favor ContextLean. Percentages use Vanilla as the denominator.

| Task | Rep | Tokens Δ | Tokens Δ % | Seconds Δ | Commands Δ |
|---|---:|---:|---:|---:|---:|
| navigation | 1 | -26,552 | -52.15 | -25.40 | -2 |
| navigation | 2 | -13,523 | -35.72 | -17.91 | -1 |
| navigation | 3 | -13,317 | -35.16 | -14.03 | -1 |
| bug-fix | 1 | 2,156 | 2.76 | -18.89 | 1 |
| bug-fix | 2 | 17,642 | 27.74 | -0.41 | 1 |
| bug-fix | 3 | -12,120 | -13.10 | 1.55 | -1 |
| feature | 1 | -12,856 | -12.97 | 4.15 | -1 |
| feature | 2 | 7,910 | 7.93 | 5.40 | -1 |
| feature | 3 | -12,328 | -14.88 | 3.12 | 1 |
| refactor | 1 | -11,538 | -12.38 | -12.29 | 0 |
| refactor | 2 | -179 | -0.21 | -5.42 | 0 |
| refactor | 3 | -25,860 | -27.77 | 2.41 | -2 |
| documentation-config | 1 | 3,268 | 4.16 | 10.52 | 0 |
| documentation-config | 2 | 17,942 | 28.47 | 8.39 | 3 |
| documentation-config | 3 | -23,309 | -25.40 | -11.85 | 0 |

| Task | Mean paired tokens Δ | Median paired tokens Δ | Paired tokens Δ range | Median paired % Δ |
|---|---:|---:|---:|---:|
| navigation | -17,797.33 | -13,523.00 | [-26552, -13317] | -35.72 |
| bug-fix | 2,559.33 | 2,156.00 | [-12120, 17642] | 2.76 |
| feature | -5,758.00 | -12,328.00 | [-12856, 7910] | -12.97 |
| refactor | -12,525.67 | -11,538.00 | [-25860, -179] | -12.38 |
| documentation-config | -699.67 | 3,268.00 | [-23309, 17942] | 4.16 |

## Overall descriptive summaries

These summaries describe this fixed set of heterogeneous tasks; task pairing and the full task-level results remain above.

Across this fixed study, the descriptive sums are Vanilla 1,145,638 tokens versus ContextLean 1,042,974 (−8.96%); 886.84 versus 816.17 measured seconds (−7.97%); and 64 versus 61 command calls (−4.69%). Task medians differ: Navigation −35.72%, Bug Fix +2.76%, Feature −12.97%, Refactor −12.38%, Documentation/config +4.16%. Do not pool these controlled v4 observations with historical harness series or interpret the pooled sum as a universal effect.

Pairs: {"contextlean": 9, "vanilla": 5, "approximately-neutral": 1}. Approximately neutral means an absolute percentage difference ≤1%, fixed before execution.

Median of five per-task median paired effects: -11,538.00 tokens; -12.38%.

All 15 paired token differences: [-26552, -13523, -13317, 2156, 17642, -12120, -12856, 7910, -12328, -11538, -179, -25860, 3268, 17942, -23309]. Mean -6,844.27; median -12,120.00; range [-26,552, 17,942]; sample SD 14,350.14.

Vanilla: 15 token observations [50910, 37856, 37873, 78211, 63588, 92535, 99122, 99708, 82869, 93190, 83304, 93117, 78587, 63018, 91750]; descriptive mean 76,375.87, median 82,869.00, range [37,856, 99,708], sample SD 21,005.74. Mean time 59.12 s; median time 56.91 s. Descriptive totals: {"input_tokens": 1124168, "cached_input_tokens": 918016, "uncached_input_tokens": 206152, "output_tokens": 21470, "total_tokens": 1145638, "duration_seconds": 886.8409553347155, "command_calls": 64}.

Contextlean: 15 token observations [24358, 24333, 24556, 80367, 81230, 80415, 86266, 107618, 70541, 81652, 83125, 67257, 81855, 80960, 68441]; descriptive mean 69,531.60, median 80,415.00, range [24,333, 107,618], sample SD 25,115.78. Mean time 54.41 s; median time 54.13 s. Descriptive totals: {"input_tokens": 1021529, "cached_input_tokens": 829312, "uncached_input_tokens": 192217, "output_tokens": 21445, "total_tokens": 1042974, "duration_seconds": 816.1659107068554, "command_calls": 61}.

## Observable repetition variance

Counts below describe shell calls containing search/read/Git/verification commands and can overlap. They do not measure file-open counts. Detailed commands, results, solution diffs, exact test identities and coverage digests are preserved.

| Task | Rep | Condition | Searches | Reads | Git | Verification | Commands | Failed | Added tests | Tool merged bytes | Cached / uncached |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| navigation | 1 | vanilla | 1 | 1 | 0 | 2 | 3 | 1 | 0 | 2748 | 40064 / 10297 |
| navigation | 1 | contextlean | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2353 | 19584 / 4474 |
| navigation | 2 | contextlean | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2284 | 0 / 24078 |
| navigation | 2 | vanilla | 1 | 1 | 0 | 2 | 2 | 0 | 0 | 3063 | 23552 / 13801 |
| navigation | 3 | vanilla | 1 | 1 | 0 | 2 | 2 | 0 | 0 | 3542 | 27264 / 10131 |
| navigation | 3 | contextlean | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 2355 | 19584 / 4608 |
| bug-fix | 1 | vanilla | 1 | 1 | 2 | 1 | 4 | 0 | 1 | 5810 | 64896 / 12101 |
| bug-fix | 1 | contextlean | 0 | 2 | 2 | 2 | 5 | 0 | 1 | 5612 | 67328 / 11654 |
| bug-fix | 2 | contextlean | 1 | 1 | 2 | 2 | 4 | 0 | 1 | 7266 | 72832 / 7274 |
| bug-fix | 2 | vanilla | 1 | 1 | 2 | 1 | 3 | 0 | 1 | 4866 | 56320 / 6196 |
| bug-fix | 3 | vanilla | 1 | 4 | 3 | 1 | 6 | 0 | 1 | 6209 | 75520 / 15462 |
| bug-fix | 3 | contextlean | 0 | 2 | 2 | 2 | 5 | 0 | 1 | 5602 | 71936 / 7174 |
| feature | 1 | vanilla | 1 | 1 | 2 | 2 | 5 | 0 | 3 | 9088 | 83200 / 13587 |
| feature | 1 | contextlean | 1 | 1 | 2 | 1 | 4 | 0 | 2 | 10809 | 66688 / 17419 |
| feature | 2 | contextlean | 1 | 2 | 2 | 2 | 4 | 0 | 3 | 11469 | 93824 / 10670 |
| feature | 2 | vanilla | 1 | 1 | 2 | 2 | 5 | 0 | 3 | 10346 | 78976 / 17931 |
| feature | 3 | vanilla | 1 | 1 | 2 | 1 | 4 | 0 | 3 | 9469 | 67584 / 13057 |
| feature | 3 | contextlean | 0 | 2 | 2 | 2 | 5 | 0 | 3 | 9286 | 36736 / 31485 |
| refactor | 1 | vanilla | 1 | 1 | 4 | 2 | 5 | 0 | 0 | 4880 | 79360 / 11879 |
| refactor | 1 | contextlean | 1 | 2 | 2 | 1 | 5 | 0 | 0 | 6387 | 72448 / 7626 |
| refactor | 2 | contextlean | 1 | 3 | 3 | 2 | 4 | 0 | 2 | 4962 | 73472 / 7851 |
| refactor | 2 | vanilla | 2 | 1 | 3 | 1 | 4 | 0 | 0 | 6722 | 73856 / 7904 |
| refactor | 3 | vanilla | 2 | 2 | 4 | 1 | 5 | 1 | 0 | 5912 | 78336 / 13273 |
| refactor | 3 | contextlean | 2 | 2 | 3 | 1 | 3 | 0 | 2 | 6444 | 58624 / 7176 |
| documentation-config | 1 | vanilla | 1 | 2 | 2 | 3 | 6 | 0 | 0 | 5260 | 54656 / 22640 |
| documentation-config | 1 | contextlean | 1 | 1 | 2 | 3 | 6 | 0 | 0 | 7060 | 67328 / 12933 |
| documentation-config | 2 | contextlean | 1 | 1 | 2 | 3 | 6 | 0 | 0 | 6827 | 55040 / 24652 |
| documentation-config | 2 | vanilla | 1 | 1 | 2 | 1 | 3 | 0 | 0 | 4213 | 51840 / 10153 |
| documentation-config | 3 | vanilla | 1 | 2 | 2 | 3 | 7 | 0 | 0 | 5445 | 62592 / 27740 |
| documentation-config | 3 | contextlean | 1 | 1 | 3 | 3 | 7 | 0 | 0 | 5178 | 53888 / 13143 |

See [the task-by-task variance review](variance-review.md) for concrete implementation, recovery, Git and verification differences. Implementation choices and recovery are also inspectable in each solution.diff and in commands.md. variance.json retains the observed changed files, added test identities, coverage/digests and exact output-byte totals; no hidden reasoning or per-action causal token cost is inferred.

Controlled environment: frozen source and prompt bytes, clean deterministic Git baselines, Python 3.14.4, Git 2.54.0, rg 15.2.0, native permissions, isolated HOME/TMP/cache/config, condition policy parity, fresh roots and verified cleanup.

Observed agent trajectory: the exposed searches/reads, code changes, Git checks, failures/recovery and verification decisions differ between repetitions. Those differences are outcomes of the sessions, not controlled treatment inputs.

Uncontrolled provider state: cache warmth, service load, opaque request handling and model stochasticity. Cached/uncached composition is measured, but does not identify a cause of a paired token/time difference.

## Usage and cost

Known primary usage: {"input_tokens": 2145697, "cached_input_tokens": 1747328, "uncached_input_tokens": 398369, "output_tokens": 42915, "total_tokens": 2188612, "duration_seconds": 1703.006866041571, "command_calls": 125}. Actual provider cost and actual credits spent are unavailable (null).

Dated credit-equivalent: 78.77, using the frozen 2026-09-30 rate card. This is an estimate, not actual credits spent or a claim about current pricing.

## Evidence and contamination review

Frozen source unchanged: True; schedule unchanged: True; unique inspected roots: 90; all absent after cleanup. No harness behavior modifications or session retries.

Public evidence excludes private originals. Individual harness artifacts retain local sequence 1–6; summary.json, observations.json and schedule.json map each to the global position 1–30. Harness-produced files are preserved unchanged. All completed solutions were independently offline-regraded with submitted tests, restored original regression tests and acceptance tests.

[Schedule](schedule.json) · [Methodology](methodology.md) · [Summary](summary.json) · [Statistics](statistics.json) · [Grading](grading.json) · [Variance](variance.json) · [Commands](commands.md) · [Measurement review](measurement-review.json) · [Checksums](checksums.json)

The public project README and prior evidence were not changed. This study alone makes no statistical-significance or universal performance claim.
