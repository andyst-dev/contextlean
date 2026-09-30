# Visible behavior review

## Refactor

ContextLean begins with a symbol/usage search limited to the mapped `expense_report` owner and its tests, then reads `filters.py`, `report.py` and `tests/test_expenses.py`. A subsequent `rg --files expense_report` inventories the owning subsystem to place the shared implementation. These answer different questions; no equivalent search or repository-wide rediscovery appears. This is consistent with trusting mapped ownership; internal reasoning is not observable.

The direct callers `select_category` and `build_report` are displayed. One successful patch adds `expense_report/categories.py` and replaces duplicate definitions with compatibility imports in the two owners. No Git command appears. Verification runs all five existing fixture tests plus direct assertions that both public imports resolve to the same function and normalization is unchanged. All three commands and the patch succeed. Independent acceptance also checks behavior preservation, including the existing raw filter-query semantics and compatibility imports.

No wider-impact evidence arose; exploration stays within the owner/tests. This supports appropriate scope for this case but does not empirically test expansion after contradictory ownership or cross-boundary impact. Targeted verification covers the fixture's only test module; it is also its full suite.

Vanilla uses five commands. It performs global inventory/symbol searches and additional CLI/configuration inspection; `git status` fails because the fixture has no metadata, and `python` is unavailable before recovery with `python3`. Both solutions pass every grading layer. Resource differences cannot be attributed solely to guidance: CLI errors, caching and stochasticity also differ.

The previous compact-final Refactor observation was ContextLean +23.30% tokens, 3→5 commands. This batch observes -24.02%, 5→3 commands. Datasets remain separate, with no causal or statistical-confidence claim. The earlier isolated pair is not reused.

## Diagnostics and recovery in all ten traces

- `navigation-1-vanilla`: command `item_2` exited 5; `/bin/zsh -lc "sed -n '1,200p' expense_report/storage.py && sed -n '1,200p' expense_report/report.py && sed -n '1,200p' expense_report/cli.py && sed -n '1,160p' tests/test_expenses.py && python3 -m expense_report.cli data/sample.csv && python3 -m unittest"`. Full output and recovery remain in the raw trace.
- `bug-fix-1-vanilla`: command `item_2` exited 129; `/bin/zsh -lc "sed -n '1,200p' expense_report/filters.py && sed -n '1,240p' expense_report/cli.py && sed -n '1,260p' tests/test_expenses.py && sed -n '1,120p' data/sample.csv && git diff --check && git status --short"`. Full output and recovery remain in the raw trace.
- `feature-1-vanilla`: command `item_5` exited 129; `/bin/zsh -lc 'python3 -m unittest discover -s tests -v && python3 -m expense_report.cli data/sample.csv --min-amount 10 && python3 -m expense_report.cli data/sample.csv --category food --min-amount 10 && git diff --check && git diff'`. Full output and recovery remain in the raw trace.
- `refactor-1-vanilla`: command `item_3` exited 128; `/bin/zsh -lc "sed -n '1,240p' expense_report/__init__.py && sed -n '1,260p' expense_report/cli.py && git status --short"`. Full output and recovery remain in the raw trace.
- `refactor-1-vanilla`: command `item_6` exited 127; `/bin/zsh -lc "python -m unittest discover -s tests -v && rg -n \"def normalize_category|from expense_report\\.categories import normalize_category\" expense_report"`. Full output and recovery remain in the raw trace.
- `documentation-config-1-vanilla`: command `item_5` exited 129; `/bin/zsh -lc 'python3 -m expense_report.cli data/sample.csv && python3 -m expense_report.cli data/sample.csv --category food --currency GBP && python3 -m unittest discover -s tests -v && git diff --check && git diff -- README.md config.json'`. Full output and recovery remain in the raw trace.

All final submitted-test, original-regression and acceptance results pass. A failed initial discovery or unavailable command is preserved even when recovered. Navigation/ContextLean does not run tests itself; offline grading independently runs them. Completed shell commands are counted exactly by the unchanged parser. Search descriptions come from command text, not inferred file-read or total tool-call counts.
