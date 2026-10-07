# ContextLean distribution

Checked **2026-10-07**. Product version remains **0.3.0 Balanced**. This pass prepares
installation and submission materials; it does not publish, register or release
anything. Start with [installation](installation.md) for user commands.

## Ownership and package structure

`skills/{bootstrap,audit,lean-review,benchmark}` are the only canonical Skill
implementations. Their `SKILL.md`, supporting files and Codex `agents/openai.yaml`
are copied unchanged. No platform-specific Skill bodies or generated guidance
copies are maintained.

| Surface | Source and purpose |
|---|---|
| Codex | `.codex-plugin/plugin.json`: supported compatibility manifest, `./skills/`, UI metadata |
| Claude Code | `.claude-plugin/plugin.json`: metadata; root `skills/` discovery |
| Shared repository catalog | `.claude-plugin/marketplace.json`: one `./` source; Codex policy and category |
| Small distribution ZIP | `packaging/build.py`: explicit public inputs, standard library only |
| ZIP README and benchmark link | `packaging/README.md`, `packaging/benchmark-suite.md`: package-specific entry points |
| Listing image | `docs/assets/contextlean.svg`: shared square 128-pixel vector icon |

The catalog name `contextlean-local` stays stable to preserve installed identities;
it also works with the hosted repository. Its Codex `policy` is intentionally
ignored by Claude. A second catalog or a third portable manifest would duplicate
metadata without improving current installation. The source checkout's `AGENTS.md`
and `CLAUDE.md` are contributor guidance, not plugin startup instructions.

The duplicated name/version/license/publisher fields are required platform metadata,
not divergent behavior. `.codex-plugin/plugin.json` is the distribution version
reference; Claude must match it. The catalog deliberately omits a version override.
The existing optional measurement helper's version is also checked. No version
file generator or runtime dependency is introduced.

## Official requirements

The following URLs were read on **2026-10-07**. Requirements below distinguish
local installation from public submission; a successful local validator is not
an approval or endorsement.

### Codex

[Packaging](https://developers.openai.com/plugins/build/plugins) documents portable
root manifests and continued `.codex-plugin/plugin.json` support. It also accepts
Claude-format repository catalogs. Relative component paths resolve inside the
plugin; repository marketplace paths resolve from the repository root. Native
marketplace registration, refresh and removal are supported. Cached installations
live under the configured Codex home.

[Submission field requirements](https://developers.openai.com/plugins/deploy/submission)
require the compatibility manifest's identifier, version, description, publisher,
Skill path and interface. Required listing fields include display name, subtitle,
long description, developer, category, capabilities, icon and logo. The subtitle
limit is 30 characters; the full tagline therefore stays in the README. Optional
metadata includes repository/homepage, license, keywords, starter prompts, dark
assets and screenshots. The shared SVG satisfies the documented size/format rules.

[Skills-only submission](https://developers.openai.com/plugins/guides/submit-claude-plugin)
is available through the OpenAI portal. It requires publisher verification and
appropriate organization access. Review and publication remain separate actions.
No MCP, authentication integration or lifecycle hooks are needed here.

### Claude Code

[Manifest reference](https://code.claude.com/docs/en/plugins-reference) requires
`name` when a manifest exists. Version, description and publisher are recommended;
root `skills/` is discovered automatically. Relative paths must stay inside the
plugin. Optional directory fields include icon, documentation and support URLs;
these are recognized by validators starting at 2.1.281.

[Marketplace instructions](https://code.claude.com/docs/en/plugin-marketplaces)
establish a catalog with name, owner and plugin entries with name/source. Local
paths and hosted Git repositories are supported. The default user install scope
uses platform config/cache, not project-generated guidance.

[Publishing](https://code.claude.com/docs/en/plugins/publish) distinguishes an owned
repository catalog from Anthropic's public directory. The latter has a paid-plan
portal submission route. The separately curated `claude-plugins-official` catalog
does not use that portal; listing there requires an Anthropic partner contact.

[Directory checklist](https://claude.com/docs/plugins/pre-submission-checklist)
requires README/license and portable regular files. Repository limits include
50 MiB archived, 256 MiB unpacked, fewer than 10,000 entries and files below 5 MiB.
More than 512 plugin files, large text files and ZIP evidence can trigger review
holds. These are not reasons to delete immutable evidence.

[Submission procedure](https://claude.com/docs/plugins/submit) uses a GitHub
repository, plugin path and branch/tag; the publisher needs a connected account
with push access. Portal validation, contact information, data-handling answers
and policy acknowledgments remain publisher actions.

### Unknown or deliberately unclaimed

- Publisher account eligibility, identity approval, name availability and review
  outcome are **UNKNOWN**; no portal operation was performed.
- Compatibility beyond the tested CLI versions and other operating systems is
  **UNKNOWN**. Neither manifest invents an unsupported compatibility field.
- No public install counts, endorsements, broad model-equivalence claim or v0.3.0
  performance-saving claim is made. The 30-run performance study belongs to v0.2.1.
- Native GitHub transport and interactive desktop selectors were not exercised by
  the offline test suite. Official hosted installation commands are documented;
  native local installation and non-model discovery were exercised.

## Build a small package

From the checkout, choose a new output path outside it:

```sh
python3 packaging/build.py /tmp/contextlean-0.3.0.zip
```

The exporter refuses to overwrite an existing output. It produces a deterministic
ZIP with both manifests, the shared catalog, license, package README, listing icon
and unchanged canonical Skill files. A small `benchmarks/README.md` points back to
the optional development suite so the existing Skill link resolves. It does not
bundle benchmark datasets, historical records, contributor startup guidance,
`.git`, ignored local reports or caches. There is no install/uninstall script.

Native installation directly from GitHub fetches the repository and therefore
includes tracked evidence; the small ZIP is a separate submission/offline artifact.
It is not a new hosted download service. Do not upload the entire working folder:
it can contain ignored private material.

## Install, update and uninstall semantics

The [user guide](installation.md) gives the copy-pasteable native commands. Codex
installs cached copies and `plugin add` refreshes from a registered source. Claude
Git installs use versioned caches. Its [loading rules](https://code.claude.com/docs/en/plugins/loading)
distinguish local source loading from cached installations and explain why an
unchanged manifest version prevents a normal versioned update.

In the tested CLIs, re-adding a same-version Codex package refreshed the cache;
Claude's update retained the old same-version cache. Local Claude discovery can
read the source directory instead. Keep that directory for local development;
use Git installation for an independent installed copy. Do not infer that cache
metadata proves which files a local Claude session loaded.

This pass changes no release version. A future published content update must get
its own version decision. An intentional same-version reinstall is documented,
but normal updates must not be advertised as delivering these edits automatically.

Both platforms' update/removal commands were tested against customized project
`AGENTS.md`, `CLAUDE.md`, nested maps, and user-created Skills. All project bytes
survived. Generated guidance needs neither this plugin nor its installation path.
Removing that guidance remains an explicit manual project change.

## Offline validation

```sh
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s tests -p test_distribution.py -v
ruff check .
ruff format --check .
git diff --check
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
```

The three portable package tests use actual exported files, relocate them, verify
all Skill bytes and references, check metadata/version consistency, reject missing
Skills and symlinks, and verify deterministic output and package hygiene.
Native lifecycle tests use **Codex 0.147.0** and **Claude Code 2.1.288**. They
install the relocated ZIP through each real CLI, inspect four-Skill discovery,
apply a synthetic `0.3.1-test` update inside the temporary directory, uninstall,
and check customized project files byte-for-byte. That synthetic version is not
a product version declaration or release.

Native commands run with fresh HOME, agent config/cache roots, Git config isolation,
no inherited credentials, denied networking and filesystem writes limited to the
test root. Codex uses only app-server `initialize` and `skills/list`, never a turn.
Claude uses component inventory and validators, never a prompt. macOS
`sandbox-exec` and the respective CLI are required for these tests; they report a
skip on other hosts instead of running unconfined. Portable tests still run in CI.
Bootstrap generation is the existing deterministic representative fixture, not a
claim that a live model bootstrapped a project during this pass.

Use the available Codex Plugin Creator validator and Skill Creator validator from
their installed locations. They are development tools, not ContextLean dependencies;
there is no invented `codex plugin validate` command. The exported Claude
manifest passes strict validation. Source-checkout validation also reports its
contributor `CLAUDE.md`, even when targeting the manifest file; the shared catalog
has the expected Codex-policy warning. These known warnings prevent strict validation
of the source root/catalog and do not occur as Skill/runtime failures.
The completed run passed **139 tests with no skips** on the tested macOS host.
Ruff 0.15.7 lint/format, whitespace checks, Codex package and all four Skill validators
passed. Recursive links/anchors, 14 evidence ledgers (3,363 entries), eight historical
fingerprints and Balanced contracts passed. All 2,256 published result files and all
15 canonical Skill files remain byte-for-byte identical to the Deep Clean baseline.

## Security and privacy

The artifact has no credentials, telemetry client, hooks, server, authentication
changes, hidden network job or install-time executable. Native installation writes
platform-owned config/cache; ContextLean adds no separate global configuration.
The workflows inspect the requested project and Bootstrap may update its guidance
and safe configuration only when invoked. Audit and Lean Review remain read-only
unless a fix is explicitly requested.

The optional Benchmark helper can inspect existing Codex authentication status and
run a provider session only for an explicitly requested live measurement. Static
measurement remains local. Installing/updating from GitHub requires a repository
download; invoking the host coding agent has that platform's normal network/data
handling. No claim is made that the host applications themselves have no telemetry.
Local measurement reports can contain project information and are never included
by the package exporter. No privacy policy, publisher email or legal attestation
is fabricated on the user's behalf.

## Publication readiness

| Destination | Repository status | Remaining external actions or limitations |
|---|---|---|
| Codex repository catalog and skills-only public-directory package | **READY** for maintainer review and submission after approval | Publish the reviewed repository changes separately; build ZIP; verify publisher identity/access; run portal scans and submit for review. No result guaranteed. |
| Claude Code repository catalog and directory submission | **READY** for maintainer review and submission after approval | Publish reviewed changes; connect an eligible GitHub/Claude account; run portal validation and complete data-handling/contact/policy steps. The evidence-heavy root can incur documented policy holds. |

No repository file exceeds 5 MiB and the tracked source is about 35 MB before ZIP
compression. The repository has over 512 files and contains immutable ZIPs and
large reports: a Claude directory reviewer may hold this root package for inspection.
A later, explicitly authorized packaging-only publication branch/repository could
host the small export if that becomes necessary. This pass creates neither, and
never moves or modifies evidence to satisfy directory preferences.

The ZIP is ready for offline/native testing and the OpenAI upload route. Anthropic's
verified portal route requires GitHub source, so do not describe a local ZIP as an
already submitted Claude directory listing. The own-repository catalog is usable
without public-directory approval. Public listing and approval remain unverified.
