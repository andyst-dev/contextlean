# Guidance authoring and optional project Skills

This is maintainer reference material, not startup guidance or a bootstrap prerequisite.
The [Balanced contract](balanced-contract.md) keeps ordinary coding guidance focused
on navigation, local changes and verification. Bootstrap preserves existing project
Skills but does not discover recurring workflows or create/share Skills by default.

## Map editorial standards

When authoring or deliberately maintaining maps, keep descriptions concise, durable
and non-obvious. Preserve important project constraints. Remove obsolete or duplicate
entries in the affected map, avoid transient task details and put substantial depth
in optional references with precise task conditions. Do not inventory every symbol.

Ordinary work corrects known invalidation or encountered stale information in the
smallest applicable map. It need not check maps after every task, document every
new reusable workflow, or perform a global documentation refresh. Use an explicitly
requested Audit to investigate broader drift.

## Optional Skill authoring

Only undertake project-Skill creation or sharing when separately requested. Create a
Skill only for a repetitive, non-trivial procedure likely to be reused.

Keep persistent navigation, architecture and rules in AGENTS.md; Skills hold reusable procedures, not simple repository facts. Use .agents/skills/<name>/SKILL.md as the canonical project source; expose the same source through .claude/skills/<name>/SKILL.md when both agents need it. These differ from plugin-root skills/. Prefer a relative directory symlink only when portable: verify target resolution inside the project, resolution after relocation, and discovery on both installed tools without a model turn. Preserve valid existing workflows/sharing. Report unsupported sharing without copying divergent instructions.

These location/sharing details describe the existing supported recipe, not a promise
that arbitrary future tool versions discover it. Check the installed tools before
claiming compatibility. Portable sharing is a specialized authoring task, not a
condition for ordinary ContextLean bootstrap success. Never rewrite working layouts
just to match this example. Keep Skill invocation explicitly requested.

## Legacy material

The [original bootstrap](reference/original-agent-bootstrap.md),
[historical coverage](history/bootstrap-coverage.md), frozen test fixture and
[historical test checker](../tests/legacy_bootstrap.py) remain available for
historical investigation. Existing receipts may be inspected explicitly against their
matching plugin/source revision; hashes can legitimately differ across revisions.
Do not regenerate historical evidence to make it match current behavior.

Balanced does not produce a replacement per-project facet ledger. Maintainer tests
exercise coding safeguards and actual generated artifacts. Keep historical comparison
counts in developer documentation, not beginner-facing guidance or project startup files.
