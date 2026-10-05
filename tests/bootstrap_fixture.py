"""Generate the representative Balanced fixture deterministically, without a model.

This is test scaffolding for one reviewed project map, not a general-purpose installer.
The product remains instruction-based; real bootstrap adapts guidance to its project.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_MAP = ROOT / "tests/fixtures/bootstrap-core/project-map.md"
CORE = ROOT / "skills/bootstrap/references/core-guidance.md"


def generate(repo):
    """Write only the two representative guidance files; return their paths."""
    repo = Path(repo)
    repo.mkdir(parents=True, exist_ok=True)
    # The reference's title identifies its setup role; the body is ordinary guidance.
    core = CORE.read_text(encoding="utf-8").split("\n\n", 1)[1]
    agents = repo / "AGENTS.md"
    agents.write_text(
        PROJECT_MAP.read_text(encoding="utf-8").rstrip() + "\n\n" + core,
        encoding="utf-8",
    )
    claude = repo / "CLAUDE.md"
    claude.write_text("@AGENTS.md\n", encoding="utf-8")
    return agents, claude
