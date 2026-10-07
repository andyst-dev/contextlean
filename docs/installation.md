# Install and use ContextLean v0.3.0

Install once, then use the same four Skills in your projects. ContextLean is
available from its repository catalog; it has not been submitted to either
platform's public directory.

## Requirements

Use a working Codex CLI with `codex plugin`, or Claude Code with `claude plugin`.
The offline native checks used Codex **0.147.0** and Claude Code **2.1.288** on
macOS. Compatibility with other versions is not established by those checks.
Git and network access are needed for repository installation and updates.
Python 3.11+ is needed only for optional measurement helpers and development.

## Install for Codex

Run in your terminal:

```sh
codex plugin marketplace add andyst-dev/contextlean
codex plugin add contextlean@contextlean-local
```

The catalog's stable name is `contextlean-local`, including when fetched from
GitHub. Start a fresh Codex session in your project. Open `/skills` or the `$`
selector to find ContextLean. Installation uses Codex's own config and cache;
there is no ContextLean installer or additional account to configure.

## Install for Claude Code

Run in your terminal:

```sh
claude plugin marketplace add andyst-dev/contextlean
claude plugin install contextlean@contextlean-local --scope user
```

Start a fresh Claude Code session in your project. User scope makes the plugin
available across projects on this machine. It does not install project guidance.

## Bootstrap a project

Open your project's directory and start your agent. In Codex, select
`contextlean:bootstrap` and ask “Bootstrap this repository.” In Claude Code:

```text
/contextlean:bootstrap Bootstrap this repository.
```

Review generated `AGENTS.md`, Claude imports and any related configuration.
Commit useful guidance with your project, then start a fresh session.
`AGENTS.md` holds the shared guidance; `CLAUDE.md` normally imports it using
`@AGENTS.md`. Existing useful project-specific content is preserved.

| Skill | Codex installed name | Claude invocation |
|---|---|---|
| Bootstrap Repository | `contextlean:bootstrap` | `/contextlean:bootstrap` |
| Audit Context Locality | `contextlean:audit` | `/contextlean:audit` |
| Lean Change Review | `contextlean:lean-review` | `/contextlean:lean-review` |
| Benchmark Context Usage | `contextlean:benchmark` | `/contextlean:benchmark` |

Workflows require explicit requests. Audit and Lean Review default to read-only.
Measurement is optional; live measurement needs separate authorization.
The Benchmark helper's example paths are relative to the installed plugin root,
not the target project. Use that root for its script path and `--repo` for the
project. The graded development suite requires a separate source checkout.

## Verify installation

```sh
codex plugin list --json
claude plugin list --json
claude plugin details contextlean@contextlean-local
```

Use the commands for your platform. Confirm the plugin is enabled and all four
Skills appear in the agent's selector. `plugin details` lists Claude components
without a model call. Discovery checks packaging, not model compliance.

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

Restart your agent afterward. Claude's versioned repository installs keep their
cached copy until the publisher changes the manifest version. This packaging pass
keeps **0.3.0**; it does not promise an automatic upgrade of existing 0.3.0 installs.
For an intentional same-version Claude refresh:

```sh
claude plugin marketplace update contextlean-local
claude plugin uninstall contextlean@contextlean-local --scope user
claude plugin install contextlean@contextlean-local --scope user
```

This leaves project guidance in place. Local-directory loading has different
behavior; see below.

Updates change the tool, not generated project files. They do not rerun Bootstrap,
rewrite `AGENTS.md` or `CLAUDE.md`, or migrate custom project Skills. Review any
future guidance refresh explicitly, just as you would another project change.

## Uninstall ContextLean

Codex:

```sh
codex plugin remove contextlean@contextlean-local
codex plugin marketplace remove contextlean-local
```

Claude Code:

```sh
claude plugin uninstall contextlean@contextlean-local --scope user
claude plugin marketplace remove contextlean-local
```

Restart the agent. Removing this catalog is optional. Native commands remove
platform installation metadata and installed copies; they leave project
`AGENTS.md`, `CLAUDE.md`, maps, user Skills and customizations intact.

**Removing generated guidance is a separate, manual project edit.** Review the
files and preserve your own content and imports. Uninstalling the plugin does
not disable the guidance that your project already contains.

## Local development and offline packages

For a source checkout or extracted distribution ZIP, replace
`andyst-dev/contextlean` in the marketplace-add command with its absolute directory
path. Codex copies it into its cache; rerun `plugin add` after editing that source.
Claude can load a local marketplace's source in place: keep that directory available
and restart to see edits. A local install must not be confused with a Git-fetched
install. For a single Claude session, no persistent installation is needed:

```sh
claude --plugin-dir /absolute/path/to/contextlean
```

The [maintainer guide](distribution.md) explains how to build the small ZIP.
No manual Skill copying or editing of global config files is required.

## Troubleshooting

- **Unknown `plugin` command:** update the platform CLI through its official
  installation instructions. The documented command spelling for tested Codex is
  `plugin add`, not `plugin install`.
- **Plugin not found:** add the repository catalog first and use the full
  `contextlean@contextlean-local` identifier. Check `plugin marketplace list`.
- **Missing Skills:** check that the plugin is enabled, restart, and select the
  qualified `contextlean:…` names. Check Claude's `/plugin` Errors tab.
- **Changed files but old behavior:** distinguish local source loading from a
  cached Git installation; review the version/update rule above. Do not edit caches.
- **Missing local checkout:** restore it or reinstall from GitHub. A Claude local
  marketplace can depend on its original directory.
- **Validator warnings:** Claude ignores the shared catalog's Codex-only `policy`.
  Validating the source checkout also warns that its contributor `CLAUDE.md` is not
  plugin context. Neither file is intended to inject runtime guidance.

The native tests block network access and exercise real installers against local
artifacts. GitHub download transport, interactive UI, account entitlements and
public-directory approval were not tested. See [distribution requirements and
validation](distribution.md) for official sources and remaining unknowns, and
[evidence](evidence.md) for the separate v0.3.0 behavioral validation.
