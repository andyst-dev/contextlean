# Clean final validation methodology

Follow the [graded benchmark guide](../../README.md) and final product Bootstrap
procedure at the pinned commit. [Preparation evidence](preparation-evidence.json)
records five separate reviewed preparations before the first model call.

1. Fresh disposable checkout at product commit `52a2c34c091f9720076cc9685fb858347d9f6dcf`.
2. Overlay only the repaired runner and preparation validator from the harness commit.
3. Create five fresh Vanilla and five fresh ContextLean copies from the pristine fixture,
   with no previous generated instructions; capture a new bootstrap baseline per copy.
4. Author guidance from the final specification and actual source. Verify eight paths
   and owner responsibilities, wrapper imports, all 71 facets, commands, safe removal,
   idempotence and equivalent non-instruction hashes. Freeze only after validation.
5. Prove all five frozen contexts identical; stage one validated source for the unchanged
   fixture runner. Run `--model gpt-5.6-terra --reasoning low --repeat 1` with its receipt.
6. The runner starts independent ephemeral calls, alternating Vanilla-first and
   ContextLean-first by task, using a common temporary workspace path and fresh copies.
   Navigation is read-only; edits are workspace-write. Both conditions ignore user
   configuration/rules, disable web search and have identical task prompts and evaluators.
7. Retain all outcomes, exact turn usage, unique command IDs and monotonic wall times.
   Regrade saved solutions offline using original regression tests and the same
   independent acceptance grader; verify submitted tests, data and guidance integrity.
8. Review raw measurements and all regressions; publish a separate new result directory.
   Redact private path prefixes and a tool-cache pathname, never numeric measurements.

Same prompts, task suite digest, evaluator digest, measurement core, model, reasoning,
configuration and recorded platform/Python/CLI as earlier batches. The product code
and all Skills are exactly the release candidate. Preparations/static reports and
acceptance graders are not loaded into the measured repositories. Plugin discovery
is excluded from both conditions; this tests generated guidance only.

Provider caching, output randomness, service load and non-Git fixture behavior remain
limitations. One run per condition per task is preliminary validation without a
statistical-confidence claim, and applies only to this tested configuration. It does
not establish universal savings or causal effects of changes between batches.

The [diagnostic batch](../2026-09-30-final-0.2.0/README.md) is invalid for headline
comparison. No runs are pooled or substituted between batches.
