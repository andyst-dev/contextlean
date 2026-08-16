# ContextLean bootstrap procedure

This is the canonical one-time bootstrap procedure. Read it only after the user
explicitly asks to bootstrap a repository, and read it completely before changing
that repository.

The outcome is a small, durable repository map for Codex and Claude Code. Bootstrap
may change agent guidance and narrowly related configuration, but it must not change
application behavior, product code, dependencies, models, providers, authentication,
credentials, or user-global configuration.

## 1. Establish scope and capture the baseline

1. Identify the repository root and the ContextLean plugin root. They may differ.
2. Confirm that the request explicitly authorizes bootstrap.
3. Inspect repository status when version control is available so existing work is
   not mistaken for bootstrap output.
4. Before modifying any repository file, run the dependency-free snapshot from the
   ContextLean plugin root:

   ```bash
   python3 skills/benchmark/scripts/benchmark.py bootstrap-start \
     --repo <repository-root>
   ```

   Resolve the script from the installed plugin when it is not inside the target
   repository. The command writes `.contextlean/.bootstrap-baseline.json`, containing
   paths and static measurements but no file contents or secrets. Stop if capture
   fails. Never reconstruct a missing before state after edits have begun.

## 2. Analyze once

Build a concise working inventory of:

- project type, languages, frameworks, entry points, and package managers;
- important directories, subsystems, ownership boundaries, and dependency flows;
- verified run, build, test, lint, format, and type-check commands;
- generated, cached, compiled, vendored, and coverage output;
- existing `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, `.codex/`, README,
  documentation, CI, and build/test configuration;
- large documentation, recurring workflows, and clear locality problems.

Search by filename or symbol before broad reading. Read large documents only where
needed to preserve their knowledge. Existing instructions are input, not disposable
scaffolding: retain accurate project-specific facts and resolve conflicts using the
current repository as evidence.

## 3. Create the smallest useful guidance hierarchy

Use `AGENTS.md` as the canonical cross-platform source. The root file should contain
only durable information that helps many future tasks, selected from:

- a brief project and stack overview;
- a map of important directories and systems;
- meaningful ownership, dependency, or data-flow boundaries;
- verified development and validation commands;
- navigation, implementation, verification, and map-maintenance rules that are
  genuinely needed by this repository.

Do not inventory every directory, class, or function. Do not copy source code or
large documentation into permanent context. Mark an uncertain command as unverified
instead of inventing certainty.

Create a nested `AGENTS.md` only when a subtree has enough specialized architecture,
conventions, or verification to justify it. A nested file contains only subtree-
specific guidance and does not repeat its parent. Prefer the shallowest hierarchy
that remains useful.

The resulting guidance should support this normal workflow:

```text
project map
→ responsible subsystem
→ targeted search and reads
→ smallest correct change
→ proportional verification
→ map update only when ownership or architecture changed
```

Include concise repository-specific rules that keep work local:

- identify the likely owner before opening broad areas;
- search before claiming duplication or creating parallel behavior;
- read immediate dependencies and relevant tests, expanding only with evidence;
- prefer the standard library, framework, and installed dependencies before adding
  code or packages;
- split by cohesive responsibility, never arbitrary file size;
- avoid speculative abstractions, forwarding wrappers, catch-all helpers, and
  unrelated cleanup;
- preserve correctness, security, validation, data safety, accessibility, and
  requested behavior;
- run the smallest meaningful verification, broadening it when shared behavior or
  repository rules require that;
- update only the nearest affected map when an important path, command, ownership
  boundary, or dependency flow changes.

Do not require future sessions to read this bootstrap procedure.

## 4. Reuse the map from Claude Code

For every useful `AGENTS.md`, create a same-directory `CLAUDE.md` when Claude Code
compatibility is appropriate. Its preferred complete content is:

```md
@AGENTS.md
```

If a pre-existing `CLAUDE.md` contains useful knowledge, do not overwrite or discard
it. Move substantial details to a clearly named optional document such as
`PROJECT_REFERENCE.md`, reference that document from the relevant `AGENTS.md`, then
replace the automatically loaded file with the lightweight import. Preserve any
Claude-specific instruction that cannot be represented safely in shared guidance and
explain the exception.

Verify every import relative to its wrapper. Re-running bootstrap on an unchanged,
already-clean repository should produce no further guidance changes.

## 5. Keep optional context optional

Large architecture notes, handoffs, changelogs, and detailed README sections remain
available but must not become mandatory startup reading. Map their purpose briefly
and use the pattern `search topic → read relevant section`.

Add an exclusion only after proving it is generated, cached, compiled, vendored, or
otherwise irrelevant to ordinary repository work. Keep exclusions minimal and local.
Never hide source, tests, fixtures, migrations, documentation, assets, or useful
archives merely because they are large.

Create a project Skill only for a repetitive, non-trivial workflow likely to be
reused. Keep persistent architecture in `AGENTS.md`; keep procedures in Skills. When
both platforms need a project Skill, expose one canonical source rather than copied
Codex and Claude variants.

## 6. Verify before finishing

Check all of the following against the final filesystem:

- documented paths, responsibilities, dependency flows, and commands are accurate;
- useful existing guidance and documentation were preserved;
- no product file, runtime dependency, application behavior, or unrelated config was
  changed by bootstrap;
- parent and nested maps do not duplicate each other;
- every Claude wrapper and Skill/reference path resolves;
- exclusions do not hide useful project material;
- large optional documents are not required at startup;
- permanent instruction files remain concise;
- a second conceptual pass would be idempotent because no unresolved bootstrap work
  remains.

Remove redundancy or speculative guidance found during verification. If a product
refactor would improve locality, report it separately; bootstrap must not perform it.

## 7. Write the static report

After successful verification, convert the captured baseline into
`.contextlean/bootstrap-report.json` with the exact action log:

```bash
python3 skills/benchmark/scripts/benchmark.py bootstrap-finish \
  --repo <repository-root> \
  --project-type <project-type> \
  --created <path> \
  --modified <path> \
  --moved <old-path->new-path> \
  --exclusion <installed-exclusion> \
  --limit <measurement-limit>
```

Repeat flags as needed and omit empty categories. Resolve the script from the plugin
root as in step 1. The report records exact file/path measurements, explicit token
estimates, heuristic startup-document detection, and the supplied action log. It must
never contain repository contents, secrets, credentials, command output, telemetry,
or an archive.

On success, `bootstrap-finish` removes only the temporary baseline. If it fails,
preserve the baseline, report the failure, and do not invent before/after values.
Never import either report from `AGENTS.md`, `CLAUDE.md`, hooks, or startup scripts.

## 8. Completion report

Report only:

1. files created;
2. files modified;
3. files moved or renamed;
4. resulting `AGENTS.md` hierarchy;
5. Skills created or shared;
6. exclusions or local configuration added;
7. documentation moved to optional references;
8. anything not confidently verified.

Mention that `.contextlean/bootstrap-report.json` was written without presenting its
static estimates as measured token savings. Do not continue into feature work.
