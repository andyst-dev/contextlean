"""Build a fresh transfer receipt from the worked, semantically reviewed guidance."""

import hashlib
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/bootstrap-transfer"


def generate(repo, transfer):
    """Offline deterministic fixture application; never invokes an agent/model."""
    for name in ("AGENTS.md", "CLAUDE.md", "PROJECT_REFERENCE.md"):
        shutil.copyfile(FIXTURE / name, repo / name)
    inventory = json.loads(transfer.RULES.read_text())
    record = {"schema_version": 2, "rules": {}}

    def destination(facets, kind, path, section):
        owner = ROOT if kind == "contextlean_skill" else repo
        item = {
            "facets": facets,
            "kind": kind,
            "path": path,
            "section": section,
            "sha256": hashlib.sha256(
                transfer.section_text(owner / path, section).encode()
            ).hexdigest(),
        }
        if kind == "contextlean_skill":
            item["skill"] = "contextlean:lean-review"
        return item

    consolidated = {
        "cohesive-files-modules-classes": "Ownership",
        "no-fragmentation-wrappers": "Ownership",
        "specific-helper-owner": "Ownership",
        "practical-regression": "Verification",
        "smallest-meaningful": "Verification",
    }
    for group in inventory["groups"]:
        buckets = {}
        for facet, category in group["delivery"].items():
            if category == "C":
                key = ("contextlean_skill", "skills/lean-review/SKILL.md", "Review workflow")
            elif category == "D":
                key = ("reference", "PROJECT_REFERENCE.md", group["reference"]["heading"])
            else:
                section = consolidated[facet] if category == "E" else group["heading"]
                key = ("guidance", "AGENTS.md", section)
            buckets.setdefault(key, []).append(facet)
        items = []
        for (kind, path, section), facets in buckets.items():
            item = destination(facets, kind, path, section)
            if kind == "reference":
                activation_section = (
                    "Project Skills" if group["id"] == "project-skills" else "Ownership"
                )
                activation = destination([], "guidance", "AGENTS.md", activation_section)
                item["activation"] = {key: activation[key] for key in ("path", "section", "sha256")}
                item["activation"]["when"] = (
                    "creating/modifying project Skills"
                    if group["id"] == "project-skills"
                    else "architecture/refactoring decisions"
                )
            items.append(item)
        record["rules"][group["id"]] = {
            "facets": group["facets"],
            "semantics_reviewed": True,
            "destinations": items,
        }
    (repo / "transfer.json").write_text(json.dumps(record, indent=2) + "\n")
    return record
