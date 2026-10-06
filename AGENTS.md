# ContextLean Repository Instructions

## Project Overview

ContextLean 0.3.0 is a dependency-free, skills-only Codex/Claude Code plugin: produce reliable maps and compact coding guidance under the Balanced contract; audit drift, review locality and measure context only on request. No MCP server, hooks, runtime package, telemetry or automatic benchmark; remain silent by default.

## Repository Map

```text
.codex-plugin/plugin.json -> Codex package manifest
.claude-plugin/plugin.json -> Claude Code package manifest
.claude-plugin/marketplace.json -> local installation catalog for both agents
skills/bootstrap/ -> explicit, side-effecting one-time bootstrap
skills/bootstrap/references/bootstrap-spec.md -> canonical detailed bootstrap procedure
skills/bootstrap/references/core-guidance.md -> Balanced ordinary coding kernel
skills/bootstrap/references/permanent-rules.json -> frozen legacy facet inventory
skills/bootstrap/scripts/verify_transfer.py -> explicit legacy receipt inspection, not a setup gate
skills/audit/ -> read-only context and locality audit; safe fix mode is explicit
skills/lean-review/ -> optional review and specialized architecture guidance
skills/benchmark/ -> static estimate and opt-in real Codex A/B benchmark
skills/benchmark/scripts/benchmark.py -> dependency-free snapshot, runner, aggregation, and reporting
skills/benchmark/data/credit-rates.json -> dated official ChatGPT credit-equivalent rates
benchmarks/ -> graded sample tasks, fixture, evaluator, and opt-in runner
benchmarks/prepare_fixture.py -> offline map review, equivalent-state check, and validated fixture freezing
benchmarks/harness.py -> v4 session isolation, runtime/Git/permission gates, and evidence hygiene
benchmarks/compare_products.py -> separate frozen Old/Balanced adapter using shared v4 execution
benchmarks/execution.py -> provider-aware sandbox strategy and offline CLI compatibility probes
benchmarks/runtime.py -> session-local runtime shims, shell/cache setup and native effective-runtime probe
benchmarks/trace.py -> exposed command, coverage, primary/helper token evidence parsing
benchmarks/methodology-v2.md -> future graded experiment controls and provider limitations
benchmarks/results/ -> optional public evidence with frozen source and solutions
tests/test_public_validation.py -> offline reconciliation and regrading of published evidence
tests/test_harness.py -> offline isolation, equivalence, instrumentation, and failure contracts
tests/test_product_comparison.py -> guided revision provenance, rejection gates and shared execution tests
tests/test_execution.py -> offline native sandbox composition, permission parity, and fail-closed guards
tests/test_runtime.py -> offline login-shell, effective-runtime, cache and coverage identity regressions
docs/ -> visual, verification records and historical release notes
docs/balanced-contract.md -> current product contract and intentional historical changes
docs/evidence.md -> separates historical performance from Balanced behavioral validation
docs/release-v0.3.0.md -> current release notes
docs/release-v0.3.0-verification.md -> deterministic release checks
docs/guidance-authoring.md -> optional map and project-Skill authoring/sharing
docs/product-comparison-adapter.md -> comparison setup, invariants and offline validation record
.github/workflows/quality.yml -> offline tests, lint, and formatting
tests/test_package.py -> dependency-free package contract tests
tests/test_benchmark.py -> offline benchmark parsing, math, and report tests
tests/test_skill_contracts.py -> fixture-backed bootstrap, audit, and review contracts
tests/test_bootstrap_transfer.py -> Balanced semantic/generation contracts and legacy smoke check
tests/bootstrap_fixture.py -> offline fresh Balanced guidance fixture generation
tests/fixtures/bootstrap-core/ -> representative project map input
tests/fixtures/bootstrap-transfer/ -> frozen legacy transfer example
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

`bootstrap` owns initial guidance setup: explicit request required, implicit Codex invocation disabled. It validates concrete outputs without historical transfer receipts or mandatory measurement reports. On-demand `audit`/`lean-review` are read-only unless narrow fixes are separately authorized. `benchmark estimate` is offline/read-only; opt-in `benchmark ab` uses isolated temporary copies and writes local reports only to the requested output path.

Keep benchmark the fourth sibling under `skills/`; static snapshot/report capture is a separately requested measurement workflow. No MCP, hooks, session-start scripts, telemetry or added startup instructions without an explicit versioned product decision.

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

Use development-only Ruff pinned in CI; frozen `benchmarks/results/` snapshots are excluded from lint/format and checked by evidence tests. Keep tests/fixtures offline: never live `codex exec` in normal tests. A/B is explicit opt-in. The graded suite owns independent task acceptance; generic navigation turn completion is not task success.

Keep changes focused: avoid duplication, speculative layers, unnecessary dependencies, misplaced responsibility and avoidable cross-file context. Packaged `contextlean:lean-review` and `contextlean:audit` remain on-demand. When changes invalidate mapped information or stale entries are encountered, correct only affected entries in the smallest map; otherwise leave maps alone.
