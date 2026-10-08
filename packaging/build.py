"""Export the canonical Skills as a small, dependency-free distribution ZIP."""

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]


def package_files(root=ROOT):
    """Explicit inputs keep private files, caches and evidence out of the artifact."""
    root = Path(root).resolve()
    paths = {
        "README.md": root / "packaging/README.md",
        "LICENSE": root / "LICENSE",
        "docs/privacy.md": root / "docs/privacy.md",
        "docs/assets/contextlean.svg": root / "docs/assets/contextlean.svg",
        "benchmarks/README.md": root / "packaging/benchmark-suite.md",
    }
    for name in (
        ".codex-plugin/plugin.json",
        ".claude-plugin/plugin.json",
        ".claude-plugin/marketplace.json",
    ):
        paths[name] = root / name
    resources = {
        "bootstrap": ("references/bootstrap-spec.md", "references/core-guidance.md"),
        "audit": (),
        "lean-review": ("references/architecture.md",),
        "benchmark": (
            "scripts/benchmark.py",
            "data/credit-rates.json",
            "references/methodology.md",
            "references/static-capture.md",
        ),
    }
    for name, extra in resources.items():
        folder = root / "skills" / name
        for relative in ("SKILL.md", "agents/openai.yaml", *extra):
            path = folder / relative
            paths[path.relative_to(root).as_posix()] = path
    for path in paths.values():
        if (
            any(p.is_symlink() for p in (path, *path.parents) if p.is_relative_to(root))
            or not path.is_file()
            or not path.resolve().is_relative_to(root.resolve())
        ):
            raise ValueError(f"Invalid package input: {path}")
    return paths


def build(output, root=ROOT):
    paths = package_files(root)
    # Exclusive creation avoids replacing an existing release artifact.
    with ZipFile(output, "x", compression=ZIP_DEFLATED) as archive:
        for name, path in sorted(paths.items()):
            info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="New ZIP path, preferably outside the checkout")
    build(parser.parse_args().output)
