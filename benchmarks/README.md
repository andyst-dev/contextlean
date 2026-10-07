# ContextLean measurement infrastructure

The reusable development runner uses **harness v4**. It grades five independent
tasks against a standard-library Python fixture, with isolated sessions, controlled
runtime and permissions, frozen preparation, and retained outcomes. Read the
[current methodology](methodology.md) for controls and limitations.

Measurement is optional. Nothing here authorizes model calls. Ordinary tests and
CI are offline; live execution requires a separate explicit request.

## Tools and responsibilities

| Tool | Responsibility |
|---|---|
| `prepare_fixture.py` | Validate reviewed map/source equivalence and freeze a new fixture |
| `run_benchmark.py` | Graded Vanilla-versus-ContextLean campaign orchestration |
| `evaluate.py` | Independent task acceptance |
| `harness.py` | Session lifecycle, Git, permissions, receipts and statistics |
| `execution.py`, `runtime.py` | Provider sandbox strategy and effective runtime controls |
| `trace.py` | Exposed commands, usage and coverage parsing |

[Task prompts](tasks/suite.json) cover navigation, bug fixing, a feature, refactoring
and documentation/configuration. The [fixture](fixtures/expense-report) is synthetic;
its results do not establish performance across real repositories.

## Prepare reviewed inputs

Use disposable copies. Author guidance separately and review mapped responsibilities
against source. Freeze to a **new path** outside both preparation inputs:

```sh
python3 benchmarks/prepare_fixture.py \
  --baseline /path/to/baseline \
  --prepared /path/to/bootstrapped-copy \
  --review /path/to/responsibility-review.json \
  --output /path/to/new-frozen-fixture \
  --record /path/to/new-preparation.json
```

Neither output nor record may already exist. The record must stay outside the
measured fixture. Invalid paths, missing semantic reviews, product differences and
stale hashes fail closed. The [historical review example](analysis/2026-09-30-final-0.2.0/corrected-preparation.json)
illustrates source attestation; its old transfer certification is not a current
Bootstrap requirement.

The CLI uses `benchmarks/fixtures/expense-report` in its source checkout. In a
**disposable runner checkout**, replace that fixture with the reviewed frozen copy
and use its matching preparation record. Preserve the original checkout. Do not
point the freeze command at the existing tracked fixture directory.

## Offline gates and opt-in execution

Python 3.11+, Git, rg and an offline-verifiable provider-native sandbox are required.
Codex uses its native sandbox. The supported Claude path fails closed while an
actual native-command probe is unavailable. See methodology for provider limits.

From the prepared disposable checkout, run gates without model calls:

```sh
python3 benchmarks/run_benchmark.py \
  --provider codex --model MODEL --reasoning EFFORT \
  --preflight-only --experiment-kind performance --repeat 3 \
  --preparation-record /path/to/new-preparation.json \
  --output-dir .contextlean/validation/preflight-v4
```

Preflight checks the planned sessions before any model invocation. Use a new output
directory. A successful preflight does not authorize live execution.

Only with explicit authorization, replace `--preflight-only` with `--live` and use
another new output directory. Five tasks × three repetitions × two conditions means
**30 model calls**. Compatibility smoke mode permits one repetition but supports no
performance claim. Performance mode requires at least three, preferably five.

The saved schedule counterbalances order. Failures and interruptions remain visible;
there are no silent retries or favorable-result stopping. Incomplete measurements
suppress comparison claims. Private originals stay local; review sanitized exports
before publication. Never publish `private/` or overwrite a published result set.

## Product measurement and published evidence

The packaged [Benchmark Skill](../skills/benchmark/SKILL.md) separately supports an
offline structural estimate, explicit before/after capture and a read-only diagnostic
navigation A/B mode. That mode does not grade answer correctness. It is not a
replacement for this graded suite.

[Evidence provenance](../docs/evidence.md) is the current results index: v0.3.0 has
Balanced behavioral validation, while the 30-session performance study describes
v0.2.1. Earlier diagnostic and release datasets retain their original limitations.

The completed Old-versus-Balanced adapter is historical tooling, reproduced from
its frozen revision and [published evidence](results/2026-10-06-balanced-product-change/README.md).
Its [dated design record](../docs/history/product-comparison-adapter.md) remains
available. It is not an active extension of the current runner.
