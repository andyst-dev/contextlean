# Offline root-cause analysis — final 0.2.0 diagnostic batch

**No model calls. The ten-run diagnostic batch is unchanged and invalid for headline performance comparison because its preparation contained an incorrect map entry.** Neither its results nor raw logs are corrected, replaced, pooled or promoted to a benchmark headline.

## Exact cause: D — manual preparation error

The preparing agent hard-coded this literal in the `intro` string at line 33 of the ephemeral `prepare_contextlean_final.py` script:

```md
- `expense_report/config.json`: default currency; CLI options can override it.
```

The original script was preserved locally as `.contextlean/rca/original-preparation.py` before repair. Original SHA-256: `16b0eb034d39a87d9a685c6a78adcdaac5d7a4849902b90f5f1d74bd33a012a8`. This is an agent-authored string, not a path emitted by ContextLean product code, the evaluator or a task prompt. The original committed sample map correctly says `config.json`; the actual CLI resolves its parent repository directory and reads `config.json`.

[Machine-readable source chain](root-cause.json):

| Stage | Exact source | What happened |
|---|---|---|
| Preparation | Original script line 33 | Incorrect literal typed in project-map intro |
| Assembly | Line 36 | Intro joined with permanent-rule paragraphs; no path transformation |
| Bootstrap application | Lines 42–43 | Local agent preparation captures baseline then writes the same intro to five AGENTS.md files; no separate paid bootstrap model invocation |
| Inadequate verification | Lines 48–58 | Transfer hashes validate rule sections, not map entries. Example commands/tests run the actual product and succeed against root config. Required map-path verification was omitted |
| Freeze | Line 62 | Same unchecked text written to temporary candidate fixture |
| Runner at release candidate | `run_benchmark.py`: `copy_repository(FIXTURE, workspace)` | ContextLean receives the map verbatim; Vanilla removes it. Product-state hashes do not establish map accuracy |
| Frozen evidence | [source-snapshot.zip](../../results/2026-09-30-final-0.2.0/source-snapshot.zip), `benchmarks/fixtures/expense-report/AGENTS.md:11` | Bad entry survives in frozen source and all five saved ContextLean maps |
| Task prompts | `suite.json` / `task_prompt` | Same exact prompts in both conditions; no bad path |
| Capture preprocessing | `save_raw_run` | Workspace/home path redaction only; no map-path generation |

The committed Bootstrap procedure section 6 already requires accurate documented paths and responsibilities. Its transfer checker explicitly verifies structural transfer integrity, not natural-language ownership or every project-map entry. The preparation agent failed the required filesystem review; the development runner lacked a fail-fast backstop. The root defect is classified only as **D**, with the missing harness guard recorded as an escape condition. No ContextLean product bug was found.

## Bad-path impact in each ContextLean run

Presence in all five frozen maps is established. Direct system-prompt loading and private reasoning were not instrumented; presence alone does not prove an access or a causal effect.

| Task | Wrong path visible in trace? | Failed path lookups caused by it | Path-specific recovery | Solution impact |
|---|---|---|---|---|
| Navigation | No | None observed | None | No observed config-path effect; correct JSON result |
| Bug fix | No | None observed | None | Actual root resolution appears in read CLI/tests; correct fix |
| Feature | No | None observed | None | Reads CLI with correct root resolution; no bad-path access |
| Refactor | No | None observed | None | Reads tests with correct config path; no bad-path access |
| Documentation/config | Yes | Executed `rg` and `sed` each report nonexistent `expense_report/config.json` | One dedicated file-listing event, followed by a correct-path combined search/read event | Exploration detoured; final solution correctly edits root `config.json` and README |

Documentation/config details from [ContextLean events](../../results/2026-09-30-final-0.2.0/raw/documentation-config-1-contextlean/events.jsonl):

- Line 5 / `item_1`: command includes wrong-path rg/sed, but preceding `git status --short &&` fails, so those lookups never execute. This is a Git failure, not a failed path lookup.
- Line 7 / `item_2`: rg and sed execute on the bad path and each emit a missing-file message. Overall exit code is **0** because the later README read succeeds; exit-code-only inspection would miss this defect.
- Line 9 / `item_3`: `rg --files` discovers root `config.json`.
- Line 11 / `item_4`: searches/reads root config, CLI and tests. This is visible recovery/verification, not a measurable counterfactual token cost.
- Line 13 / `item_5`: successful patch updates only `config.json` and README; no erroneous file is created.

The documentation/config stderr also records a rejected patch. Its rejected arguments are absent from JSONL; there is no evidence tying that patch rejection to the bad config path. No token amount is attributed to the typo.

## Task-by-task Vanilla / ContextLean traces

All task success, acceptance and original regression results are PASS. This does not make the preparation valid. Cached input is a subset of input, not an extra amount to add to totals.

| Task | Total tokens V / C | C difference | Commands V / C | Wall seconds V / C |
|---|---:|---:|---:|---:|
| navigation | 47,841 / 43,338 | -9.41% | 2 / 2 | 15.13 / 14.52 |
| bug-fix | 70,818 / 61,228 | -13.54% | 3 / 4 | 32.28 / 29.89 |
| feature | 75,636 / 133,530 | +76.54% | 3 / 4 | 48.57 / 74.95 |
| refactor | 100,057 / 108,596 | +8.53% | 4 / 4 | 34.07 / 44.63 |
| documentation-config | 88,894 / 123,667 | +39.12% | 4 / 5 | 35.73 / 36.41 |

### navigation

No recorded bad-path access. ContextLean git-status command short-circuits search/CLI; second command repeats them without Git. Vanilla lists and searches the whole repository, reads storage/report/tests, then runs CLI; ContextLean targeted search plus CLI only. Same command count, less aggregate input but slightly more output. Causal token allocation unavailable.

Both run the sample CLI; no agent test suite invocation.

Correct final navigation JSON, identical in both conditions.

Trace command sequence (the ids and line numbers refer to the unmodified saved logs):

**vanilla**: [events](../../results/2026-09-30-final-0.2.0/raw/navigation-1-vanilla/events.jsonl), [diagnostics](../../results/2026-09-30-final-0.2.0/raw/navigation-1-vanilla/events.stderr.txt).

- Line 5, `item_1`, exit 0: `/bin/zsh -lc 'rg --files && rg -n "csv|category|total|argparse|__main__|sample" .'`
- Line 7, `item_2`, exit 0: `/bin/zsh -lc "sed -n '1,160p' expense_report/storage.py && sed -n '1,200p' expense_report/report.py && sed -n '1,160p' tests/test_expenses.py && python3 -m expense_report.cli data/sample.csv"`

**contextlean**: [events](../../results/2026-09-30-final-0.2.0/raw/navigation-1-contextlean/events.jsonl), [diagnostics](../../results/2026-09-30-final-0.2.0/raw/navigation-1-contextlean/events.stderr.txt).

- Line 5, `item_1`, exit 128: `/bin/zsh -lc 'git status --short && rg -n "def |amount|total|cli" expense_report tests/test_expenses.py && python3 -m expense_report.cli data/sample.csv'`
- Line 7, `item_2`, exit 0: `/bin/zsh -lc 'rg -n "def |amount|total|cli" expense_report tests/test_expenses.py; python3 -m expense_report.cli data/sample.csv'`


### bug-fix

Both read cli.py and tests/test_expenses.py containing the actual root config resolution. ContextLean starts with targeted three-file reads; Vanilla starts with a broad listing/search and reads four files including sample CSV. Both fail one Git command; ContextLean does not rerun its blocked search, proceeding from already-read code. ContextLean runs three CLI examples vs one Vanilla, and both leave six tests. Its aggregate input is lower; output higher.

Both run six tests once; C targeted discovery, V full discovery, same module. C runs three CLI examples, V one.

Both normalize the query in the existing filter and add the requested CLI regression.

Trace command sequence (the ids and line numbers refer to the unmodified saved logs):

**vanilla**: [events](../../results/2026-09-30-final-0.2.0/raw/bug-fix-1-vanilla/events.jsonl), [diagnostics](../../results/2026-09-30-final-0.2.0/raw/bug-fix-1-vanilla/events.stderr.txt).

- Line 5, `item_1`, exit 0: `/bin/zsh -lc "rg --files -g '"'!*__pycache__*'"' && rg -n \"category|--category|sample.csv\" ."`
- Line 7, `item_2`, exit 128: `/bin/zsh -lc "sed -n '1,160p' expense_report/filters.py && sed -n '1,200p' tests/test_expenses.py && sed -n '1,120p' expense_report/cli.py && sed -n '1,80p' data/sample.csv && git status --short"`
- Line 12, `item_5`, exit 0: `/bin/zsh -lc "python3 -m unittest discover -s tests -v && python3 -m expense_report.cli data/sample.csv --category ' FOOD ' --currency GBP"`

**contextlean**: [events](../../results/2026-09-30-final-0.2.0/raw/bug-fix-1-contextlean/events.jsonl), [diagnostics](../../results/2026-09-30-final-0.2.0/raw/bug-fix-1-contextlean/events.stderr.txt).

- Line 5, `item_1`, exit 0: `/bin/zsh -lc "sed -n '1,240p' expense_report/cli.py && sed -n '1,200p' expense_report/filters.py && sed -n '1,260p' tests/test_expenses.py"`
- Line 7, `item_2`, exit 128: `/bin/zsh -lc 'git status --short && rg -n "category|filter" expense_report tests/test_expenses.py'`
- Line 12, `item_5`, exit 0: `/bin/zsh -lc "python3 -m expense_report.cli data/sample.csv --category ' FOOD ' && python3 -m expense_report.cli data/sample.csv --category food --currency GBP && python3 -m expense_report.cli data/sample.csv"`
- Line 13, `item_4`, exit 0: `/bin/zsh -lc 'python3 -m unittest discover -s tests -p test_expenses.py -v'`


### feature

C Git-before-search fails, requiring another discovery command; V discovery succeeds immediately. C explicitly reads five files (cli/filter/tests/storage/README), V four (cli/filter/tests/sample CSV). C stderr records one rejected patch; subsequent successful file-change includes README in addition to three code/test files. C uses combined select_expenses plus a compatibility select_category wrapper; V uses select_min_amount after select_category. Both add three tests (eight total); C runs that suite twice vs V once. V also fails git diff after successful verification and emits a large usage message. Bad config path is never accessed.

C eight-test suite twice plus two CLI examples; V eight-test suite once plus the same examples and failed git diff.

Both pass all acceptance/regression checks. C modifies four files; V three. Valid ownership/reuse rules are not removed.

Trace command sequence (the ids and line numbers refer to the unmodified saved logs):

**vanilla**: [events](../../results/2026-09-30-final-0.2.0/raw/feature-1-vanilla/events.jsonl), [diagnostics](../../results/2026-09-30-final-0.2.0/raw/feature-1-vanilla/events.stderr.txt).

- Line 5, `item_1`, exit 0: `/bin/zsh -lc "rg --files -g '"'!*node_modules*'"' && rg -n \"category|expense|argparse|min\" ."`
- Line 7, `item_2`, exit 0: `/bin/zsh -lc "sed -n '1,220p' expense_report/cli.py && sed -n '1,160p' expense_report/filters.py && sed -n '1,220p' tests/test_expenses.py && sed -n '1,80p' data/sample.csv"`
- Line 12, `item_5`, exit 129: `/bin/zsh -lc 'python3 -m unittest discover -s tests -v && python3 -m expense_report.cli data/sample.csv --min-amount 10 && python3 -m expense_report.cli data/sample.csv --category food --min-amount 10 && git diff --check && git diff'`

**contextlean**: [events](../../results/2026-09-30-final-0.2.0/raw/feature-1-contextlean/events.jsonl), [diagnostics](../../results/2026-09-30-final-0.2.0/raw/feature-1-contextlean/events.stderr.txt).

- Line 5, `item_1`, exit 128: `/bin/zsh -lc "git status --short && rg -n --glob '"'!AGENTS.md'"' \"category|filter|parse_args|amount\" expense_report tests/test_expenses.py"`
- Line 7, `item_2`, exit 0: `/bin/zsh -lc "pwd; rg -n --glob '"'!AGENTS.md'"' \"category|filter|parse_args|amount\" expense_report tests/test_expenses.py; rg --files -g '.git' -g 'pyproject.toml' -g 'setup.cfg' -g 'README.md'"`
- Line 9, `item_3`, exit 0: `/bin/zsh -lc "sed -n '1,160p' expense_report/cli.py; sed -n '1,160p' expense_report/filters.py; sed -n '1,220p' tests/test_expenses.py; sed -n '1,120p' expense_report/storage.py; sed -n '1,140p' README.md"`
- Line 14, `item_6`, exit 0: `/bin/zsh -lc 'python3 -m unittest discover -s tests -p test_expenses.py -v && python3 -m unittest discover -s tests -v && python3 -m expense_report.cli data/sample.csv --min-amount 10 && python3 -m expense_report.cli data/sample.csv --category food --min-amount 10'`


### refactor

Both have four command events. C fails Git before search, then repeats search; V fails Git after a file listing. Both read filtering/report/tests and extract categories.py with compatible exports. C stderr records one rejected patch and saved solution adds a permanent compatibility test (six tests); V leaves five tests and executes a standalone compatibility assertion script. C also runs two CLI examples. Source read stdout is not larger in C; aggregates cannot isolate the costs of map, recovery or tests.

C six tests plus two CLI examples; V five tests plus import/normalization assertion script.

Same shared-helper design; C additionally modifies tests/test_expenses.py.

Trace command sequence (the ids and line numbers refer to the unmodified saved logs):

**vanilla**: [events](../../results/2026-09-30-final-0.2.0/raw/refactor-1-vanilla/events.jsonl), [diagnostics](../../results/2026-09-30-final-0.2.0/raw/refactor-1-vanilla/events.stderr.txt).

- Line 5, `item_1`, exit 0: `/bin/zsh -lc "pwd && rg -n \"normalize_category|category\" . --glob '"'!*.pyc'"'"`
- Line 7, `item_2`, exit 0: `/bin/zsh -lc "sed -n '1,200p' expense_report/filters.py && sed -n '1,240p' expense_report/report.py && sed -n '1,260p' tests/test_expenses.py && rg --files -g 'AGENTS.md' -g 'pyproject.toml' -g 'setup.cfg' -g 'tox.ini' -g 'Makefile' -g 'README.md'"`
- Line 9, `item_3`, exit 128: `/bin/zsh -lc 'rg --files expense_report tests && git status --short'`
- Line 14, `item_6`, exit 0: `/bin/zsh -lc "python3 -m unittest discover -s tests -v && python3 - <<'PY' ↵ from expense_report.categories import normalize_category as shared ↵ from expense_report.filters import normalize_category as filtering ↵ from expense_report.report import normalize_category as grouping ↵ assert filtering is shared ↵ assert grouping is shared ↵ assert filtering('  FÖÖD  ') == 'föö d'.replace(' ', '') ↵ print('compatibility imports verified') ↵ PY"`

**contextlean**: [events](../../results/2026-09-30-final-0.2.0/raw/refactor-1-contextlean/events.jsonl), [diagnostics](../../results/2026-09-30-final-0.2.0/raw/refactor-1-contextlean/events.stderr.txt).

- Line 5, `item_1`, exit 128: `/bin/zsh -lc 'git status --short && rg -n "normalize_category" expense_report tests'`
- Line 7, `item_2`, exit 0: `/bin/zsh -lc "pwd; rg -n \"normalize_category\" expense_report tests; rg --files -g 'AGENTS.md' -g 'filters.py' -g 'report.py' -g 'test_expenses.py'"`
- Line 9, `item_3`, exit 0: `/bin/zsh -lc "sed -n '1,160p' expense_report/filters.py; sed -n '1,180p' expense_report/report.py; sed -n '1,240p' tests/test_expenses.py; rg --files expense_report"`
- Line 14, `item_6`, exit 0: `/bin/zsh -lc 'python3 -m unittest discover -s tests -v && python3 -m expense_report.cli data/sample.csv && python3 -m expense_report.cli data/sample.csv --category food --currency GBP'`


### documentation-config

C item_1 names the bad path but Git fails first, so its rg/sed do not run. C item_2 executes rg and sed on expense_report/config.json, producing two missing-file messages. Shell exit is zero because the later README sed succeeds; command exit alone misses the failures. C item_3 lists files and discovers config.json; item_4 searches and reads root config, CLI and tests. C ultimately patches only root config and README correctly. C stderr records a patch rejection (target arguments absent, cannot link it to bad path). C runs the same five tests twice, V once. V post-verification git diff fails, then performs its own final read/search.

Both run documented default and GBP examples; C five tests twice, V once.

Both modify config.json and README correctly; no incorrect-path file created.

Trace command sequence (the ids and line numbers refer to the unmodified saved logs):

**vanilla**: [events](../../results/2026-09-30-final-0.2.0/raw/documentation-config-1-vanilla/events.jsonl), [diagnostics](../../results/2026-09-30-final-0.2.0/raw/documentation-config-1-vanilla/events.stderr.txt).

- Line 5, `item_1`, exit 0: `/bin/zsh -lc "rg -n --hidden -S \"USD|GBP|currency|pytest|unittest\" . -g '"'!/.git'"' && rg --files -g '"'!*'"\\.pyc' | sed -n '1,160p'"`
- Line 7, `item_2`, exit 0: `/bin/zsh -lc "find .. -name AGENTS.md -print; sed -n '1,120p' README.md; sed -n '1,120p' expense_report/cli.py; sed -n '1,120p' tests/test_expenses.py; sed -n '1,80p' config.json"`
- Line 12, `item_5`, exit 129: `/bin/zsh -lc 'python3 -m expense_report.cli data/sample.csv && python3 -m expense_report.cli data/sample.csv --category food --currency GBP && python3 -m unittest discover -s tests -v && git diff --check && git diff -- README.md config.json'`
- Line 14, `item_6`, exit 0: `/bin/zsh -lc "rg -n -S \"USD|EUR|GBP\" README.md config.json expense_report tests && sed -n '1,12p' README.md && sed -n '1p' config.json"`

**contextlean**: [events](../../results/2026-09-30-final-0.2.0/raw/documentation-config-1-contextlean/events.jsonl), [diagnostics](../../results/2026-09-30-final-0.2.0/raw/documentation-config-1-contextlean/events.stderr.txt).

- Line 5, `item_1`, exit 128: `/bin/zsh -lc "git status --short && rg -n -i -e 'USD|EUR|currency|GBP' expense_report/config.json README.md && sed -n '1,160p' expense_report/config.json && sed -n '1,220p' README.md"`
- Line 7, `item_2`, exit 0: `/bin/zsh -lc "pwd; rg -n -i -e 'USD|EUR|currency|GBP' expense_report/config.json README.md; sed -n '1,160p' expense_report/config.json; sed -n '1,220p' README.md"`
- Line 9, `item_3`, exit 0: `/bin/zsh -lc "rg --files -g '"'!*.pyc'"' -g '"'!__pycache__/**'"'"`
- Line 11, `item_4`, exit 0: `/bin/zsh -lc "rg -n -e 'config|currency|USD|EUR|GBP' expense_report/cli.py tests/test_expenses.py config.json; sed -n '1,240p' expense_report/cli.py; sed -n '1,120p' config.json; sed -n '1,260p' tests/test_expenses.py"`
- Line 16, `item_7`, exit 0: `/bin/zsh -lc 'python3 -m expense_report.cli data/sample.csv && python3 -m expense_report.cli data/sample.csv --category food --currency GBP && python3 -m unittest discover -s tests -p test_expenses.py -v && python3 -m unittest discover -s tests -v'`


## What the Feature regression supports

Feature C has an extra discovery command after its Git-before-search failure, one recovered patch rejection, a README edit, a different combined-selector implementation, more explicit source-file reads, and duplicate execution of the same eight-test suite. Both conditions leave eight tests; C did not add more test cases than V. V also fails its final Git diff command, so failure overhead exists on both sides.

| Feature quantity | Vanilla | ContextLean | Difference |
|---|---:|---:|---:|
| input_tokens | 74,057 | 130,612 | +56,555 |
| cached_input_tokens | 54,272 | 107,008 | +52,736 |
| output_tokens | 1,579 | 2,918 | +1,339 |
| Uncached input (input−cached) | 19,785 | 23,604 | +3,819 |

The extra 56,555 input tokens comprise 52,736 more cached input and 3,819 more uncached input. These are exact arithmetic differences, not causes. C output is 1,339 tokens higher. Captured command-output bytes are 13,927 V versus 6,250 C; the larger V output includes Git usage text. Therefore the token regression cannot simply be explained as larger captured C stdout.

All C runs have a 7,087-byte AGENTS.md plus a 10-byte wrapper; V has neither. These are exact file sizes, not measured loaded-token amounts. The prior compact map had 932 bytes. Larger persistent guidance and additional interaction cycles are possible contributors, but the logs do not partition model usage by instruction, command, patch attempt or hidden reasoning. **The Feature +76.5% regression is not explained by an observed lookup of the incorrect config path.**

## Cache and recovered errors

| Task | Cached input V / C | Cached fraction V / C | Patch rejections V / C | Saved command-output bytes V / C |
|---|---:|---:|---:|---:|
| navigation | 14,080 / 27,136 | 29.6% / 63.1% | 0 / 0 | 5,103 / 2,407 |
| bug-fix | 63,232 / 42,240 | 90.4% / 70.1% | 0 / 0 | 5,056 / 3,209 |
| feature | 54,272 / 107,008 | 73.3% / 81.9% | 0 / 1 | 13,927 / 6,250 |
| refactor | 91,648 / 95,488 | 92.6% / 89.3% | 0 / 1 | 3,925 / 3,492 |
| documentation-config | 76,288 / 111,616 | 86.9% / 91.1% | 0 / 1 | 13,069 / 5,200 |

Cached fractions affect the credit-equivalent calculation, not total-token arithmetic. They do not identify what content was cached. Model-cache schema warnings are CLI metadata errors, not proof of provider cache misses. All ten stderr logs retain state-database warnings. Model-cache schema warnings occur on navigation V, both Feature runs and both Refactor runs; recovered patch rejections occur on C Feature, C Refactor and C Documentation/config. Git failures occur on C Navigation, both Bug Fix runs, both Feature runs, both Refactor runs and both Documentation/config runs (some produce usage text rather than the exact “not a git repository” string).

No complete file-read or tool-call counts are inferred. Explicit source-read/search commands are described, including repeated searches and repeated test execution. Per-command tokens, rejected patch arguments, hidden reasoning and direct instruction-loading evidence are unavailable.

## Repair and offline verification

The literal is corrected at its true source, and the unchecked legacy preparation route is retired. `benchmarks/prepare_fixture.py` provides the supported offline freeze route; it does not author project maps or alter valid product rules. A human/agent responsibility review records each exact description and actual source excerpts. The validator checks every explicit map path, containment, wrapper, review coverage, description/evidence consistency, unchanged non-instruction state and exact frozen hashes. Natural-language correctness still requires the explicit source review; the checker does not claim to prove semantics.

The runner requires a preparation receipt and validates the fixture before CLI probing/output creation, validates the snapshot after copying, and rechecks every fresh workspace before model execution. Missing paths, missing/stale review, changed frozen instructions or changed product state fail closed. Successful preparation never invokes a model. Existing outputs and records are not overwritten. Unsupported map syntax is rejected rather than skipped.

Five independent corrected preparations were validated and frozen locally; [corrected preparation evidence](corrected-preparation.json) retains all eight reviewed roles and source excerpts, shared product digest and 71-facet transfer results. Only the erroneous path was corrected in guidance; all eleven permanent-rule paragraph bodies are unchanged. Product files match the fixture at `52a2c34c091f9720076cc9685fb858347d9f6dcf`. Documented CLI examples and original five tests pass for every prepared copy. The new nonexistent-path regression mocks both CLI probing and model execution and asserts zero calls before rejection.

[Structured trace comparison](trace-comparison.json) retains exact command strings, ids, line numbers, outcomes, recorded metrics, cache arithmetic, diagnostics and visible agent messages. This analysis is outside the immutable result folder. Full diagnostic-file hashes were checked before/after the work. No numbers enter the main headline table.

Offline quality checks: **88 tests pass**, Ruff lint/format pass, all four Skill validators and Codex package validation pass, and both Claude manifests validate with their documented warnings. The actual archived bad map was rejected by the repaired runner with zero CLI/model calls and no output directory. [Quality record](quality-checks.json). Lean Change Review found no material duplication, speculative layer, dependency or misplaced product responsibility. Tracked product Skill files remain byte-identical to the release candidate.

## Release decision and minimum next runs

No ContextLean product behavior change is required. Release candidate `52a2c34c…` remains a valid product candidate; the bad map was an external manual benchmark preparation output. This work repairs development preparation/preflight only. It does not prove that corrected guidance saves tokens or that a future live suite will pass. CLI/cache/Git noise remains disclosed.

The harness is ready to accept a separately authorized, reviewed, fresh preparation and reject this bad fixture before spending usage. The minimum recommended next complete validation is **10 fresh live runs: all five tasks, one Vanilla and one corrected ContextLean run each**, in one new result set. Do not reuse the diagnostic Vanilla runs or cherry-pick the four C runs without observed bad-path access. No additional repetitions are recommended yet and none were run.

ContextLean product remains release-ready; benchmark harness is repaired.
