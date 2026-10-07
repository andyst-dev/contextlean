# ContextLean

**Bootstrap once. Read less. Change locally.**

ContextLean produces a reliable project map and a compact coding discipline for
Codex and Claude Code. It helps agents find responsible code, preserve important
constraints, make focused changes, and verify sufficient coverage.

## Install for Codex

```sh
codex plugin marketplace add andyst-dev/contextlean
codex plugin add contextlean@contextlean-local
```

## Install for Claude Code

```sh
claude plugin marketplace add andyst-dev/contextlean
claude plugin install contextlean@contextlean-local --scope user
```

These commands use our repository catalog, whose stable name is `contextlean-local`.
ContextLean is not listed in either platform's public directory yet.

## Bootstrap a project

Start a fresh agent session in your project. In Codex, use `/skills` or `$` to
select **Bootstrap Repository** (`contextlean:bootstrap`) and ask it to bootstrap
this repository. In Claude Code:

```text
/contextlean:bootstrap Bootstrap this repository.
```

Review the generated guidance, commit useful changes with your project, and start
a fresh session. Ordinary coding then uses your project's `AGENTS.md` and Claude
imports independently of the plugin.

## Update ContextLean

Codex:

```sh
codex plugin marketplace upgrade contextlean-local
codex plugin add contextlean@contextlean-local
```

Claude Code:

```sh
claude plugin update contextlean@contextlean-local --scope user
```

Restart afterward. Project guidance and customizations remain yours. Claude's
versioned installs can now update from 0.3.0 to **0.3.1**. See the
[installation guide](docs/installation.md) for requirements,
verification, same-version refreshes, local packages, troubleshooting and safe
uninstallation. [Distribution details](docs/distribution.md) cover maintainers.

**v0.3.1 — Packaging and distribution readiness.** See the
[v0.3.1 release notes](docs/release-v0.3.1.md). Balanced runtime guidance is unchanged.

## Balanced guidance

**v0.3.0 introduces the Balanced contract:** compact, maintained project guidance
for ordinary coding work, with less setup administration in startup context. Audit,
Lean Review and measurement remain optional, explicitly requested workflows.
See the [v0.3.0 release notes](docs/release-v0.3.0.md).

![Without ContextLean: explore the repository to find relevant code. With ContextLean: use a small project map to reach relevant code and tests.](docs/assets/before-after.svg)

*An intended navigation pattern, not a trace of every agent run or a measured saving.*

## The problem

A coding agent entering an unfamiliar project may read documentation, list folders,
search source files, and inspect tests before it finds the code that matters.
That exploration is useful, but repeating it can consume time and attention.
ContextLean records the stable directions once and helps you keep them accurate.

- **Context window:** the information an agent can work with at one time. Unrelated
  material takes room that could hold the task and relevant code.
- **Tokens:** the units a model reads and writes. Prompts, code and tool results all
  contribute to usage; fewer files do not automatically mean fewer tokens.
- **Repository exploration:** reading and searching to learn where things live.
- **Tool calls:** actions such as searching files or running tests. Necessary checks
  still matter even when they increase usage.

The intended result is less unnecessary exploration while preserving correct work.
ContextLean does not guarantee savings or make a model inherently smarter.

## What ContextLean does

- **Bootstrap Repository** inspects your project once and writes lean repository
  instructions: a small project map, verified commands and important rules.
- **Audit Context Locality** checks whether those directions still match the code.
- **Lean Change Review** checks changes for unnecessary complexity and scattered ownership.
- **Benchmark Context Usage** measures structure offline or, when explicitly requested,
  compares real model runs and their outcomes.

## Evidence and limits

- **Historical v0.2.1 performance evidence:** the
  [30-session harness-v4 study](benchmarks/results/2026-10-02-harness-v4-repeated-performance/README.md)
  measured a descriptive aggregate of **8.96% fewer tokens**, with mixed task-level
  outcomes. It tested the previous v0.2.1 contract. This is **not a v0.3.1 performance result**.
- **Balanced product-change validation:** the separate
  [six-session Old-versus-Balanced Refactor validation](benchmarks/results/2026-10-06-balanced-product-change/README.md)
  passed submitted tests, original regression tests and acceptance tests in **6/6**
  solutions. No material retained-contract regression was found. Its primary result
  is behavioral: Balanced preserved the tested Refactor behavior after simplifying
  the runtime contract. It is not a general performance benchmark.

The validation does not establish equivalence for complex architectural refactors;
three paired repetitions do not justify statistical-significance claims. The
representative automatic guidance is 4,752 bytes, down from 5,486 (13.38%); this is
an instruction-size measurement, not a promised token saving.
[Evidence provenance and earlier studies](docs/evidence.md).

## What gets created?

Bootstrap writes repository guidance; it does not change your application's behavior.

- `AGENTS.md`: a project map, ownership boundaries, verified commands and important
  coding rules. Existing useful knowledge is preserved. Nested maps are added only
  for genuinely specialized subtrees.
- `CLAUDE.md`: normally `@AGENTS.md`, so Claude reads the same guidance. Useful existing
  Claude notes and necessary platform exceptions are preserved during setup.
- Only when needed: targeted project references and proven-safe local exclusions.

Default bootstrap creates no project Skills, transfer receipts or measurement reports.
Ordinary work corrects map entries made inaccurate by the change or discovered stale;
it does not require a map check after every task. Request Audit for broader drift.

If you separately request measurement, keep its local `.contextlean/` reports out of
Git and startup context. Existing reports and guidance are not deleted by this change.

## What is AGENTS.md?

`AGENTS.md` is repository guidance that compatible coding agents can read when they
start work. It gives directions without replacing the code or tests. For example:

```md
# Project map
- API routes: app/api.py
- Business logic: app/services.py
- Security checks: app/security.py
- Tests: tests/

# Important rules
- Run pytest before finishing.
- Do not bypass server-side request validation.
```

This is an example, not files or commands generated for every repository. ContextLean
tries to keep guidance small instead of copying the README or cataloguing every file.
See the [representative project map](tests/fixtures/bootstrap-core/project-map.md) and
[ordinary coding guidance](skills/bootstrap/references/core-guidance.md).

## Skills

| Workflow | Codex selector / installed name | Claude Code | What it does |
|---|---|---|---|
| Bootstrap Repository | `contextlean:bootstrap` | `/contextlean:bootstrap` | Creates or improves small repository instructions once. Explicit invocation required. |
| Lean Change Review | `contextlean:lean-review` | `/contextlean:lean-review` | Checks a change for duplicate behavior, unnecessary complexity and scattered ownership. Read-only. |
| Audit Context Locality | `contextlean:audit` | `/contextlean:audit` | Checks whether guidance matches the repository and whether responsibilities remain local. Read-only. |
| Benchmark Context Usage | `contextlean:benchmark` | `/contextlean:benchmark` | Offers an offline structural estimate or opt-in live Codex measurement. |

In Codex, use `/skills` or the `$` selector to choose the installed name above.
[Official skill selection guidance](https://learn.chatgpt.com/docs/build-skills).

For audit, **PASS** means verified with no action needed; **WARNING** means a concern
needs judgment; **ACTION NEEDED** means a concrete mismatch or broken configuration.
An illustrative report might read:

```text
PASS — CLAUDE.md imports the existing AGENTS.md.
WARNING — a startup instruction appears to require a large architecture document.
ACTION NEEDED — AGENTS.md points to a test command that no longer exists.
```

Request `audit fix` explicitly to allow narrow, safe guidance/configuration repairs.
A lean review edits code only when you separately request a fix.

## How it works

The plugin packages four instruction-based workflows shared by both agents.
Bootstrap preserves project knowledge, writes focused guidance, sets up compatible
Claude imports and validates actual paths, commands, ownership and references.
Later sessions use the project guidance without needing an installed ContextLean plugin.

Balanced intentionally retires complete original-bootstrap compatibility. The original
specification and previous validation remain historical evidence; their behavior and
measurements are not claims about this new contract. See the
[Balanced contract and historical comparison](docs/balanced-contract.md).

There is no MCP server, hook, background process, runtime package or telemetry.
Skill discovery can add descriptions to agent context; workflows run only on request.
Project-Skill authoring and sharing remain available as
[optional maintainer guidance](docs/guidance-authoring.md), outside default setup.

## Benchmark methodology

There are two kinds of evidence:

- **Static estimate:** exact instruction-file counts plus a labelled byte-to-token
  approximation. It does not measure model usage, speed or task quality.
- **Live measurement:** isolated Codex runs with the same task, model, reasoning,
  starting code and evaluator. The graded sample suite covers five task categories.
  The older read-only `benchmark ab` mode measures navigation but leaves answer
  correctness unverified; it cannot support a gain claim.

Live runs consume provider usage and are never part of CI.
The [evidence guide](docs/evidence.md) separates historical performance studies
from the Balanced product-change validation, with frozen prompts, source snapshots,
evaluators, ordering and raw outcomes.
Provider caching and service load were uncontrolled; the plugin itself was excluded
from both conditions to isolate the generated guidance. For reproduction and grading,
use the [benchmark guide](benchmarks/README.md).

## Supported agents

| Agent | Integration | Verified scope |
|---|---|---|
| Codex CLI | Plugin + shared skills; project `AGENTS.md` | Isolated native installation, four-Skill discovery, relocation, update and uninstall. |
| Claude Code | Same skills; project `CLAUDE.md` imports `AGENTS.md` | Isolated native installation, four-Skill discovery, relocation, update and uninstall. No live workflow run in this pass. |

The [distribution guide](docs/distribution.md) records current official platform
requirements, tested CLI versions and publication limits. No other agent integration
is claimed. The [release verification](docs/release-v0.3.0-verification.md) is the
separate, preserved record of v0.3.0 validation.

## Limitations

Route to code instead of duplicating it. Keep stable information. Avoid documenting
facts that are cheap to rediscover. Preserve correctness and security. Prefer one
clear owner and existing tooling over speculative abstractions.

Guidance can become stale and agents can ignore it. A small map may increase tokens
on easy tasks. Results depend on the model, task, caching and environment. The sample
suite is a small synthetic Python project, not evidence for every real repository.
ContextLean runs locally without telemetry; live runs use your configured model provider.
Raw logs from arbitrary projects need review before sharing.

## Development / contributing

Python 3.11+; the product and test suite use only the standard library.

```sh
python3 -m unittest discover -s tests -v
python3 -m pip install ruff==0.15.7  # development checker only
ruff check .
ruff format --check .
```

[Quality CI](.github/workflows/quality.yml) runs offline tests and checks on Python
3.11 and 3.14. [Contributor guidance](AGENTS.md) maps the package, skills and benchmark
owners. The [installation guide](docs/installation.md) routes to optional validators
and verification limits. Do not add runtime dependencies, hooks or automatic live runs.

## License

[MIT](LICENSE)
