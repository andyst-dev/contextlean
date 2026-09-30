import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROJECT_FIXTURES = ROOT / "tests/fixtures/projects"
REVIEW_FIXTURES = ROOT / "tests/fixtures/reviews"
BENCHMARK_SCRIPT = ROOT / "skills/benchmark/scripts/benchmark.py"
SPEC = importlib.util.spec_from_file_location("contextlean_fixture_benchmark", BENCHMARK_SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load benchmark module")
benchmark = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(benchmark)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ProjectFixtureTests(unittest.TestCase):
    def fixture_manifests(self) -> list[tuple[Path, dict]]:
        manifests = []
        for path in sorted(PROJECT_FIXTURES.glob("*/fixture.json")):
            manifests.append((path.parent, json.loads(path.read_text(encoding="utf-8"))))
        return manifests

    def test_fixture_matrix_covers_requested_repository_shapes(self) -> None:
        traits = {
            trait for _root, manifest in self.fixture_manifests() for trait in manifest["traits"]
        }
        self.assertTrue(
            {
                "small-python",
                "node-typescript",
                "monorepo",
                "nested-structure",
                "existing-agents",
                "large-claude",
                "large-docs",
                "already-clean",
            }.issubset(traits)
        )

    def test_every_declared_product_file_exists(self) -> None:
        for fixture_root, manifest in self.fixture_manifests():
            for relative_path in manifest["product_files"]:
                with self.subTest(fixture=fixture_root.name, path=relative_path):
                    self.assertTrue((fixture_root / relative_path).is_file())

    def test_static_bootstrap_capture_never_modifies_fixture_product(self) -> None:
        for fixture_root, manifest in self.fixture_manifests():
            with (
                self.subTest(fixture=fixture_root.name),
                tempfile.TemporaryDirectory() as temporary,
            ):
                copy = Path(temporary) / fixture_root.name
                shutil.copytree(fixture_root, copy)
                product = [copy / path for path in manifest["product_files"]]
                before = {path.relative_to(copy).as_posix(): digest(path) for path in product}
                baseline = copy / ".contextlean/.bootstrap-baseline.json"
                report = copy / ".contextlean/bootstrap-report.json"

                benchmark.bootstrap_start(copy, baseline, None)
                benchmark.bootstrap_finish(copy, baseline, report, None, [], [], [], [], [])

                after = {path.relative_to(copy).as_posix(): digest(path) for path in product}
                self.assertEqual(before, after)
                self.assertTrue(report.is_file())

    def test_existing_guidance_and_clean_wrapper_are_explicit_fixtures(self) -> None:
        existing_agents = PROJECT_FIXTURES / "python-existing/AGENTS.md"
        large_claude = PROJECT_FIXTURES / "node-large-claude/CLAUDE.md"
        clean_wrapper = PROJECT_FIXTURES / "clean/CLAUDE.md"

        self.assertIn("public output contract", existing_agents.read_text(encoding="utf-8"))
        self.assertGreater(len(large_claude.read_text(encoding="utf-8")), 1_500)
        self.assertEqual(clean_wrapper.read_text(encoding="utf-8"), "@AGENTS.md\n")


class SkillContractTests(unittest.TestCase):
    def test_bootstrap_contract_covers_preservation_idempotence_and_scope(self) -> None:
        spec = (ROOT / "skills/bootstrap/references/bootstrap-spec.md").read_text(encoding="utf-8")
        lowered = spec.lower()
        for required in (
            "do not overwrite or discard",
            "should produce no further guidance changes",
            "application behavior, product code",
            "search topic → read relevant section",
            "repository contents, secrets",
        ):
            with self.subTest(required=required):
                self.assertIn(required, lowered)
        self.assertIn("@AGENTS.md", spec)

    def test_audit_contract_has_fixed_evidence_statuses(self) -> None:
        audit = (ROOT / "skills/audit/SKILL.md").read_text(encoding="utf-8")
        for status in ("PASS", "WARNING", "ACTION NEEDED"):
            self.assertIn(status, audit)
        self.assertIn("Default to read-only", audit)
        self.assertIn("Claude wrappers", audit)

    def test_lean_review_fixtures_cover_duplicate_and_focused_diffs(self) -> None:
        expected = json.loads((REVIEW_FIXTURES / "expected.json").read_text(encoding="utf-8"))
        duplicate = (REVIEW_FIXTURES / "duplicate-helper.diff").read_text(encoding="utf-8")
        focused = (REVIEW_FIXTURES / "focused-change.diff").read_text(encoding="utf-8")
        lean_review = (ROOT / "skills/lean-review/SKILL.md").read_text(encoding="utf-8")

        self.assertEqual(duplicate.count("+def slugify"), 1)
        self.assertIn("src/shared/slug.py", duplicate)
        self.assertEqual(focused.count("diff --git"), 1)
        self.assertEqual(expected["duplicate-helper.diff"], "duplicated behavior")
        self.assertEqual(expected["focused-change.diff"], "no material finding")
        self.assertIn("duplicates existing behavior", lean_review)
        self.assertIn("If there are no material findings", lean_review)


if __name__ == "__main__":
    unittest.main()
