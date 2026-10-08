# ContextLean v0.3.2 — Privacy disclosure

This patch adds the [privacy notice](privacy.md) and its public URL to the Codex and
Claude plugin manifests for directory submission. The deterministic distribution
package includes the notice, and the repository and package READMEs link to it.

The notice documents local project access and output, the absence of a hosted
ContextLean collection service, and the provider data flow of explicitly requested
live benchmarks. Contact: andyst-dev@proton.me.

All four Skill behaviors and v0.3.0 Balanced guidance remain unchanged. The optional
measurement helper changes only its reported version. No model benchmark was run,
and no historical evidence was changed. Published v0.3.1 remains untouched.

Directory review and publication are separate from this GitHub release. This
release does not claim Anthropic or OpenAI approval or new performance results.

## Validation and artifact

- 139 offline tests passed with no skips, including native Codex/Claude lifecycle
  checks. No model session or live benchmark was run.
- Ruff 0.15.7 lint and format checks, four Skill validators, Claude manifest/catalog
  validation and whitespace checks passed. Source-root CLAUDE.md and shared catalog
  policy warnings remain expected.
- The four Skill bodies, references and UI metadata are byte-identical to v0.3.1.
  Published historical evidence and the original Bootstrap specification are unchanged.

Release asset: `contextlean-0.3.2.zip` — **23 files, 34,882 bytes**.
SHA-256 (also recorded in `contextlean-0.3.2.sha256`):

```text
41a23e53dfa06b7d4576f87f874368c4d0faf0d0739c2ab81adb242b60374772
```
