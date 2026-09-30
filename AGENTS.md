# ContextLean Repository Instructions

## Project Overview

ContextLean is a dependency-free, skills-only plugin for Codex and Claude Code. It bootstraps repository guidance once, audits that guidance over time, reviews changes for unnecessary context and complexity, and measures context impact without inventing gains. Version 0.2.0 intentionally has no MCP server, hooks, runtime package, telemetry, or automatic benchmark.

## Repository Map

```text
.codex-plugin/plugin.json                 -> Codex package manifest
.claude-plugin/plugin.json                -> Claude Code package manifest
.claude-plugin/marketplace.json           -> local installation catalog for both agents
skills/bootstrap/                         -> explicit, side-effecting one-time bootstrap
skills/bootstrap/references/bootstrap-spec.md -> canonical detailed bootstrap procedure
skills/audit/                             -> read-only context and locality audit; safe fix mode is explicit
skills/lean-review/                       -> read-only review of the current change
skills/benchmark/                         -> static estimate and opt-in real Codex A/B benchmark
skills/benchmark/scripts/benchmark.py     -> dependency-free snapshot, runner, aggregation, and reporting
skills/benchmark/data/credit-rates.json   -> dated official ChatGPT credit-equivalent rates
benchmarks/                              -> graded sample tasks, fixture, evaluator, and opt-in runner
benchmarks/results/                     -> optional public evidence with frozen source and solutions
tests/test_public_validation.py          -> offline reconciliation and regrading of published evidence
docs/                                   -> visual, verification record, and draft release notes
.github/workflows/quality.yml            -> offline tests, lint, and formatting
tests/test_package.py                     -> dependency-free package contract tests
tests/test_benchmark.py                   -> offline benchmark parsing, math, and report tests
tests/test_skill_contracts.py             -> fixture-backed bootstrap, audit, and review contracts
tests/fixtures/projects/                  -> minimal cross-project guidance fixtures
tests/fixtures/reviews/                   -> representative lean-review diffs
README.md                                 -> public usage and development documentation
LICENSE                                   -> MIT license
```

Each Skill's `agents/openai.yaml` contains Codex UI metadata. The canonical cross-platform workflow remains its adjacent `SKILL.md`.

## Architecture and Ownership

The two manifests own platform packaging only. Both platforms discover the same canonical Skill directories at the plugin root:

```text
plugin manifest -> skills/ -> focused SKILL.md -> optional targeted reference
```

Only `bootstrap` owns repository-guidance mutation. Its detailed procedure lives in one optional reference, its common description requires an explicit request, and Codex metadata disables implicit invocation. It also captures a small local static before/after report for later estimates. `audit` and `lean-review` are read-only unless the user separately and explicitly authorizes their narrow fix behavior. `benchmark estimate` is offline and read-only; `benchmark ab` creates temporary isolated copies and writes only its local reports to the requested output path.

Keep benchmark as the fourth sibling Skill under `skills/`. Its only bootstrap coupling is the explicit static snapshot/report procedure; live A/B runs remain opt-in. Do not add MCP, hooks, session-start scripts, telemetry, or always-loaded instructions without an explicit versioned product decision.

## Navigation and Implementation

1. Start with the nearest applicable `AGENTS.md` and identify the owning manifest, Skill, reference, or test.
2. Search by filename or text before broad reading. Read the bootstrap specification only when applying that procedure, changing it, or validating its content.
3. Keep cross-platform workflow behavior in one `SKILL.md`; use platform metadata only for a concrete compatibility need.
4. Prefer the standard library and existing repository tooling. Add no runtime dependency for behavior expressible as agent instructions.
5. Preserve the no-MCP, no-hooks, no-telemetry, silent-by-default v0.2.0 boundaries.

## Verification

Run the package contract tests after changing manifests, Skills, wrappers, or layout:

```bash
python3 -m unittest discover -s tests -v
ruff check .
ruff format --check .
```

Also run the current Codex plugin validator and Skill validator when those tools are available. Run `claude plugin validate .claude-plugin/plugin.json` and `claude plugin validate .claude-plugin/marketplace.json` when Claude Code is installed. The plugin manifest warning explains that the repository's root `CLAUDE.md` wrapper is not injected as plugin context. Do not invent or document a command that has not been verified.

Use the development-only Ruff version pinned in CI. Benchmark unit tests and fixtures must remain offline. Never invoke live `codex exec` from the normal test suite; live A/B runs are explicitly opt-in. The graded development suite owns independent task acceptance; the generic navigation runner must not equate turn completion with task success.

Use `lean-review` conceptually on the final change: seek duplication, speculative layers, unnecessary dependencies, misplaced responsibility, and avoidable cross-file context. Update this map only when an important path, ownership boundary, dependency flow, or verification command changes.
