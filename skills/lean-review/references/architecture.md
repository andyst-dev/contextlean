# Architecture and locality review

This is optional material for an explicitly requested Lean Review. Read only when
that review concerns ownership, extraction, boundaries, dependency direction or
indirection. These signals do not authorize a refactor or an implementation edit.

Before adding/extracting behavior, identify its owner, whether it can stay local, whether it adds an unrelated responsibility, and whether cohesive extraction reduces future unrelated reading. Create a module only for a genuine responsibility. Maintainability and context efficiency both benefit from local changes.

Refactoring signals: independent responsibilities, repeated unrelated edits, large unrelated reads, catch-all/god objects, a new independent responsibility, or extraction that improves locality. Signals invite judgment, not automatic refactoring; apply the permanent current-task/request threshold.

For an explicit refactor, start from the mapped owner and code being changed; inspect direct callers/usages and affected tests as needed, then make the smallest behavior-preserving structural change and verify proportionally. This is a route, not a fixed checklist: skip unnecessary steps, such as inspecting every caller for a private implementation change that cannot affect callers. Known references need no global search. Multiple searches are useful when they answer different unresolved questions; do not repeat an equivalent answered search.

Review only architecture boundaries relevant to the change; refactor signals do not require a repository-wide architecture audit. Expand when ownership is ambiguous, the map is stale or contradicted by source, usages cross boundaries, public interfaces change, shared/core behavior is affected, tests expose wider impact, dependency flow needs investigation, or other concrete evidence requires it. Source evidence overrides the map. Preserve ownership/locality, interface stability and dependency direction unless the requested change requires altering them; preserve behavior and avoid unnecessary abstractions or unrelated cleanup.

Separate UI, domain, persistence, transport and infrastructure when genuinely distinct. Events, signals, interfaces or dependency injection must meaningfully reduce coupling; architectural purity alone is insufficient.
