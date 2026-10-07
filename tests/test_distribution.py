"""Actual package bytes and native offline plugin lifecycle; never run models."""

import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from zipfile import ZipFile

from bootstrap_fixture import generate
from distribution_support import IsolatedPlatform, PLUGIN, snapshot
from document_links import link_errors
from test_package import SKILLS, frontmatter


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("distribution_build", ROOT / "packaging/build.py")
package = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package)


def unpack(root):
    archive = root / "contextlean.zip"
    package.build(archive)
    source = root / "unpacked"
    with ZipFile(archive) as zipped:
        zipped.extractall(source)
    return source


class DistributionTests(unittest.TestCase):
    def test_artifact_is_reproducible_and_contains_only_public_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = unpack(root)
            package.build(root / "again.zip")
            self.assertEqual(
                (root / "contextlean.zip").read_bytes(), (root / "again.zip").read_bytes()
            )
            files = snapshot(source)
            for name, data in files.items():
                self.assertTrue(
                    name.startswith(("skills/", ".codex-plugin/", ".claude-plugin/"))
                    or name
                    in {
                        "README.md",
                        "LICENSE",
                        "docs/assets/contextlean.svg",
                        "benchmarks/README.md",
                    }
                )
                self.assertNotIn(b"/Users/", data)
                self.assertNotIn(b"/home/", data)
                self.assertFalse((source / name).is_symlink())
            for path in (ROOT / "skills").rglob("*"):
                if path.is_file() and path.suffix in {".md", ".yaml", ".py", ".json"}:
                    self.assertEqual(files[path.relative_to(ROOT).as_posix()], path.read_bytes())
            self.assertFalse((source / ".contextlean").exists())
            self.assertEqual(
                list((source / "benchmarks").iterdir()), [source / "benchmarks/README.md"]
            )
            self.assertEqual(link_errors(source / "README.md", source), [])
            with self.assertRaises(FileExistsError):
                package.build(root / "contextlean.zip")

    def test_relocated_package_has_all_skills_references_and_consistent_versions(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = unpack(root)
            moved = root / "relocated package"
            source.rename(moved)
            codex = json.loads((moved / ".codex-plugin/plugin.json").read_text())
            claude = json.loads((moved / ".claude-plugin/plugin.json").read_text())
            catalog = json.loads((moved / ".claude-plugin/marketplace.json").read_text())
            self.assertEqual(codex["version"], claude["version"])
            self.assertEqual(codex["version"], "0.3.1")
            for key in (
                "name",
                "description",
                "author",
                "license",
                "keywords",
                "homepage",
                "repository",
            ):
                self.assertEqual(codex[key], claude[key], key)
            entry = catalog["plugins"][0]
            self.assertEqual(entry.get("version", claude["version"]), claude["version"])
            self.assertEqual(entry["name"], claude["name"])
            self.assertEqual((moved / entry["source"]).resolve(), moved.resolve())
            self.assertEqual((moved / codex["skills"]).resolve(), (moved / "skills").resolve())
            self.assertEqual(
                {p.name for p in ((moved / "skills").resolve()).iterdir()}, set(SKILLS)
            )
            for name in SKILLS:
                skill = moved / "skills" / name / "SKILL.md"
                self.assertEqual(frontmatter(skill)["name"], name)
                for path in skill.parent.rglob("*.md"):
                    self.assertEqual(link_errors(path, moved), [])
            for field in ("composerIcon", "logo"):
                self.assertTrue((moved / codex["interface"][field]).is_file())
            self.assertLessEqual(len(codex["interface"]["shortDescription"]), 30)
            self.assertEqual(claude["icon"], codex["interface"]["logo"])
            self.assertFalse(
                any(
                    k in codex or k in claude
                    for k in ("hooks", "mcpServers", "settings", "dependencies")
                )
            )

    def test_export_rejects_missing_skill_and_symlink(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            # Copy real inputs, including the package README's source location.
            source = unpack(root)
            (source / "packaging").mkdir()
            shutil.copyfile(ROOT / "packaging/README.md", source / "packaging/README.md")
            shutil.copyfile(
                ROOT / "packaging/benchmark-suite.md", source / "packaging/benchmark-suite.md"
            )
            skill = source / "skills/audit/SKILL.md"
            original = skill.read_bytes()
            skill.unlink()
            with self.assertRaises(ValueError):
                package.build(root / "missing.zip", source)
            (root / "private.md").write_bytes(original)
            skill.symlink_to(root / "private.md")
            with self.assertRaises(ValueError):
                package.build(root / "symlink.zip", source)
            skill.unlink()
            skill.write_bytes(original)
            (source / "skills/audit/private.json").write_text('{"private": true}')
            package.build(root / "public.zip", source)
            with ZipFile(root / "public.zip") as archive:
                self.assertNotIn("skills/audit/private.json", archive.namelist())


@unittest.skipUnless(
    sys.platform == "darwin" and shutil.which("sandbox-exec"),
    "Native installation requires the macOS network/write sandbox",
)
class NativeInstallationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="contextlean-install-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.platform = IsolatedPlatform(self.root)
        self.source = unpack(self.root)
        # The installer sees a relocated artifact, never the repository checkout.
        relocated = self.root / "relocated package"
        self.source.rename(relocated)
        self.source = relocated
        generate(self.platform.project)
        for name in ("AGENTS.md", "CLAUDE.md"):
            with (self.platform.project / name).open("a") as handle:
                handle.write("\nUser customization: preserve this.\n")
        for name in (
            "src/AGENTS.md",
            ".agents/skills/personal/SKILL.md",
            ".claude/skills/personal/SKILL.md",
            "docs/project-map.md",
        ):
            path = self.platform.project / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                "---\nname: personal\ndescription: Explicit personal fixture\n---\nProject-owned content\n"
                if path.name == "SKILL.md"
                else "Project-owned content\n"
            )
        self.project_before = snapshot(self.platform.project)

    def assert_preserved(self):
        self.assertEqual(snapshot(self.platform.project), self.project_before)
        wrapper = (self.platform.project / "CLAUDE.md").read_text().splitlines()[0]
        self.assertTrue((self.platform.project / wrapper.removeprefix("@")).is_file())

    def prepare_update(self):
        # Synthetic next version exists only inside the temporary package.
        for name in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
            path = self.source / name
            manifest = json.loads(path.read_text())
            manifest["version"] = "0.3.2-test"
            path.write_text(json.dumps(manifest))
        (self.source / "README.md").write_text("Updated package marker\n")

    @unittest.skipUnless(shutil.which("codex"), "Codex CLI not installed")
    def test_codex_fresh_discovery_relocation_update_and_uninstall(self):
        run = self.platform.run
        run("codex", "plugin", "marketplace", "add", str(self.source))
        installed = json.loads(run("codex", "plugin", "add", PLUGIN, "--json"))
        cache = Path(installed["installedPath"])
        self.assertTrue(cache.is_relative_to(self.root / "codex"))
        self.assertEqual(snapshot(cache), snapshot(self.source))
        self.assert_preserved()
        # Discovery must work without the original package source.
        hidden = self.root / "source-unavailable"
        self.source.rename(hidden)
        skills = self.platform.codex_skills()
        self.assertEqual({s["name"] for s in skills}, {f"contextlean:{n}" for n in SKILLS})
        self.assertTrue(all(s["enabled"] and Path(s["path"]).is_relative_to(cache) for s in skills))
        hidden.rename(self.source)
        self.prepare_update()
        updated = json.loads(run("codex", "plugin", "add", PLUGIN, "--json"))
        self.assertEqual(updated["version"], "0.3.2-test")
        self.assertEqual(snapshot(Path(updated["installedPath"])), snapshot(self.source))
        self.assert_preserved()
        run("codex", "plugin", "remove", PLUGIN)
        self.assertEqual(self.platform.codex_skills(), [])
        self.assertEqual(json.loads(run("codex", "plugin", "list", "--json"))["installed"], [])
        run("codex", "plugin", "marketplace", "remove", "contextlean-local")
        self.assert_preserved()

    @unittest.skipUnless(shutil.which("claude"), "Claude Code not installed")
    def test_claude_fresh_discovery_relocation_update_and_uninstall(self):
        run = self.platform.run
        run(
            "claude",
            "plugin",
            "validate",
            str(self.source / ".claude-plugin/plugin.json"),
            "--strict",
        )
        run("claude", "plugin", "validate", str(self.source / ".claude-plugin/marketplace.json"))
        run("claude", "plugin", "marketplace", "add", str(self.source))
        run("claude", "plugin", "install", PLUGIN, "--scope", "user")
        installed = json.loads(run("claude", "plugin", "list", "--json"))[0]
        cache = Path(installed["installPath"])
        self.assertTrue(cache.is_relative_to(self.root / "claude"))
        self.assertEqual(snapshot(cache), snapshot(self.source))
        self.assert_preserved()
        inventory = run("claude", "plugin", "details", PLUGIN)
        self.assertIn("Skills (4)", inventory)
        for name in SKILLS:
            self.assertIn(name, inventory)
        # Local marketplaces load in place. Standalone --plugin-dir must also work
        # with the copied artifact when the original source is unavailable.
        hidden = self.root / "source-unavailable"
        self.source.rename(hidden)
        inventory = run("claude", "--plugin-dir", str(cache), "plugin", "details", "contextlean")
        self.assertIn("Skills (4)", inventory)
        hidden.rename(self.source)
        # Same-version updates keep the old cache: don't promise otherwise.
        (self.source / "README.md").write_text("Same-version change\n")
        run("claude", "plugin", "update", PLUGIN, "--scope", "user")
        self.assertNotEqual(
            (cache / "README.md").read_bytes(), (self.source / "README.md").read_bytes()
        )
        run("claude", "plugin", "marketplace", "update", "contextlean-local")
        run("claude", "plugin", "uninstall", PLUGIN, "--scope", "user")
        run("claude", "plugin", "install", PLUGIN, "--scope", "user")
        self.assertEqual(
            (cache / "README.md").read_bytes(), (self.source / "README.md").read_bytes()
        )
        self.assert_preserved()
        self.prepare_update()
        run("claude", "plugin", "update", PLUGIN, "--scope", "user")
        updated = json.loads(run("claude", "plugin", "list", "--json"))[0]
        self.assertEqual(updated["version"], "0.3.2-test")
        self.assertEqual(snapshot(Path(updated["installPath"])), snapshot(self.source))
        self.assert_preserved()
        run("claude", "plugin", "uninstall", PLUGIN, "--scope", "user")
        self.assertEqual(json.loads(run("claude", "plugin", "list", "--json")), [])
        run("claude", "plugin", "marketplace", "remove", "contextlean-local")
        self.assert_preserved()
