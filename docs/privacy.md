# ContextLean privacy notice

Effective 8 October 2026.

## Scope

This notice describes ContextLean, maintained by andyst-dev. ContextLean is a
skills-only developer tool. It does not operate a hosted backend, MCP server,
telemetry collector, background service, or advertising service.

## Project files and local output

When explicitly invoked, ContextLean guides your coding agent to inspect the
project you select. Project files may contain personal or confidential information.
Bootstrap can write project guidance and safe configuration. Audit and Lean Review
are read-only unless you separately request fixes. Optional measurements create
local reports, logs, and temporary project copies. Such output can contain project
information. Review it before sharing it.

ContextLean does not automatically upload these reports or send them to its
maintainer. Local output remains under your control; you can remove reports and
logs from your machine when no longer needed. Uninstalling the plugin does not
necessarily remove guidance or reports previously created in your projects.

## Coding agents and optional live benchmarks

The coding agent that runs a Skill processes its conversation and any project
content it reads according to that agent's own settings and privacy terms.
ContextLean's absence of telemetry does not mean that the host application has no
network activity or telemetry.

Static measurement runs locally without a model request. Only an explicitly
requested live benchmark invokes Codex and its configured model provider. The
provider may receive task prompts and project content read during that run, and
live requests may consume your model usage. Authentication uses the configured
coding tools; ContextLean has no separate account or credential-collection service.
The benchmark helper may inspect Codex's existing authentication status. Historical
benchmark reproduction tools in the source repository may use existing provider
authentication to run isolated provider sessions; they do not run on installation.

Provider-side processing, retention, and deletion are governed by that provider's
terms and your account settings. ContextLean does not control those retention
periods. Installing or updating from GitHub also contacts GitHub through the normal
plugin installation tools.

## No maintainer-side collection service

ContextLean itself does not send project content, credentials, usage analytics, or
measurement reports to a service operated by its maintainer. Files you voluntarily
publish or send to someone are outside this local-only storage description.

## Contact

Questions about this notice: andyst-dev@proton.me.
