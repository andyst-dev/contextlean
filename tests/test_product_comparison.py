"""Offline product adapter contracts; synthetic Git history and provider events only."""

from contextlib import ExitStack
import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "comparison_tests", ROOT / "benchmarks/compare_products.py"
)
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)
r, h = adapter.runner, adapter.h


class ProductComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # CI need not fetch historical commits. Build real local commits from
        # representative frozen test artifacts; only these test SHAs are substituted.
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.repo = Path(cls.temporary.name) / "git"
        cls.repo.mkdir()
        paths = [
            *adapter.UNCHANGED,
            "tests/bootstrap_fixture.py",
            "tests/fixtures/bootstrap-core",
            "tests/fixtures/bootstrap-transfer",
            "benchmarks/fixtures/expense-report",
            "skills/bootstrap",
            "skills/lean-review",
        ]
        for relative in paths:
            src, dest = ROOT / relative, cls.repo / relative
            if dest.exists():
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__"))
            else:
                shutil.copyfile(src, dest)
        generator = cls.repo / "tests/bootstrap_fixture.py"
        balanced = generator.read_bytes()
        generator.write_text("""from pathlib import Path
import shutil
def generate(repo, transfer):
    source = Path(__file__).resolve().parent / "fixtures/bootstrap-transfer"
    for name in ("AGENTS.md", "CLAUDE.md", "PROJECT_REFERENCE.md"):
        shutil.copyfile(source / name, repo / name)
    (repo / "transfer.json").write_text("{}")
""")
        cls.git("init", "--initial-branch=main")
        for key, value in h.GIT_SETTINGS.items():
            cls.git("config", "--local", key, value)
        cls.git("add", ".")
        cls.git("commit", "-m", "Old fixture test inputs")
        old = cls.git("rev-parse", "HEAD").strip()
        generator.write_bytes(balanced)
        cls.git("add", ".")
        cls.git("commit", "-m", "Balanced fixture test inputs")
        cls.revisions = {"old": old, "balanced": cls.git("rev-parse", "HEAD").strip()}
        # Poison the working tree after committing. The adapter must ignore it.
        generator.write_text('raise RuntimeError("must never load worktree generator")\n')
        (cls.repo / "skills/bootstrap/references/core-guidance.md").write_text("poisoned core")

    @classmethod
    def git(cls, *args):
        return subprocess.check_output(
            ["git", "-C", str(cls.repo), *args],
            text=True,
            env=dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull),
        )

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.revisions_patch = patch.object(adapter, "REVISIONS", self.revisions)
        self.revisions_patch.start()
        self.addCleanup(self.revisions_patch.stop)
        self.comparison = adapter.GuidedComparison(self.repo, self.base / "inputs")

    def args(self, **overrides):
        values = dict(
            tasks_file=self.comparison.tasks,
            output_dir=self.base / "output",
            model="gpt-5.6-sol",
            reasoning="high",
            repeat=3,
            timeout=10,
            provider="codex",
            codex=sys.executable,
            shell="/bin/sh",
            preflight_only=True,
            live=False,
        )
        values.update(overrides)
        return r.argparse.Namespace(**values)

    def test_committed_provenance_and_guidance_ignore_poisoned_worktree(self):
        for name in self.revisions:
            identity = self.comparison.identity(name)
            self.assertEqual(identity["product_revision"], self.revisions[name])
            self.assertEqual(identity["condition_kind"], "guided_product_revision")
            self.assertEqual(identity["automatic_guidance_bytes"], 5486 if name == "old" else 4752)
            self.assertNotIn("poisoned", (self.comparison.paths[name] / "AGENTS.md").read_text())
        self.assertNotEqual(*self.revisions.values())
        serialized = json.dumps(self.comparison.frozen)
        self.assertNotIn('"vanilla"', serialized)
        self.assertNotIn("vanilla_digest", serialized)
        self.assertEqual(
            adapter.product_inventory(self.comparison.paths["old"]),
            adapter.product_inventory(self.comparison.paths["balanced"]),
        )

    def test_both_conditions_require_exact_revision_guidance(self):
        for name in self.revisions:
            path = self.comparison.paths[name] / "AGENTS.md"
            original = path.read_bytes()
            for replacement in [
                None,
                b"",
                (
                    self.comparison.paths["balanced" if name == "old" else "old"] / "AGENTS.md"
                ).read_bytes(),
            ]:
                if replacement is None:
                    path.unlink()
                else:
                    path.write_bytes(replacement)
                with self.assertRaises((h.HarnessError, r.core.BenchmarkError, FileNotFoundError)):
                    self.comparison.validate(self.comparison.frozen)
                path.write_bytes(original)

    def test_fixture_task_source_and_grader_mutation_fail_closed(self):
        paths = [
            self.comparison.paths["balanced"] / "expense_report/report.py",
            self.comparison.tasks,
            self.comparison.inputs / "sources/old/benchmarks/evaluate.py",
            self.comparison.inputs / "sources/balanced/tests/bootstrap_fixture.py",
        ]
        for path in paths:
            before = path.read_bytes()
            path.write_bytes(before + b"\n# drift\n")
            with self.assertRaises(h.HarnessError):
                self.comparison.validate(self.comparison.frozen)
            path.write_bytes(before)
        with self.assertRaisesRegex(h.HarnessError, "prompt bytes"):
            self.comparison.manifest(self.comparison.paths, b"old", b"different")
        with self.assertRaises(h.HarnessError):
            adapter.archive_revision(self.repo, "HEAD", self.base / "bad")

    def test_existing_vanilla_contract_still_omits_and_rejects_guidance(self):
        v, c = h.make_conditions(r.FIXTURE, self.base / "ordinary", h.copy_fixture)
        self.assertFalse(set(h.inventory(v)) & h.GUIDANCE)
        h.fixture_manifest(v, c, b"prompt", b"prompt")
        (v / "AGENTS.md").write_bytes((c / "AGENTS.md").read_bytes())
        with self.assertRaisesRegex(h.HarnessError, "Vanilla must omit"):
            h.fixture_manifest(v, c, b"prompt", b"prompt")
        self.assertEqual(
            [x["condition"] for x in h.schedule(["refactor"], 3)],
            ["vanilla", "contextlean", "contextlean", "vanilla", "vanilla", "contextlean"],
        )

    def test_exact_schedule_runtime_and_no_resuming(self):
        plan = self.comparison.schedule(r.load_suite(self.comparison.tasks), self.args())
        self.assertEqual([x["condition"] for x in plan], list(adapter.ORDER))
        self.assertEqual([x["repeat"] for x in plan], [1, 1, 2, 2, 3, 3])
        for item in plan:
            self.assertEqual(item["product_revision"], self.revisions[item["condition"]])
        with self.assertRaises(h.HarnessError):
            self.comparison.schedule(r.load_suite(self.comparison.tasks), self.args(repeat=4))
        with self.assertRaises(h.HarnessError):
            adapter.GuidedComparison(self.repo, self.comparison.inputs)
        runtime = {
            "binaries": {
                k: {"version": v}
                for k, v in {
                    "python3": "Python 3.14.4",
                    "git": "git version 2.54.0 (Apple Git-157)",
                    "rg": "ripgrep 15.2.0 (rev test)\nfeatures:+pcre2",
                }.items()
            }
        }
        self.comparison.check_runtime(runtime)
        for key in runtime["binaries"]:
            drift = copy.deepcopy(runtime)
            drift["binaries"][key]["version"] = "wrong version"
            with self.assertRaisesRegex(h.HarnessError, "runtime mismatch"):
                self.comparison.check_runtime(drift)

    def mocked_controls(self, stack):
        # Deterministic orchestration test only. The separately recorded native
        # six-slot validation exercises real sandbox/runtime gates without mocks.
        stack.enter_context(patch.object(self.comparison, "check_runtime"))
        stack.enter_context(
            patch.object(
                h,
                "environment_source",
                return_value=h.environment_source(
                    "codex", {"OPENAI_API_KEY": "offline-test-secret"}
                ),
            )
        )
        stack.enter_context(
            patch.object(h, "permission_policy", return_value={"sandbox": "workspace-write"})
        )
        stack.enter_context(
            patch.object(
                h,
                "permission_preflight",
                side_effect=lambda s, p, o: dict(p, native_preflight={"mocked": True}),
            )
        )
        stack.enter_context(
            patch.object(
                h, "effective_runtime_preflight", return_value={"passed": True, "mocked": True}
            )
        )
        stack.enter_context(patch.object(h, "boundary_command", side_effect=lambda s, p, c, o: c))

    def test_six_preparations_delegate_and_never_execute_a_model(self):
        roots = []
        original = h.initialize_git

        def initialize(session):
            roots.append(session.root)
            saved = json.loads((self.base / "output/schedule.json").read_text())
            self.assertEqual([x["condition"] for x in saved["order"]], list(adapter.ORDER))
            return original(session)

        with ExitStack() as stack:
            self.mocked_controls(stack)
            execute = stack.enter_context(
                patch.object(h, "execute_session", side_effect=AssertionError("no model calls"))
            )
            stack.enter_context(patch.object(h, "initialize_git", side_effect=initialize))
            report = r.run(self.args(), comparison=self.comparison)
        execute.assert_not_called()
        self.assertEqual(report["model_calls"], 0)
        self.assertEqual(report["status"], "preflight-passed")
        self.assertEqual(len(set(roots)), 6)
        self.assertTrue(all(not p.exists() for p in roots))
        self.assertTrue(
            all(
                s["cleanup_verified"] and s["preparation_passed"]
                for s in report["preparation_slots"]
            )
        )
        receipts = [
            json.loads((self.base / f"output/preflight/{i}.json").read_text()) for i in range(1, 7)
        ]
        for key in [
            "environment",
            "permission",
            "runtime",
            "prompt_sha256",
            "grader_sha256",
            "git_policy",
            "preflight_coverage",
        ]:
            self.assertTrue(all(receipt[key] == receipts[0][key] for receipt in receipts))
        self.assertNotIn('"vanilla"', json.dumps(report))
        self.assertNotIn("Vanilla", r.render(report))

    def test_synthetic_execution_reuses_tracing_grading_and_explicit_identity(self):
        calls = []

        def execute(session, command, prompt, timeout, policy, output):
            calls.append(session.root)
            path = session.repo / "expense_report/report.py"
            path.write_text(
                path.read_text().replace(
                    "def normalize_category(value):\n    return value.strip().casefold()",
                    "from expense_report.filters import normalize_category",
                )
            )
            events = {
                "type": "turn.completed",
                "usage": {
                    "input_tokens": 100 + len(calls),
                    "cached_input_tokens": 20,
                    "output_tokens": 5,
                },
            }
            return {
                "stdout": json.dumps(events),
                "stderr": "",
                "error": None,
                "duration_seconds": 1,
                "exit_code": 0,
            }

        with ExitStack() as stack:
            self.mocked_controls(stack)
            stack.enter_context(patch.object(h, "execute_session", side_effect=execute))
            grade = stack.enter_context(patch.object(r, "grade", wraps=r.grade))
            report = r.run(self.args(live=True, preflight_only=False), comparison=self.comparison)
        self.assertEqual(len(calls), 6)
        self.assertEqual(grade.call_count, 6)
        self.assertTrue(all(not root.exists() for root in calls))
        self.assertEqual(report["status"], "complete")
        for run in report["runs"]:
            self.assertTrue(run["evaluation"]["agent_tests_passed"])
            self.assertTrue(run["evaluation"]["tests_passed"])
            self.assertTrue(run["evaluation"]["acceptance_passed"])
            self.assertEqual(run["product_revision"], self.revisions[run["condition"]])
            parsed = json.loads(
                (self.base / "output" / run["raw_directory"] / "execution.json").read_text()
            )
            self.assertEqual(parsed["condition_name"], run["condition"])
            self.assertEqual(parsed["product_revision"], run["product_revision"])
        pairs = report["paired_differences"][0]
        self.assertEqual([p["differences"]["total_tokens"] for p in pairs["pairs"]], [1, -1, 1])
        self.assertAlmostEqual(pairs["differences"]["total_tokens"]["mean"], 1 / 3)
        self.assertNotIn('"vanilla"', json.dumps(report))
        self.assertNotIn("Vanilla", r.render(report))

    def test_runtime_policy_drift_aborts_before_execution_and_cleans_roots(self):
        roots = []

        def drift(session, policy, output):
            roots.append(session.root)
            return dict(policy, native_preflight={"drift": len(roots)})

        with ExitStack() as stack:
            self.mocked_controls(stack)
            stack.enter_context(patch.object(h, "permission_preflight", side_effect=drift))
            execute = stack.enter_context(
                patch.object(h, "execute_session", side_effect=AssertionError("no model calls"))
            )
            with self.assertRaisesRegex(h.HarnessError, "execution"):
                r.run(self.args(), comparison=self.comparison)
        execute.assert_not_called()
        self.assertEqual(len(roots), 2)
        self.assertTrue(all(not p.exists() for p in roots))


if __name__ == "__main__":
    unittest.main()
