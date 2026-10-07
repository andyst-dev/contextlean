> Current release: [v0.3.0 deterministic verification](../release-v0.3.0-verification.md).
> The installation and earlier release observations below retain their original scope.

# ContextLean 0.2.0 verification

The current v0.3.0 contract is [Balanced](../balanced-contract.md). It intentionally
retires full original-bootstrap compatibility. The release/coverage records below
describe their historical revisions; they do not certify the Balanced contract.
See [v0.3.0 verification](../release-v0.3.0-verification.md) for current checks and limits.

## Historical v0.2.0 released status

[ContextLean v0.2.0](https://github.com/andyst-dev/contextlean/releases/tag/v0.2.0)
was publicly released on 2026-09-30. The annotated tag resolves to
`6113896f283f34558cbabaa1d6d25b6aa614b7a5`, which contains product commit
`86043499d5a375cc6a3b295bc7c03b0999eb458c` and the release-aligned evidence/docs.
Both manifests and the measurement helper identify 0.2.0.

- Main [Quality CI](https://github.com/andyst-dev/contextlean/actions/runs/36748490974)
  and [tag CI](https://github.com/andyst-dev/contextlean/actions/runs/36749324799)
  passed on Python 3.11 and 3.14.
- A fresh clone of the public release revision passed **114 offline tests**, Ruff
  0.15.7 lint/format, all four Skill validators, Codex/Claude package validators,
  evidence checksums, relative links and hygiene. The README tables and SVG were
  inspected on GitHub; benchmark and historical-bootstrap links resolved.
- Fresh temporary Codex and Claude profiles installed version 0.2.0 and discovered
  all four Skills without starting a model turn. Discovery does not establish full
  live workflow behavior or Claude's consumption of generated project imports.
- Semantic coverage remains **74 PASS / 0 PARTIAL / 0 MISSING / 2 INTENTIONALLY
  REPLACED**, with **71/71 permanent facets** preserved.
- The [release-aligned batch](../../benchmarks/results/2026-09-30-release-aligned-0.2.0/README.md)
  has ten passing solutions and independent offline regrading. It is preliminary:
  one run per condition per task, with no statistical-confidence, causal or universal
  token-savings claim. Unfavorable submetrics and earlier datasets remain preserved.

See [released v0.2.0 notes](release-notes.md). The records below document earlier
verification stages for maintainers. Their test counts, release-state limitations
and benchmark observations apply to those stages, not the current release status.
Optional development validators are maintainer checks, not user installation steps.

## Historical pre-commit verification — 2026-09-30

This record describes the local candidate before the
[semantic preservation repair](bootstrap-coverage.md), committed-revision checks,
push, remote CI and release. Both candidate manifests and the measurement helper
identified 0.2.0; the historical validation dataset retained its recorded 0.1.0 version.
No tag or release was created during this verification stage.

### Installation and discovery

Tests used a copied checkout, a fresh temporary target project, and empty temporary
Codex/Claude configuration directories. They used the installed CLIs; this is not a
clean-machine download test. Codex can still discover machine-wide/user skills;
verification selected the four ContextLean entries from the new plugin cache.

| Check | Result |
|---|---|
| Codex CLI 0.147.0: `codex plugin marketplace add .`, then `codex plugin add contextlean@contextlean-local` | PASS; cached plugin version 0.2.0 |
| Codex app-server `skills/list`, from the fresh target project | PASS; four enabled ContextLean skills, no discovery errors; metadata below |
| Claude Code 2.1.233: `claude --plugin-dir /path/to/contextlean plugin details contextlean` | PASS; 0.2.0, four skills, zero agents/hooks/MCP/LSP |
| Bundled Codex plugin-creator `scripts/validate_plugin.py` | PASS; manifest and skill metadata |
| Official skill-creator `scripts/quick_validate.py` | PASS for all four skill directories |
| `claude plugin validate .claude-plugin/plugin.json` | PASS; expected plugin-root CLAUDE.md warning |
| `claude plugin validate .claude-plugin/marketplace.json` | PASS; expected unknown Codex `policy` warning; Claude ignores that field |

Discovery returned this compact inventory (not a model-session transcript):

| UI name | Codex installed name | Claude command |
|---|---|---|
| Bootstrap Repository | `contextlean:bootstrap` | `/contextlean:bootstrap` |
| Audit Context Locality | `contextlean:audit` | `/contextlean:audit` |
| Lean Change Review | `contextlean:lean-review` | `/contextlean:lean-review` |
| Benchmark Context Usage | `contextlean:benchmark` | `/contextlean:benchmark` |

In Codex CLI, use `/skills` or type `$` and select the installed skill. UI default
prompts now reference the qualified installed name. `$bootstrap` alone is ambiguous.
[Official skill selection guidance](https://learn.chatgpt.com/docs/build-skills).
Codex installation takes **two commands** from an obtained checkout. The README
has five usage steps; Claude session loading takes one launch command after entering
the target project. Agent installation/authentication and Python 3.11+ are prerequisites.

The catalog uses a shared Claude-compatible local source and Codex policy metadata;
no duplicate catalog or always-loaded wrapper was added. With this catalog,
`claude plugin validate .` selects the marketplace, so verify both explicit paths.
The root `CLAUDE.md` is contributor guidance, not injected plugin context. Bootstrap
creates a wrapper in the user's project. Codex caches the plugin; reinstall after
editing it and start a fresh session. Claude `--plugin-dir` loads that session only.

No paid model session was started during these installation checks. Independent
full live bootstrap/audit/review invocation on both CLIs and Claude's consumption of
the project import remain unverified. Earlier procedure checks and static wrappers
are separate evidence; discovery alone does not establish model behavior.

#### Optional development validators

When the bundled validator files and temporary PyYAML dependency are available:

```sh
python3 /path/to/plugin-creator/scripts/validate_plugin.py .
python3 /path/to/skill-creator/scripts/quick_validate.py skills/bootstrap
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
```

Repeat the skill validator for audit, lean-review and benchmark. The Codex validator
was obtained from the installed CLI's bundled system skill in a temporary home.
These are verified script interfaces, not an invented `codex plugin validate` command.
They are optional development checks, not beginner installation prerequisites.

### Quality and deterministic CI

- Full standard-library test suite: **58 tests pass** locally on Python 3.14.4.
- Ruff **0.15.7** lint and format check pass; whitespace check passes.
- Public links, cross-platform packaging, skill frontmatter/metadata, explicit
  bootstrap policy and no-MCP/no-hooks contracts are checked by tests.
- Benchmark tests check event parsing, usage arithmetic, unavailable fields,
  suppression of ungraded gain claims, isolation, original-test restoration and grading.
- Public evidence tests check checksums, archive paths, frozen source/fixture/prompt/
  evaluator hashes, all ten recorded usage/command counts, negative cases and saved
  solutions. Regrading runs only local Python tests, with no model calls.
- [Quality CI](../../.github/workflows/quality.yml) runs tests, Ruff and formatting on
  Python **3.11 and 3.14**, with read-only repository permission. No live benchmark
  command or provider authentication is part of CI. Python 3.11 and remote Actions
  execution had not yet been verified at this stage; the workflow awaited a committed push.

No 100% coverage claim is made. Dependency-free refers to the product and tests;
Ruff and PyYAML for official validators are development-only tools.

### Evidence and hygiene

[Public validation](../../benchmarks/results/2026-09-30-validation/README.md) retains
all ten runs, original numeric records, prompts, diagnostics, grading and resulting
solutions. The source archive retains the exact source files used, with ten Finder/
linter metadata files excluded. The selection manifest records the original
whole-tree hash, curated hash, retained-file hashes and omitted-file hashes. The
original whole-tree hash includes excluded files and cannot be recomputed from the
curated archive; fixture/task/evaluator hashes still match.

Workspace/home prefixes were sanitized at capture. A scan of the public evidence,
archive contents and commit candidates found no personal paths/usernames or
credential patterns. This is a pattern scan, not proof that every possible secret
format is detectable. Original local validation, copied validator tooling, previews,
bytecode, Finder metadata, virtual environments and linter caches remain excluded
from Git. No public log or recorded number was edited to remove an inconvenient outcome.

The local SVG was rendered at 960 and 720 px and inspected. It uses an opaque dark
panel with high-contrast text, so the content has the same contrast on light/dark
pages. It states that agents may inspect more files. Remote GitHub rendering
had not yet been checked on an uploaded revision at this stage.

### ContextLean dogfood

Applied the canonical Audit Context Locality and Lean Change Review workflows to
this repository/change. Bootstrap was not repeated.

| Audit area | Status and evidence |
|---|---|
| Project map, ownership and commands | PASS; current paths and verified checks, one owner per skill, benchmark parsing reused by the graded runner |
| Startup context | PASS; concise root map and one-line `@AGENTS.md` wrapper; README, evidence archives and detailed bootstrap reference are optional |
| Shared skill layout and metadata | PASS; four canonical skill directories, validated metadata and qualified discovery names |
| Exclusions and preservation | PASS; generated-only exclusions; source, fixtures, documentation, assets and useful public archives stay available |
| Documentation freshness | PASS; 0.2.0 alignment, preliminary results labelled, negative cases and installation limits visible |
| Architecture and locality | PASS; no new runtime dependency, MCP, hook, telemetry, automatic model run or speculative wrapper |
| Independent agent behavior | WARNING; complete live invocation/Claude import consumption unverified; not inferred from installation |
| Measurement strength | WARNING; one observation per task/condition, uneven CLI errors/cache noise and non-Git workspaces; no final efficiency claim |
| Remote release checks | WARNING at this stage; remote CI and clean committed-revision installation had not yet been verified |

Lean Change Review found a concrete hygiene issue: snapshots retained Finder and
linter metadata. Public artifacts now omit those files with an explicit selection
record, and future copies exclude them through one shared name set with an offline
regression check. No other material duplication, dead layer, dependency or misplaced
owner remains in the reviewed change. The evaluator stays outside measured workspaces;
raw artifacts and archived historical source are evidence, not additional startup guidance.

### Release scope

At this stage, the candidate was ready for review before its initial 0.2.0 release
commit, with the limitations above.
Repeated benchmarks and independent paid workflow sessions are **not prerequisites**
for this scoped release and were not authorized at this stage. Remote CI and a
committed-revision install check remained subsequent release verification steps.
No universal performance claim, v1.0 claim or public marketplace listing is made. The [release notes](release-notes.md) now describe the published release.

## Historical clean-final benchmark verification — 2026-09-30

The [clean final evidence](../../benchmarks/results/2026-09-30-clean-final-0.2.0/README.md)
uses unchanged product commit `52a2c34` and the repaired preparation harness. All
five paired preparations pass before model execution; all ten saved solutions pass
offline regrading. The offline suite at this stage passed **92 tests**, with Ruff 0.15.7
lint/format, all four Skill validators and both platform package validators passing.
[Detailed quality record](../../benchmarks/results/2026-09-30-clean-final-0.2.0/quality-checks.json)
retains link, hygiene and preservation checks. At this stage the README used this
preliminary batch and disclosed its resource regressions. Historical and invalid diagnostic
files remain unchanged. No tag, release or further repetition was created.

## Historical compact-final validation — 2026-09-30

The [compact-final evidence](../../benchmarks/results/2026-09-30-compact-final-0.2.0/README.md)
uses frozen product `90ed9a4a049af519a40c36424ed1ff8b6acefe48`: the unchanged
completed Bug Fix pair plus exactly eight new calls, one per condition for each
remaining task. Every preparation passes before execution. All ten solutions pass
independent offline regrading. No additional model calls, tag or release were made.

ContextLean uses 16.84% fewer aggregate tokens and 5.97% less model-process time,
with 20% more commands. Feature regresses in time/commands, Refactor in all three,
and Documentation/config in commands. At this stage the README headlined this
preliminary tested configuration; previous datasets remain unchanged and are never pooled.
Between-batch differences establish neither causality nor statistical confidence.

The [quality record](../../benchmarks/results/2026-09-30-compact-final-0.2.0/quality-checks.json)
retains final offline test, Ruff, Skill/plugin validator, evidence/checksum, relative-link,
hygiene and frozen-content checks. The [standalone offline evidence validator](../../benchmarks/results/2026-09-30-compact-final-0.2.0/verify_evidence.py)
reconciles all ten conversations and independently regrades their archived solutions.
Product implementation, benchmark tasks/prompts/graders and the historical bootstrap
remain byte-identical to the frozen commit. Changes are documentation and evidence only.

## Historical release-aligned validation — 2026-09-30

The [release-aligned evidence](../../benchmarks/results/2026-09-30-release-aligned-0.2.0/README.md)
tests frozen product `86043499d5a375cc6a3b295bc7c03b0999eb458c` with exactly ten
fresh `gpt-5.6-terra` / low-reasoning calls: one per condition for each existing task.
All five paired preparations validate before execution, including mapped ownership,
equivalent code, fresh guidance, 71 permanent facets and unchanged prompts/tests.
No previous result is reused; all ten saved solutions pass independent offline regrading.

Measured totals: 482,024→341,676 tokens (-29.12%), 189.97→134.52 seconds (-29.19%),
and 18→16 commands. Bug Fix uses more output tokens/commands; Navigation has a
higher dated credit-equivalent. Raw diagnostics and recoveries are retained. Refactor
stays within mapped owners/tests with distinct searches, no Git inspection and
behavior-preserving verification; wider-impact expansion was not exercised.
One run per condition per task is preliminary validation, with no statistical-confidence,
causal or universal token-savings claim. Earlier datasets remain unchanged and separate.

The [quality record](../../benchmarks/results/2026-09-30-release-aligned-0.2.0/quality-checks.json)
records offline tests, Ruff, four Skill validators, Codex/Claude validators, semantic
coverage, relative links, hygiene and protected-content hashes. The
[standalone offline validator](../../benchmarks/results/2026-09-30-release-aligned-0.2.0/verify_evidence.py)
checks source/fixture provenance, checksums, ten unique fresh conversations, exact
usage/cost aggregation and all ten independent regrades without model calls.
Product behavior, benchmark tasks/prompts/graders/measurement and the original bootstrap
remain unchanged. Only release-aligned evidence and documentation are committed;
this validation stage did not include additional calls, a push, tag or release.
The subsequent release gate completed publication without additional model benchmarks,
as recorded above.
