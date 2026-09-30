# Compact permanent context — historical offline verification

This maintainer record preserves the offline checks performed before committing and
benchmarking the guidance changes. Its statements about uncommitted work, zero model
calls and pending isolated validation apply only to those stages. For the released
v0.2.0 status and subsequent validation, see [current verification](verification.md#current-released-status).

The initial record below describes frozen product `90ed9a4`. The subsequent general
[refactor and repository state update](#refactor-and-repository-state-update) has its
own offline verification below; benchmark evidence continues to describe the frozen product.

ContextLean 0.2.0 retains **74 PASS / 0 PARTIAL / 0 MISSING / 2 INTENTIONALLY
REPLACED**, including all **71 permanent semantic facets**. The category decisions
in the original design request were the design input; no separate classification file
was saved. This is general repository guidance compression, with no task-specific
prompt, grader, product or evidence changes.

## Semantic comparison

The [76-row comparison](bootstrap-coverage.md#coverage-matrix) was reviewed again
against the immutable [714-line historical specification](reference/original-agent-bootstrap.md).
Its original-body SHA-256 remains
`ecc02ff12623297e057eafb78e16ab8020953b317cc07cbf27bf764ab60d3f05`.
Setup scope, preservation, ordered analysis, command verification, compatible wrappers,
exclusions, lifecycle and completion duties remain in the canonical bootstrap procedure.
Permanent obligations have hash-bound durable destinations in the
[worked transfer](../tests/fixtures/bootstrap-transfer/transfer.json).

The changes to destinations are:

- Navigation stays automatic, including owner/search-first exploration. Repository
  state applies to broad/state-sensitive changes when version control is available;
  read-only navigation requires no Git ritual.
- Ownership, cohesive files, nonfragmentation, focused interfaces and local internals
  stay automatic. Extraction questions, refactoring signals, distinct boundaries and
  coupling-based indirection decisions load only for architecture/refactoring work.
- The six-step reuse order, focused readable changes, root-cause fixes, safe obsolete
  removal and all correctness/security/trust/data/accessibility safeguards stay automatic.
- Proportional verification chooses scope, rather than mandating three sequential
  stages. A single automatic regression rule covers both non-trivial logic and fixes.
- After every task, map accuracy is checked; only meaningful navigation/architecture
  changes update the smallest map. Broad drift inspection remains on-demand Audit.
- The automatic project Skill rule contains the reusable-procedure threshold and a
  creation/modification trigger. Locations, discovery and portable sharing load only
  under that trigger. No generic project review Skill is generated.
- Advisory Lean Review retains explicit packaged delegation. Both review Skills remain
  on-demand and cannot replace ordinary coding/maintenance duties.

Five consolidated facets retain their individual identities: cohesive files/modules/
classes shares the owner rule; nonfragmentation and specific helper ownership also use
Ownership; practical bug regression and smallest meaningful verification use Verification.
Seven conditional facets use Architecture decisions or Project Skills. The other optional
reference sections explain bug diagnosis and verification scope; those duties already
exist automatically and do not depend on consulting the examples.

Structural checks bind reviewed content and applicability sections, require each facet
exactly once, and reject missing destinations, changed content, orphan references,
automatic reference imports, unsupported delegation and setup-only duties. Semantic
preservation is the reviewed comparison, not an automated proof of prose meaning or
future model compliance.

## Measured context

Exact UTF-8 measurements, with **bytes ÷ 4 estimates** rather than tokenizer/session
measurements. The before map is read from the unchanged clean-final source snapshot.
The after map is the generated worked fixture, preserving the same eight mapped
project roles, flow, Decimal handling, commands and useful local context in shorter prose.

| Material | Before bytes / lines | After bytes / lines | Estimated tokens before → after |
|---|---:|---:|---:|
| Representative AGENTS.md | 7,956 / 82 | 5,478 / 68 | 1,989 → 1,369.5 |
| Claude wrapper | 11 / 1 | 11 / 1 | 2.75 → 2.75 |
| Automatic files, including wrapper | 7,967 / 83 | 5,489 / 69 | 1,991.75 → 1,372.25 |
| Conditional PROJECT_REFERENCE.md | absent | 2,378 / 24 | 594.5, excluded from startup |

AGENTS.md decreases **31.15%**; automatic files including the Claude wrapper decrease
**31.10%**. Codex's canonical map estimate is 1,369.5 tokens; Claude also reads the small
wrapper. Conditional reference bytes are never counted as automatic startup context.
Setup procedure/inventory, transfer receipts, Skill discovery descriptions and global
instructions are outside this estimate. No measured runtime/token-usage gain is claimed.
The previous smaller worked example was 6,478 bytes / 56 lines; it is a different baseline
from the requested representative map and is not substituted for the 7,956-byte baseline.
ContextLean’s own root map also falls from 6,023 bytes / 74 lines to 4,961 bytes /
74 lines (**17.63%**), keeping all existing mapped paths and adding the fresh-fixture helper.

## Rule distribution

Each of the 71 stable facets has one primary category in the setup-only inventory.
Consolidated facets still point to their own durable destination; categories do not erase
identities or obligations.

| Category | Facets | Delivery |
|---|---:|---|
| A: automatic invariants | 28 | Compact permanent constraints |
| B: routing/action rules | 28 | Automatic task actions and conditional triggers |
| C: packaged Skill delegation | 3 | Explicit on-demand Lean Review handoff |
| D: conditional references | 7 | Four architecture facets, three project Skill facets |
| E: consolidated duplicates | 5 | Shared automatic owner/verification wording |

## Offline quality

**105 offline tests pass**, along with Ruff 0.15.7 lint/format, all four official Skill validators,
Codex package validation, both Claude manifest/catalog validators, transfer contracts,
safe-removal contracts, 46 relative links/anchors, hygiene and fresh fixture/map validation.
Claude reports its existing wrapper-context and ignored catalog-policy warnings.
The fixture application is deterministic and model-free; it demonstrates generated
filesystem/receipt consistency, not independent live bootstrap behavior.

The transfer gate passes for 11 groups / 71 facets with and without a disposable copy
of the exact historical bootstrap. Version 1 receipts from the frozen clean source remain
valid. Version 2 records cover split destinations and explicit conditional applicability.
The normal suite includes offline regrading and mocked runner tests; no live five-task
benchmark was executed.

## Dogfood

Audit Context Locality: **9 PASS / 0 WARNING / 0 ACTION NEEDED** for maps/commands,
instruction duplication, startup/optional context, wrappers, Skill/reference structure,
exclusions, documentation freshness, transfer/removal and architectural locality.
The sole project reference has section-specific triggers, never an automatic import.
Inventory and worked fixture are canonical setup input and test output respectively,
not competing live instruction owners. No new exclusions hide useful material.
Platform discovery/compliance is not remeasured by this offline check.

Lean Change Review: **no material findings**. Bootstrap owns the explicit standard-library
checker and receipt schema; tests own deterministic fixture application. The second schema
is required for real facet splits and preserves existing receipts. No runtime dependency,
forwarding wrapper, hidden mandatory reference, contradictory rule or context fragmentation
was introduced. Safety and regression obligations remain automatic.

## Benchmark and Git boundary

**Zero new live/model benchmark runs.** All historical, diagnostic and clean evidence,
benchmark tasks/prompts/graders and the immutable original specification remain byte-identical
to HEAD. No commit or push was made. Local verification logs are ignored; only guidance,
bootstrap verification, contracts and developer documentation changed.

Compact ContextLean preserves complete semantic coverage.

## Refactor and repository state update

This is a general product guidance improvement after the compact product freeze,
not benchmark tuning. Benchmark tasks, prompts, graders, measurement code, historical
and compact-final evidence, and the original bootstrap specification are unchanged.
No model call, commit, push, tag or release was made.

The permanent navigation rule now trusts mapped ownership and architecture unless
source contradicts them. Start at the smallest owner with relevant usages/dependencies/
tests; skip broad ownership reconfirmation and equivalent searches already answered.
Distinct unresolved questions still warrant searches. Concrete evidence still warrants
expansion: ambiguous/stale ownership, contradictory source, cross-boundary usages,
public interfaces, shared/core effects, wider test impact or dependency-flow uncertainty.
Source evidence overrides the map. This preserves targeted exploration and risk handling.

Explicit refactors preserve behavior and assess relevant boundaries. The existing
Architecture decisions reference describes the owner → changed code → needed callers/
usages/tests → smallest structural change → proportional verification route, with
unnecessary steps skipped. It retains all original refactor signals without making
signals an architecture audit. Its trigger is uncertain extraction/boundary/refactor
scope; routine refactors need not load it. Audit and Lean Review remain on-demand.

Repository-state inspection now requires broad/state-sensitive work, available
version-control metadata and relevant state. The setup procedure identifies uncommitted
work, generated state, branching, conflicts and broad edits as reasons state may matter.
Read-only navigation and small local edits alone require neither Git inspection nor
an availability probe. Explicit bootstrap's own state inspection remains appropriate
for its broad configuration changes. Proportional verification still starts targeted,
broadens for shared/core/public effects, and uses full verification when necessary or
project-required; these are scope choices, not three mandatory stages or token-saving cuts.

The original 76-row comparison was reviewed against the immutable historical bootstrap
and final durable destinations: **74 PASS / 0 PARTIAL / 0 MISSING / 2 INTENTIONALLY
REPLACED**. All **71 permanent facets**, their identifiers/order and delivery categories
are preserved. The hash-bound worked receipt and its activation descriptions were
regenerated after review. Tests guard concept clauses, actual destinations and context
size; they do not prove natural-language semantics or future model compliance.

| Material | Previous bytes / lines | New bytes / lines | Estimated tokens before → after |
|---|---:|---:|---:|
| Representative AGENTS.md | 5,478 / 68 | 5,476 / 68 | 1,369.5 → 1,369 |
| Claude wrapper | 11 / 1 | 11 / 1 | 2.75 → 2.75 |
| Total automatic startup | 5,489 / 69 | 5,487 / 69 | 1,372.25 → 1,371.75 |
| Conditional PROJECT_REFERENCE.md | 2,378 / 24 | 3,564 / 28 | 594.5 → 891 |

UTF-8 bytes are exact; tokens are bytes ÷ 4 estimates. Automatic context decreases
**2 bytes**; conditional detail increases **1,186 bytes**, outside startup context.
ContextLean's own root map is unchanged: no path, ownership or verification-flow change
requires a map edit. The bootstrap procedure retains its existing 249-line contract.

Offline quality: **114 tests pass**, Ruff 0.15.7 lint/format pass, all four official Skill
validators pass, the Codex plugin validator passes, and both Claude validators pass
with their existing wrapper-context/catalog-policy warnings. Transfer/safe-removal
contracts, fresh generated maps/paths, relative links/anchors, whitespace, hygiene and
protected-file SHA-256 checks pass. All 310 tracked protected files equal their before
hashes and HEAD; this includes all benchmark material and the original specification.

Audit Context Locality: **9 PASS / 0 WARNING / 0 ACTION NEEDED** across map/commands,
instruction duplication, startup/conditional context, wrappers, Skill/reference structure,
exclusions, documentation freshness, transfer/removal and architectural locality.
Navigation has one automatic rule; detailed examples are conditional. No mandatory
Git check, large automatic reference, architecture audit or under-exploration rule was
introduced. Lean Change Review: **no material findings**; the change stays within the
bootstrap owner, deterministic fixtures/contracts and this verification record, without
new dependencies or checker schema changes. Actual model behavior remains unmeasured.

The compact-final historical result remains **434,893 → 361,650 tokens (-16.84%)**,
**167.80s → 157.79s (-5.97%)**, **5/5 → 5/5 success**, with ContextLean Refactor
**+23.30% tokens**. These numbers describe the previous frozen product and are unchanged.
The general implementation is semantically safe for one separately authorized isolated
Refactor Vanilla/ContextLean validation pair; no such pair was run here.
