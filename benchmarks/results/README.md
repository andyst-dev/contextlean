# Public benchmark evidence

- [Release-aligned v0.2.0 validation](2026-09-30-release-aligned-0.2.0/README.md):
  frozen product `86043499`, exactly ten fresh calls, 10/10 independent offline passes.
  ContextLean -29.12% tokens, -29.19% time, 18→16 commands. Bug Fix has more output
  tokens/commands; Navigation's credit-equivalent increases. Current preliminary README
  evidence; no statistical-confidence or universal token-savings claim.

- [Final compact-context 0.2.0 validation](2026-09-30-compact-final-0.2.0/README.md):
  frozen product `90ed9a4`, existing Bug Fix pair plus exactly eight new calls, all
  ten independently offline-regraded. ContextLean uses 16.84% fewer aggregate tokens,
  5.97% less time and 20% more commands. Every unfavorable task result is disclosed.
  Historical preliminary evidence, tested configuration only, no confidence or
  universal token-savings claim.

- [Clean final 0.2.0 validation](2026-09-30-clean-final-0.2.0/README.md): ten fresh
  runs against product commit `52a2c34`, repaired harness, validated preparations and
  offline regrading. 10/10 succeed; ContextLean uses 9.9% more tokens, 17.7% more time,
  and one fewer command call. Previous preliminary evidence, preserved without edits
  and never pooled with the compact-final batch.

- [2026-09-30 validation batch](2026-09-30-validation/README.md): `gpt-5.6-terra`,
  low reasoning, five tasks, one Vanilla and one ContextLean run each. Preliminary;
  all ten pass, including two token regressions. Exact prompts, all raw outcomes,
  frozen source, solutions and offline audit checks are retained.

No statistically robust final benchmark is published. Repetitions need separate
approval; ordinary tests and CI never start model runs. See the [benchmark guide](../README.md).

[2026-09-30 final 0.2.0 candidate diagnostic validation](2026-09-30-final-0.2.0/README.md):
ten runs, all task checks pass; aggregate ContextLean resource regressions and a known
generated-map path error are retained. This does not establish a clean final-bootstrap
validation or statistical confidence. The historical batch above remains unchanged.
