import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("bootstrap", "audit", "lean-review", "benchmark")


def load_json(relative_path: str) -> dict:
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise AssertionError(f"missing YAML frontmatter: {path}")

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip()
    return values


class PackageContractTests(unittest.TestCase):
    def test_required_layout_exists(self) -> None:
        required = [
            ".codex-plugin/plugin.json",
            ".claude-plugin/plugin.json",
            ".claude-plugin/marketplace.json",
            "skills/bootstrap/references/bootstrap-spec.md",
            "skills/benchmark/scripts/benchmark.py",
            "skills/benchmark/references/methodology.md",
            "skills/benchmark/data/credit-rates.json",
            "tests/test_package.py",
            "tests/test_benchmark.py",
            "tests/test_skill_contracts.py",
            "AGENTS.md",
            "CLAUDE.md",
            "README.md",
            "LICENSE",
            "benchmarks/run_benchmark.py",
            "benchmarks/evaluate.py",
            "benchmarks/tasks/suite.json",
            "benchmarks/README.md",
            "docs/assets/before-after.svg",
            "docs/verification.md",
            "docs/release-notes.md",
            ".github/workflows/quality.yml",
        ]
        required.extend(f"skills/{name}/SKILL.md" for name in SKILLS)
        for relative_path in required:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file())

        self.assertFalse((ROOT / "AGENT_BOOTSTRAP.md").exists())

    def test_manifests_identify_the_same_release(self) -> None:
        codex = load_json(".codex-plugin/plugin.json")
        claude = load_json(".claude-plugin/plugin.json")

        for manifest in (codex, claude):
            self.assertEqual(manifest["name"], "contextlean")
            self.assertEqual(manifest["version"], "0.2.0")
            self.assertEqual(manifest["license"], "MIT")
            self.assertEqual(manifest["author"]["name"], "ContextLean contributors")
            self.assertNotIn("[TODO:", json.dumps(manifest))

        self.assertEqual(codex["skills"], "./skills/")

        benchmark_script = (ROOT / "skills/benchmark/scripts/benchmark.py").read_text(
            encoding="utf-8"
        )
        self.assertIn('CONTEXTLEAN_VERSION = "0.2.0"', benchmark_script)

        self.assertLessEqual(len(codex["interface"]["defaultPrompt"]), 3)

    def test_local_catalog_resolves_to_plugin_and_exposes_safe_policy(self) -> None:
        catalog = load_json(".claude-plugin/marketplace.json")
        self.assertEqual(catalog["name"], "contextlean-local")
        self.assertEqual(len(catalog["plugins"]), 1)
        entry = catalog["plugins"][0]
        self.assertEqual(entry["name"], "contextlean")
        self.assertEqual((ROOT / entry["source"]).resolve(), ROOT)
        self.assertEqual(entry["policy"]["installation"], "AVAILABLE")

    def test_public_document_links_resolve(self) -> None:
        documents = [ROOT / "README.md", ROOT / "benchmarks/README.md"]
        documents.extend((ROOT / "docs").glob("*.md"))
        documents.extend((ROOT / "benchmarks/results").rglob("*.md"))
        for path in documents:
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                with self.subTest(document=path.name, target=target):
                    self.assertTrue((path.parent / target.split("#")[0]).exists())

    def test_skills_have_matching_names_and_no_placeholders(self) -> None:
        for name in SKILLS:
            skill_path = ROOT / "skills" / name / "SKILL.md"
            with self.subTest(skill=name):
                values = frontmatter(skill_path)
                self.assertEqual(values["name"], name)
                self.assertTrue(values["description"])
                self.assertNotIn("TODO", skill_path.read_text(encoding="utf-8"))
                self.assertTrue((skill_path.parent / "agents/openai.yaml").is_file())
                self.assertIn(
                    f"$contextlean:{name}",
                    (skill_path.parent / "agents/openai.yaml").read_text(encoding="utf-8"),
                )

    def test_bootstrap_requires_explicit_invocation(self) -> None:
        skill = ROOT / "skills/bootstrap/SKILL.md"
        metadata = ROOT / "skills/bootstrap/agents/openai.yaml"

        description = frontmatter(skill)["description"]
        self.assertIn("explicitly", description)
        self.assertIn("must never run implicitly", description)
        self.assertIn("allow_implicit_invocation: false", metadata.read_text(encoding="utf-8"))

    def test_has_no_mcp_hooks_or_session_scripts(self) -> None:
        forbidden_paths = (".mcp.json", ".app.json", "hooks", "scripts")
        for relative_path in forbidden_paths:
            with self.subTest(path=relative_path):
                self.assertFalse((ROOT / relative_path).exists())

        for relative_path in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
            manifest = load_json(relative_path)
            for key in ("mcpServers", "apps", "hooks"):
                with self.subTest(manifest=relative_path, key=key):
                    self.assertNotIn(key, manifest)

    def test_claude_wrapper_reuses_agents_instructions(self) -> None:
        self.assertEqual((ROOT / "CLAUDE.md").read_text(encoding="utf-8"), "@AGENTS.md\n")

    def test_bootstrap_spec_is_targeted_and_canonical(self) -> None:
        spec = ROOT / "skills/bootstrap/references/bootstrap-spec.md"
        content = spec.read_text(encoding="utf-8")
        self.assertGreater(len(content.splitlines()), 100)
        self.assertLess(len(content.splitlines()), 250)
        self.assertEqual(
            [path for path in ROOT.rglob("bootstrap-spec.md") if ".contextlean" not in path.parts],
            [spec],
            "bootstrap specification must have one canonical copy",
        )
        self.assertIn("Read it only after", content)

    def test_benchmark_is_local_and_not_automatically_loaded(self) -> None:
        benchmark = (ROOT / "skills/benchmark/SKILL.md").read_text(encoding="utf-8")
        methodology = (ROOT / "skills/benchmark/references/methodology.md").read_text(
            encoding="utf-8"
        )
        bootstrap = (ROOT / "skills/bootstrap/references/bootstrap-spec.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("never invent gains", benchmark.lower())
        self.assertIn("danger-full-access", methodology)
        self.assertIn("never used", methodology)
        self.assertIn(".contextlean/bootstrap-report.json", bootstrap)
        self.assertNotIn("bootstrap-report.json", (ROOT / "AGENTS.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
