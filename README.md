# ContextLean

Help coding agents find owners, limit exploration, and verify focused changes.

ContextLean produces a reliable project map and a compact coding discipline for
Codex and Claude Code. It helps agents find responsible code, preserve important
constraints, make focused changes, and verify sufficient coverage.

The current **Balanced** contract focuses on ordinary coding work. Audit, Lean Review
and measurement are optional, explicitly requested workflows.

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

## Historical results (before Balanced)

**Release-aligned v0.2.0 preliminary validation — one fresh run per condition per task.**

Five existing tasks in a small Python expense-report fixture, tested on 2026-09-30 using
`gpt-5.6-terra` with low reasoning. Product commit tested:
`86043499d5a375cc6a3b295bc7c03b0999eb458c`. Vanilla contains no ContextLean guidance;
ContextLean starts with equivalent code and fresh validated guidance from that commit.
Exactly ten fresh calls; no historical or isolated Refactor result is reused. All ten
pass acceptance, original regression and submitted tests, including independent offline regrading.

| Task | Vanilla total | ContextLean total | Difference | V time | C time | Commands V/C | Success |
|---|---:|---:|---:|---:|---:|---:|---|
| navigation | 55,054 | 50,553 | -8.18% | 17.88s | 15.29s | 3/3 | Both pass |
| bug-fix | 88,459 | 78,423 | -11.35% | 29.18s | 28.50s | 3/5 | Both pass |
| feature | 94,876 | 77,823 | -17.97% | 60.41s | 39.68s | 3/3 | Both pass |
| refactor | 99,049 | 75,257 | -24.02% | 37.17s | 28.18s | 5/3 | Both pass |
| documentation-config | 144,586 | 59,620 | -58.77% | 45.33s | 22.88s | 4/2 | Both pass |

| Aggregate | Vanilla | ContextLean | Difference |
|---|---:|---:|---:|
| Input tokens | 475,198 | 337,007 | -29.08% |
| Cached input tokens (included in input) | 369,920 | 257,280 | -30.45% |
| Output tokens | 6,826 | 4,669 | -31.60% |
| Total tokens | 482,024 | 341,676 | -29.12% |
| Wall time (s) | 189.97 | 134.52 | -29.19% |
| Command calls | 18 | 16 | -11.11% |
| Acceptance / original regression / submitted-test success | 5/5 each | 5/5 each | Same |

ContextLean measured **29.12% fewer aggregate tokens**, **29.19% less wall time** and
**11.11% fewer commands** in this batch. Unfavorable cases are preserved: Bug Fix uses
35 more output tokens (+3.35%) and two more commands (3→5, +66.67%); Navigation's
dated credit-equivalent is higher (0.76752→1.22746, +59.93%) because cache composition differs.
All diagnostics and recoveries remain visible.

These are **preliminary results for this tested configuration**, with no
statistical-confidence claim and **no universal token-savings claim**. Provider caching,
service load and stochasticity are uncontrolled. File reads and total tool calls are unavailable.
[Release-aligned results and raw evidence](benchmarks/results/2026-09-30-release-aligned-0.2.0/README.md) ·
[methodology](benchmarks/results/2026-09-30-release-aligned-0.2.0/methodology.md) ·
[measurement review](benchmarks/results/2026-09-30-release-aligned-0.2.0/measurement-review.json).

The [compact-final batch at `90ed9a4`](benchmarks/results/2026-09-30-compact-final-0.2.0/README.md),
[previous clean-final batch](benchmarks/results/2026-09-30-clean-final-0.2.0/README.md) and
[historical validation](benchmarks/results/2026-09-30-validation/README.md) remain separate,
unchanged historical evidence. Between-batch differences establish no causal conclusion.
The [diagnostic batch](benchmarks/results/2026-09-30-final-0.2.0/README.md) contains a map-preparation
error and is **invalid for headline performance comparison**.
[Root-cause analysis and harness repair](benchmarks/analysis/2026-09-30-final-0.2.0/README.md).

## Quick start

You need an installed, working Codex or Claude Code. Python 3.11+ is needed only
for optional measurement helpers and development checks. Use a local checkout of this repository; ContextLean is not in a
public marketplace yet.

1. **Install / load ContextLean.** For Codex, run these from the ContextLean checkout:

   ```sh
   codex plugin marketplace add .
   codex plugin add contextlean@contextlean-local
   ```

   Claude Code can load the checkout for one session using `--plugin-dir` in step 2.
   No separate plugin-authoring tool is needed.

2. **Open your project.** Start a fresh agent session in the repository you want to configure:

   ```sh
   cd /path/to/my-project
   codex
   ```

   Or, for Claude Code:

   ```sh
   cd /path/to/my-project
   claude --plugin-dir /path/to/contextlean
   ```

3. **Invoke Bootstrap Repository.** In Codex CLI, open `/skills` or type `$`,
   then select **Bootstrap Repository** from ContextLean (installed name
   `contextlean:bootstrap`). Add “Bootstrap this repository.” In Claude Code, enter
   `/contextlean:bootstrap` followed by the same request. `$bootstrap` alone is
   not the installed plugin's full name.

4. **Inspect the generated guidance.** Review the changes to `AGENTS.md`, any
   `CLAUDE.md` imports, and related configuration. Select **Audit Context Locality**
   in Codex, or enter `/contextlean:audit` in Claude Code, for an evidence-based check.
   Commit useful guidance with your project.

5. **Use the agent normally.** Start a new session so it loads the new guidance.
   Ask for your usual coding tasks. Audit again when structure or commands change.

If the four skills are missing, confirm the plugin is enabled and start a new session.
Codex installs a cached copy: after editing the plugin, reinstall it and restart.
See [installation details and verification status](docs/verification.md).

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
The [release-aligned validation record](benchmarks/results/2026-09-30-release-aligned-0.2.0/README.md)
records the identical prompts, source snapshot, evaluator, ordering and raw outcomes.
Provider caching and service load were uncontrolled; the plugin itself was excluded
from both conditions to isolate the generated guidance. For reproduction and grading,
use the [benchmark guide](benchmarks/README.md).

## Supported agents

| Agent | Integration | Verified scope |
|---|---|---|
| Codex CLI | Plugin + shared skills; project `AGENTS.md` | Fresh local installation and four packaged skills. Live guidance-consumption status is recorded separately. |
| Claude Code | Same skills; project `CLAUDE.md` imports `AGENTS.md` | Manifest validation and session plugin discovery. Full live workflow is unverified. |

The Codex desktop Plugins Directory is an alternative installation surface described
in the [official packaging guide](https://developers.openai.com/plugins/build/plugins).
This change tests the CLI route. Claude session loading follows the
[official plugin guide](https://code.claude.com/docs/en/plugins).
No other agent integration is claimed. [Detailed verification](docs/verification.md)
separates packaging checks from actual model execution.

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
owners. The [verification record](docs/verification.md) lists optional agent validators
and verification limits. Do not add runtime dependencies, hooks or automatic live runs.

## License

[MIT](LICENSE)
