# Bootstrap semantic preservation — 0.2.0 repair

This is developer verification, not agent startup guidance. It revisits every grouped
requirement in the owner-reviewed comparison against the supplied 714-line
[`AGENT_BOOTSTRAP.md`, preserved as historical reference](reference/original-agent-bootstrap.md)
(original-body SHA-256: `ecc02ff12623297e057eafb78e16ab8020953b317cc07cbf27bf764ab60d3f05`).
Original line numbers below identify that preserved body, excluding its historical
header; examples and repeated statements share a row with their behavior.
The archive is optional developer documentation, never required by normal Skills or
project startup guidance. Its rules are not modernized or maintained as a second source.
The safe-removal contract verifies the body's original digest and that transfer still
passes before and after removing a disposable copy of that exact original specification.

The [canonical setup procedure](../skills/bootstrap/references/bootstrap-spec.md)
owns setup only. [Permanent rules](../skills/bootstrap/references/permanent-rules.json)
own 11 compact groups / 71 stable semantic facets. Bootstrap adapts their meaning
into project guidance, preserving existing equivalent instructions. The complete
[worked example](../tests/fixtures/bootstrap-transfer/AGENTS.md) is 56 lines, not a
copy of the original specification. Advisory review is explicitly delegated to
[Lean Change Review](../skills/lean-review/SKILL.md); separate drift inspection uses
[Audit Context Locality](../skills/audit/SKILL.md). Neither replaces ordinary coding
or after-task maintenance duties.

## Acceptance and transfer record

Each permanent facet requires an agent's semantic review and one actual durable
destination. The [read-only checker](../skills/bootstrap/scripts/verify_transfer.py)
verifies completeness, reachability without setup files, explicit supported delegation
and hashes of the reviewed destination sections. It **cannot prove natural-language
meaning or future model compliance**. Semantic comparison, nested scope, reference
applicability, configuration effectiveness and actual Skill discovery remain agent
verification duties; do not treat the attestation flag as a substitute.

The [example transfer record](../tests/fixtures/bootstrap-transfer/transfer.json)
shows the schema. It records section hashes, facet identifiers and review attestations,
not copied project contents. In a bootstrapped project, keep it locally at
`.contextlean/bootstrap-transfer.json`; it is not needed by future development sessions.
Keep this receipt out of Git/startup context. Permanent guidance itself stays durable.

For example, navigation transfers into the project's `AGENTS.md` / `Navigation`
section with `kind: guidance`, all navigation facets, `semantics_reviewed: true` and
that section body's SHA-256. Advisory review uses `kind: contextlean_skill`, qualified
name `contextlean:lean-review` and the installed workflow's reviewed section hash;
project guidance documents the invocation and its advisory scope. No generic review
Skill is generated. Missing semantics, stale evidence or losing a destination blocks
completion before the static report's successful finish.

Removing/ignoring the original specification must leave every permanent duty in the
AGENTS hierarchy, Claude wrappers, available Skills, local configuration or explicitly
applicable targeted references. Do not delete the reusable installed plugin specification.
The example passes both with and without the old target specification; a rule left
only in that old file fails the checker. There are no intentionally discarded permanent
behaviors or undocumented obsolescence exceptions.

## Project Skill compatibility

Current project sources use `.agents/skills/<name>/SKILL.md`, with Claude exposure at
`.claude/skills/<name>/SKILL.md`. Relative directory symlinks may share one source when
portable; verify resolution after relocation and discovery on both tools. These are
project-local paths, not ContextLean's plugin-root `skills/`. Sources checked on
2026-09-30: [official Codex Skill locations](https://learn.chatgpt.com/docs/build-skills),
[official Claude project Skills and symlinks](https://code.claude.com/docs/en/skills).
If a platform cannot load a portable shared source, report the limitation rather than
claiming success or creating divergent copies.

## Coverage matrix

PASS means explicit/equivalent preserved semantics; PARTIAL means a substantive gap
remains; MISSING means no destination; INTENTIONALLY REPLACED means a documented
mechanism/owner replacement. Compression alone is not a reason to classify PARTIAL.

74 PASS; 0 PARTIAL; 0 MISSING; 2 INTENTIONALLY REPLACED (76 grouped rows).

| Area | Original lines | Requirement | Result | Current destination |
|---|---|---|---|---|
| Initial analysis | 3–13, 63 | Complete reading, one ordered setup, no product work | PASS | procedure: scope, analyze once, completion |
| Initial analysis | 67–70, 79 | Project, languages, frameworks, entry points and package managers | PASS | procedure: analyze once |
| Initial analysis | 69 | Major libraries/dependencies, not every dependency | PASS | procedure: analyze once |
| Initial analysis | 71–78 | Systems, owners, flows and development/validation commands | PASS | procedure: analyze once and hierarchy |
| Initial analysis | 80–98 | Output, agent configs, docs, CI/build configs, workflows and hotspots | PASS | procedure: analyze once |
| Initial analysis | 100–113 | Preserve/consolidate existing useful information | PASS | procedure: preservation and final verification |
| Initial analysis | 104–111 | Model, reasoning, provider, auth, credentials and global-settings protection | PASS | procedure: scope; context / protected-agent-settings |
| AGENTS hierarchy | 119–133 | Concise durable canonical root map and stack overview | PASS | procedure: smallest useful hierarchy |
| AGENTS hierarchy | 137–195 | Important systems, owners and meaningful dependency/data flows; no copied code or exhaustive inventories | PASS | procedure: smallest useful hierarchy |
| AGENTS hierarchy | 199–211 | Verified run/build/lint/format/type-check commands; uncertain commands labelled | PASS | procedure: analyze once and hierarchy; verification |
| AGENTS hierarchy | 203–204 | Both targeted and full commands when available | PASS | procedure: analyze once; verification / targeted-affected-full |
| AGENTS hierarchy | 215–230 | Justified, specialized nested maps without parent duplication | PASS | procedure: smallest useful hierarchy and verification |
| Navigation | 238, 240–243, 251–252 | Map → smallest owner → search → relevant dependencies/tests → verification → meaningful maintenance | PASS | navigation; verification; maintenance |
| Navigation | 239 | No rediscovery of documented architecture | PASS | navigation / no-rediscovery |
| Navigation | 244 | No ordinary whole-repository scan without evidence | PASS | navigation / no-ordinary-scan, evidence-expansion |
| Navigation | 245 | No unjustified rereading of understood files | PASS | navigation / no-unjustified-reread |
| Navigation | 246 | Extend responsible existing behavior rather than parallel implementations | PASS | ownership; implementation / reuse-project, reuse-minimum-new-code |
| Navigation | 247 | Preserve architecture unless the task requires change | PASS | navigation / preserve-architecture |
| Navigation | 248–249 | Selective document reading; ordinary output exclusions with task exceptions | PASS | context |
| Navigation | 250 | Version-control state before broad changes | PASS | navigation / repository-state |
| Ownership / locality | 260–271 | Clear cohesive owners; related together, unrelated separate; unique state/behavior ownership | PASS | ownership |
| Ownership / locality | 273–280 | Owner/locality/unrelated-responsibility/extraction decision; genuine new modules | PASS | ownership / owner-locality-unrelated-extraction, genuine-new-module |
| Ownership / locality | 284–297 | No arbitrary size limits; cohesive large files; split by responsibility | PASS | structure |
| Ownership / locality | 288–295 | All original refactoring signals, including improved locality | PASS | structure; ownership / owner-locality-unrelated-extraction |
| Ownership / locality | 299–306 | No tiny-file fragmentation, forwarding wrappers or unnecessary layers | PASS | structure / no-fragmentation-wrappers; implementation / no-speculation |
| Ownership / locality | 310–312 | Simple dependency direction and no cycles | PASS | interfaces / simple-direction-no-cycles-globals |
| Ownership / locality | 313–315, 320 | No hidden global coupling; focused public interfaces; local internals and independent callers | PASS | interfaces |
| Ownership / locality | 316 | Separate genuinely distinct UI/domain/persistence/transport/infrastructure | PASS | interfaces / distinct-boundaries |
| Ownership / locality | 317–318 | Indirection justified by coupling reduction, not purity | PASS | interfaces / coupling-justifies-indirection |
| Ownership / locality | 324–330 | Coherent functions/classes, meaningful extraction, shallow readable code, focused APIs, specific helpers | PASS | implementation / readable-coherent-shallow, specific-helper-owner; interfaces |
| Ownership / locality | 334–346 | Owner + dependencies + verification; locality signals do not authorize automatic refactors | PASS | navigation; ownership; structure / refactor-current-need |
| Claude | 352–362 | Canonical shared map and same-directory lightweight import | PASS | procedure: Claude reuse; context / shared-claude-knowledge |
| Claude | 364–381 | Preserve knowledge, optional reference, wrapper replacement and link | PASS | procedure: Claude reuse |
| Claude | 362, 664 | No duplicate instruction sets; imports resolve | PASS | procedure: Claude reuse and verification |
| Large documentation | 387–401 | Identify/preserve large references; no mandatory full startup reading | PASS | procedure: optional context; context / large-documents-optional-search |
| Large documentation | 403–409 | Purpose map and topic-search/selective-section reading | PASS | procedure: optional context; context |
| Exclusions | 411–437 | Actual generated/cache/build/vendor inventory; proven minimal local exclusions | PASS | procedure: analyze once and optional context; context |
| Exclusions | 439–449 | Preserve useful source, tests, fixtures, migrations, docs, assets and archives | PASS | context / preserve-useful-material |
| Implementation | 455 | Smallest correct solution | PASS | procedure: normal workflow; implementation / reuse-minimum-new-code |
| Implementation | 457–464 | Original six-step ordered reuse ladder | PASS | implementation / first six ordered reuse facets |
| Implementation | 468–472 | Reuse, existing architecture, justified dependencies and no speculative layers | PASS | implementation; navigation / preserve-architecture |
| Implementation | 473 | Readable straightforward code rather than clever code | PASS | implementation / readable-coherent-shallow |
| Implementation | 474–476 | Focused diffs/files, no unrelated cleanup | PASS | implementation / focused-diff |
| Implementation | 477 | No stylistic rewriting of working systems | PASS | implementation / no-style-rewrite |
| Implementation | 478 | Safely remove newly obsolete code | PASS | implementation / safe-obsolete-removal |
| Implementation | 490–497 | Correctness/security/trust validation/data safety/accessibility/requested behavior | PASS | implementation / preserve-safety |
| Bug fixes | 482–484 | Root cause first; trace relevant flow and callers | PASS | bug-fix / root-cause-first, trace-flow-callers |
| Bug fixes | 485–487 | Responsible shared-layer fix, no duplicate workarounds or unnecessary broad refactor | PASS | bug-fix |
| Bug fixes | 488 | Practical useful runnable regression verification | PASS | bug-fix / practical-regression; verification / existing-infrastructure |
| Project Skills | 503–519 | Recurring workflow inventory; repetitive, non-trivial, reusable creation threshold | PASS | procedure: analyze once and optional context; project-skills |
| Project Skills | 521–549 | Persistent facts/rules in maps, reusable procedures in Skills; no simple-fact Skills | PASS | project-skills / maps-versus-procedures, repetitive-nontrivial-reusable |
| Project Skills | 529–543 | Canonical project locations and Claude exposure; distinct from plugin packaging | PASS | project-skills / canonical-project-discovery; procedure: optional context |
| Project Skills | 547, 665 | Portable sharing and verified relative symlink resolution/discovery | PASS | project-skills / portable-verified-sharing; procedure: verification |
| Lean Review | 555 | Optional creation if not covered by tooling | INTENTIONALLY REPLACED | packaged contextlean:lean-review; no redundant generic project copy |
| Lean Review | 557–566 | All original advisory complexity/locality review checks | PASS | packaged skills/lean-review/SKILL.md: review workflow |
| Lean Review | 568–577 | Advisory review and behavior/safety/readability/maintainability preservation | PASS | packaged skills/lean-review/SKILL.md: boundaries |
| Lean Review | 671, 706–708 | Explicit durable handoff rather than silent omission | PASS | lean-review / explicit-packaged-handoff; procedure: transfer gate |
| Verification | 583–599, 607 | Smallest meaningful checks; targeted/affected/full distinction and project rules | PASS | verification |
| Verification | 601 | Prefer existing testing infrastructure | PASS | verification / existing-infrastructure |
| Verification | 603 | Runnable regression coverage for non-trivial logic when practical | PASS | verification / runnable-regression |
| Verification | 605 | No framework solely for one small check without justification | PASS | verification / no-single-check-framework |
| Verification | 609 | Skill when verification is repetitive and complex | PASS | project-skills / repetitive-nontrivial-reusable |
| Map maintenance | 615 | Check map accuracy after every future task | PASS | maintenance / after-every-task |
| Map maintenance | 617–626, 628 | Smallest map; path, owner, subsystem, architecture, flow and command triggers | PASS | maintenance / paths-owners-subsystems-architecture-flows-commands-workflows |
| Map maintenance | 627 | New reusable-workflow documentation trigger | PASS | maintenance / paths-owners-subsystems-architecture-flows-commands-workflows |
| Map maintenance | 630–637 | No churn for ordinary details/content/tuning/UI or ownership-preserving refactors | PASS | maintenance / no-detail-churn |
| Map maintenance | 639–650 | Stale/duplicate removal; concise durable non-obvious guidance; optional depth; no needless global refresh | PASS | maintenance |
| Bootstrap verification | 658–669 | Paths/owners/commands/preservation/no behavior change/hierarchy/imports/references/exclusions/concision | PASS | procedure: verify before finishing |
| Bootstrap verification | 670 | Preserve useful existing workflows | PASS | procedure: preservation, sharing and verification |
| Bootstrap verification | 665 | Explicit portable symlink verification | PASS | procedure: optional context and verification |
| Bootstrap verification | 671 | Review every permanent-rule transfer before completion | PASS | procedure: permanent-rule transfer and safe-removal gate; scripts/verify_transfer.py |
| Bootstrap verification | 673 | Remove redundant/speculative guidance without product refactors | PASS | procedure: verify before finishing |
| Lifecycle | 679–690 | Eight completion categories, no product work | PASS | procedure: completion report |
| Lifecycle | 692–704 | Future maps/wrappers/Skills/config/targeted references; no startup setup dependency | PASS | procedure: transfer gate and report boundaries |
| Lifecycle | 692–704 | Reusable setup specification location | INTENTIONALLY REPLACED | installed plugin optional reference, not required target-project startup copy |
| Lifecycle | 706–714 | No rule only in setup; deletion loses no behavior; otherwise reject completion | PASS | procedure: transfer gate; removal/negative contract tests |

## Repair verification

The following records the semantic repair before its GitHub release gate. Commit,
push, remote CI and clean-clone results belong to the subsequent release-gate report.

Offline verification on 2026-09-30: **80 tests passed**, including **22 new semantic
and transfer contracts** (eight permanent-behavior contracts and fourteen gate tests).
Ruff 0.15.7 lint and formatting passed. All four official Skill validations, Codex
package validation and Claude manifest/catalog validations passed. The existing
Claude wrapper warning remains expected. Normal Quality CI still runs only lint,
formatting, offline tests and whitespace checks; no model runs were added.

A fresh filesystem snapshot of this uncommitted candidate was installed using empty
temporary Codex/Claude configurations. All installed Skill files matched the candidate.
Codex discovery returned the four enabled qualified ContextLean Skills without errors;
Claude's local plugin inspection listed all four. Codex also discovered a disposable
project Skill at the canonical location. Its relative Claude symlink resolved and
survived relocation. Interactive Claude project-Skill menu inspection stopped on
`api.anthropic.com: ENOTFOUND` before a model turn, so that particular discovery check
is **unverified**, not a claimed pass. The procedure requires actual discovery before
declaring completion when shared project Skills are created.

The disposable expense project passed its five existing tests, the documented targeted
test command and its CLI example. Its lightweight Claude import resolved. The installed
read-only transfer checker passed with all 11 groups / 71 facets before and after removal
of the disposable setup file; negative contracts reject incomplete, changed, unreviewed,
unreachable or setup-only destinations. Static baseline/finish reporting also passed.
This smoke test applies the reviewed guidance deterministically; it is not an independent
live-model execution of the bootstrap workflow.

### Context size

These are exact UTF-8 byte/line counts. Token figures are **bytes ÷ 4 estimates**, not
tokenizer measurements or a measured session total; global instructions, discovery
descriptions and other session overhead are outside the comparison.

| Material | Lines | Bytes | Estimated tokens |
|---|---:|---:|---:|
| Canonical procedure before repair | 193 | 8,411 | 2,103 |
| Canonical procedure after repair | 239 | 12,189 | 3,047 |
| New permanent-rule inventory, setup-only | 153 | 9,404 | 2,351 |
| Mandatory procedure + inventory during explicit bootstrap | 392 | 21,593 | 5,398 |
| Original owner specification | 714 | 19,277 | 4,819 |
| Worked generated AGENTS.md | 56 | 6,478 | 1,620 |
| Lightweight Claude wrapper | 1 | 11 | 3 |
| Earlier incomplete expense benchmark fixture AGENTS.md, unchanged | 21 | 932 | 233 |
| ContextLean's own root map before / after | 70 / 73 | 5,592 / 5,903 | 1,398 / 1,476 |

The worked permanent map is about **66% smaller in bytes** than loading the original
setup specification. Claude reuses that map through an 11-byte import; it does not
maintain a second instruction set. The richer worked map is materially larger than
the earlier incomplete fixture (about 1,387 additional estimated tokens), and explicit
one-time bootstrap reading also grows materially: the mandatory procedure plus inventory
is about 12% larger in bytes than the original specification. This is not a startup
saving for setup itself. Neither setup document, transfer receipt nor detailed comparison
is required by later development sessions. ContextLean's own automatic root guidance
grew by only 311 bytes, about 78 estimated tokens. No live benchmark gain is inferred.

### ContextLean dogfood

Audit Context Locality: **7 PASS / 2 WARNING / 0 ACTION NEEDED**.

| Check | Result | Evidence / smallest next action |
|---|---|---|
| Map, ownership, paths and commands | PASS | Root map covers the new bootstrap-owned inventory, checker and contracts; offline commands pass. |
| Instruction duplication | PASS | One canonical permanent-rule inventory; example guidance is an explicit test fixture, not a second live rule owner; no new generic review Skill. |
| Startup context and optional depth | WARNING | Size growth versus incomplete guidance is material and disclosed above; retain targeted optional references and assess size on real projects. No file split is requested. |
| Claude wrappers | PASS | Root/example imports resolve to canonical AGENTS.md; no copied live Claude instruction set. |
| Skills and portable sharing | WARNING | Four packaged Skills validate/discover; portable project sharing resolves. Claude's interactive project discovery needs a later connectivity-enabled local menu check, without a model turn. |
| Exclusions | PASS | Existing local exclusions keep receipts/caches out of Git; no source or public evidence was newly excluded. |
| Documentation freshness | PASS | Historical release verification is labelled historical; repaired coverage and measured limits have their own developer record. |
| Transfer and safe removal | PASS | Manual facet comparison plus complete/hash-bound durable destinations; positive removal and negative gate tests pass. Structural evidence does not claim NLP proof. |
| Architectural locality | PASS | Bootstrap owns transfer verification; Audit inspects drift; Lean Review owns advisory change review; no runtime dependency, hook or background process. |

Lean Change Review: **no material findings**. The standard-library checker belongs to
bootstrap and performs one explicit read-only verification responsibility. Stable facets
support focused failure tests; prose is not stored as a giant snapshot. The fixture and
its reviewed hashes exercise the same installed checker. No forwarding layer, speculative
extension mechanism, runtime dependency or unrelated product refactor was introduced.
Live model compliance and Claude's interactive project discovery remain the stated
verification limits.

The existing ten-run validation evidence remains byte-for-byte unchanged (47 published
evidence files, including the results index). No additional paid/live benchmark calls
or model turns were submitted. The repair changes 13 public files (six modified, seven
new); local verification logs remain ignored. No commit, push, tag or release was made.
Previous remote CI concerns the earlier committed revision, not these uncommitted repairs.

Changed public files:

- Bootstrap: [entry point](../skills/bootstrap/SKILL.md),
  [procedure](../skills/bootstrap/references/bootstrap-spec.md),
  [permanent rules](../skills/bootstrap/references/permanent-rules.json),
  [transfer checker](../skills/bootstrap/scripts/verify_transfer.py).
- Audit: [Skill](../skills/audit/SKILL.md).
- Guidance/documentation: [repository map](../AGENTS.md), [README](../README.md),
  [historical verification note](verification.md), this coverage report.
- Contracts/fixtures: [semantic tests](../tests/test_bootstrap_transfer.py),
  [example AGENTS.md](../tests/fixtures/bootstrap-transfer/AGENTS.md),
  [Claude wrapper](../tests/fixtures/bootstrap-transfer/CLAUDE.md),
  [reviewed transfer record](../tests/fixtures/bootstrap-transfer/transfer.json).

The semantic acceptance criterion passes: ignoring/deleting the original target setup
specification loses no required permanent behavior in the reviewed durable guidance.
The two intentional replacements change the owner/location of optional review and setup,
not the behavior required for ordinary development.
