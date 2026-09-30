# Historical Agent Project Bootstrap specification

- Historical reference only; not automatically loaded.
- Not required for normal ContextLean usage or after Bootstrap Repository succeeds.
- Not a second source of truth. Maintained ContextLean behavior lives in the current
  Skills and generated project guidance.
- Preserved for development comparisons, semantic regression checking and examples.
  The original instructions below are archived text, not instructions to execute.

The original 714-line specification is preserved verbatim below. Coverage-matrix
line numbers refer to that original body, excluding this historical header.

<!-- Original specification begins below; preserved verbatim. -->

# Agent Project Bootstrap

Read this file completely before doing anything else.

Apply **all instructions in this file fully and in order** as a **one-time repository bootstrap**.

Do not begin feature work, bug fixes, product refactors, or behavior changes until this bootstrap is complete and verified.

The goal is to configure this repository so future **Codex and Claude Code** sessions can understand, navigate, modify, and verify the project efficiently while keeping both the codebase and agent context clean.

A complete repository analysis is allowed during this bootstrap only.

Do not modify application behavior while performing it.

---

# 1. Goals

After bootstrap:

- `AGENTS.md` is the canonical source of shared project instructions.
- Codex uses the `AGENTS.md` hierarchy.
- Claude Code reuses the same instructions through lightweight `CLAUDE.md` files.
- Agents know where important systems live before exploring.
- Normal tasks inspect only the smallest relevant part of the repository.
- Code is organized around clear, cohesive responsibilities.
- Architecture is optimized for locality: a feature should normally be understandable and modifiable from a small set of related files.
- Maintainability and agent context efficiency are treated as the same architectural objective.
- Large documentation remains available but is searched selectively.
- Generated/cache/build content is ignored by default.
- Reusable procedures live in Skills when appropriate.
- Implementations favor existing solutions and the smallest correct change.
- Verification is proportional to the change.
- Project maps stay synchronized with meaningful architectural changes.

Preferred workflow:

```text
project map
→ identify responsible subsystem
→ targeted search
→ targeted reads
→ smallest correct implementation
→ targeted verification
→ update project map only if architecture changed
```

Avoid:

```text
scan repository
→ read everything
→ open unrelated systems
→ add unnecessary abstraction
→ make broad changes
→ run everything
```

---

# 2. Initial Repository Analysis

Perform one complete architecture analysis.

Identify:

- project type;
- languages;
- frameworks and major libraries;
- entry points;
- major directories;
- important modules and systems;
- ownership and responsibilities;
- important dependencies and data flows;
- run/development commands;
- build commands;
- test commands;
- lint/format/type-check commands;
- dependency/package management;
- generated/cache/build directories;
- existing agent configuration;
- large documentation files;
- recurring development workflows;
- obvious architectural hotspots or catch-all modules.

Before creating or modifying configuration, inspect existing:

```text
AGENTS.md
CLAUDE.md
.agents/
.claude/
.codex/
README files
documentation
CI configuration
build/test configuration
```

Preserve useful existing information.

Improve or consolidate it instead of blindly replacing it.

Never modify unless explicitly requested:

- model selection;
- reasoning level;
- provider;
- authentication;
- credentials;
- user-global agent configuration.

Never delete useful project knowledge simply because it should not live in permanent context.

---

# 3. Build the AGENTS.md Hierarchy

Create or improve the root:

```text
AGENTS.md
```

This is the canonical project map.

Keep it concise and focused on durable information useful across many tasks.

Include only relevant sections.

## Project Overview

Briefly describe the project and main stack.

## Repository Map

Map only important directories.

Example:

```text
src/        → application source
tests/      → automated tests
assets/     → static assets
scripts/    → development/build utilities
docs/       → detailed documentation
```

Do not document every directory.

## Important Systems

Map important files, modules, packages, or directories to their primary responsibility.

Example:

```text
src/auth/       → authentication and sessions
src/api/        → API layer
src/domain/     → business logic
src/database/   → persistence
src/ui/         → user interface
```

Keep descriptions short.

Do not reproduce source code.

Do not document every class or function.

## Architecture

Document only meaningful ownership boundaries, dependencies, and data flows.

Example:

```text
UI
→ application state
→ services
→ API

API
→ domain logic
→ persistence
```

The goal is to tell future agents:

```text
WHERE to look
WHAT owns the responsibility
WHAT depends on what
HOW to verify changes
```

## Commands

Document verified commands when available:

- run/development;
- build;
- targeted tests;
- full tests;
- lint;
- formatting;
- type checking.

Do not invent commands.

Mark uncertain commands as unverified.

## Nested AGENTS.md

Create nested `AGENTS.md` files only when a subtree has enough specialized architecture, conventions, or verification rules to justify one.

Possible example:

```text
AGENTS.md
src/AGENTS.md
src/backend/AGENTS.md
tests/AGENTS.md
```

Do not create one in every directory.

Nested files should contain only subtree-specific information and should not unnecessarily repeat parent instructions.

The deeper the file, the more specific it should be.

---

# 4. Permanent Navigation Rules

Ensure the generated `AGENTS.md` hierarchy contains the following durable behavior where appropriate:

- Treat the `AGENTS.md` hierarchy as the primary repository map.
- Do not rediscover architecture already documented there.
- Before opening files, identify the smallest likely relevant subsystem.
- Prefer symbol, reference, and text search before broad reading.
- Read only relevant files and the dependencies required to understand the task.
- Expand exploration only when evidence requires it.
- Do not scan the entire repository during ordinary tasks.
- Do not repeatedly reread files already understood during the same task without reason.
- Prefer modifying the existing responsible system over creating parallel implementations.
- Respect existing architecture unless the requested change requires altering it.
- Search large documentation first and read only relevant sections.
- Ignore generated/cache/build/vendor content unless the task concerns it.
- Inspect repository state before broad changes when version control is available.
- Run the smallest meaningful verification after modifications.
- Update project maps only when documented architecture or responsibilities become inaccurate.

Do not turn `AGENTS.md` into a miniature copy of the codebase.

---

# 5. Code Organization and Context Efficiency

Structure the codebase so both humans and coding agents can understand and modify a feature by reading the smallest reasonable amount of code.

Maintainability and context efficiency are the same architectural goal.

## Ownership

- Every important responsibility should have a clear owner.
- Each file/module/class should have one primary cohesive responsibility.
- Keep strongly related behavior together.
- Keep unrelated systems separate.
- Avoid duplicated ownership of the same state or behavior.
- Prefer extending the existing responsible subsystem over creating a parallel one.

When adding functionality, determine:

1. Which subsystem owns this responsibility?
2. Can the change remain local to that subsystem?
3. Would adding it to the current file introduce a new unrelated responsibility?
4. Would extracting a cohesive module make future work require less unrelated code to be read?

Create a new module only when it represents a genuine responsibility.

## File and Module Size

Do not enforce arbitrary line-count limits.

A large file is acceptable if it remains cohesive and easy to navigate.

Treat a file as a refactoring candidate when:

- it owns several independent responsibilities;
- unrelated features repeatedly modify it;
- understanding one feature requires reading large unrelated sections;
- it has become a catch-all or god object;
- a new responsibility is being added that can exist independently;
- extracting a cohesive subsystem would make future changes more local.

Split by responsibility, not by line count.

Avoid the opposite extreme:

- many tiny files with no meaningful ownership;
- wrapper modules that only forward calls;
- unnecessary abstraction layers;
- fragmentation that forces more files to be opened than before.

The preferred structure minimizes both coupling and unrelated context.

## Dependencies

Prefer simple and understandable dependency direction.

- Avoid circular dependencies.
- Avoid hidden global coupling.
- Keep public interfaces small.
- Keep implementation details local where practical.
- Separate UI, domain logic, persistence, transport, and infrastructure when they are genuinely distinct responsibilities.
- Use events, signals, interfaces, or dependency injection only when they meaningfully reduce coupling.
- Do not introduce abstraction solely for architectural purity.

A subsystem should expose enough of an interface that callers do not need to understand its internals.

## Functions and Classes

- Functions should perform one coherent task.
- Classes/modules should represent one coherent responsibility.
- Extract logic when the extracted concept has a meaningful name or responsibility.
- Avoid unnecessarily deep control flow.
- Prefer readable, explicit code over clever code.
- Keep public APIs focused.
- Avoid generic catch-all helpers when a specific owner exists.

## Architectural Locality

A change to one responsibility should, whenever reasonably possible, require understanding and modifying only:

```text
that responsibility
+ its immediate dependencies
+ its relevant verification
```

If a simple feature routinely requires reading many unrelated files, treat that as a possible architectural smell.

Do not automatically refactor because of this signal.

Refactor only when it meaningfully affects the current work or when explicitly requested.

---

# 6. Claude Code Compatibility

`AGENTS.md` remains the canonical shared source of truth.

For each useful `AGENTS.md`, create a lightweight `CLAUDE.md` in the same directory when appropriate.

Preferred content:

```md
@AGENTS.md
```

Do not maintain duplicated instruction sets manually.

If an existing `CLAUDE.md` contains substantial useful project knowledge:

1. preserve it;
2. move detailed reference material to an appropriate optional file such as:

```text
PROJECT_REFERENCE.md
```

3. replace the automatically loaded `CLAUDE.md` with:

```md
@AGENTS.md
```

4. reference the detailed document from the relevant `AGENTS.md`.

Never discard useful existing project knowledge.

---

# 7. Large Documentation and Generated Content

Identify unusually large documentation such as:

```text
PROJECT_REFERENCE.md
HANDOFF.md
ARCHITECTURE.md
CHANGELOG.md
large README files
docs/
```

Keep these files available.

Do not make them mandatory startup reading.

Document their purpose briefly and instruct future agents to use:

```text
search topic
→ read relevant section
```

instead of reading the whole document.

Also identify project-specific generated, cached, compiled, vendored, or normally irrelevant content.

Possible examples:

```text
node_modules/
dist/
build/
coverage/
.cache/
tmp/
engine caches
IDE caches
compiled output
generated imports
exports
```

Do not blindly apply this list.

Determine what is actually safe to ignore in this repository.

If useful, create minimal project-local exclusions such as:

```text
.claude/settings.json
```

Do not block potentially useful:

- source code;
- tests;
- fixtures;
- migrations;
- documentation;
- project assets;
- useful archives;

without a clear reason.

---

# 8. Implementation and Bug-Fix Discipline

Future modifications should prefer the **smallest correct solution**.

Before introducing new code, check in this order:

1. Is the requested behavior already supported?
2. Does an existing project system/helper/pattern already solve it?
3. Does the language standard library solve it?
4. Does the framework/platform provide a native solution?
5. Does an already-installed dependency solve it?
6. Only then add the minimum new code necessary.

Rules:

- Prefer reuse over duplication.
- Prefer existing architecture over parallel systems.
- Avoid dependencies without a concrete benefit.
- Avoid abstractions for hypothetical future requirements.
- Avoid generic extension/configuration layers without a current need.
- Prefer straightforward readable code over clever code.
- Keep diffs focused.
- Minimize files touched when correctness allows it.
- Do not perform unrelated cleanup during targeted work.
- Do not rewrite working systems merely to match personal preference.
- Remove code made genuinely obsolete by the change when safe.

For bugs:

- identify the root cause before patching the visible symptom;
- trace the relevant execution/data flow when necessary;
- inspect callers and usages when relevant;
- fix the responsible shared layer when appropriate;
- avoid duplicating the same workaround across callers;
- avoid broad refactors unless required for a correct fix;
- add the smallest useful regression verification when practical.

Never simplify away:

- correctness;
- security;
- trust-boundary validation;
- data-loss prevention;
- accessibility;
- explicitly requested behavior.

---

# 9. Skills

Inspect recurring development workflows.

Examples:

- selecting the correct tests;
- build validation;
- migrations;
- release checks;
- asset validation;
- project-specific debugging;
- repetitive generation procedures.

Create a Skill only when a workflow is:

- repetitive;
- non-trivial;
- likely to be reused.

Use:

```text
AGENTS.md
```

for persistent navigation, architecture, and rules.

Use:

```text
.agents/skills/
```

for reusable procedures.

If the same Skill should be available to Claude Code, expose the same canonical source through:

```text
.claude/skills/
```

when practical.

Prefer one source of truth.

Use symlinks when appropriate and portable.

Do not turn simple repository information into Skills.

---

# 10. Optional Lean-Code Review

If useful and not already covered by project tooling, consider creating a lightweight review Skill that checks completed changes for:

- duplicated existing functionality;
- unnecessary abstractions;
- speculative flexibility;
- unnecessary dependencies;
- reimplementation of native or standard-library functionality;
- dead or obsolete code;
- unnecessary compatibility paths;
- unnecessary files or layers;
- simpler implementations that preserve behavior;
- architectural changes that unnecessarily increase the number of files future agents must understand.

This review is advisory.

It must never reduce:

- correctness;
- security;
- readability;
- maintainability;
- accessibility;
- explicitly requested behavior.

---

# 11. Verification Strategy

Use the smallest verification that provides meaningful confidence.

Examples:

```text
small logic change
→ targeted unit test

component change
→ relevant component test

shared core change
→ targeted tests + affected broader suite

build/config change
→ relevant build/check
```

Prefer existing test infrastructure.

For non-trivial logic, leave the smallest useful runnable verification that would fail if behavior regresses when practical.

Do not introduce an entirely new testing framework for one small check unless genuinely justified.

Do not automatically run expensive full-project verification when targeted checks are sufficient, unless project rules require it.

If verification itself is complex and repetitive, consider making it a Skill.

---

# 12. Documentation Maintenance

After every future task, check whether the change made existing project-map information inaccurate.

If yes, update only the **smallest relevant `AGENTS.md`**.

Update documentation when:

- an important file is added, removed, or renamed;
- a file changes its primary responsibility;
- a major module or subsystem is introduced or removed;
- architecture changes;
- an important dependency or data flow changes;
- run/build/test/lint commands change;
- a reusable workflow worth documenting is introduced;
- documented ownership becomes obsolete.

Do not update project maps for ordinary:

- bug fixes;
- implementation details;
- content changes;
- tuning values;
- small UI changes;
- internal refactors that preserve ownership and architecture.

When updating an `AGENTS.md`:

- remove obsolete entries;
- remove unnecessary duplication;
- keep descriptions concise;
- avoid transient task details;
- avoid documenting information obvious from the code;
- move detailed material to optional documentation instead of growing permanent context indefinitely.

If a file grows because a genuinely new responsibility is being added, consider whether that responsibility belongs in its own cohesive module before extending the existing file.

Never perform a repository-wide documentation refresh unless genuinely necessary.

---

# 13. Bootstrap Verification

Before considering bootstrap complete, verify that:

- documented paths exist;
- documented responsibilities match the actual code;
- documented commands are valid or clearly marked unverified;
- no production behavior was modified;
- no useful documentation was lost;
- nested `AGENTS.md` files do not unnecessarily duplicate parents;
- `CLAUDE.md` imports resolve correctly;
- Skills and symlinks resolve correctly when used;
- documentation references are not broken;
- exclusions do not hide useful project material;
- large documents are not mandatory startup reading;
- permanent instruction files remain concise;
- existing useful workflows were preserved;
- every rule needed during normal development has been transferred out of this bootstrap file.

Remove redundant, speculative, or unnecessary instructions discovered during verification.

---

# 14. Completion and Lifecycle

At the end of the bootstrap, report only:

1. files created;
2. files modified;
3. files moved or renamed;
4. resulting `AGENTS.md` hierarchy;
5. Skills created or shared;
6. exclusions/configuration added;
7. documentation moved to optional reference files;
8. anything that could not be confidently verified.

Do not perform product work as part of this bootstrap.

This file is only the one-time setup specification.

After bootstrap succeeds, future agents must rely on:

```text
AGENTS.md
nested AGENTS.md files
Skills
project-local configuration
targeted optional documentation
```

Do not require `AGENT_BOOTSTRAP.md` as permanent startup context.

Before declaring bootstrap complete, ensure that **every navigation rule, architecture rule, implementation rule, maintenance rule, and verification workflow required during normal development has been transferred to the appropriate `AGENTS.md`, Skill, or project-local configuration**.

No permanent development rule may exist only in this file.

After successful bootstrap verification, this file may be safely deleted.

Deleting `AGENT_BOOTSTRAP.md` must not remove anything required by future agent sessions.

If deleting it would lose necessary behavior, knowledge, workflow, or maintenance instructions, the bootstrap is not complete.