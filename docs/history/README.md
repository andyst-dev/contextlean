# Historical and design records

These records describe their original revisions and verification stages. Statements
about pending work, untracked archives, test counts or installed tools retain that
dated scope. They are not current setup instructions.

Current readers should start with [installation](../installation.md), the
[Balanced contract](../balanced-contract.md) and [evidence provenance](../evidence.md).

- [Original bootstrap specification](../reference/original-agent-bootstrap.md):
  preserved at its protected path, unchanged.
- [v0.2.0 semantic coverage](bootstrap-coverage.md),
  [compact-context work](compact-context.md), [release notes](release-notes.md) and
  [verification chronology](verification.md).
- [Balanced migration review, 2026-10-05](2026-10-05-balanced-migration.md) and
  [implementation-stage verification](balanced-verification.md).
- [Completed Old-versus-Balanced adapter](product-comparison-adapter.md).
- [Harness v3 sandbox diagnosis](sandbox-composition.md). Its exact macOS exit-71
  reproduction is historical. Current tests enforce native execution, permission
  parity and rejection of nested strategies without requiring an old OS error code.
- [Earlier preparation investigation](../../benchmarks/analysis/2026-09-30-final-0.2.0/README.md):
  retained at its evidence-linked path.

Code paths and commands in dated records refer to the matching source revisions.
The completed comparison is reproducible from adapter commit
`43972cb610755dde7a2866595a8e1f34f2b2d907`; its published source and outcomes are in
[Balanced validation](../../benchmarks/results/2026-10-06-balanced-product-change/README.md).
The active runner no longer maintains that experiment's adapter API.

Legacy transfer inspection lives in `tests/legacy_bootstrap.py`, with its inventory
and frozen fixture in `tests/fixtures/bootstrap-transfer/`. It is historical test
support, not a current Bootstrap prerequisite. Use matching frozen source when
reproducing old experiments; do not regenerate receipts against current guidance.
