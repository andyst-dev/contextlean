# ContextLean v0.2.0

Released on 2026-09-30. [Public GitHub Release](https://github.com/andyst-dev/contextlean/releases/tag/v0.2.0).
Release commit: `6113896f283f34558cbabaa1d6d25b6aa614b7a5`.
[Release verification and historical records](verification.md).

ContextLean gives coding agents a compact, maintained map of a repository so they can find
relevant code without repeatedly exploring everything.

## Highlights

- Bootstrap Repository
- Audit Context Locality
- Lean Change Review
- Benchmark Context Usage
- Codex and Claude Code support
- Compact AGENTS.md guidance with conditional detailed references
- Project-map-driven navigation
- Semantic transfer and safe-removal contracts
- Original bootstrap intent preserved

ContextLean remains dependency-free and skills-only, with no MCP server, hooks, telemetry or
automatic benchmark runs.

## Compact context

Representative automatic AGENTS.md guidance was reduced from **7,956 bytes → approximately
5.5 KB** (5,476 bytes), while maintaining **74 PASS / 0 PARTIAL / 0 MISSING** across the
semantic coverage gate. Two mechanisms are intentionally replaced; all **71/71 permanent
facets** are preserved.

## Preliminary validation

The release-aligned batch used five existing tasks and **10 fresh runs**, with
`gpt-5.6-terra`, low reasoning, and one Vanilla and one ContextLean run per task. All ten
solutions passed acceptance, regression and submitted tests, including independent offline
regrading.

- Total tokens: **482,024 → 341,676 (-29.12%)**
- Wall time: **189.97s → 134.52s (-29.19%)**
- Commands: **18 → 16 (-11.11%)**
- Task success: **5/5 → 5/5**

Task token differences:

- Navigation: **-8.18%**
- Bug Fix: **-11.35%**
- Feature: **-17.97%**
- Refactor: **-24.02%**
- Documentation/config: **-58.77%**

**These results are preliminary. There was one run per condition per task. They do not
establish statistical confidence, causality, or universal savings. Results apply to the
tested configuration.**

Unfavorable submetrics remain disclosed: Bug Fix used 35 more output tokens (+3.35%) and two
more commands (3→5, +66.67%); Navigation had a higher dated credit-equivalent (+59.93%)
because cache composition differed. Raw diagnostics, recoveries and previous datasets are
preserved separately.

Product tested: `86043499d5a375cc6a3b295bc7c03b0999eb458c`.
[Full committed evidence](../benchmarks/results/2026-09-30-release-aligned-0.2.0/README.md).

## Verification

114 offline tests, Ruff lint/format, all four Skill validators, Codex/Claude package
validators, evidence checksums, relative links and hygiene pass. No model benchmark was
rerun for release.

[Installation and usage](../README.md) · [Preserved original bootstrap](reference/original-agent-bootstrap.md).
