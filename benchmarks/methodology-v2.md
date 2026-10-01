# Graded benchmark methodology — harness v3 (v2 controls, corrected composition)

This version applies to future runs of `benchmarks/run_benchmark.py`. It changes
development benchmark infrastructure, not ContextLean instructions or product
behavior. Every new summary records `schema_version: 3` and
`benchmark_harness_version: 3`. Historical datasets and their frozen runners remain
unchanged; do not pool them with v3 observations as one controlled experiment.
The packaged generic navigation A/B runner retains its existing diagnostic contract
and does not acquire these stronger controls.

## Preparation and session isolation

Use one reviewed, frozen canonical fixture and an offline preparation attestation.
The existing map checker validates explicit paths, responsibility evidence,
guidance transfer and frozen hashes. Natural-language ownership review is still a
preparing agent/human responsibility; a hash does not prove semantic accuracy.

Vanilla and ContextLean are derived from that one canonical fixture. An exhaustive
manifest records each non-Git file's relative path, SHA-256 and size in both
conditions. The only permitted condition-specific files are `AGENTS.md`,
`CLAUDE.md` and optional `PROJECT_REFERENCE.md`, which Vanilla omits. Undeclared
differences, symlinks, prompt mismatches and invalid mapped paths block execution.
Each task's exact UTF-8 prompt bytes, size and digest are recorded. Prompts are not
altered to influence caching. All source, tests and runtime files in the fixture
are covered, regardless of extension.

Every preparation and model session gets a new system-generated root:

```text
<session-root>/
  repo/       # task fixture and deterministic Git repository
  tmp/        # session-local scratch files
  cache/      # pinned executable aliases and isolated auth-only CLI profile
  artifacts/  # disposable CLI control artifacts
  receipts/   # permission profile and preparation receipts
```

No parent root, CLI profile, shell startup state, memory file, conversation or
scratch directory is reused. Intended evidence is copied out before cleanup. The
entire root is removed, including scratch files above `repo/`; absence is checked.
Cleanup errors stop the campaign. A regression test writes a scratch script above
session A's repository, verifies its removal and verifies invisibility to session B.

Execution is provider-aware. Codex uses its native command sandbox, with no
outer OS sandbox around its driver. One named permission profile is passed to
both `codex sandbox` preflight and `codex exec`; legacy `--sandbox` options are
not mixed into that profile. The profile denies filesystem access by default,
permits minimal OS/pinned runtime reads, grants task `repo/` and `tmp/` writes,
and keeps `.git` read-only. Navigation permits only `tmp/` writes. The evidence
root is explicitly denied. Task-command networking is disabled; the provider
driver retains the network access needed for provider requests.

The trusted provider driver uses fresh session-local cache/profile/control areas;
command tools cannot write those areas. Receipts distinguish driver control writes
from effective task writable roots. Neither earlier sessions nor shared scratch
parents are readable through the native command sandbox. Roots are deleted after
use, and tests check both concurrent scratch denial and subsequent invisibility.
This remains local filesystem isolation, not a virtual machine or a proof of every
opaque provider implementation detail.

Claude selects provider-native execution and requires its sandbox enabled with
failure on unavailable isolation and no unsandboxed-command fallback. Its supported
CLI has no exposed offline native-command probe. A deterministic OS-primitive
probe is recorded as a diagnostic only; it cannot validate Claude's actual Bash
sandbox or built-in Read/Edit/Write policy. Claude execution therefore fails closed
before any model call until an actual native path can be checked offline. No
Claude CLI is run inside a second OS sandbox. For explicitly non-native external
runners, a supported harness outer boundary remains available (macOS Seatbelt or
Linux Bubblewrap), with its own permission gate; it is never combined with native
sandboxing.

Before execution the actual Codex CLI sandbox attempts repository and session-temp
writes, parent and outside writes, and evidence/unrelated scratch reads. It must report the expected
allowed/denied results with exit 0. Per-operation process exit codes are unavailable
because operations run in one local Python process; receipts retain booleans and
the enclosing CLI exit code without estimation. Canonical fixture tests run through
that same CLI-native sandbox path. Missing/unsupported native profiles, denied
sandbox initialization, incorrect permission results and nested strategy selections
are harness/preparation failures, with no retries or model calls. Failed and passed
probe receipts are saved publicly with sanitized paths and privately with exact
invocations before root cleanup.

Receipts record harness version, OS/platform, provider/CLI version, execution
strategy, configured native/outer sandbox states, native availability as actually
probed (null if unverified), permission mode, effective writable roots, cwd and
environment policy, probe scope/result and exit code. Normalized policy receipts
must match between Vanilla and ContextLean. Only guidance/configuration differs.
See [the sandbox composition diagnosis](sandbox-composition.md) for the exact
macOS failure and the provider-specific limits. Linux must pass the real CLI gate
on its deployment host; macOS evidence does not establish Linux compatibility.

## Git, runtime and environment

Every session initializes a real Git repository, branch `main`, with an empty
template, fixed local identity and UTC commit date, no remotes or hooks, and no
inherited metadata. Global/system Git configuration is disabled. Relevant local
settings are fixed and recorded. The untouched baseline is committed, clean status
is required, and an offline diff probe modifies and restores one tracked file.
The receipt includes Git version, commit, tree, branch, configuration and status.
Repeated baselines within a condition must match. Vanilla and ContextLean commit
and tree hashes differ because committed guidance differs; product bytes and Git
policy must match across conditions. Requiring identical full-tree hashes would
contradict the intended treatment.

Python, Git, rg, shell and CLI paths are resolved once, with executable hashes and
versions (shell version is null if its version probe is unsupported). Session
aliases resolve these same binaries. Hashes are rechecked before execution. The
receipt records OS/platform/architecture and working directory. Auxiliary system
utilities and opaque CLI dependency internals are outside this small pinned binary
set; their drift is a remaining host limitation. This fixture uses only Python's
standard library. Dependency-bearing fixtures fail preparation rather than silently
installing or inheriting packages; supporting them requires a separately pinned
environment and a new documented series.

The child environment is rebuilt from an explicit allowlist. Locale is recorded;
UTC, bytecode suppression, Git isolation, session temporary/cache/profile paths
and shell startup isolation are fixed. Child HOME is the isolated profile, so
login-shell home startup files cannot come from the host account; Python user-site
loading is disabled. The parent process environment remains unchanged. Python paths, proxy overrides, injected
shell startup files and provider overrides are not inherited. Relevant environment
receipts are compared after portable path normalization. Secret variables record
presence/absence only. Authentication can come from provider variables or a copied
auth-only credential file; user settings, plugins, memories and history are not
copied. Auth values never enter receipts. Quota is explicitly unknown because no
reliable cross-provider check exists in this harness; unknown is not sufficient
quota or a zero balance. A future reliable check must become a gate.

All scheduled condition/task preparations pass before the first authorized model
call. Each actual session repeats its own checks: root freshness, frozen source
and grader hashes, manifest, map, Git, runtime, environment, permissions, runnable
canonical verbose tests and available/compilable grader. The grader uses pinned
Python and the same restricted environment in a separate evaluation copy, restoring
canonical regression tests. Its acceptance rules are unchanged. Its subprocesses
are not part of the measured provider execution or its native boundary.

## Evidence and accounting

Before each invocation, record the exact provider, requested model, reasoning/effort,
CLI version, timeout, permission policy, cwd and flags. Afterwards add reported
model/permission mode and exposed request/session identifiers. A reported Claude
permission mismatch stops the campaign. A requested model alias may resolve to a
provider model name; both are retained without inventing equivalence.

Raw private stdout/stderr are byte-exact, including partial streams from timeouts.
Public traces preserve event order but redact private paths, secrets and structured
account identifiers. The parser records every supported exposed tool attempt,
exact inputs, command, session cwd, status, denial reason, exit, duration and
returned/output UTF-8 sizes when exposed. A shell may change cwd internally; this
is stated. Codex merges command output, so its stdout/stderr split is null. Hidden
tool calls, per-command filesystem snapshots, unreported durations and hidden
internal model requests are unavailable, not estimated. Exposed file-change events
are recorded separately from the complete post-run repository diff.

Verbose unittest coverage records test identities, discovered/passed/failed counts
and a digest only when the full exposed list matches the discovered count. Count-only
pytest output has no invented test identities. Equal digests detect targeted and
full commands that ran the same tests. Intervening exposed mutations are recorded;
an intervening shell/tool whose changes are unobservable leaves the change flag
unknown. Hidden state is never inferred from two matching test lists.

Usage records retain each exposed message/turn report, including partial/duplicate
stream reports, without summing overlapping reports. Codex's current top-level
turn aggregate does not expose internal request counts. Claude message IDs count
distinct exposed assistant messages; provider turn counts are retained independently.
The final primary aggregate is used for campaign metrics. Missing or malformed
usage fields are null. Input includes cached input; total is input plus output.
Claude cache creation and cache reads are incorporated in input, with cache reads
reported separately. Reasoning output is already included in output and is never
added a second time. No per-action token attribution is invented.

Claude `modelUsage` entries for the reported primary model are preserved separately
from helper/Haiku entries. If the primary model is unreported, those entries are
unclassified rather than silently called helpers. Helper usage is not merged into
primary token metrics. Tool-output byte totals use original exposed strings before
redaction; absent streams remain null. Private raw byte totals and decoded trace
digests have explicitly separate scopes.

After execution, preserve solutions and inspect repository changes/status, `tmp/`
files, control-area file sizes/links and unexpected entries above approved roots.
Unexpected root entries, incomplete traces or cleanup failure invalidate measurement
completeness. External hidden side effects cannot be inspected; the native write
boundary blocks ordinary outside writes. No measured state is carried forward.

## Experiment design and failure rules

Compatibility smoke tests are explicitly labeled and cannot establish performance.
Performance mode requires at least three independent repetitions per task/condition;
five is preferred. The deterministic schedule is saved before any model invocation.
Pair order alternates Vanilla→ContextLean, ContextLean→Vanilla, Vanilla→ContextLean,
also offset by task index. No adaptive order, replacement of unfavorable repetitions,
silent retries or early stopping after a favorable outcome is permitted.

Every scheduled and completed observation remains identifiable by sequence, task,
repeat, condition and timestamps. Summaries retain observations, mean, median,
min/max/range and sample standard deviation (`n−1`; null at one observation).
Paired differences are ContextLean minus Vanilla within a task/repetition. An
unavailable or interrupted side blocks that pair's comparison; incomplete planned
pairs block the overall paired aggregate for that metric. Complete incorrect task
solutions remain in descriptive measurements and prohibit gain claims. Partial
provider measurements remain in individual raw evidence but are excluded from
comparison statistics. No confidence interval or statistical-significance claim is
computed. Use sample size and task success before interpreting resource usage.

Failure categories are explicit:

| Category | Treatment |
|---|---|
| A: model/task failure | Retain incorrect solution and complete usage; continue scheduled work |
| B: provider usage-limit interruption | Task success null; preserve partial usage; stop without retry |
| C: provider/network failure | Task success null; stop without retry |
| D: harness/preparation failure | Zero calls if preflight fails; invalidate affected measurement; stop |
| E: grading infrastructure failure | Task success null; invalidate comparison; stop |

Quota detection uses exposed error text, not a claim about unexposed provider
internals. CLI/service errors whose origin is ambiguous are retained in category C
with their original diagnostics. Test/acceptance assertion failures are category A;
grader startup failures and timeouts are category E. Campaigns stopped for B–E
remain incomplete; unattempted schedule entries are not fabricated observations.

## Public export and limitations

`private/` is local debugging material, protected by its private directory mode.
It contains original streams, exact runtime/cwd receipts (auth presence only),
original infrastructure/task/canonical fixture bytes and unredacted solutions.
**Never publish that directory.** The public sibling artifacts are sanitized;
host paths become `<session-root>`, `<evidence>`, `<home>` or `<host-path>`.
Known credential strings and common credential patterns are redacted, as are
structured auth/account fields. Arbitrary provider output can contain unknown
private data, so review the public export before publishing. No upload is automatic.
Binary files are omitted from public tree exports with an explicit omission list;
their exact originals remain private. Sanitized files can differ from original
bytes: input manifests hash originals, while public `checksums.json` hashes the
export. Exact reproduction uses reviewed original inputs, not a redacted archive.

The harness controls fixture bytes, Git policy, filesystem writes/session isolation,
pinned runtimes, task prompts, declared permissions, grader, order and exposed
evidence capture. It cannot fully control model stochasticity, provider caching,
service load, hidden provider changes or unexposed reasoning/tool selection.
Cache state stays explicitly uncontrolled; cached/uncached usage, order, timestamps
and exposed identifiers make that limitation auditable. Three or five observations
do not automatically establish causality, generalization or significance.

Offline self-tests exercise isolation, manifest/path drift, deterministic Git,
runtime/environment/permission parity, fail-before-launch behavior, quota handling,
unavailable metrics, equivalent coverage, raw byte preservation and export hygiene.
Model invocations are mocked; one stream test runs only Python printing literal
bytes. Native permission probes and CLI version probes do not run models.
