"""Offline transfer contracts: durable scope, review integrity and removable setup."""

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

from bootstrap_fixture import generate


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "contextlean_transfer", ROOT / "skills/bootstrap/scripts/verify_transfer.py"
)
transfer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(transfer)
FIXTURE = ROOT / "tests/fixtures/bootstrap-transfer"
GROUPS = {g["id"]: g for g in json.loads(transfer.RULES.read_text())["groups"]}


class PermanentBehaviorContracts(unittest.TestCase):
    def guidance_sources(self, group):
        """Check setup semantics and their actual automatic destination."""
        return (
            GROUPS[group]["guidance"],
            transfer.section_text(FIXTURE / "AGENTS.md", GROUPS[group]["heading"]),
        )

    def architecture_sources(self):
        return (
            GROUPS["structure"]["reference"]["guidance"],
            transfer.section_text(FIXTURE / "PROJECT_REFERENCE.md", "Architecture decisions"),
        )

    def test_generated_guidance_matches_reviewed_inventory(self):
        # Destinations must communicate the canonical rules, not just name facets.
        for group in GROUPS.values():
            with self.subTest(group=group["id"]):
                automatic = transfer.section_text(FIXTURE / "AGENTS.md", group["heading"])
                self.assertEqual(automatic.strip(), group["guidance"])
                if "reference" in group:
                    reference = group["reference"]
                    self.assertIn(
                        reference["guidance"],
                        transfer.section_text(
                            FIXTURE / "PROJECT_REFERENCE.md", reference["heading"]
                        ),
                    )

    def test_mapped_ownership_is_trusted_subject_to_source(self):
        for text in self.guidance_sources("navigation"):
            with self.subTest(source=text):
                self.assertRegex(
                    text, r"trust mapped ownership/architecture.*unless source contradicts"
                )
                self.assertRegex(text, r"smallest owner.*search before broad reads")
                self.assertRegex(text, r"[Ss]kip broad ownership/architecture reconfirmation")

    def test_expansion_remains_evidence_driven(self):
        for text in self.guidance_sources("navigation"):
            self.assertRegex(text, r"[Ee]xpand only with evidence")
        for text in self.architecture_sources():
            # Distinct risk signals must survive compression of automatic context.
            for signal in (
                "ownership is ambiguous",
                "map is stale",
                "contradicted by source",
                "usages cross boundaries",
                "public interfaces change",
                "shared/core behavior",
                "tests expose wider impact",
                "dependency flow",
                "other concrete evidence",
                "Source evidence overrides the map",
            ):
                with self.subTest(signal=signal):
                    self.assertIn(signal, text)

    def test_search_reuse_does_not_ban_distinct_questions(self):
        for text in self.guidance_sources("navigation"):
            self.assertRegex(text, r"[Ss]kip.*equivalent answered searches")
        for text in self.architecture_sources():
            self.assertRegex(text, r"Multiple searches.*different unresolved questions")
            self.assertRegex(text, r"Known references.*no global search")

    def test_explicit_refactor_is_scoped_and_behavior_preserving(self):
        for text in self.guidance_sources("structure"):
            self.assertRegex(text, r"explicit request.*preserve behavior")
            self.assertRegex(text, r"assess relevant boundaries")
        for text in self.architecture_sources():
            self.assertRegex(text, r"Review only architecture boundaries relevant to the change")
            self.assertRegex(text, r"signals do not require.*repository-wide architecture audit")
            for safeguard in ("ownership/locality", "interface stability", "dependency direction"):
                self.assertIn(safeguard, text)
            self.assertRegex(text, r"smallest behavior-preserving structural change")

    def test_refactor_route_allows_unnecessary_steps_to_be_skipped(self):
        for text in self.architecture_sources():
            self.assertRegex(text, r"mapped owner.*code being changed")
            self.assertRegex(text, r"callers/usages and affected tests as needed")
            self.assertRegex(text, r"not a fixed checklist.*skip unnecessary steps")
            self.assertRegex(text, r"private implementation change.*cannot affect callers")
        for text in self.guidance_sources("ownership"):
            self.assertRegex(text, r"If .*refactor scope is unclear, read.*PROJECT_REFERENCE")
        automatic = transfer.automatic_guidance(FIXTURE)
        self.assertNotIn((FIXTURE / "PROJECT_REFERENCE.md").resolve(), automatic)

    def test_repository_state_requires_relevance_and_availability(self):
        for text in self.guidance_sources("navigation"):
            self.assertRegex(text, r"broad/state-sensitive.*available version-control state")
            self.assertRegex(text, r"inspect.*state only if relevant")
            self.assertRegex(text, r"no routine Git checks")
        procedure = (ROOT / "skills/bootstrap/references/bootstrap-spec.md").read_text()
        # This is future permanent guidance routing, not the one-time setup inspection.
        routing = procedure.split("Transfer all 71", 1)[1].split("## 4.", 1)[0]
        for state in (
            "uncommitted work",
            "generated state",
            "branching",
            "conflicts",
            "broad edits",
        ):
            self.assertIn(state, routing)
        self.assertRegex(routing, r"read-only navigation and small local edits alone require")
        self.assertRegex(routing, r"neither Git inspection nor a preliminary availability command")
        self.assertRegex(routing, r"proceed when state is irrelevant")

    def test_refactor_verification_preserves_proportional_scope(self):
        for text in self.guidance_sources("verification"):
            self.assertRegex(text, r"smallest meaningful check.*targeted first")
            self.assertRegex(text, r"broaden for shared/core/public")
            self.assertRegex(text, r"full suite only when necessary/project-required")
            self.assertRegex(text, r"[Ss]cope choices.*not mandatory sequential steps")
            self.assertRegex(text, r"existing infrastructure.*runnable regression")
        for text in self.architecture_sources():
            self.assertRegex(text, r"behavior-preserving.*verify proportionally")

    def test_automatic_context_stays_within_compact_baseline(self):
        automatic = transfer.automatic_guidance(FIXTURE)
        self.assertEqual({path.name for path in automatic}, {"AGENTS.md", "CLAUDE.md"})
        self.assertLessEqual(sum(len(path.read_bytes()) for path in automatic), 5489)
        self.assertLessEqual(len((FIXTURE / "AGENTS.md").read_text().splitlines()), 68)

    def test_navigation_contract(self):
        self.assertEqual(
            set(GROUPS["navigation"]["facets"]),
            {
                "map-primary",
                "no-rediscovery",
                "owner-first",
                "search-first",
                "immediate-dependencies",
                "evidence-expansion",
                "no-ordinary-scan",
                "no-unjustified-reread",
                "repository-state",
                "preserve-architecture",
            },
        )

    def test_architecture_decisions_and_interfaces(self):
        for group, required in {
            "ownership": {
                "clear-owner",
                "cohesive-files-modules-classes",
                "related-together",
                "unrelated-separated",
                "unique-state-behavior",
                "owner-locality-unrelated-extraction",
                "genuine-new-module",
            },
            "interfaces": {
                "simple-direction-no-cycles-globals",
                "focused-public-api",
                "local-internals",
                "distinct-boundaries",
                "coupling-justifies-indirection",
            },
            "structure": {
                "no-arbitrary-size",
                "cohesive-large-files",
                "refactor-signals",
                "refactor-current-need",
                "no-fragmentation-wrappers",
            },
        }.items():
            with self.subTest(group=group):
                self.assertEqual(set(GROUPS[group]["facets"]), required)

    def test_ordered_reuse_contract(self):
        self.assertEqual(
            GROUPS["implementation"]["facets"][:6],
            [
                "reuse-supported",
                "reuse-project",
                "reuse-standard-library",
                "reuse-framework-platform",
                "reuse-installed-dependency",
                "reuse-minimum-new-code",
            ],
        )

    def test_bug_fix_root_cause_and_regression_contract(self):
        self.assertEqual(
            set(GROUPS["bug-fix"]["facets"]),
            {
                "root-cause-first",
                "trace-flow-callers",
                "responsible-shared-layer",
                "no-repeated-workaround",
                "no-unnecessary-broad-refactor",
                "practical-regression",
            },
        )

    def test_verification_scope_and_infrastructure(self):
        self.assertEqual(
            set(GROUPS["verification"]["facets"]),
            {
                "targeted-affected-full",
                "smallest-meaningful",
                "broaden-shared-core-or-rules",
                "existing-infrastructure",
                "runnable-regression",
                "no-single-check-framework",
            },
        )

    def test_after_task_map_maintenance(self):
        self.assertEqual(
            set(GROUPS["maintenance"]["facets"]),
            {
                "after-every-task",
                "paths-owners-subsystems-architecture-flows-commands-workflows",
                "smallest-map-stale-removal",
                "no-detail-churn",
                "durable-concise-not-obvious",
                "no-global-refresh",
            },
        )

    def test_lean_review_is_delegated_not_recreated(self):
        item = json.loads((FIXTURE / "transfer.json").read_text())["rules"]["lean-review"][
            "destinations"
        ][0]
        self.assertEqual(
            (item["kind"], item["skill"]), ("contextlean_skill", "contextlean:lean-review")
        )
        self.assertFalse((FIXTURE / ".agents/skills/lean-review").exists())

    def test_model_reasoning_provider_and_credentials_are_protected(self):
        self.assertIn("protected-agent-settings", GROUPS["context"]["facets"])
        # Setting names are semantic concepts, not an exact prose snapshot.
        for text in [
            GROUPS["context"]["guidance"],
            (ROOT / "skills/bootstrap/references/bootstrap-spec.md").read_text(),
        ]:
            for setting in [
                "model",
                "reasoning",
                "provider",
                "authentication",
                "credentials",
                "user-global",
            ]:
                with self.subTest(setting=setting):
                    self.assertIn(setting, text)


class TransferGateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name) / "repo"
        shutil.copytree(FIXTURE, self.repo)
        self.record = json.loads((self.repo / "transfer.json").read_text())

    def destination(self, group):
        return self.record["rules"][group]["destinations"][0]

    def test_inventory_classifies_all_71_stable_facets(self):
        # Freeze identifiers/order, not prose; independent of Git availability.
        original = "f893e2913cc0888538c59b373a99732e02502fbbfac124e0c84d90d2784f7c0d"
        self.assertEqual(
            hashlib.sha256(
                json.dumps({g["id"]: g["facets"] for g in GROUPS.values()}, sort_keys=True).encode()
            ).hexdigest(),
            original,
        )
        self.assertEqual(sum(len(g["facets"]) for g in GROUPS.values()), 71)
        for group in GROUPS.values():
            self.assertEqual(set(group["delivery"]), set(group["facets"]))
            self.assertTrue(set(group["delivery"].values()) <= set("ABCDE"))

    def test_historical_semantic_matrix_retains_acceptance(self):
        import collections

        matrix = (ROOT / "docs/bootstrap-coverage.md").read_text().split("## Coverage matrix", 1)[1]
        matrix = matrix.split("## Repair verification", 1)[0]
        results = collections.Counter(
            line.split("|")[4].strip()
            for line in matrix.splitlines()
            if line.startswith("| ") and "Original lines" not in line
        )
        self.assertEqual(results, {"PASS": 74, "INTENTIONALLY REPLACED": 2})

    def test_fresh_fixture_generation_and_mapped_paths(self):
        from benchmarks.prepare_fixture import project_map

        fresh = Path(self.temporary.name) / "fresh"
        shutil.copytree(ROOT / "benchmarks/fixtures/expense-report", fresh)
        record = generate(fresh, transfer)
        self.assertEqual(record, self.record)
        self.assertEqual(transfer.verify(fresh, record)["facets"], 71)
        self.assertEqual(len(project_map(fresh)), 8)
        self.assertEqual(
            transfer.automatic_guidance(fresh),
            {fresh.resolve() / "AGENTS.md", fresh.resolve() / "CLAUDE.md"},
        )

    def test_existing_version_one_receipts_still_pass(self):
        archive = ROOT / "benchmarks/results/2026-09-30-clean-final-0.2.0/source-snapshot.zip"
        with zipfile.ZipFile(archive) as source:
            prefix = "tests/fixtures/bootstrap-transfer/"
            for name in ("AGENTS.md", "CLAUDE.md", "transfer.json"):
                (self.repo / name).write_bytes(source.read(prefix + name))
        record = json.loads((self.repo / "transfer.json").read_text())
        self.assertEqual(record["schema_version"], 1)
        self.assertEqual(transfer.verify(self.repo, record)["facets"], 71)

    def test_conditional_guidance_is_not_an_every_task_requirement(self):
        destinations = [
            d
            for rule in self.record["rules"].values()
            for d in rule["destinations"]
            if d["kind"] == "reference"
        ]
        self.assertEqual(
            {d["activation"]["when"] for d in destinations},
            {"uncertain extraction/boundary/refactor scope", "creating/modifying project Skills"},
        )
        automatic = (self.repo / "AGENTS.md").read_text()
        self.assertNotIn(".agents/skills/", automatic)
        self.assertNotIn(".claude/skills/", automatic)
        self.assertNotIn("symlink", automatic)
        self.assertEqual((self.repo / "CLAUDE.md").read_text(), "@AGENTS.md\n")
        reference = self.repo / "PROJECT_REFERENCE.md"
        self.assertIn(reference.resolve(), transfer.reachable_guidance(self.repo.resolve()))
        self.assertNotIn(reference.resolve(), transfer.automatic_guidance(self.repo))

    def test_fixture_keeps_mandatory_behavior_automatic(self):
        expected_kind = {
            "A": "guidance",
            "B": "guidance",
            "C": "contextlean_skill",
            "D": "reference",
            "E": "guidance",
        }
        for group, rule in self.record["rules"].items():
            for destination in rule["destinations"]:
                for facet in destination["facets"]:
                    category = GROUPS[group]["delivery"][facet]
                    with self.subTest(group=group, facet=facet):
                        self.assertEqual(destination["kind"], expected_kind[category])

    def test_each_lost_destination_facet_blocks_completion(self):
        for group, rule in self.record["rules"].items():
            for index, destination in enumerate(rule["destinations"]):
                for facet in destination["facets"]:
                    record = copy.deepcopy(self.record)
                    record["rules"][group]["destinations"][index]["facets"].remove(facet)
                    with self.subTest(group=group, facet=facet), self.assertRaises(ValueError):
                        transfer.verify(self.repo, record)

    def test_duplicate_destination_facet_blocks_completion(self):
        self.destination("ownership")["facets"].append("clear-owner")
        with self.assertRaises(ValueError):
            transfer.verify(self.repo, self.record)

    def test_automatic_reference_import_blocks_completion(self):
        wrapper = self.repo / "CLAUDE.md"
        wrapper.write_text(wrapper.read_text() + "@PROJECT_REFERENCE.md\n")
        with self.assertRaisesRegex(ValueError, "automatic startup"):
            transfer.verify(self.repo, self.record)

    def test_missing_reference_or_activation_blocks_completion(self):
        reference = next(
            d for d in self.record["rules"]["ownership"]["destinations"] if d["kind"] == "reference"
        )
        original = copy.deepcopy(reference)
        for key in ("activation", "sha256"):
            reference.clear()
            reference.update(original)
            reference.pop(key)
            with self.subTest(key=key), self.assertRaises(ValueError):
                transfer.verify(self.repo, self.record)

    def test_reference_activation_requires_condition_and_actual_link(self):
        reference = next(
            d for d in self.record["rules"]["ownership"]["destinations"] if d["kind"] == "reference"
        )
        activation = reference["activation"]
        activation["when"] = ""
        with self.assertRaisesRegex(ValueError, "applicability"):
            transfer.verify(self.repo, self.record)
        activation["when"] = "uncertain extraction/boundary/refactor scope"
        activation["section"] = "Navigation"
        activation["sha256"] = hashlib.sha256(
            transfer.section_text(self.repo / "AGENTS.md", "Navigation").encode()
        ).hexdigest()
        with self.assertRaisesRegex(ValueError, "must link"):
            transfer.verify(self.repo, self.record)

    def test_changed_conditional_detail_invalidates_review(self):
        path = self.repo / "PROJECT_REFERENCE.md"
        path.write_text(path.read_text() + "\nChanged Skill sharing.\n")
        with self.assertRaises(ValueError):
            transfer.verify(self.repo, self.record)

    def test_safety_obligation_change_invalidates_review(self):
        path = self.repo / "AGENTS.md"
        for obligation in (
            "correctness",
            "security",
            "trust-boundary validation",
            "data safety",
            "data-loss prevention",
            "readability",
            "maintainability",
            "accessibility",
            "requested behavior",
        ):
            original = path.read_text()
            path.write_text(original.replace(obligation, "", 1))
            with self.subTest(obligation=obligation), self.assertRaises(ValueError):
                transfer.verify(self.repo, self.record)
            path.write_text(original)

    def test_complete_transfer_passes_without_any_setup_specification(self):
        result = transfer.verify(self.repo, self.record)
        self.assertEqual(result["groups"], len(GROUPS))
        self.assertFalse(result["setup_specification_required"])
        historical = (ROOT / "docs/reference/original-agent-bootstrap.md").read_text()
        original = historical.split(
            "<!-- Original specification begins below; preserved verbatim. -->\n\n", 1
        )[1]
        self.assertEqual(
            hashlib.sha256(original.encode()).hexdigest(),
            "ecc02ff12623297e057eafb78e16ab8020953b317cc07cbf27bf764ab60d3f05",
        )
        old_spec = self.repo / "AGENT_BOOTSTRAP.md"
        old_spec.write_text(original)
        self.assertEqual(transfer.verify(self.repo, self.record), result)
        old_spec.unlink()
        self.assertEqual(transfer.verify(self.repo, self.record), result)
        active = [ROOT / "AGENTS.md", ROOT / "CLAUDE.md"]
        active.extend((ROOT / "skills").rglob("*.md"))
        for path in active:
            with self.subTest(active=path.relative_to(ROOT)):
                self.assertNotIn("original-agent-bootstrap.md", path.read_text())

    def test_each_missing_group_blocks_completion(self):
        for group in GROUPS:
            record = copy.deepcopy(self.record)
            del record["rules"][group]
            with self.subTest(group=group), self.assertRaises(ValueError):
                transfer.verify(self.repo, record)

    def test_each_missing_facet_blocks_completion(self):
        for group in GROUPS:
            record = copy.deepcopy(self.record)
            record["rules"][group]["facets"].pop()
            with self.subTest(group=group), self.assertRaises(ValueError):
                transfer.verify(self.repo, record)

    def test_unreviewed_meaning_blocks_completion(self):
        self.record["rules"]["bug-fix"]["semantics_reviewed"] = False
        with self.assertRaises(ValueError):
            transfer.verify(self.repo, self.record)

    def test_removed_regression_guidance_invalidates_the_review(self):
        path = self.repo / "AGENTS.md"
        body = transfer.section_text(path, "Bug fixes")
        path.write_text(path.read_text().replace(body, "Patch symptoms only.\n\n"))
        with self.assertRaises(ValueError):
            transfer.verify(self.repo, self.record)

    def move_navigation(self, path):
        guidance = self.repo / "AGENTS.md"
        body = transfer.section_text(guidance, "Navigation")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)
        # Actually move the duty: an unreachable reference must not leave a fallback copy.
        guidance.write_text(guidance.read_text().replace(body, ""))
        item = self.destination("navigation")
        item.update(
            kind="reference",
            path=path.relative_to(self.repo).as_posix(),
            section="",
            sha256=hashlib.sha256(body.encode()).hexdigest(),
        )
        item["activation"] = {
            "path": "AGENTS.md",
            "section": "",
            "when": "navigation",
            "sha256": hashlib.sha256(guidance.read_bytes()).hexdigest(),
        }

    def test_unreachable_optional_reference_blocks_completion(self):
        self.move_navigation(self.repo / "docs/navigation.md")
        with self.assertRaises(ValueError):
            transfer.verify(self.repo, self.record)

    def test_linked_optional_destination_survives_spec_removal(self):
        self.move_navigation(self.repo / "docs/navigation.md")
        path = self.repo / "AGENTS.md"
        path.write_text(
            path.read_text() + "\nFor navigation, follow [navigation](docs/navigation.md).\n"
        )
        self.destination("navigation")["activation"]["sha256"] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        old_spec = self.repo / "AGENT_BOOTSTRAP.md"
        old_spec.write_text("Obsolete setup only.\n")
        before = transfer.verify(self.repo, self.record)
        old_spec.unlink()
        self.assertEqual(transfer.verify(self.repo, self.record), before)

    def test_rule_only_in_old_specification_is_rejected(self):
        self.move_navigation(self.repo / "AGENT_BOOTSTRAP.md")
        path = self.repo / "AGENTS.md"
        path.write_text(path.read_text() + "\n[Setup](AGENT_BOOTSTRAP.md)\n")
        with self.assertRaises(ValueError):
            transfer.verify(self.repo, self.record)

    def test_local_receipt_cannot_carry_permanent_rules(self):
        self.move_navigation(self.repo / ".contextlean/navigation.md")
        path = self.repo / "AGENTS.md"
        path.write_text(path.read_text() + "\n[Navigation](.contextlean/navigation.md)\n")
        with self.assertRaises(ValueError):
            transfer.verify(self.repo, self.record)

    def test_missing_lean_review_handoff_blocks_completion(self):
        path = self.repo / "AGENTS.md"
        path.write_text(path.read_text().replace("contextlean:lean-review", "other-review"))
        with self.assertRaises(ValueError):
            transfer.verify(self.repo, self.record)

    def test_normal_development_cannot_be_silently_delegated_to_review(self):
        self.destination("bug-fix").update(
            kind="contextlean_skill", skill="contextlean:lean-review"
        )
        with self.assertRaises(ValueError):
            transfer.verify(self.repo, self.record)

    def test_destination_cannot_escape_the_repository(self):
        self.destination("navigation")["path"] = "../outside.md"
        with self.assertRaises(ValueError):
            transfer.verify(self.repo, self.record)

    def test_relative_project_skill_sharing_survives_relocation(self):
        source = self.repo / ".agents/skills/verify-project"
        source.mkdir(parents=True)
        (source / "SKILL.md").write_text(
            "---\nname: verify-project\ndescription: Verify this project.\n---\n"
        )
        shared = self.repo / ".claude/skills/verify-project"
        shared.parent.mkdir(parents=True)
        shared.symlink_to("../../.agents/skills/verify-project", target_is_directory=True)
        relocated = Path(self.temporary.name) / "relocated"
        shutil.copytree(self.repo, relocated, symlinks=True)
        self.assertEqual(
            (relocated / ".claude/skills/verify-project").resolve(),
            (relocated / ".agents/skills/verify-project").resolve(),
        )

    def test_cli_is_read_only_and_failure_is_nonzero(self):
        files = {
            p.relative_to(self.repo): p.read_bytes() for p in self.repo.rglob("*") if p.is_file()
        }
        command = [
            sys.executable,
            str(ROOT / "skills/bootstrap/scripts/verify_transfer.py"),
            "--repo",
            str(self.repo),
            "--record",
            str(self.repo / "transfer.json"),
        ]
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
        self.assertEqual(
            files,
            {p.relative_to(self.repo): p.read_bytes() for p in self.repo.rglob("*") if p.is_file()},
        )
        self.record["rules"].pop("navigation")
        (self.repo / "transfer.json").write_text(json.dumps(self.record))
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)


if __name__ == "__main__":
    unittest.main()
