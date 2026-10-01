# ContextLean Repository Instructions

## Project Overview

ContextLean 0.2.1 candidate is a dependency-free, skills-only Codex/Claude Code plugin: bootstrap guidance once, audit drift, review complexity/locality and measure context without invented gains. No MCP server, hooks, runtime package, telemetry or automatic benchmark; remain silent by default.

## Repository Map

```text
.codex-plugin/plugin.json -> Codex package manifest
.claude-plugin/plugin.json -> Claude Code package manifest
.claude-plugin/marketplace.json -> local installation catalog for both agents
skills/bootstrap/ -> explicit, side-effecting one-time bootstrap
skills/bootstrap/references/bootstrap-spec.md -> canonical detailed bootstrap procedure
skills/bootstrap/references/permanent-rules.json -> compact permanent behavior and semantic identifiers
skills/bootstrap/scripts/verify_transfer.py -> explicit, read-only bootstrap transfer verification
skills/audit/ -> read-only context and locality audit; safe fix mode is explicit
skills/lean-review/ -> read-only review of the current change
skills/benchmark/ -> static estimate and opt-in real Codex A/B benchmark
skills/benchmark/scripts/benchmark.py -> dependency-free snapshot, runner, aggregation, and reporting
skills/benchmark/data/credit-rates.json -> dated official ChatGPT credit-equivalent rates
benchmarks/ -> graded sample tasks, fixture, evaluator, and opt-in runner
benchmarks/prepare_fixture.py -> offline map review, equivalent-state check, and validated fixture freezing
benchmarks/results/ -> optional public evidence with frozen source and solutions
tests/test_public_validation.py -> offline reconciliation and regrading of published evidence
docs/ -> visual, verification record, and release notes
.github/workflows/quality.yml -> offline tests, lint, and formatting
tests/test_package.py -> dependency-free package contract tests
tests/test_benchmark.py -> offline benchmark parsing, math, and report tests
tests/test_skill_contracts.py -> fixture-backed bootstrap, audit, and review contracts
tests/test_bootstrap_transfer.py -> semantic contracts, transfer failures, and safe-removal checks
tests/bootstrap_fixture.py -> offline fresh compact guidance/transfer fixture application
tests/fixtures/projects/ -> minimal cross-project guidance fixtures
tests/fixtures/reviews/ -> representative lean-review diffs
README.md -> public usage and development documentation
LICENSE -> MIT license
```

`agents/openai.yaml` owns Codex UI metadata; adjacent `SKILL.md` owns the shared workflow.

## Architecture and Ownership

Manifests own platform packaging; both agents discover the same plugin-root Skills:

```text
plugin manifest -> skills/ -> focused SKILL.md -> optional targeted reference
```

Only `bootstrap` owns guidance mutation: explicit request required, implicit Codex invocation disabled. Its optional procedure captures a local static before/after report. On-demand `audit`/`lean-review` are read-only unless narrow fixes are separately authorized. `benchmark estimate` is offline/read-only; opt-in `benchmark ab` uses isolated temporary copies and writes local reports only to the requested output path.

Keep benchmark the fourth sibling under `skills/`; its sole bootstrap coupling is explicit static snapshot/report capture. No MCP, hooks, session-start scripts, telemetry or added startup instructions without an explicit versioned product decision.

## Navigation and Implementation

1. Use the nearest applicable `AGENTS.md`; identify the owning manifest, Skill, reference or test.
2. Search before broad reading. Read the bootstrap spec only when applying, changing or validating it.
3. Keep shared behavior in one `SKILL.md`; platform metadata needs a concrete compatibility reason.
4. Prefer existing tooling/standard library; no runtime dependency for behavior expressible as instructions.

## Verification

Run the package contract tests after changing manifests, Skills, wrappers, or layout:

```bash
python3 -m unittest discover -s tests -v
ruff check .
ruff format --check .
```

Run current Codex plugin/Skill validators when available; with Claude installed, run `claude plugin validate .claude-plugin/plugin.json` and `claude plugin validate .claude-plugin/marketplace.json`. Its wrapper warning means root `CLAUDE.md` is not injected as plugin context. Do not invent unverified commands.

Use development-only Ruff pinned in CI. Keep tests/fixtures offline: never live `codex exec` in normal tests. A/B is explicit opt-in. The graded suite owns independent task acceptance; generic navigation turn completion is not task success.

Keep changes focused: avoid duplication, speculative layers, unnecessary dependencies, misplaced responsibility and avoidable cross-file context. Packaged `contextlean:lean-review` and `contextlean:audit` remain on-demand. After each task, check map accuracy; update only for important path, ownership, dependency-flow or verification-command changes.
