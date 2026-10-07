# ContextLean contributor guidance

ContextLean v0.3.0 Balanced is a dependency-free, skills-only Codex/Claude Code
plugin. Bootstrap writes reliable maps and compact coding guidance. Audit, Lean
Review and measurement run only on explicit request.

## Map and ownership

- `skills/`: four canonical shared workflows. Each `SKILL.md` owns behavior;
  adjacent `agents/openai.yaml` owns Codex UI metadata. Bootstrap's targeted
  references own setup and ordinary coding guidance respectively.
- `.codex-plugin/`, `.claude-plugin/`: platform manifests and the shared
  installation catalog. Both platforms discover the same plugin-root Skills.
- `docs/`: current installation, Balanced contract, authoring and evidence guides;
  `docs/history/` holds dated records. Start with `README.md` for public usage.
- `benchmarks/`: optional graded runner, fixture preparation, evaluator and harness
  controls. `benchmarks/README.md` routes to the current methodology.
- `benchmarks/results/`: immutable published evidence. `benchmarks/analysis/`
  retains linked historical investigations.
- `packaging/`: deterministic ZIP export from canonical Skills; no installer runtime.
- `tests/`: offline product, installation, harness and historical preservation tests.
  Historical support is test-only; it is not part of Bootstrap's current contract.
- `.github/workflows/quality.yml`, `pyproject.toml`: offline CI and development Ruff
  configuration. `LICENSE` contains the MIT terms.

## Invariants

Keep shared behavior in one Skill; platform differences need a concrete compatibility
reason. No runtime package, MCP server, hooks, telemetry, automatic benchmark or
startup workflow without an explicit versioned product decision. Keep Benchmark as
the fourth Skill. Default Bootstrap needs no transfer receipt or measurement report.
Audit and Lean Review are read-only unless narrow fixes are separately requested.

Never modify published result bytes or their frozen source, solutions and ledgers.
Preserve the original specification at `docs/reference/original-agent-bootstrap.md`
and paths used by immutable evidence links. Historical reproduction uses matching
frozen inputs, not rewritten current implementations. Never run live models in tests.

## Development

Use the nearest map and search before broad reading. Read the Bootstrap specification
only when applying, changing or validating it. Prefer the standard library and
existing tooling; keep changes with their responsible owner.

After changes to manifests, Skills, wrappers or layout, run:

```sh
python3 -m unittest discover -s tests -v
ruff check .
ruff format --check .
git diff --check
```

Use Ruff 0.15.7, pinned in CI. Frozen evidence is excluded from formatting and checked
by integrity tests. Native sandbox tests require a host that supports their probes;
report skips or environmental failures rather than weakening the gates.

Run available Codex plugin/Skill validators. With Claude installed, also run:

```sh
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
```

The root `CLAUDE.md` warning means it is not injected as plugin context. Do not invent
validator commands. Correct only map entries invalidated by a change or encountered
stale, in the smallest applicable map; otherwise leave maps alone.
