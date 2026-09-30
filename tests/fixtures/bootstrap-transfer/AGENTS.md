# Example bootstrapped expense-report project

Dependency-free Python CSV CLI; preserve Decimal amounts and public imports.

## Project map and commands

- `expense_report/cli.py`: parsing/orchestration; `storage.py`: CSV/Decimal loading.
- `filters.py`: category selection; `report.py`: totals/grouping.
- `tests/test_expenses.py`: logic and CLI verification; `config.json`: default currency.
- Targeted: `python3 -m unittest discover -s tests -p test_expenses.py -v`.
- Full: `python3 -m unittest discover -s tests -v`; this small project has one test file.
- Example: `python3 -m expense_report.cli data/sample.csv`.

## Navigation

Use the AGENTS.md hierarchy as the primary map; do not rediscover documented architecture. Identify the smallest responsible subsystem, search symbols/references/text before reading, then inspect relevant code, immediate dependencies and tests. Expand only with evidence; avoid whole-repository scans during ordinary tasks and rereading understood files without reason. Inspect version-control state before broad changes. Respect existing architecture unless the requested task requires changing it.

## Ownership

Give each important responsibility a clear owner and each file/module/class one primary cohesive responsibility. Keep related behavior together, separate unrelated systems, and avoid duplicate ownership of state or behavior. Before adding or extracting a subsystem, ask who owns it, whether the change can stay local, whether it introduces an unrelated responsibility, and whether cohesive extraction reduces future unrelated reading. Create a module only for a genuine responsibility.

## Structure

Maintainability and context efficiency share the goal of local changes. Split by responsibility, never line count; cohesive large files are acceptable. Mixed responsibilities, repeated unrelated edits, unrelated reading, catch-all objects or a new independent responsibility are refactoring signals, not automatic permission. Refactor only when the current task benefits meaningfully or the user requests it. Avoid tiny-file fragmentation, forwarding wrappers and layers that increase the files needed to understand one responsibility.

## Interfaces

Keep dependency direction simple; avoid cycles and hidden global coupling. Keep public interfaces focused and implementation details local, so callers need no unnecessary knowledge of internals. Separate UI, domain, persistence, transport and infrastructure when genuinely distinct. Use events, signals, interfaces or dependency injection only when they reduce coupling; do not abstract for architectural purity.

## Implementation

Before new code, check in order: behavior already supported → project solution/helper/pattern → standard library → native framework/platform → installed dependency → minimum necessary new code. Prefer explicit readable code, coherent functions/classes, meaningful extractions and shallow control flow. Keep diffs and touched files focused; avoid unrelated cleanup, stylistic rewrites of working systems and speculative configuration/extension layers or dependencies without concrete benefit. Safely remove code made obsolete by the change. Preserve correctness, security, trust-boundary validation, data safety, readability, maintainability, accessibility and requested behavior. Prefer a specific responsible owner over generic catch-all helpers.

## Bug fixes

Find the root cause before patching symptoms; trace relevant data/execution flow and callers/usages when needed. Fix the responsible shared layer rather than duplicating workarounds across callers. Avoid broad refactors unless correctness requires them. Add the smallest useful runnable regression verification for non-trivial fixes when practical.

## Verification

Use the smallest meaningful verification: targeted checks first, affected broader checks for shared/core changes, and the full suite when necessary or required by project rules. Prefer existing test infrastructure; leave runnable regression coverage for non-trivial logic when practical. Do not introduce a test framework for one small check without genuine justification. Keep verified targeted and full commands distinct when both exist; mark uncertain commands unverified.

## Context

Keep large documentation available as optional topic references: search first, read relevant sections, never require whole-document startup reading. Ignore only proven generated/cache/build/vendor material during ordinary work; inspect it when the task concerns it. Never hide useful source, tests, fixtures, migrations, documentation, assets or archives without a clear reason. Keep AGENTS.md canonical and Claude wrappers lightweight; preserve useful knowledge and necessary platform-specific exceptions. Never change model selection, reasoning level, provider, authentication, credentials or user-global agent settings without an explicit request.

## Map maintenance

After each task, check map accuracy. Update only the smallest relevant AGENTS.md for important path, ownership, subsystem, architecture, dependency/data-flow, command or reusable-workflow changes; remove stale entries and duplication. Avoid map churn for ordinary bug fixes, details, content, tuning, small UI changes or internal refactors preserving ownership. Keep guidance concise and durable, omit transient or code-obvious details, and move depth to optional references. Avoid repository-wide documentation refreshes unless necessary. Use ContextLean Audit Context Locality (contextlean:audit) for a separate drift inspection when needed.

## Project Skills

Keep persistent navigation, architecture and rules in AGENTS.md. Create project Skills only for repetitive, non-trivial reusable procedures, not simple repository facts. Use .agents/skills/<name>/SKILL.md as the canonical project source and expose it at .claude/skills/<name>/SKILL.md when both agents need it. Prefer a relative directory symlink to the same source only when portable and discovery/target resolution are verified; otherwise report the sharing limitation without copying instructions. These project locations differ from plugin-root skills/.

## Lean Review

Delegate optional completed-change complexity/locality review to ContextLean Lean Change Review (contextlean:lean-review), which is advisory and read-only unless a fix is separately requested. Do not recreate a generic project review Skill; preserve behavior and safety when considering its findings.
