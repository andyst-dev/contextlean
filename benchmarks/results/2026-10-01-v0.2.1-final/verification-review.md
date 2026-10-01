# Verification coverage review

All 18 visible traces reviewed offline. No duplicate equivalent **passed** verification was established in any ContextLean session (or in Vanilla). This is a bounded trace observation, not a universal guarantee. Missing/truncated test identities/counts stay unavailable; shell labels do not establish different coverage.

| Session | Visible test commands | Counts where exposed | Equivalent passed repeat |
|---|---:|---|---|
| terra-navigation-vanilla | 1 | [[5]] | 0 |
| terra-navigation-contextlean | 0 | not exposed | 0 |
| terra-bug-fix-contextlean | 1 | [[6]] | 0 |
| terra-bug-fix-vanilla | 1 | [[6]] | 0 |
| terra-feature-vanilla | 2 | [[8]] | 0 |
| terra-feature-contextlean | 1 | [[8]] | 0 |
| terra-refactor-contextlean | 1 | [[5]] | 0 |
| terra-refactor-vanilla | 2 | not exposed | 0 |
| terra-documentation-config-vanilla | 0 | not exposed | 0 |
| terra-documentation-config-contextlean | 1 | [[5]] | 0 |
| claude-bug-fix-contextlean | 1 | [[7]] | 0 |
| claude-bug-fix-vanilla | 2 | [[7], [7]] | 0 |
| claude-refactor-contextlean | 1 | [[5]] | 0 |
| claude-refactor-vanilla | 1 | [[5]] | 0 |
| sol-bug-fix-contextlean | 1 | [[6]] | 0 |
| sol-bug-fix-vanilla | 2 | [[6]] | 0 |
| sol-refactor-contextlean | 1 | [[6]] | 0 |
| sol-refactor-vanilla | 1 | not exposed | 0 |

Terra Feature Vanilla first tried `python`, which is unavailable, then successfully ran the eight-test suite with `python3`; this is recovery from a failed command, not duplicated passed coverage. Claude Bug Fix Vanilla ran seven tests, changed the regression-test implementation, then reran seven tests; the intervening test change justifies revalidation. Searches merely containing the word unittest are not executed test suites; inspect the command/output records in the JSON.

Claude Refactor ContextLean passed the five-test suite once. Subsequent shared-function identity/CLI probes incurred permission/shell recovery: an inline probe was denied for brace/quote expansion; an external scratch-file command was blocked for removal outside the workspace; the scratch script then failed its package import; an environment-prefixed command required approval; a copy across the workspace boundary was blocked. A workspace-local probe finally passed. The raw command metric counts nine Bash tool-use attempts, including these denied attempts, versus four in Vanilla. It does not assert nine executed shell processes. This concrete recovery explains extra visible work; it does not establish token causality or a product defect.

Sol Refactor ContextLean adds a sixth regression test and checks package/module ownership, then runs its six-test suite once and reviews the diff. Vanilla runs the original five-test suite and separate import/query assertions. These are different actual coverage choices; neither demonstrates redundant full-suite verification.

Terra Refactor ContextLean runs five tests once. Terra Bug Fix runs six once, Feature eight once and Documentation/config five once. ContextLean Navigation runs its example without a full test-suite command. Offline evaluation is outside measured model timing/commands and remains independently required.

The fixture map says five baseline tests, with no mandatory repeat. All grader-required independent submitted/original/acceptance checks are outside model metrics. Instruction attribution and hidden model intent are not claimed. Full command/output records and mutation epochs are in [verification-review.json](verification-review.json); raw traces remain authoritative.
