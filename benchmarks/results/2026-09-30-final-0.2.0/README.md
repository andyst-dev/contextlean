# Final 0.2.0 candidate validation — 2026-09-30

**Preliminary validation: one run per condition per task; ten live runs total. No statistical confidence claim. Results apply to the tested configuration, not a universal savings claim.**

**Bootstrap quality limitation:** Generated map incorrectly points to expense_report/config.json; actual config is config.json. Discovered after live execution began. Context frozen throughout all ten runs; no corrected or replacement run. Transfer checker passes structure/71 facets, but repository-path verification is incomplete. Not a clean bootstrap quality pass. The data are suitable for transparent diagnostic evidence, but not a clean final-bootstrap README headline or release validation. No replacement or additional model runs were started.

## Configuration and reproduction

- Final product implementation: `52a2c34c091f9720076cc9685fb858347d9f6dcf` (ContextLean 0.2.0).
- Model `gpt-5.6-terra`; reasoning `low`; repeats `1`.
- Window: 2026-09-30T12:15:40+00:00 to 2026-09-30T12:21:50+00:00.
- CLI `codex-cli 0.147.0`; Darwin arm64, Python 3.14.4; default service tier.
- [Exact summary and prompts](summary.json), [source archive](source-snapshot.zip), [selection/hashes](source-selection.json), [all saved solutions](solutions.zip), [checksums](checksums.json).
- [Bootstrap provenance](bootstrap-provenance.json): five independent preparations with final procedure and all 71 facets; outputs identical, frozen for the unchanged runner. Transfer ledgers are under `bootstrap-transfers/<task>/transfer.json`.
- The only uncommitted candidate files are the freshly generated fixture AGENTS.md and CLAUDE.md. They replace the historical guidance; no old generated map was reused.
- Baseline capture, local bootstrap, deterministic preparation checks and grading are outside measured execution. Local static reports do not enter the measured fixture.
- Extract `source-snapshot.zip` into a separate directory to recover exact source and generated context. Running its original `benchmarks/run_benchmark.py --model gpt-5.6-terra --reasoning low --repeat 1 --output-dir <new-empty-local-directory>` would consume ten new live runs and requires separate authorization. Do not run it as a validation check.

## Fairness and measurement

Same code/fixture state, prompt, model, reasoning, environment, sandbox and unchanged evaluator in each pair. Only AGENTS.md/CLAUDE.md differ. Fresh copy and ephemeral conversation for every run; identical temporary workspace path. Navigation is read-only; other tasks use workspace-write. User config and exec rules ignored; web disabled; approval never. Both conditions exclude the plugin, so this measures generated guidance rather than Skill invocation or bootstrap cost. Original regression tests are restored in a separate evaluation copy, and acceptance checks never enter measured repos.

All ten runs share non-instruction digest `361ede5431a41c0e1fcba8b5cecca598d3090eb5d775a25c4e128cbf0a1a12f2`, identical to the old batch. Task/evaluator hashes and executed prompts match the old batch exactly. Event parsing, execution flags, timing and grading logic match. Candidate-copy changes since the historical batch exclude Finder/linter/virtual-environment junk absent from the fixture; static-report labels and generic ungraded A/B cost handling changed, not this suite's measurements.

Order: navigation V→C, bug-fix C→V, feature V→C, refactor C→V, documentation/config V→C. Service load, cache state and model stochasticity are uncontrolled. Five pairs cannot perfectly balance order. Workspaces omit Git metadata as in the previous batch. Direct system-prompt consumption was not independently instrumented.

Input, cached input and output come directly from completed-turn usage. Cached input is included in input; total=input+output. Optional reasoning usage is retained but never added again. Commands count unique command_execution ids, including failures, not all tool calls. File reads/all tool calls remain unavailable/null. Wall time is recorded monotonic process duration excluding evaluator time; it cannot be reconstructed from JSONL alone.

## Every run

| Task | Condition | Input | Cached | Output | Total | Commands | Seconds | Success / acceptance / regression | Evidence |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| navigation | vanilla | 47,525 | 14,080 | 316 | 47,841 | 2 | 15.12762 | PASS / PASS / PASS | [events](raw/navigation-1-vanilla/events.jsonl), [diagnostics](raw/navigation-1-vanilla/events.stderr.txt), [record](raw/navigation-1-vanilla/run.json), [grading](raw/navigation-1-vanilla/evaluation.txt), [offline regrade](regrading/navigation-1-vanilla/evaluation.txt) |
| navigation | contextlean | 43,006 | 27,136 | 332 | 43,338 | 2 | 14.52009 | PASS / PASS / PASS | [events](raw/navigation-1-contextlean/events.jsonl), [diagnostics](raw/navigation-1-contextlean/events.stderr.txt), [record](raw/navigation-1-contextlean/run.json), [grading](raw/navigation-1-contextlean/evaluation.txt), [offline regrade](regrading/navigation-1-contextlean/evaluation.txt) |
| bug-fix | contextlean | 60,260 | 42,240 | 968 | 61,228 | 4 | 29.89421 | PASS / PASS / PASS | [events](raw/bug-fix-1-contextlean/events.jsonl), [diagnostics](raw/bug-fix-1-contextlean/events.stderr.txt), [record](raw/bug-fix-1-contextlean/run.json), [grading](raw/bug-fix-1-contextlean/evaluation.txt), [offline regrade](regrading/bug-fix-1-contextlean/evaluation.txt) |
| bug-fix | vanilla | 69,935 | 63,232 | 883 | 70,818 | 3 | 32.28483 | PASS / PASS / PASS | [events](raw/bug-fix-1-vanilla/events.jsonl), [diagnostics](raw/bug-fix-1-vanilla/events.stderr.txt), [record](raw/bug-fix-1-vanilla/run.json), [grading](raw/bug-fix-1-vanilla/evaluation.txt), [offline regrade](regrading/bug-fix-1-vanilla/evaluation.txt) |
| feature | vanilla | 74,057 | 54,272 | 1,579 | 75,636 | 3 | 48.57418 | PASS / PASS / PASS | [events](raw/feature-1-vanilla/events.jsonl), [diagnostics](raw/feature-1-vanilla/events.stderr.txt), [record](raw/feature-1-vanilla/run.json), [grading](raw/feature-1-vanilla/evaluation.txt), [offline regrade](regrading/feature-1-vanilla/evaluation.txt) |
| feature | contextlean | 130,612 | 107,008 | 2,918 | 133,530 | 4 | 74.95339 | PASS / PASS / PASS | [events](raw/feature-1-contextlean/events.jsonl), [diagnostics](raw/feature-1-contextlean/events.stderr.txt), [record](raw/feature-1-contextlean/run.json), [grading](raw/feature-1-contextlean/evaluation.txt), [offline regrade](regrading/feature-1-contextlean/evaluation.txt) |
| refactor | contextlean | 106,944 | 95,488 | 1,652 | 108,596 | 4 | 44.63287 | PASS / PASS / PASS | [events](raw/refactor-1-contextlean/events.jsonl), [diagnostics](raw/refactor-1-contextlean/events.stderr.txt), [record](raw/refactor-1-contextlean/run.json), [grading](raw/refactor-1-contextlean/evaluation.txt), [offline regrade](regrading/refactor-1-contextlean/evaluation.txt) |
| refactor | vanilla | 98,960 | 91,648 | 1,097 | 100,057 | 4 | 34.07208 | PASS / PASS / PASS | [events](raw/refactor-1-vanilla/events.jsonl), [diagnostics](raw/refactor-1-vanilla/events.stderr.txt), [record](raw/refactor-1-vanilla/run.json), [grading](raw/refactor-1-vanilla/evaluation.txt), [offline regrade](regrading/refactor-1-vanilla/evaluation.txt) |
| documentation-config | vanilla | 87,818 | 76,288 | 1,076 | 88,894 | 4 | 35.72600 | PASS / PASS / PASS | [events](raw/documentation-config-1-vanilla/events.jsonl), [diagnostics](raw/documentation-config-1-vanilla/events.stderr.txt), [record](raw/documentation-config-1-vanilla/run.json), [grading](raw/documentation-config-1-vanilla/evaluation.txt), [offline regrade](regrading/documentation-config-1-vanilla/evaluation.txt) |
| documentation-config | contextlean | 122,494 | 111,616 | 1,173 | 123,667 | 5 | 36.41365 | PASS / PASS / PASS | [events](raw/documentation-config-1-contextlean/events.jsonl), [diagnostics](raw/documentation-config-1-contextlean/events.stderr.txt), [record](raw/documentation-config-1-contextlean/run.json), [grading](raw/documentation-config-1-contextlean/evaluation.txt), [offline regrade](regrading/documentation-config-1-contextlean/evaluation.txt) |

## Pair comparison and all negative cases

| Task | Total tokens V / C | Token difference | Seconds V / C | Time difference | Commands V / C | Success V / C |
|---|---:|---:|---:|---:|---:|---|
| navigation | 47,841 / 43,338 | -9.41% | 15.12762 / 14.52009 | -4.02% | 2 / 2 | True / True |
| bug-fix | 70,818 / 61,228 | -13.54% | 32.28483 / 29.89421 | -7.40% | 3 / 4 | True / True |
| feature | 75,636 / 133,530 | +76.54% | 48.57418 / 74.95339 | +54.31% | 3 / 4 | True / True |
| refactor | 100,057 / 108,596 | +8.53% | 34.07208 / 44.63287 | +31.00% | 4 / 4 | True / True |
| documentation-config | 88,894 / 123,667 | +39.12% | 35.72600 / 36.41365 | +1.92% | 4 / 5 | True / True |

- **navigation**: ContextLean higher for cached_input_tokens (14,080 → 27,136, +92.73%), output_tokens (316 → 332, +5.06%).
- **bug-fix**: ContextLean higher for output_tokens (883 → 968, +9.63%), command_calls (3 → 4, +33.33%).
- **feature**: ContextLean higher for input_tokens (74,057 → 130,612, +76.37%), cached_input_tokens (54,272 → 107,008, +97.17%), output_tokens (1,579 → 2,918, +84.80%), total_tokens (75,636 → 133,530, +76.54%), command_calls (3 → 4, +33.33%), duration_seconds (48.57418 → 74.95339, +54.31%).
- **refactor**: ContextLean higher for input_tokens (98,960 → 106,944, +8.07%), cached_input_tokens (91,648 → 95,488, +4.19%), output_tokens (1,097 → 1,652, +50.59%), total_tokens (100,057 → 108,596, +8.53%), duration_seconds (34.07208 → 44.63287, +31.00%).
- **documentation-config**: ContextLean higher for input_tokens (87,818 → 122,494, +39.49%), cached_input_tokens (76,288 → 111,616, +46.31%), output_tokens (1,076 → 1,173, +9.01%), total_tokens (88,894 → 123,667, +39.12%), command_calls (4 → 5, +25.00%), duration_seconds (35.72600 → 36.41365, +1.92%).

## Aggregate within this batch

| Metric | Vanilla | ContextLean | C vs V |
|---|---:|---:|---:|
| input_tokens | 378,295 | 463,316 | +22.47% |
| cached_input_tokens | 299,520 | 383,488 | +28.03% |
| output_tokens | 4,951 | 7,043 | +42.25% |
| total_tokens | 383,246 | 470,359 | +22.73% |
| command_calls | 16 | 19 | +18.75% |
| duration_seconds | 165.78472 | 200.41420 | +20.89% |
| task_success | 5/5 (100%) | 5/5 (100%) | Same |
| acceptance_passed | 5/5 (100%) | 5/5 (100%) | Same |
| tests_passed | 5/5 (100%) | 5/5 (100%) | Same |
| agent_tests_passed | 5/5 (100%) | 5/5 (100%) | Same |

## Previous bootstrap vs final bootstrap

The [historical batch](../2026-09-30-validation/README.md) is retained byte-for-byte. Its 0.1.0 label describes the historical archived candidate, not the final 0.2.0 implementation. These are separate validation series; neither pooled results nor repeated-trial confidence is claimed.

| Condition | Metric | Previous | Final | Absolute difference | Relative difference |
|---|---|---:|---:|---:|---:|
| vanilla | input_tokens | 396,727 | 378,295 | -18,432 | -4.65% |
| vanilla | cached_input_tokens | 294,400 | 299,520 | 5,120 | +1.74% |
| vanilla | output_tokens | 6,645 | 4,951 | -1,694 | -25.49% |
| vanilla | total_tokens | 403,372 | 383,246 | -20,126 | -4.99% |
| vanilla | command_calls | 15 | 16 | 1 | +6.67% |
| vanilla | duration_seconds | 188.28271 | 165.78472 | -22.49799 | -11.95% |
| contextlean | input_tokens | 350,329 | 463,316 | 112,987 | +32.25% |
| contextlean | cached_input_tokens | 279,296 | 383,488 | 104,192 | +37.31% |
| contextlean | output_tokens | 4,978 | 7,043 | 2,065 | +41.48% |
| contextlean | total_tokens | 355,307 | 470,359 | 115,052 | +32.38% |
| contextlean | command_calls | 13 | 19 | 6 | +46.15% |
| contextlean | duration_seconds | 149.85422 | 200.41420 | 50.55998 | +33.74% |

Success remains 5/5 in each condition in both batches. The observed token/time/command differences are shown in full above. Their cause cannot be assigned to semantic bootstrap changes: there is one observation per task/condition, Vanilla changes too, cache/service/model state is uncontrolled, and the new generated map has a known path error. No variance, confidence interval, significance or universal effect is established.

| Task | Previous V / C total | Final V / C total | ContextLean change |
|---|---:|---:|---:|
| navigation | 48,156 / 26,441 | 47,841 / 43,338 | +63.90% |
| bug-fix | 88,404 / 59,206 | 70,818 / 61,228 | +3.42% |
| feature | 109,417 / 97,114 | 75,636 / 133,530 | +37.50% |
| refactor | 72,376 / 84,130 | 100,057 / 108,596 | +29.08% |
| documentation-config | 85,019 / 88,416 | 88,894 / 123,667 | +39.87% |

## Offline quality and cost

All ten saved solutions were regraded offline with the frozen acceptance evaluator and original regression tests. Results match the saved outcomes; usage and command counts reconcile with raw events; input/guidance preservation and read-only navigation were checked. See [machine-readable measurement review](measurement-review.json). Archive/fixture/task/evaluator hashes and public text/archive hygiene were checked. No public evidence was rewritten to remove a failure or unfavorable result.

ChatGPT authentication was confirmed. Measured usage totals 841,611 input tokens (683,008 cached) and 11,994 output tokens. Standard-speed **credit-equivalent: 14.94339** across all ten runs. Calculation: ((input−cached)×50 + cached×5 + output×300)/1,000,000. [Official rates](https://learn.chatgpt.com/docs/pricing) verified 2026-09-30. Actual credits charged, subscription usage and currency cost are unavailable; this calculation does not claim a charge. Per-run equivalents are in the measurement review.

State-database warnings occurred in all ten runs. Model-cache schema warnings occurred on navigation Vanilla, both feature runs and both refactor runs. Recovered patch rejections occurred on ContextLean feature, refactor and documentation/config. Failed Git checks occurred on ContextLean navigation, both bug fixes, ContextLean feature, both refactors and ContextLean documentation/config; workspaces have no Git metadata. A sandbox warning occurred on ContextLean navigation. These uneven diagnostics may inflate either condition; their effects cannot be isolated. Per-run flags are in the measurement review.

Diagnostics, including recovered CLI/patch/Git errors, are retained verbatim after capture-time path redaction. Raw JSONL cannot establish missing tool/file metrics or an actual subscription charge.

## README and release suitability

Retain the headline table as explicitly historical, and link this diagnostic candidate batch. Do not use these observations as a clean final-bootstrap headline: correct map-path verification requires a separately authorized future validation. No extra live repetitions, push, tag or release occurred. The evidence supports reporting exactly what happened, including regressions and the preparation defect. It does not clear a new benchmark release gate.
