# Install and use ContextLean v0.3.0

Use a local checkout with an installed, working Codex or Claude Code. These are the
repository's existing installation paths; public marketplace distribution is not
introduced here. Python 3.11+ is needed for optional measurement and development,
not ordinary Bootstrap.

## Load the plugin

For Codex, run from the ContextLean checkout:

```sh
codex plugin marketplace add .
codex plugin add contextlean@contextlean-local
```

Start a fresh Codex session in the project you want to configure. Use `/skills` or
the `$` selector to find ContextLean's installed Skills.

For Claude Code, start a session in your target project using the checkout:

```sh
claude --plugin-dir /path/to/contextlean
```

## Bootstrap a project

Select **Bootstrap Repository** (`contextlean:bootstrap`) in Codex, or invoke
`/contextlean:bootstrap` in Claude, and ask it to bootstrap the repository.
Review the generated `AGENTS.md`, Claude imports and any related configuration.
Commit useful guidance in your own project and start a fresh agent session.

| Skill | Installed name | Purpose |
|---|---|---|
| Bootstrap Repository | `contextlean:bootstrap` | Explicit setup of maps and coding guidance |
| Audit Context Locality | `contextlean:audit` | Read-only guidance and locality audit |
| Lean Change Review | `contextlean:lean-review` | Read-only review of a change |
| Benchmark Context Usage | `contextlean:benchmark` | Requested static measurement or separately authorized live measurement |

Claude commands use `/` before these names. None runs automatically. Request
`audit fix` explicitly for narrow guidance/configuration repairs.

## Verify and update

Confirm that all four Skills appear and that the plugin is enabled. If they are
missing, check the selected checkout and start a fresh session. Discovery verifies
installation; it does not prove model compliance with a workflow.

Codex uses a cached plugin copy: after updating your local checkout, reinstall from
that checkout using the existing plugin installation flow and restart the session.
Claude's `--plugin-dir` loads the selected checkout for that session; restart against
the updated checkout. Existing project guidance is not automatically migrated.

For development, run the offline commands in [contributor guidance](../AGENTS.md).
The [v0.3.0 verification record](release-v0.3.0-verification.md) gives the checked
scope and limitations; [evidence provenance](evidence.md) separates Balanced
validation from previous performance studies. Historical installation observations
remain in the [dated verification record](history/verification.md).
