# Balanced verification

This record concerns the uncommitted Balanced working-tree change verified on
2026-10-05. Historical releases and benchmarks describe their own frozen products.
The [Balanced contract](balanced-contract.md) owns the new behavior and comparison.

No model benchmark, external model invocation, commit, push or historical evidence
edit was performed. Offline tests use deterministic fixtures, fake providers and local
commands. They do not prove live model compliance or a model-executed bootstrap.

## Representative automatic context

The same representative project map is used before and after the contract change.
Counts are UTF-8 filesystem bytes, including the lightweight Claude wrapper once.
They exclude optional plugin discovery descriptions and tools' own startup context.

| Artifact | Before | Balanced |
| --- | ---: | ---: |
| AGENTS.md | 5,475 | 4,741 |
| CLAUDE.md | 11 | 11 |
| Total automatic guidance | 5,486 | 4,752 |

Reduction: **734 bytes / 13.38%**. The illustrative 4,724-byte goal is not a cap;
no retained coding safeguard was removed to close the 28-byte difference. This is a
static context measurement, not evidence of better model performance or token usage.

A fresh deterministic fixture generates only AGENTS.md and CLAUDE.md from the reviewed
project map and canonical core. Tests check idempotence, valid map paths/imports,
unchanged product files, runnable project tests and the sample CLI. This fixture is
test scaffolding, not an automated general-purpose bootstrap implementation.

## Checks and limitations

| Check | Result and scope |
| --- | --- |
| Full offline suite | **127 tests PASS**, no skips, 63.855 seconds on macOS / Python 3.14.7 in an isolated candidate copy outside the app sandbox. |
| Ruff 0.15.7 | Lint PASS; format PASS, 22 files already formatted. |
| Skill validators | Bootstrap, Audit, Lean Review and Benchmark PASS. |
| Codex package validator | PASS using the available local plugin validator. |
| Claude plugin and catalog validators | PASS with expected warnings: plugin-root CLAUDE.md is not injected project context; Claude ignores the catalog policy field. |
| Links | Candidate full-suite public document checks PASS; changed/new Markdown local file links and anchors checked separately. Remote links were not fetched. |
| Hygiene | Diff whitespace check PASS; no runtime dependency, new product/configuration behavior, tracked local report, credential or model setting added. Development tools stay in ignored local storage. |
| Historical preservation | All 2,077 pre-change protected benchmark/reference files are byte-identical. Frozen tracked evidence also passes aggregate fingerprint tests. |
| Fresh generation | Only the two guidance files created; map/import resolution, product preservation, idempotence and offline fixture commands PASS. |

The initial working-directory run reported 127 tests with one failure, four errors
and one skip. The errors/skip came from native macOS sandbox tests inside the app's
sandbox. The failure is a pre-existing broken relative link in the untracked
`benchmarks/results/2026-10-02-harness-v4-repeated-performance/harness-methodology-v4.md`:
`sandbox-composition.md` is absent from that archive.

The successful full run used current tracked file contents plus the eight new candidate
files, including all tracked historical evidence, without that pre-existing untracked
archive. It ran outside the app sandbox so the native permission tests could execute.
The original archive was neither changed nor deleted, and the public link test was not
weakened. Therefore the candidate suite is green; the complete working directory still
has that known archive link failure. Subsequent small documentation clarifications
were covered by targeted package/core/Skill tests, validators and link checks.

Frozen benchmark snapshots are excluded from Ruff because sanitized archived source
can intentionally be non-executable. This is a development-linter exclusion, not an
agent visibility exclusion. Fingerprint and published-evidence tests still check them.

## Audit

Read-only review used the repository's Audit Skill against the selected Balanced contract.

| Check | Status | Evidence / smallest action |
| --- | --- | --- |
| Maps and ownership | PASS | Root map names the canonical core, setup, optional references and tests; responsibilities match the change. |
| Runtime and hierarchy | PASS | Core is directly generated; no setup/reference import, root Skill handoff, broad startup read or after-every-task map audit. |
| Claude compatibility | PASS | Generated wrapper resolves to AGENTS.md; setup explicitly preserves useful existing Claude notes/exceptions. |
| Skills and routing | PASS | All four Codex metadata files disable implicit invocation; workflows require requests. Architecture reference has a concrete review trigger. |
| Exclusions and preservation | PASS | Source/tests/docs remain visible; safe exclusion validation stays in setup. Historical files and original bootstrap remain intact. |
| Current documentation | PASS | README explains Balanced; old coverage/release records are labelled historical; specialized obligations have named owners. |
| Historical archive link | ACTION NEEDED | Pre-existing missing sibling in the untracked archive above. Its owner should restore the missing evidence file or correct the link in a separately authorized evidence change. No archive edit made here. |
| Locality | PASS | Canonical runtime core, setup procedure and optional review/authoring material have distinct responsibilities; no runtime package or speculative layer. |

## Lean Review

Read-only review used the repository's Lean Review Skill and architecture reference.
No material finding in the candidate change. Existing shared workflows remain canonical;
there is no platform-specific workflow duplication or new runtime dependency. The
legacy checker is retained for explicit historical inspection and its existing smoke
case, not as a default setup gate. Test-only fixture generation has an explicit narrow
scope. Verification does not claim live model behavior or portable discovery on every
future client version.

## Historical compatibility

**55 legacy-equivalent PASS / 13 intentionally RE-SCOPED / 6 intentionally RETIRED /
2 previously REPLACED.** The 76-row comparison is in the Balanced contract; retired
rows are not counted as PASS. The former 74 PASS / 0 PARTIAL / 0 MISSING result remains
a statement about the historical contract, not the current product promise.

## Files

The lists below describe this implementation only; the pre-existing untracked benchmark
archive is excluded. Ignored local logs, development tools and temporary test copies
are not product files.

### Modified (19)

- `AGENTS.md`
- `README.md`
- `docs/bootstrap-coverage.md`
- `docs/release-notes.md`
- `docs/verification.md`
- `pyproject.toml`
- `skills/audit/SKILL.md`
- `skills/audit/agents/openai.yaml`
- `skills/benchmark/SKILL.md`
- `skills/benchmark/agents/openai.yaml`
- `skills/benchmark/references/methodology.md`
- `skills/bootstrap/SKILL.md`
- `skills/bootstrap/references/bootstrap-spec.md`
- `skills/bootstrap/scripts/verify_transfer.py`
- `skills/lean-review/SKILL.md`
- `skills/lean-review/agents/openai.yaml`
- `tests/bootstrap_fixture.py`
- `tests/test_bootstrap_transfer.py`
- `tests/test_package.py`

### Created (8)

- `docs/balanced-contract.md`
- `docs/balanced-verification.md`
- `docs/guidance-authoring.md`
- `skills/benchmark/references/static-capture.md`
- `skills/bootstrap/references/core-guidance.md`
- `skills/lean-review/references/architecture.md`
- `tests/fixtures/bootstrap-core/historical-hashes.json`
- `tests/fixtures/bootstrap-core/project-map.md`
