# Benchmark evidence

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
