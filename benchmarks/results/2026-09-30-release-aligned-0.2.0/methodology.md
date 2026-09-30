# Release-aligned methodology

Product commit: `86043499d5a375cc6a3b295bc7c03b0999eb458c`.
Exactly ten fresh `gpt-5.6-terra`, low-reasoning, ephemeral conversations:
one Vanilla and one ContextLean for each of the five existing tasks. No earlier
compact-final, isolated Refactor, historical or diagnostic result is reused.

All five pairs were prepared before any model call. Guidance was freshly generated
from the frozen semantically reviewed fixture; eight map responsibilities were
reviewed against actual source. The unchanged repaired preparation helper binds
paths, responsibility snippets, equivalent product state and hashes. The transfer
checker verifies all 71 facets. Both fixtures and frozen preparation evidence were
checked before every call. Prompts, task suite, grader, submitted/original regression
and acceptance tests, execution/usage parsing and measurement logic are unchanged.

The unchanged compact-final adapter excludes PROJECT_REFERENCE.md from product-state
hashes and removes it from Vanilla with AGENTS.md/CLAUDE.md. Startup discovery is
unchanged. ContextLean has 5,476 AGENTS.md bytes, an 11-byte wrapper and a 3,564-byte
conditional reference. The measured fixtures contain no plugin or Git metadata.

The repaired harness's deterministic order is retained: Navigation V/C, Bug Fix C/V,
Feature V/C, Refactor C/V, Documentation/config V/C. Each condition starts fresh,
and the same temporary workspace path is reused within each pair. No product or
benchmark tuning occurs between conditions or after observing results.

Codex CLI 0.147.0, Darwin arm64, Python 3.14.4 match compact-final. Commands use
--json --ephemeral --ignore-user-config --ignore-rules --strict-config; web search
disabled, approvals never, default service tier. Navigation is read-only; editing
tasks use workspace-write. No dependencies are installed and full-access mode is unused.

Input/cached/output come from exact turn.completed.usage. Total is input + output;
cached input is a subset of input, reasoning a subset of output. Commands are unique
command_execution event ids. Wall time is the unchanged monotonic execution timer,
excluding preparation/grading. File reads, all tool calls, unique files and actual
credits charged remain unavailable. Dated ChatGPT credit-equivalents use the frozen
rate card and unchanged calculation, with authentication confirmed by login status.

All ten solutions are independently offline-regraded: submitted tests, separately
restored original regressions and independent acceptance checks. Raw traces/stderr,
failures/recoveries, all solutions, receipts and numeric records remain available.
The source archive omits recursive old evidence/analysis only, with complete selection
hashes. Public raw copies are byte-identical; redundant local execution summaries
remain local because they can contain temporary paths.

One observation per condition/task is preliminary validation of this configuration.
Caching, model stochasticity, service load, order and CLI diagnostics are uncontrolled.
No causality, statistical-confidence or universal-savings claim is made. All older
datasets remain unchanged and separate. No additional calls, tag or release followed.
