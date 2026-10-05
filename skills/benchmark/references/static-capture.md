# Explicit static before/after capture

Use only when the user requests measurement; this is not a bootstrap prerequisite.
These standard-library commands do not start a model. Resolve the helper from the
installed ContextLean plugin root, not from an assumed target-project installation.

Before any measured change:

```bash
python3 skills/benchmark/scripts/benchmark.py bootstrap-start --repo <repository-root>
```

This captures local file metrics in `.contextlean/.bootstrap-baseline.json`.
Stop the measurement if capture fails; never reconstruct a before state after edits.
The separately requested setup can still be performed without a measurement claim.

After concrete setup validation:

```bash
python3 skills/benchmark/scripts/benchmark.py bootstrap-finish \
  --repo <repository-root> \
  --created <path> \
  --modified <path> \
  --limit <measurement-limit>
```

Repeat flags for actual changes and omit unused flags. The helper also supports
`--project-type`, `--moved`, and `--exclusion`. It writes the local
`.contextlean/bootstrap-report.json` and removes the temporary default baseline only
after success. Preserve failed measurement evidence; never invent before/after values.
No transfer receipt or historical-completeness certificate is needed.

Report exact bytes/counts separately from byte-based token estimates. These are not
measured model usage, speed or quality. Store no repository contents, secrets,
credentials, raw command output or telemetry in reports. Keep reports out of Git and
automatic instructions. Model benchmarks require a separate explicit request.
