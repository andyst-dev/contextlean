---
name: audit
description: Audit a repository's agent instructions, project maps, Skills, exclusions, documentation freshness, and architectural locality. Use when asked to audit, check, validate, or repair ContextLean configuration; default to read-only, and modify only safe documentation or configuration when the user explicitly requests "audit fix".
---

# Audit repository context

Run only when the user requests an audit. Default to read-only. Treat `audit fix` as explicit permission only for safe documentation and configuration repairs; never refactor product code silently.

## Inspect

Start from the applicable `AGENTS.md` hierarchy and repository state. Use targeted searches to compare documented claims with the files and configuration that actually exist. Check:

- maps, ownership, paths, dependency flow, and verified commands;
- duplication between parent and nested instructions;
- oversized always-loaded instructions or large documentation made mandatory at startup;
- Claude wrappers and imports;
- Skill structure, frontmatter, references, scripts, and symlinks;
- exclusions that hide source, tests, fixtures, migrations, documentation, assets, or useful archives;
- stale documentation and responsibilities that no longer match the implementation;
- the selected product contract: new Balanced guidance must retain the coding
  kernel and work without setup documents or installed ContextLean Skills; do not
  silently migrate a project that selected a historical contract;
- unintended automatic Skill invocation, after-every-task map-check rituals, or
  required historical receipts/measurement reports in new Balanced guidance;
- known stale map information and whether corrections stay within affected entries;
- legacy transfer records only when historical investigation is explicitly requested:
  an absent receipt is not a Balanced defect; use the matching historical revision
  and do not regenerate old evidence or demand compatibility with every old facet;
- potential god objects, catch-all modules, circular or non-local dependencies, and simple features spread across unrelated files.

File length alone is never a defect. Report a large file only when evidence shows mixed responsibilities or degraded locality. Do not recommend fragmenting cohesive code into wrappers or micro-files.

## Classify

For each check, emit exactly one status with a concise evidence-based justification:

- `PASS` — verified and no action is needed.
- `WARNING` — a plausible issue or drift signal needs judgment.
- `ACTION NEEDED` — a concrete mismatch, broken path, invalid command, unsafe exclusion, or failed configuration needs correction.

Include the relevant path and the smallest sensible next action. Distinguish observed facts from inferences.

## Fix mode

When the user explicitly requests `audit fix`, repair only issues that are safe and unambiguous, such as stale paths, broken lightweight wrappers, clear parent/child duplication, invalid safe exclusions, or obsolete command documentation. Preserve useful knowledge by moving it to an optional reference when necessary.

Do not change product behavior, redesign architecture, split modules, install dependencies, or perform speculative cleanup. Report anything requiring such work as `ACTION NEEDED` for separate approval. Re-run the affected checks after every repair.
