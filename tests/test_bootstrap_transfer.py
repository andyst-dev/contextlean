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


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "contextlean_transfer", ROOT / "skills/bootstrap/scripts/verify_transfer.py"
)
transfer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(transfer)
FIXTURE = ROOT / "tests/fixtures/bootstrap-transfer"
GROUPS = {g["id"]: g for g in json.loads(transfer.RULES.read_text())["groups"]}


class PermanentBehaviorContracts(unittest.TestCase):
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
        item = json.loads((FIXTURE / "transfer.json").read_text())["rules"]["lean-review"]
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
        item = self.record["rules"]["navigation"]
        item.update(
            kind="reference",
            path=path.relative_to(self.repo).as_posix(),
            section="",
            sha256=hashlib.sha256(body.encode()).hexdigest(),
        )

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
        self.record["rules"]["bug-fix"].update(
            kind="contextlean_skill", skill="contextlean:lean-review"
        )
        with self.assertRaises(ValueError):
            transfer.verify(self.repo, self.record)

    def test_destination_cannot_escape_the_repository(self):
        self.record["rules"]["navigation"]["path"] = "../outside.md"
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
