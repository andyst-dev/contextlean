# ContextLean

**Bootstrap once. Read less. Change locally.**

ContextLean is a dependency-free, skills-only plugin for Codex and Claude Code.
Coding agents lose useful context when they repeatedly rediscover repository
architecture, read large documentation wholesale, or navigate code whose
responsibilities are spread across unrelated modules. ContextLean configures a
repository once so later work can begin from a small, maintained project map.

It favors:

- lightweight project maps;
- targeted reads;
- local architectural ownership;
- automatic maintenance rules for those maps;
- reusable workflows;
- measurable benchmarks.

ContextLean 0.1.0 has no MCP server, hooks, background process, runtime package,
telemetry, or automatic live benchmark. Nothing runs until a Skill is invoked.

## Capabilities

### `bootstrap`

An explicit, one-time setup. It preserves existing repository knowledge, creates or
improves the smallest useful `AGENTS.md` hierarchy, adds lightweight Claude wrappers,
and records a local static before/after report. It does not change product behavior.

- Codex: `$bootstrap`
- Claude Code: `/contextlean:bootstrap`

### `audit`

Checks maps, paths, commands, wrappers, Skills, exclusions, documentation drift, and
architectural locality. It is read-only by default. The explicit `audit fix` mode is
limited to safe documentation and configuration repairs.

### `lean-review`

Reviews a change for duplicated behavior, unnecessary abstraction or dependencies,
misplaced ownership, dead code, speculative flexibility, and poor locality. It is
read-only unless a separate fix is requested.

### `benchmark`

Provides an offline static estimate and an opt-in controlled Codex A/B experiment.
Every output distinguishes exact measurements, estimates, and heuristics.

## Installation

This repository is not published to a public marketplace yet. Use the official local
development mechanisms for 0.1.0.

### Codex

Codex installs plugins from marketplaces. Use the built-in `$plugin-creator` to add
this checkout to a local marketplace, then install ContextLean from that source in
the Plugins Directory or with `codex plugin add contextlean@<marketplace-name>`.
Start a new task after installation so the four Skills are discovered.

After `$plugin-creator` creates the local marketplace outside the plugin checkout,
register that marketplace root and install its entry:

```bash
codex plugin marketplace add /absolute/path/to/local-marketplace
codex plugin add contextlean@personal
```

See the official [Codex plugin packaging and local marketplace guide](https://developers.openai.com/plugins/build/plugins).

### Claude Code

Load the checkout directly during development:

```bash
claude --plugin-dir /absolute/path/to/contextlean
```

Then invoke `/contextlean:bootstrap`, `/contextlean:audit`,
`/contextlean:lean-review`, or `/contextlean:benchmark`. Claude Code namespaces
plugin Skills automatically. See the official [Claude Code plugin guide](https://code.claude.com/docs/en/plugins).

ContextLean keeps one canonical `skills/` implementation for both platforms. The two
manifests contain only platform packaging metadata. Codex-specific invocation policy
lives in `agents/openai.yaml`; workflow behavior remains in each shared `SKILL.md`.

## How it works

```text
install
→ bootstrap once
→ project maintains AGENTS.md
→ future sessions read less unrelated context
```

`AGENTS.md` is the shared source of repository guidance. Lightweight `CLAUDE.md`
files import the corresponding map instead of copying it. Detailed procedures and
large documentation stay behind targeted references and are loaded only when needed.

## Benchmark

`benchmark estimate` is structural and static. It compares the instruction footprint
captured before and after bootstrap, uses an explicitly labelled byte-to-token
approximation, and never runs Codex. Static metrics are not measured token savings.

`benchmark ab` performs real Codex runs against isolated baseline and optimized
copies. It uses identical read-only tasks and options, balanced ordering, fresh
ephemeral conversations, JSONL usage events, and local JSON and Markdown reports.
Tasks, model, reasoning effort, repetitions, and runner options are retained so the
experiment can be reproduced.

Live A/B runs consume model usage and are never part of the default test suite. No
gain is claimed from a failed or incomplete comparison, and no percentage is shown
here before a real benchmark has been executed.

Measured results can be added here after a reproducible run:

> No published results yet.

See [the benchmark methodology](skills/benchmark/references/methodology.md) for the
measurement model and limitations.

## Privacy

ContextLean operates locally and sends no telemetry. Bootstrap reports and benchmark
reports remain in `.contextlean/`, which is ignored by Git. A live A/B benchmark uses
the provider configured in the local Codex installation; that ordinary model traffic
is the only external interaction initiated by the benchmark workflow.

## Philosophy

- Give each important responsibility one clear owner.
- Navigate from a concise map into the smallest relevant subsystem.
- Keep large or specialized context optional.
- Prefer existing code and standard tooling before adding abstractions or dependencies.
- Split by cohesive responsibility, never arbitrary file size.
- Verify proportionally and report uncertainty honestly.

## Codex support

The required manifest is `.codex-plugin/plugin.json`. Each Skill also contains
`agents/openai.yaml` for Codex UI metadata. `bootstrap` disables implicit invocation
because it modifies repository guidance; the other Skills remain read-only by
default. The package is validated with the current `plugin-creator` validator.

## Claude Code support

The Claude manifest is `.claude-plugin/plugin.json`. Claude Code discovers the same
`skills/<name>/SKILL.md` directories without a fork. Local development uses
`--plugin-dir`; release validation uses `claude plugin validate .` when the CLI is
installed. The repository-level `CLAUDE.md` is contributor guidance and is not
injected as plugin context.

## Development and testing

The default suite is offline, fast, and dependency-free:

```bash
python3 -m unittest discover -s tests -v
```

It checks packaging, versions, paths, Skill boundaries, fixture contracts, static
bootstrap reporting, JSONL parsing, calculations, and report rendering. It never runs
`codex exec` or performs network calls.

Optional local validators:

```bash
claude plugin validate .
python3 /path/to/plugin-creator/scripts/validate_plugin.py .
```

## Contributing

Keep changes focused on the four existing responsibilities. Add no MCP server, hooks,
telemetry, runtime package, or always-loaded context without an explicit versioned
product decision. Run the offline suite and both available platform validators before
submitting a change. Live benchmarks require an explicit model, reasoning effort, and
usage approval.

## License

[MIT](LICENSE)
