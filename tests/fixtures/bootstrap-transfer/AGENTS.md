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
- `.contextlean/` holds ignored local receipts; `__pycache__/` is generated. Inspect when relevant; preserve samples/tests.

## Navigation

Use AGENTS.md as the primary map; do not rediscover documented architecture. Identify the smallest owner, search before broad reading; inspect immediate dependencies/tests only when relevant. Expand only with evidence; avoid ordinary whole-repo scans and unjustified rereads. Before broad/state-sensitive changes, inspect version-control state when available. Preserve architecture unless the task requires change.

## Ownership

Give files/modules/classes cohesive owners: related behavior together, unrelated responsibilities separate, no duplicate state/behavior. Prefer specific owners over catch-all helpers. New modules need a genuine responsibility; split only for locality benefit; avoid fragmentation/forwarding wrappers. For architecture/refactoring decisions, read [Architecture decisions](PROJECT_REFERENCE.md#architecture-decisions).

## Structure

Split by responsibility, never size; cohesive large files are acceptable. Refactor only for meaningful current-task benefit or an explicit request; assess signals using the architecture reference.

## Interfaces

Keep dependencies simple, without cycles/hidden global coupling; public interfaces focused; internals local so callers need no unnecessary internal knowledge. For boundary/indirection decisions, use the architecture reference.

## Implementation

Reuse in order: existing support → project solution → standard library → framework/platform → installed dependency → minimum new code. Write explicit, readable, coherent code with meaningful extractions and shallow flow. Focus diffs/files; no unrelated cleanup, style-only rewrites, speculative abstractions/configuration or dependencies without concrete benefit. Remove newly obsolete code safely. Preserve correctness, security, trust-boundary validation, data safety and data-loss prevention, readability, maintainability, accessibility and requested behavior.

## Bug fixes

Diagnose root cause; inspect relevant flow/callers when needed. Fix the owner/shared layer, avoid repeated workarounds and broad refactors unless correctness requires them. Apply the regression rule below. For difficult diagnosis, see [Bug diagnosis](PROJECT_REFERENCE.md#bug-diagnosis).

## Verification

Use the smallest meaningful check, targeted first; broaden for shared/core changes; full suite only when necessary/project-required. These are scope choices, not mandatory sequential steps. Use existing infrastructure; leave a small runnable regression check for non-trivial logic/fixes when practical. No new framework for one check without justification. Distinguish verified targeted/full commands; label uncertainty. If scope is unclear, see [Verification scope](PROJECT_REFERENCE.md#verification-scope).

## Context

Search large docs; read relevant sections, never whole documents at startup. Ignore only proven local generated/cache/build/vendor material; inspect when task-relevant. Preserve useful source/tests/fixtures/migrations/docs/assets/archives. Keep AGENTS.md canonical, Claude wrappers light, useful knowledge/platform exceptions intact. Never change model selection, reasoning, provider, authentication, credentials or user-global agent settings without an explicit request.

## Map maintenance

After every task, check map accuracy. Update only the smallest map for meaningful path/owner/subsystem/architecture/dependency/data-flow/command/reusable-workflow changes; remove stale/duplicate entries. No churn for ordinary fixes/details/content/tuning/UI or ownership-preserving refactors. Keep maps concise, durable, non-obvious; depth optional. No global documentation refresh unless necessary.

## Project Skills

Create/share project Skills only for repetitive, non-trivial reusable procedures. When creating/modifying them, read [Project Skills](PROJECT_REFERENCE.md#project-skills).

## Lean Review

On demand: ContextLean Lean Change Review (`contextlean:lean-review`) advises on completed changes; read-only unless fixes are requested, preserving behavior/safety. Do not recreate a generic review Skill. ContextLean Audit Context Locality (`contextlean:audit`) owns broader context/drift review. Neither runs automatically or replaces coding/maintenance duties.
