---
name: bootstrap
description: Configure a repository once for lean Codex and Claude Code navigation. Use only when the user explicitly asks to bootstrap, initialize, or install ContextLean repository guidance; this workflow changes repository files and must never run implicitly.
---

# Bootstrap a repository

Read `references/bootstrap-spec.md` and `references/permanent-rules.json` completely before inspecting or changing the target repository. They own the setup procedure and permanent behavior respectively; do not rely on a summary or partial search result.

Then apply the specification to the current repository in order:

1. Confirm that the user explicitly requested bootstrap and identify the repository root.
2. Before changing the repository, capture the static ContextLean baseline required by the specification.
3. Analyze the repository once, preserving existing instructions and documentation.
4. Create or improve the smallest useful `AGENTS.md` hierarchy and matching lightweight Claude wrappers.
5. Move large optional guidance behind targeted references, add only proven-safe exclusions, and create project Skills only for reusable non-trivial workflows.
6. Verify every documented path, responsibility, command, wrapper, Skill, reference, and exclusion; pass the permanent-rule transfer and safe-removal gate before declaring success.
7. Write `.contextlean/bootstrap-report.json` from the captured before state and verified after state.
8. Report only the completion items required by the specification.

Do not perform feature work or product refactors during bootstrap. Never change model selection, reasoning level, provider, authentication, credentials, or user-global agent configuration unless separately and explicitly requested. Keep one canonical source for every instruction.
