# Example bootstrapped expense-report project

Dependency-free Python CSV CLI using Decimal and unittest; preserve public imports.

## Project map

- `expense_report/cli.py`: arguments/configuration and orchestration.
- `expense_report/storage.py`: CSV loading and Decimal conversion.
- `expense_report/filters.py`: category normalization/selection.
- `expense_report/report.py`: normalized grouping and totals.
- `config.json`: default currency; CLI options override it.
- `tests/test_expenses.py`: loading, filtering, report and CLI regression tests.
- `data/sample.csv`: runnable input.
- `README.md`: usage/development; search relevant sections when needed.

Flow: CLI/config → loader → selection → report → JSON. Keep Decimal through totals.

## Commands and local context

- Targeted: `python3 -m unittest discover -s tests -p test_expenses.py -v`.
- Full: `python3 -m unittest discover -s tests -v` (currently the same module).
- CLI: `python3 -m expense_report.cli data/sample.csv`; add `--category food --currency GBP` to check options.
- No build/lint/format/type-check or package-manager configuration is present.
- `__pycache__/` is generated. Inspect when relevant; preserve samples/tests.

## Navigation

AGENTS.md is the primary map; trust documented ownership/architecture unless source contradicts it. Start at the smallest responsible subsystem; search before broad reads; inspect relevant usages/dependencies/tests. Expand only with concrete evidence; no ordinary whole-repository scans or broad rediscovery of mapped architecture. Skip equivalent answered searches and unjustified rereads. For broad/state-sensitive work, inspect available version-control state only if relevant; no routine Git checks. Preserve architecture unless the requested change requires it.

## Ownership and scope

Keep cohesive files/modules/classes: related behavior together, unrelated responsibilities separate, unique state/behavior owners; prefer specific owners over catch-all helpers. New modules need genuine responsibilities. Split by responsibility, not line count; cohesive large files are valid. Avoid fragmentation, forwarding wrappers and unnecessary layers. Refactor only for meaningful current-task benefit or explicit request; preserve behavior and assess relevant boundaries. Keep dependency direction simple, without cycles/hidden global coupling; APIs focused and internals local so callers need no unnecessary internal knowledge.

## Implementation

Reuse in order: existing support → project solution → standard library → framework/platform → installed dependency → minimum new code. Keep code explicit, readable, coherent and shallow; extract meaningful concepts. Focus diffs/files; no unrelated cleanup or style-only rewrites. Add abstractions, configuration, dependencies or test frameworks only for a justified current need. Safely remove code made obsolete by the change.

Preserve correctness, security, trust-boundary validation, data safety/data-loss prevention, readability, maintainability, accessibility and requested behavior. Preserve useful source/tests/fixtures/migrations/docs/assets/archives. Never change model selection, reasoning, provider, authentication, credentials or user-global agent settings without explicit request.

## Bug fixes

Diagnose the root cause before patching symptoms; trace relevant execution/data flow and callers when needed. Fix the responsible owner/shared layer; do not repeat workarounds across callers. Avoid broad refactors unless correctness requires them.

## Verification

Use the smallest sufficient targeted check first; broaden only for insufficient coverage, shared/core/public impact or project rules. Targeted, affected and full checks are scope choices, not mandatory stages; full-project checks require necessity or project rules. Reuse equivalent passed coverage unless relevant code/test/config/environment changes, failures, unresolved results or project-required repeats justify reruns. Reuse infrastructure; leave a small runnable regression check for non-trivial logic or bug fixes when practical. Report verified scope and uncertainty.

## Context and map accuracy

Search large documentation and read relevant sections; never make whole documents startup reading. Skip generated/cache/build/vendor material unless task-relevant; never hide useful material merely because it is large.

When your change invalidates a mapped path, owner, boundary, flow, constraint, or command—or you encounter stale mapped information—correct only the affected entries in the smallest applicable map. Otherwise leave maps alone. Remove obsolete/duplicate entries in that affected map; do not expand the correction into unrelated documentation work.
