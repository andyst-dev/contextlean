# ContextLean

**Bootstrap once. Read less. Change locally.**

ContextLean creates compact maintained project guidance for coding agents so they
can locate responsible code, avoid unnecessary exploration, make focused changes,
and verify them proportionally. It includes Bootstrap, Audit, Lean Review and
Benchmark, with one shared implementation for Codex and Claude Code.

Follow the [installation guide](https://github.com/andyst-dev/contextlean/blob/main/docs/installation.md)
to install, discover the four Skills, bootstrap a project, update and uninstall.
Generated project guidance belongs to the project and survives plugin removal.
Workflows require explicit invocation; live measurement needs separate authorization.

This package includes only the canonical Skills, platform metadata, privacy notice, icon and MIT
license. The optional graded benchmark development suite and immutable evidence
remain in the [source repository](https://github.com/andyst-dev/contextlean).
Python 3.11+ is needed only for the optional measurement helper, not Bootstrap.
Helper examples use paths relative to this package's installation root; the target
project is selected separately with `--repo`.

ContextLean has no telemetry, installer hooks, credentials or background services.
Native platform installation may download the repository. Explicit live measurement
uses the user's existing Codex authentication and provider; it is never automatic.

[Documentation](https://github.com/andyst-dev/contextlean/tree/main/docs) ·
[Issues](https://github.com/andyst-dev/contextlean/issues) ·
[Privacy](https://github.com/andyst-dev/contextlean/blob/v0.3.2/docs/privacy.md) ·
[License](https://github.com/andyst-dev/contextlean/blob/main/LICENSE)
