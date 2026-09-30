# Conditional project guidance

Read only the relevant section when AGENTS.md directs it for the current task.
This file is not startup context.

## Architecture decisions

Before adding/extracting behavior, identify its owner, whether it can stay local, whether it adds an unrelated responsibility, and whether cohesive extraction reduces future unrelated reading. Create a module only for a genuine responsibility. Maintainability and context efficiency both benefit from local changes.

Refactoring signals: independent responsibilities, repeated unrelated edits, large unrelated reads, catch-all/god objects, a new independent responsibility, or extraction that improves locality. Signals invite judgment, not automatic refactoring; apply the permanent current-task/request threshold.

For an explicit refactor, start from the mapped owner and code being changed; inspect direct callers/usages and affected tests as needed, then make the smallest behavior-preserving structural change and verify proportionally. This is a route, not a fixed checklist: skip unnecessary steps, such as inspecting every caller for a private implementation change that cannot affect callers. Known references need no global search. Multiple searches are useful when they answer different unresolved questions; do not repeat an equivalent answered search.

Review only architecture boundaries relevant to the change; refactor signals do not require a repository-wide architecture audit. Expand when ownership is ambiguous, the map is stale or contradicted by source, usages cross boundaries, public interfaces change, shared/core behavior is affected, tests expose wider impact, dependency flow needs investigation, or other concrete evidence requires it. Source evidence overrides the map. Preserve ownership/locality, interface stability and dependency direction unless the requested change requires altering them; preserve behavior and avoid unnecessary abstractions or unrelated cleanup.

Separate UI, domain, persistence, transport and infrastructure when genuinely distinct. Events, signals, interfaces or dependency injection must meaningfully reduce coupling; architectural purity alone is insufficient.

## Bug diagnosis

Trace only the data/execution path needed to explain the failure. Inspect callers/usages when they establish a shared cause; correct that owner rather than repeating caller patches. A local fix needs no broad exploration ritual. Leave the practical runnable regression check required by the permanent verification rule.

## Verification scope

Small logic change: targeted unit test. Component change: relevant component test. Shared/core change: targeted plus affected broader tests. Build/config change: relevant build/check. Stop when meaningful confidence is sufficient; full-project verification is for necessity or project requirements. Complex repetitive verification can qualify for a project Skill.

## Project Skills

Keep persistent navigation, architecture and rules in AGENTS.md; Skills hold reusable procedures, not simple repository facts. Use .agents/skills/<name>/SKILL.md as the canonical project source; expose the same source through .claude/skills/<name>/SKILL.md when both agents need it. These differ from plugin-root skills/. Prefer a relative directory symlink only when portable: verify target resolution inside the project, resolution after relocation, and discovery on both installed tools without a model turn. Preserve valid existing workflows/sharing. Report unsupported sharing without copying divergent instructions.
