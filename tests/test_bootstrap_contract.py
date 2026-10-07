"""Balanced concept and filesystem contracts, not proof of model compliance."""

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from bootstrap_fixture import ROOT, generate


SPEC = ROOT / "skills/bootstrap/references/bootstrap-spec.md"


def section(text, heading):
    match = re.search(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not match:
        raise AssertionError(f"missing section: {heading}")
    return " ".join(match[1].lower().split())


class BalancedKernelTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)
        generate(self.repo)
        self.guidance = (self.repo / "AGENTS.md").read_text()
        self.spec = " ".join(SPEC.read_text().lower().split())

    def concepts(self, heading, patterns):
        text = section(self.guidance, heading)
        for pattern in patterns:
            with self.subTest(heading=heading, pattern=pattern):
                self.assertRegex(text, pattern)

    def test_navigation_and_relevant_repository_state(self):
        self.concepts(
            "Navigation",
            [
                r"agents.md.*primary map",
                r"trust.*ownership/architecture.*unless source contradicts",
                r"smallest responsible subsystem.*search before broad reads",
                r"relevant usages/dependencies/tests",
                r"expand only.*evidence",
                r"no ordinary whole.repository scans.*broad rediscovery",
                r"skip.*equivalent answered searches.*unjustified rereads",
                r"broad/state-sensitive.*available version-control state only if relevant",
                r"no routine git checks",
                r"preserve architecture unless.*change requires",
            ],
        )
        self.assertRegex(self.spec, r"read-only navigation and small local edits alone need no git")

    def test_cohesive_ownership_interfaces_and_restrained_refactoring(self):
        self.concepts(
            "Ownership and scope",
            [
                r"cohesive files/modules/classes",
                r"related behavior together.*unrelated responsibilities separate",
                r"unique state/behavior owners",
                r"specific owners.*catch-all",
                r"new modules.*genuine responsibilities",
                r"responsibility, not line count.*cohesive large files",
                r"avoid fragmentation.*forwarding wrappers.*unnecessary layers",
                r"refactor only for meaningful current-task benefit or explicit request",
                r"preserve behavior.*relevant boundaries",
                r"dependency direction simple.*without cycles/hidden global coupling",
                r"apis focused.*internals local.*callers need no unnecessary",
            ],
        )

    def test_six_reuse_choices_keep_their_order(self):
        text = section(self.guidance, "Implementation")
        choices = [
            "existing support",
            "project solution",
            "standard library",
            "framework/platform",
            "installed dependency",
            "minimum new code",
        ]
        positions = [text.index(choice) for choice in choices]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("reuse in order:", text)

    def test_focused_readable_changes_and_consolidated_framework_guard(self):
        self.concepts(
            "Implementation",
            [
                r"explicit, readable, coherent and shallow.*meaningful concepts",
                r"focus diffs/files.*no unrelated cleanup or style-only rewrites",
                r"abstractions.*configuration.*dependencies.*test frameworks only.*justified current need",
                r"safely remove code made obsolete by the change",
            ],
        )

    def test_safety_and_material_preservation_remain_direct(self):
        text = section(self.guidance, "Implementation")
        clause = text[text.index("preserve correctness") : text.index("never change")]
        for concept in [
            "correctness",
            "security",
            "trust-boundary validation",
            "data safety",
            "data-loss prevention",
            "readability",
            "maintainability",
            "accessibility",
            "requested behavior",
            "source/tests/fixtures/migrations/docs/assets/archives",
        ]:
            with self.subTest(concept=concept):
                self.assertIn(concept, clause)

    def test_configuration_protection_requires_explicit_authorization(self):
        for text in [section(self.guidance, "Implementation"), self.spec]:
            clause = text[text.index("never change") :].split(".", 1)[0]
            for concept in [
                "model",
                "reasoning",
                "provider",
                "authentication",
                "credentials",
                "user-global",
            ]:
                self.assertIn(concept, clause)
            self.assertIn("explicit request", clause)

    def test_root_cause_bug_fixing_is_not_optional_review(self):
        self.concepts(
            "Bug fixes",
            [
                r"root cause before patching symptoms",
                r"trace relevant execution/data flow and callers when needed",
                r"responsible owner/shared layer",
                r"do not repeat workarounds across callers",
                r"avoid broad refactors unless correctness requires",
            ],
        )

    def test_proportional_verification_and_practical_regressions(self):
        self.concepts(
            "Verification",
            [
                r"smallest sufficient targeted check first",
                r"broaden only for insufficient coverage, shared/core/public impact or project rules",
                r"targeted, affected and full.*not mandatory stages",
                r"full-project checks require necessity or project rules",
                r"reuse infrastructure",
                r"small runnable regression check.*non-trivial logic or bug fixes.*practical",
                r"report verified scope and uncertainty",
            ],
        )

    def test_equivalent_coverage_keeps_every_rerun_exception(self):
        text = section(self.guidance, "Verification")
        clause = text[text.index("reuse equivalent") :].split(".", 1)[0]
        self.assertIn("passed coverage unless", clause)
        for reason in [
            "code",
            "test",
            "config",
            "environment",
            "failures",
            "unresolved results",
            "project-required repeats",
        ]:
            with self.subTest(reason=reason):
                self.assertIn(reason, clause)

    def test_map_corrections_require_invalidation_or_encountered_staleness(self):
        self.concepts(
            "Context and map accuracy",
            [
                r"when your change invalidates.*mapped path, owner, boundary, flow, constraint, or command",
                r"or you encounter stale mapped information.*correct only the affected",
                r"smallest applicable map.*otherwise leave maps alone",
                r"remove obsolete/duplicate entries.*affected map",
                r"do not expand.*unrelated documentation work",
            ],
        )
        self.assertNotRegex(self.guidance.lower(), r"after (every|each) task|reusable.workflow")

    def test_document_and_generated_material_access_remains_scoped(self):
        self.concepts(
            "Context and map accuracy",
            [
                r"search large documentation.*relevant sections",
                r"never make whole documents startup reading",
                r"generated/cache/build/vendor.*unless task-relevant",
                r"never hide useful material merely because it is large",
            ],
        )

    def test_runtime_is_independent_of_plugin_history_and_receipts(self):
        for name in [
            "contextlean:",
            "PROJECT_REFERENCE.md",
            "bootstrap-spec.md",
            "core-guidance.md",
            "permanent-rules.json",
            "AGENT_BOOTSTRAP.md",
            "transfer.json",
            ".contextlean/",
            ".agents/skills",
            ".claude/skills",
            "symlink",
            "71 facets",
        ]:
            self.assertNotIn(name, self.guidance)
        self.assertFalse(re.findall(r"\]\([^)]+\)", self.guidance))
        self.assertEqual({p.name for p in self.repo.iterdir()}, {"AGENTS.md", "CLAUDE.md"})

    def test_default_setup_has_no_project_skills_or_historical_bookkeeping(self):
        self.assertRegex(
            self.spec, r"default bootstrap does not.*create, synchronize or relocate project skills"
        )
        for clause in [
            "preserve existing skills",
            "do not require a transfer ledger",
            "default bootstrap writes no measurement report",
            "no fixed eight-category report",
        ]:
            self.assertIn(clause, self.spec)
        entry = (ROOT / "skills/bootstrap/SKILL.md").read_text()
        self.assertNotIn("permanent-rules.json", entry)
        self.assertIn("core-guidance.md", entry)

    def test_claude_setup_preserves_knowledge_and_import_resolution(self):
        for pattern in [
            r"pre-existing claude.md.*do not overwrite or discard",
            r"necessary claude-specific exceptions",
            r"verify every relative import and reference resolves",
            r"unchanged, already-clean repository should produce no further",
        ]:
            self.assertRegex(self.spec, pattern)
        wrapper = (self.repo / "CLAUDE.md").read_text()
        self.assertEqual(wrapper, "@AGENTS.md\n")
        self.assertTrue((self.repo / wrapper.strip()[1:]).is_file())

    def test_setup_validates_actual_outputs_and_safe_exclusions(self):
        for concept in [
            "mapped paths exist",
            "responsibilities",
            "flows match source",
            "commands are verified",
            "explicitly labelled unverified",
            "useful knowledge",
            "existing workflows",
            "references resolve",
            "exclusions do not hide",
            "no unauthorized",
            "without loading setup",
        ]:
            self.assertIn(concept, self.spec)
        self.assertRegex(self.spec, r"exclusion only after proving.*local generated")
        self.assertIn("must not change application behavior, product code", self.spec)

    def test_optional_skills_and_specialized_guidance_have_separate_owners(self):
        for name in ["audit", "lean-review", "benchmark", "bootstrap"]:
            metadata = (ROOT / "skills" / name / "agents/openai.yaml").read_text()
            self.assertIn("allow_implicit_invocation: false", metadata)
        review = (ROOT / "skills/lean-review/SKILL.md").read_text().lower()
        for concept in [
            "user requests a review",
            "do not edit files by default",
            "never trade away correctness",
            "references/architecture.md",
        ]:
            self.assertIn(concept, review)
        authoring = (ROOT / "docs/guidance-authoring.md").read_text()
        for concept in [
            ".agents/skills/",
            ".claude/skills/",
            "relocation",
            "non-trivial",
            "separately requested",
        ]:
            self.assertIn(concept, authoring)


class FreshGenerationTests(unittest.TestCase):
    def test_fresh_generation_preserves_product_commands_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary) / "project"
            shutil.copytree(
                ROOT / "benchmarks/fixtures/expense-report",
                repo,
                ignore=shutil.ignore_patterns(
                    "AGENTS.md", "CLAUDE.md", ".contextlean", "__pycache__"
                ),
            )
            before = {p.relative_to(repo): p.read_bytes() for p in repo.rglob("*") if p.is_file()}
            generated = generate(repo)
            first = [p.read_bytes() for p in generated]
            generate(repo)
            self.assertEqual(first, [p.read_bytes() for p in generated])
            self.assertEqual(before, {p: (repo / p).read_bytes() for p in before})
            new = {p.relative_to(repo) for p in repo.rglob("*") if p.is_file()} - set(before)
            self.assertEqual(new, {Path("AGENTS.md"), Path("CLAUDE.md")})
            mapped = (
                generated[0].read_text().split("## Project map", 1)[1].split("## Commands", 1)[0]
            )
            for name in re.findall(r"`([^`]+)`:", mapped):
                self.assertTrue((repo / name).exists(), name)
            result = subprocess.run(
                [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                cwd=repo,
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertRegex(result.stderr, r"Ran [1-9][0-9]* tests")
            cli = subprocess.run(
                [sys.executable, "-m", "expense_report.cli", "data/sample.csv"],
                cwd=repo,
                text=True,
                capture_output=True,
            )
            self.assertEqual(cli.returncode, 0, cli.stderr)
            self.assertIsInstance(json.loads(cli.stdout), dict)

    def test_generation_never_reads_historical_or_setup_inputs(self):
        read = Path.read_text

        def guarded(path, *args, **kwargs):
            self.assertNotIn(
                path.name,
                {
                    "bootstrap-spec.md",
                    "permanent-rules.json",
                    "original-agent-bootstrap.md",
                    "transfer.json",
                },
            )
            return read(path, *args, **kwargs)

        with tempfile.TemporaryDirectory() as temporary, patch.object(Path, "read_text", guarded):
            agents, claude = generate(Path(temporary))
            self.assertIn("Diagnose the root cause", agents.read_text())
            self.assertEqual(claude.read_text(), "@AGENTS.md\n")
