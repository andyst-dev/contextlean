# Balanced migration review — 2026-10-05

Historical semantic comparison for the v0.3.0 transition. The [current contract](../balanced-contract.md) owns maintained behavior. This intentional product simplification is distinguished from a semantic regression below.

## Historical comparison

The [original bootstrap](../reference/original-agent-bootstrap.md) and
[old coverage matrix](bootstrap-coverage.md) remain historical evidence. Previous
benchmarks describe their frozen products, not Balanced. Their evidence is unchanged;
the separate [Balanced product-change validation](../../benchmarks/results/2026-10-06-balanced-product-change/README.md)
checks the tested Refactor behavior, not general performance or complex-refactor equivalence.

The comparison is **55 legacy-equivalent PASS / 13 intentionally RE-SCOPED /
6 intentionally RETIRED / 2 previously REPLACED**. PASS means equivalent behavior
still has a home in the selected product, not that every row is runtime guidance.
Re-scoped rows retain only the stated narrower/optional promise. Retired rows are not
PASS. This is reviewed semantic analysis, not an automated proof of prose or model behavior.

The historical facet comparison is 55 runtime facets (including eight consolidations),
six optional review facets, five authoring-documentation facets, two bootstrap facets
and three retired universal requirements. These are migration counts, not a new
mandatory ledger. Known-invalidation correction replaces the retired map cadence and
full maintenance enumeration. Losses include unconditional map checks, workflow
cultivation, portable-Skill setup certification and universal historical compatibility.

## Historical rule consolidation

Eight meanings share simpler rules: cohesive files/modules/classes and specific helper
ownership share cohesive ownership; cohesive large files share responsibility-based
sizing; bug regression shares practical regression; smallest meaningful checks share
proportional coverage; test frameworks share justified-current-need requirements;
map churn/global refresh restraints share invalidation-driven, focused correction.

## Original grouped requirements

Rows follow the historical matrix order; original line references identify the archived specification.

| Row | Original area / lines | Historical requirement | Balanced status | Disposition and consequence |
|---|---|---|---|---|
| 1 | Initial analysis / 3–13, 63 | Complete reading, one ordered setup, no product work | RE-SCOPED | Relevant setup instructions replace historical reading choreography; no-product-work boundary remains. |
| 2 | Initial analysis / 67–70, 79 | Project, languages, frameworks, entry points and package managers | PASS | Bootstrap inspection, preservation and scope checks. |
| 3 | Initial analysis / 69 | Major libraries/dependencies, not every dependency | PASS | Bootstrap inspection, preservation and scope checks. |
| 4 | Initial analysis / 71–78 | Systems, owners, flows and development/validation commands | PASS | Bootstrap inspection, preservation and scope checks. |
| 5 | Initial analysis / 80–98 | Output, agent configs, docs, CI/build configs, workflows and hotspots | RE-SCOPED | Relevant structure/configuration inspection replaces broad workflow/hotspot inventory; preserve existing knowledge. |
| 6 | Initial analysis / 100–113 | Preserve/consolidate existing useful information | PASS | Bootstrap inspection, preservation and scope checks. |
| 7 | Initial analysis / 104–111 | Model, reasoning, provider, auth, credentials and global-settings protection | PASS | Bootstrap inspection, preservation and scope checks. |
| 8 | AGENTS hierarchy / 119–133 | Concise durable canonical root map and stack overview | PASS | Bootstrap map/command validation and minimal hierarchy. |
| 9 | AGENTS hierarchy / 137–195 | Important systems, owners and meaningful dependency/data flows; no copied code or exhaustive inventories | PASS | Bootstrap map/command validation and minimal hierarchy. |
| 10 | AGENTS hierarchy / 199–211 | Verified run/build/lint/format/type-check commands; uncertain commands labelled | PASS | Bootstrap map/command validation and minimal hierarchy. |
| 11 | AGENTS hierarchy / 203–204 | Both targeted and full commands when available | PASS | Bootstrap map/command validation and minimal hierarchy. |
| 12 | AGENTS hierarchy / 215–230 | Justified, specialized nested maps without parent duplication | PASS | Bootstrap map/command validation and minimal hierarchy. |
| 13 | Navigation / 238, 240–243, 251–252 | Map → smallest owner → search → relevant dependencies/tests → verification → meaningful maintenance | PASS | Ordinary core navigation and focused exploration. |
| 14 | Navigation / 239 | No rediscovery of documented architecture | PASS | Ordinary core navigation and focused exploration. |
| 15 | Navigation / 244 | No ordinary whole-repository scan without evidence | PASS | Ordinary core navigation and focused exploration. |
| 16 | Navigation / 245 | No unjustified rereading of understood files | PASS | Ordinary core navigation and focused exploration. |
| 17 | Navigation / 246 | Extend responsible existing behavior rather than parallel implementations | PASS | Ordinary core navigation and focused exploration. |
| 18 | Navigation / 247 | Preserve architecture unless the task requires change | PASS | Ordinary core navigation and focused exploration. |
| 19 | Navigation / 248–249 | Selective document reading; ordinary output exclusions with task exceptions | PASS | Ordinary core navigation and focused exploration. |
| 20 | Navigation / 250 | Version-control state before broad changes | PASS | Ordinary core navigation and focused exploration. |
| 21 | Ownership / locality / 260–271 | Clear cohesive owners; related together, unrelated separate; unique state/behavior ownership | PASS | Ordinary core ownership, interfaces and restrained structure. |
| 22 | Ownership / locality / 273–280 | Owner/locality/unrelated-responsibility/extraction decision; genuine new modules | RE-SCOPED | Core ownership remains automatic; extraction decision questions move to optional Lean Review. |
| 23 | Ownership / locality / 284–297 | No arbitrary size limits; cohesive large files; split by responsibility | PASS | Ordinary core ownership, interfaces and restrained structure. |
| 24 | Ownership / locality / 288–295 | All original refactoring signals, including improved locality | RE-SCOPED | Full refactor signal catalogue moves to optional review; automatic current-task threshold remains. |
| 25 | Ownership / locality / 299–306 | No tiny-file fragmentation, forwarding wrappers or unnecessary layers | PASS | Ordinary core ownership, interfaces and restrained structure. |
| 26 | Ownership / locality / 310–312 | Simple dependency direction and no cycles | PASS | Ordinary core ownership, interfaces and restrained structure. |
| 27 | Ownership / locality / 313–315, 320 | No hidden global coupling; focused public interfaces; local internals and independent callers | PASS | Ordinary core ownership, interfaces and restrained structure. |
| 28 | Ownership / locality / 316 | Separate genuinely distinct UI/domain/persistence/transport/infrastructure | RE-SCOPED | Named architectural layer examples become optional review advice; cohesive boundaries stay core. |
| 29 | Ownership / locality / 317–318 | Indirection justified by coupling reduction, not purity | RE-SCOPED | Coupling-specific indirection criteria become optional; justified current need stays core. |
| 30 | Ownership / locality / 324–330 | Coherent functions/classes, meaningful extraction, shallow readable code, focused APIs, specific helpers | PASS | Ordinary core ownership, interfaces and restrained structure. |
| 31 | Ownership / locality / 334–346 | Owner + dependencies + verification; locality signals do not authorize automatic refactors | PASS | Ordinary core ownership, interfaces and restrained structure. |
| 32 | Claude / 352–362 | Canonical shared map and same-directory lightweight import | PASS | Bootstrap-only compatible imports and knowledge preservation. |
| 33 | Claude / 364–381 | Preserve knowledge, optional reference, wrapper replacement and link | PASS | Bootstrap-only compatible imports and knowledge preservation. |
| 34 | Claude / 362, 664 | No duplicate instruction sets; imports resolve | PASS | Bootstrap-only compatible imports and knowledge preservation. |
| 35 | Large documentation / 387–401 | Identify/preserve large references; no mandatory full startup reading | PASS | Core selective reading and bootstrap preservation. |
| 36 | Large documentation / 403–409 | Purpose map and topic-search/selective-section reading | PASS | Core selective reading and bootstrap preservation. |
| 37 | Exclusions / 411–437 | Actual generated/cache/build/vendor inventory; proven minimal local exclusions | PASS | Bootstrap validates exclusion changes; runtime preserves useful material and task exceptions. |
| 38 | Exclusions / 439–449 | Preserve useful source, tests, fixtures, migrations, docs, assets and archives | PASS | Bootstrap validates exclusion changes; runtime preserves useful material and task exceptions. |
| 39 | Implementation / 455 | Smallest correct solution | PASS | Ordinary core reuse, scope and safety. |
| 40 | Implementation / 457–464 | Original six-step ordered reuse ladder | PASS | Ordinary core reuse, scope and safety. |
| 41 | Implementation / 468–472 | Reuse, existing architecture, justified dependencies and no speculative layers | PASS | Ordinary core reuse, scope and safety. |
| 42 | Implementation / 473 | Readable straightforward code rather than clever code | PASS | Ordinary core reuse, scope and safety. |
| 43 | Implementation / 474–476 | Focused diffs/files, no unrelated cleanup | PASS | Ordinary core reuse, scope and safety. |
| 44 | Implementation / 477 | No stylistic rewriting of working systems | PASS | Ordinary core reuse, scope and safety. |
| 45 | Implementation / 478 | Safely remove newly obsolete code | PASS | Ordinary core reuse, scope and safety. |
| 46 | Implementation / 490–497 | Correctness/security/trust validation/data safety/accessibility/requested behavior | PASS | Ordinary core reuse, scope and safety. |
| 47 | Bug fixes / 482–484 | Root cause first; trace relevant flow and callers | PASS | Ordinary core root-cause and regression discipline. |
| 48 | Bug fixes / 485–487 | Responsible shared-layer fix, no duplicate workarounds or unnecessary broad refactor | PASS | Ordinary core root-cause and regression discipline. |
| 49 | Bug fixes / 488 | Practical useful runnable regression verification | PASS | Ordinary core root-cause and regression discipline. |
| 50 | Project Skills / 503–519 | Recurring workflow inventory; repetitive, non-trivial, reusable creation threshold | RE-SCOPED | No default workflow inventory or Skill creation; retain threshold in optional authoring documentation. |
| 51 | Project Skills / 521–549 | Persistent facts/rules in maps, reusable procedures in Skills; no simple-fact Skills | RE-SCOPED | Maps-versus-procedures guidance becomes optional authoring documentation. |
| 52 | Project Skills / 529–543 | Canonical project locations and Claude exposure; distinct from plugin packaging | RE-SCOPED | Project discovery locations become an optional authoring recipe; plugin packaging is unchanged. |
| 53 | Project Skills / 547, 665 | Portable sharing and verified relative symlink resolution/discovery | RE-SCOPED | Portable sharing/discovery remains an optional recipe, not a bootstrap deliverable. |
| 54 | Lean Review / 555 | Optional creation if not covered by tooling | REPLACED | Optional packaged review replaces generic project review-Skill creation; no mandatory root handoff. |
| 55 | Lean Review / 557–566 | All original advisory complexity/locality review checks | PASS | Explicitly requested packaged review retains standalone safeguards. |
| 56 | Lean Review / 568–577 | Advisory review and behavior/safety/readability/maintainability preservation | PASS | Explicitly requested packaged review retains standalone safeguards. |
| 57 | Lean Review / 671, 706–708 | Explicit durable handoff rather than silent omission | RETIRED | No mandatory qualified runtime handoff. Lean Review remains available on explicit request. |
| 58 | Verification / 583–599, 607 | Smallest meaningful checks; targeted/affected/full distinction and project rules | PASS | Ordinary core proportional coverage and practical regression checks. |
| 59 | Verification / 601 | Prefer existing testing infrastructure | PASS | Ordinary core proportional coverage and practical regression checks. |
| 60 | Verification / 603 | Runnable regression coverage for non-trivial logic when practical | PASS | Ordinary core proportional coverage and practical regression checks. |
| 61 | Verification / 605 | No framework solely for one small check without justification | PASS | Ordinary core proportional coverage and practical regression checks. |
| 62 | Verification / 609 | Skill when verification is repetitive and complex | RETIRED | No standing verification-Skill suggestion. Workflow authoring can be requested separately. |
| 63 | Map maintenance / 615 | Check map accuracy after every future task | RETIRED | No after-every-task cadence. Correct known invalidation/staleness; unrelated drift may wait for Audit. |
| 64 | Map maintenance / 617–626, 628 | Smallest map; path, owner, subsystem, architecture, flow and command triggers | PASS | Invalidation-driven smallest-map corrections and focused scope. |
| 65 | Map maintenance / 627 | New reusable-workflow documentation trigger | RETIRED | No standing reusable-workflow documentation trigger. Changed mapped commands/constraints still get corrected. |
| 66 | Map maintenance / 630–637 | No churn for ordinary details/content/tuning/UI or ownership-preserving refactors | PASS | Invalidation-driven smallest-map corrections and focused scope. |
| 67 | Map maintenance / 639–650 | Stale/duplicate removal; concise durable non-obvious guidance; optional depth; no needless global refresh | RE-SCOPED | Local corrections and focused scope stay core; detailed editorial standards move to authoring documentation. |
| 68 | Bootstrap verification / 658–669 | Paths/owners/commands/preservation/no behavior change/hierarchy/imports/references/exclusions/concision | PASS | Concrete setup checks without historical-completeness prerequisites. |
| 69 | Bootstrap verification / 670 | Preserve useful existing workflows | PASS | Concrete setup checks without historical-completeness prerequisites. |
| 70 | Bootstrap verification / 665 | Explicit portable symlink verification | RETIRED | No default project-Skill portability certification. Preserve existing sharing and validate links actually changed. |
| 71 | Bootstrap verification / 671 | Review every permanent-rule transfer before completion | RETIRED | No historical facet/hash transfer gate. Validate concrete outputs and selected coding safeguards. |
| 72 | Bootstrap verification / 673 | Remove redundant/speculative guidance without product refactors | PASS | Concrete setup checks without historical-completeness prerequisites. |
| 73 | Lifecycle / 679–690 | Eight completion categories, no product work | RE-SCOPED | Report actual changes, checks and limits without eight fixed categories; no product work remains allowed. |
| 74 | Lifecycle / 692–704 | Future maps/wrappers/Skills/config/targeted references; no startup setup dependency | PASS | Generated core remains independent of setup and plugin availability. |
| 75 | Lifecycle / 692–704 | Reusable setup specification location | REPLACED | Reusable setup stays in the installed plugin, not target-project startup context. |
| 76 | Lifecycle / 706–714 | No rule only in setup; deletion loses no behavior; otherwise reject completion | RE-SCOPED | Core works without setup documents; retire certification that every historical behavior survives deletion. |
