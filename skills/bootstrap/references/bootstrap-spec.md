# ContextLean bootstrap procedure

This is the canonical one-time procedure. Read it only after an explicit bootstrap request,
completely before changing the repository. Also read `permanent-rules.json` completely:
stable group/facet identifiers define behaviors to transfer, not extra startup context or
a verbatim instruction template.

The outcome is a small, durable repository map for Codex and Claude Code. Bootstrap
may change agent guidance and narrowly related configuration, but it must not change
application behavior, product code or runtime dependencies. Never modify model
selection, reasoning level, provider, authentication, credentials or user-global
configuration unless the user separately and explicitly requests that change.

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

- project type, languages, important frameworks/libraries/dependencies, entry points,
  and package managers; inventory only libraries that help explain the project;
- important directories, subsystems, ownership boundaries, and dependency flows;
- verified run, build, test, lint, format, and type-check commands; distinguish targeted,
  affected broader and full verification, recording targeted/full commands when they exist;
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
→ check map accuracy and update only the smallest relevant map when needed
```

Transfer all 71 `permanent-rules.json` facets with their identifiers, meanings and ordered
choices intact. Categories distinguish automatic invariants/actions, packaged delegation,
conditional detail and consolidated duplicates. Share wording/destinations, never drop duties.
Keep navigation, coding, safety, proportional verification and after-task map checks automatic.
Inspect version-control state before broad/state-sensitive changes when available; read-only
navigation needs no Git ritual. Verification chooses scope: targeted first, broaden for shared/
core impact, full only when necessary/project-required, not three mandatory sequential steps.

Use one optional `PROJECT_REFERENCE.md` (or an equivalent existing reference) for the inventory's
architecture/extraction and project Skill creation/sharing/discovery details. Link each section
from the map with an explicit task trigger; never import it or require it on every task. Bug/
verification examples may share it, with baseline duties automatic. Adapt existing equivalent
rules instead of duplicating them; nested maps are only for subtree-specific behavior. Aim for
roughly 4.5–5.5 KB on a small representative map; preservation overrides this nonbinding target.
Do not copy setup steps, identifiers or the transfer ledger into permanent context.

Explicitly delegate advisory completed-change review to packaged `contextlean:lean-review`
in reachable guidance; do not generate another generic review Skill. Document the
separate `contextlean:audit` drift-inspection workflow. Ordinary implementation and
maintenance duties still belong in project guidance; optional review is not their substitute.

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

Verify every relative import; re-running bootstrap on an unchanged, already-clean repository
should produce no further guidance changes.

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
Codex and Claude variants. Project sources belong at `.agents/skills/<name>/SKILL.md`;
Claude discovery uses `.claude/skills/<name>/SKILL.md`. These are target-project locations,
distinct from ContextLean's plugin-root `skills/`. Prefer a relative directory symlink
for sharing only when portable: resolve it inside the project, verify discovery on both
installed tools without a model turn, and report an unsupported sharing route rather
than copying instructions. Preserve existing project workflows and valid sharing layouts.

## 6. Verify before finishing

Check all of the following against the final filesystem:

- documented paths, responsibilities, dependency flows, and commands are accurate;
- useful existing guidance and documentation were preserved;
- no product file, runtime dependency, application behavior, or unrelated config was
  changed by bootstrap;
- parent and nested maps do not duplicate each other;
- every Claude wrapper and Skill/reference path resolves;
- project Skill symlinks are relative, portable and resolve to the canonical source;
- exclusions do not hide useful project material;
- large optional documents are not required at startup;
- permanent instruction files remain concise;
- a second conceptual pass would be idempotent because no unresolved bootstrap work
  remains.

Remove redundancy/speculation. Report product-locality refactors separately; bootstrap must not
perform them.

### Permanent-rule transfer and safe-removal gate

Before success, review every facet in `permanent-rules.json` against its actual durable
destination. No required normal-development behavior may exist only in a setup file.
Write local `.contextlean/bootstrap-transfer.json`: `schema_version: 2`, `rules` keyed by group
ids. Each group has all `facets`, `semantics_reviewed: true`, and `destinations`; each destination
has its subset of `facets`, `kind`, relative `path`, optional Markdown `section` and `sha256`
of the exact UTF-8 section body (whole file without a heading). Assign every facet exactly once,
including consolidated facets sharing another group's section; hashes bind review to final
content. Existing version 1 records remain supported; use version 2 for the split.
Do not attest a missing or weakened facet; adapt the guidance first. This record is
verification evidence, not agent context; ignore `.contextlean/` in project Git rules.

Kinds are `guidance`, `configuration`, `reference` or `project_skill`, reachable through
explicit local links/imports from the root map. Nested destinations must apply to every
subtree needing the rule; a local-only map cannot carry a repository-wide duty alone.
Each `reference` also has `activation`: automatic source `path`, `section`, `sha256`, and `when`
describing its task trigger. The reviewed source must link to the reference and instruct reading
for that condition. Automatic reference imports fail. Review the trigger semantically; a nonempty
`when` cannot prove appropriate applicability in prose.
Only the advisory `lean-review` group may use `contextlean_skill`, with
`skill: contextlean:lean-review`, `path: skills/lean-review/SKILL.md` resolved from the
installed plugin and its reviewed section/hash. Verify that workflow remains available
to future sessions; record its qualified name in project guidance. Other development
rules cannot be silently assigned to optional review. See the compact worked transfer
example in `docs/bootstrap-coverage.md` when authoring the record.

Run from the installed ContextLean plugin root, without starting a model:

```bash
python3 skills/bootstrap/scripts/verify_transfer.py --repo <repository-root>
```

The read-only checker rejects incomplete groups/facets, unreviewed or changed content,
unreachable destinations and reliance on setup specifications. It checks structure and
review integrity, not natural-language meaning: the agent must perform the semantic
comparison and verify scope/applicability, configuration effect and Skill discovery.
Conceptually exclude/remove `AGENT_BOOTSTRAP.md` and any target copy of this procedure
from future context; verify that every duty remains available through maps, wrappers,
Skills, local configuration or targeted optional references. If anything would be lost,
reject completion, preserve the baseline and report what remains unresolved.
Do not delete useful files automatically or delete the installed reusable plugin spec.

## 7. Write the static report

Only after semantic review, safe-removal verification and a passing transfer check,
convert the captured baseline into
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

Repeat flags as needed; omit empty categories and resolve the script as in step 1. The report
records exact file/path measurements, token estimates, heuristic startup-document detection
and the supplied action log. Never include repository contents, secrets, credentials, command
output, telemetry or an archive.

On success, `bootstrap-finish` removes only the temporary baseline. On failure preserve it, report
the failure, and do not invent before/after values.
Never import reports or the transfer record from `AGENTS.md`, `CLAUDE.md`, hooks,
or startup scripts. Future sessions must not need a bootstrap specification.

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
