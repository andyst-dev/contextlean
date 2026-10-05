# Old-versus-Balanced product comparison adapter

This is a separate product-change validation path, not a new headline benchmark.
The adapter schema is **1**; execution remains **harness v4**, coverage parser **2**,
and the ContextLean package version is unchanged. No model sessions, commit or push
were performed for this infrastructure change. Historical evidence is untouched.

## Frozen conditions

| Condition | Product revision | Automatic bytes | Optional reference bytes |
| --- | --- | ---: | ---: |
| old | `ae8653b123bdb4c686ee36825c80db851c8595ea` | 5,486 | 3,922 |
| balanced | `1a6e67fb9e5c3d5a91ca89a9f5466d2fa037ea52` | 4,752 | 0 |

The adapter exports committed source with `git archive`, runs each revision's own
`tests/bootstrap_fixture.py` in an isolated Python import context, and records the
source inventory plus exact generated guidance sizes and hashes. Old's generator
also constructs a legacy transfer receipt; that administration file is not installed
in the task fixture. No guidance is reconstructed manually or read from current
working-tree guidance. Both conditions require nonempty AGENTS.md and CLAUDE.md;
Old additionally requires its committed PROJECT_REFERENCE.md.

The same committed task source, test files, sample data and configuration are required
byte-for-byte in both fixtures. The exact Refactor task object is selected from the
committed suite. The grader, prompt builder and shared infrastructure retain their
existing responsibilities. Committed task/grader/control inputs must match the shared
checkout before preparation; frozen source, fixture and execution inputs are checked
again before every slot. Any undeclared difference fails closed.

## Architecture and unchanged behavior

[compare_products.py](../benchmarks/compare_products.py) owns revision materialization,
explicit `old` / `balanced` identity, guidance-only manifest assertions, the six-slot
schedule, exact runtime requirements and paired product statistics.

[run_benchmark.py](../benchmarks/run_benchmark.py) accepts an optional comparison input
through its Python API. Its public CLI has no guided-comparison switch. The same
session loop still owns isolation, native sandbox probes, normalized environment,
cache/profile setup, Git initialization, repeated gate checks, tracing, saved solutions,
submitted/original/acceptance grading, interruption handling and cleanup. The grader
accepts the frozen original-test fixture rather than assuming the current fixture.

`harness.py`, `execution.py`, `runtime.py`, `trace.py`, `prepare_fixture.py`,
`evaluate.py`, the task suite and the packaged measurement helper are byte-identical
to both product revisions. There is no second execution implementation, monkeypatch
or runtime replacement of a harness control in the adapter.

The existing condition constructor and manifest are unchanged: Vanilla still omits
all guidance and rejects any supplied guidance. The new guided manifest uses the
existing complete inventory, copier and receipt-comparison primitives with a different,
explicit product contract. It does not invoke the Vanilla constructor/manifest or
relabel a Vanilla fixture. Receipts, schedule entries, saved run records and parsed
trace records carry `condition_kind: guided_product_revision`, `condition_name` and
`product_revision`, plus guidance hashes/bytes. Raw provider streams retain original
content and are associated with these identities by their condition-labelled directory.

Both conditions use the same non-guidance repository baseline and Git policy. Their
Git tree/commit IDs necessarily differ because guidance files are tracked; each
condition's baseline repeats identically across its three slots. Requiring identical
whole-tree commits would contradict the intended guidance difference.

## Offline preparation

Run from a checkout containing both immutable Git objects:

```bash
python3 -B benchmarks/compare_products.py --preflight-only \
  --shell /bin/zsh \
  --output-dir .contextlean/validation/old-balanced-offline
```

The output directory must be new. Inputs, schedule and source hashes are retained.
The adapter is fixed to Refactor, `gpt-5.6-sol`, high reasoning, three pairs and zero
retries. The schedule is written before preparation/model execution:

1. old
2. balanced
3. balanced
4. old
5. old
6. balanced

`--preflight-only` returns before invocation. It uses offline provider version/native
sandbox commands; it never calls a model. A future `--live` use requires a separate
explicit request and a fresh output directory, runs all six gates before the first
call, and repeats them before each measured session. Failed/interrupted observations
are retained under the existing v4 no-retry semantics.

The adapter requires Python 3.14.4, Git 2.54.0 and rg 15.2.0. Shared gates verify the
actual login-shell environment and selected executables, separate HOME/TMP/cache/config,
no host-cache diagnostics, blocked outside/evidence/cross-session access and successful
cleanup. The pinned binaries and normalized receipts must match across conditions.

## Validation record

Native validation ran on 2026-10-05. Evidence is retained locally at
`.contextlean/validation/2026-10-05-old-balanced-adapter-final/`; the initial offline
development preparation is retained separately at
`.contextlean/validation/2026-10-05-old-balanced-adapter/`. Both used zero model calls.
The final preparation binds the finished adapter source, including its exit-status
check for future failed grading. No measured session was retried.
The prior 30-run v0.2.1 study remains historical and is not replaced. No README headline
performance values are changed, and offline preparation is not behavioral evidence
that a model will solve Refactor successfully.


| Slot | Condition | Automatic bytes | Native preparation | Cleanup |
| --- | --- | ---: | --- | --- |
| 1 | old | 5,486 | PASS | PASS |
| 2 | balanced | 4,752 | PASS | PASS |
| 3 | balanced | 4,752 | PASS | PASS |
| 4 | old | 5,486 | PASS | PASS |
| 5 | old | 5,486 | PASS | PASS |
| 6 | balanced | 4,752 | PASS | PASS |

All six final slots have distinct native probe root IDs, no surviving prior root,
clean deterministic Git state, five passing canonical tests, and identical normalized
runtime/environment/permission/grader/prompt/coverage receipts. Effective runtime is
Python **3.14.4**, Git **2.54.0**, rg **15.2.0**, with `/bin/zsh` and Codex CLI 0.147.0.
All cache-location write probes pass without diagnostics. Repo/tmp writes succeed;
parent/outside writes and evidence/unrelated-session reads are denied. No model runs
or task solutions exist in this offline preparation.

The canonical Git commit repeats as `139297b7ccb0b591f383dbb2c09df8d841fd8a3c`
for Old and `367762a0a395284c7d0b71d4d661fbf62e8d1ff8` for Balanced. Their non-guidance
bytes and Git configuration match. Differences in tracked guidance explain the
condition-specific commit IDs.

Frozen final execution inputs:

- `benchmarks/run_benchmark.py`: `2494e377c11e26fc51a740410c31cc4f2f0b14334244ac9a0a917f8d8cb488ec`
- `benchmarks/compare_products.py`: `6043b7c70eaee6eafae0ddcc85229e9eb1c798aaebac7487ae0afc1ebded8060`
- Refactor prompt: `464e90080aad8fbba255ac27e48b7bd0faa0fc33098d3eba0a6c3473da7589e3`
- Grader: `3200e20da7522c1a063cda247433efcdcaf2e6f945c7cdf951dee35e624fd686`
- Five-test coverage identity: `3ecb703b5031cfb650873bd0c0da23174187806cebd6330acdfa7f843155f29a`

Current-product manifests, Skills and generated guidance are unchanged by the adapter.
Only the root repository map gains the adapter/test/document paths. The existing
Vanilla runner gets an optional artifact-selection input; its default conditions,
rejection invariant, CLI, gates and execution order remain covered by the original
suite. Added tests use synthetic local Git commits so CI needs no deep history;
poisoned working-tree generators prove committed-input selection. A synthetic provider
trace test exercises six observations, all three grading layers, explicit identities
and paired statistics without any provider execution. Real native preparation above
uses neither fake runtime nor mocked controls.

Quality: **135 offline tests PASS**, no skips, 98.826 seconds, including all existing
harness/provider/runtime contracts and **8 adapter tests**. Ruff lint and formatting
pass (24 Python files); whitespace and local documentation links pass. The final
source hashes above match the native preparation inputs. Public evidence is sanitized;
raw/private evidence remains separate and was not published. All 2,048 historical
result/reference files match their pre-change checksums; other pre-existing benchmark
inputs remain unchanged except the explicitly adapted shared runner.

The full suite ran on an exact candidate copy outside the app sandbox, with all
tracked evidence and new adapter files. It excluded the pre-existing untracked
`benchmarks/results/2026-10-02-harness-v4-repeated-performance/` archive, whose known
missing `sandbox-composition.md` link still fails the working-directory public-link
test. That archive is unchanged, and the link test was not weakened. Native permission
tests require running outside the application's nested sandbox on this macOS host.
The successful result applies to the candidate, not a claim that the unrelated archive
has been repaired.

Files modified: `AGENTS.md`, `benchmarks/run_benchmark.py`.
Files created: `benchmarks/compare_products.py`, `tests/test_product_comparison.py`,
`docs/product-comparison-adapter.md`.
