#!/usr/bin/env python3
"""Explicit legacy transfer check; not a Balanced bootstrap prerequisite."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
RULES = PLUGIN_ROOT / "tests/fixtures/bootstrap-transfer/permanent-rules.json"
SPEC_NAMES = {"AGENT_BOOTSTRAP.md", "bootstrap-spec.md", "permanent-rules.json"}


def section_text(path, heading):
    text = path.read_text(encoding="utf-8")
    if not heading:
        return text
    lines = text.splitlines(keepends=True)
    start = None
    level = 0
    for index, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not match:
            continue
        if start is not None and len(match[1]) <= level:
            return "".join(lines[start:index])
        if match[2] == heading:
            start, level = index + 1, len(match[1])
    if start is None:
        raise ValueError(f"missing destination section: {heading}")
    return "".join(lines[start:])


def local_file(root, name):
    path = Path(name)
    if path.is_absolute():
        raise ValueError("destination must be relative")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root) or not resolved.is_file():
        raise ValueError("destination must resolve to a file inside its repository/plugin")
    return resolved


def reachable_guidance(repo):
    """Follow explicit local links/imports; ignore the removable setup specifications."""
    pending = [repo / "AGENTS.md"]
    visited = set()
    while pending:
        path = pending.pop().resolve()
        if path in visited or path.name in SPEC_NAMES or not path.is_file():
            continue
        if not path.is_relative_to(repo) or ".contextlean" in path.relative_to(repo).parts:
            continue
        visited.add(path)
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)
        links += re.findall(r"^@([^\s]+)\s*$", text, re.MULTILINE)
        for link in links:
            name = link.split("#")[0]
            if name and not re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", name):
                pending.append(path.parent / name)
    return visited


def automatic_guidance(repo):
    """Root/nested maps and Claude wrappers load automatically; links do not."""
    repo = repo.resolve()
    pending = list(repo.rglob("AGENTS.md")) + list(repo.rglob("CLAUDE.md"))
    visited = set()
    while pending:
        path = pending.pop().resolve()
        if path in visited or not path.is_file() or not path.is_relative_to(repo):
            continue
        if ".contextlean" in path.relative_to(repo).parts:
            continue
        visited.add(path)
        for name in re.findall(r"^@([^\s]+)\s*$", path.read_text(), re.MULTILINE):
            pending.append(path.parent / name)
    return visited


def reviewed_content(path, item):
    content = section_text(path, item.get("section", ""))
    if not content.strip() or hashlib.sha256(content.encode()).hexdigest() != item.get("sha256"):
        raise ValueError("reviewed destination is missing or changed")
    return content


def verify_destination(repo, plugin, reachable, automatic, group_id, item, conditional):
    kind = item.get("kind")
    if kind == "contextlean_skill":
        # Optional review cannot carry normal implementation obligations.
        if group_id != "lean-review" or item.get("skill") != "contextlean:lean-review":
            raise ValueError("unsupported packaged Skill delegation")
        if not any(
            "contextlean:lean-review" in p.read_text() for p in automatic if p.suffix == ".md"
        ):
            raise ValueError("Lean Review delegation is not documented in automatic guidance")
        path = local_file(plugin, item["path"])
        if path != plugin / "skills/lean-review/SKILL.md":
            raise ValueError("Lean Review destination must be the packaged workflow")
    elif kind in {"guidance", "configuration", "reference", "project_skill"}:
        path = local_file(repo, item["path"])
        if path not in reachable:
            raise ValueError(f"destination is not reachable without bootstrap context: {group_id}")
        if kind == "reference" and conditional:
            if path in automatic:
                raise ValueError("conditional reference must not be automatic startup context")
            activation = item.get("activation", {})
            source = local_file(repo, activation.get("path", ""))
            if source not in automatic or not activation.get("when", "").strip():
                raise ValueError("conditional reference requires an automatic applicability rule")
            route = reviewed_content(source, activation)
            links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", route)
            if not any((source.parent / link.split("#")[0]).resolve() == path for link in links):
                raise ValueError("applicability rule must link to its conditional reference")
    else:
        raise ValueError("unknown durable destination kind")
    if path.name in SPEC_NAMES:
        raise ValueError("setup specification is not a durable destination")
    reviewed_content(path, item)


def verify(repo, record, plugin=PLUGIN_ROOT):
    repo, plugin = repo.resolve(), plugin.resolve()
    groups = json.loads(RULES.read_text(encoding="utf-8"))["groups"]
    expected = {group["id"]: set(group["facets"]) for group in groups}
    version = record.get("schema_version")
    if version not in {1, 2} or set(record.get("rules", {})) != set(expected):
        raise ValueError("transfer record must cover every permanent rule group exactly once")
    reachable = reachable_guidance(repo)
    if repo / "AGENTS.md" not in reachable:
        raise ValueError("canonical project AGENTS.md is required")
    automatic = automatic_guidance(repo)
    destinations = set()
    for group_id, facets in expected.items():
        item = record["rules"][group_id]
        declared = item.get("facets", [])
        if len(declared) != len(set(declared)) or set(declared) != facets:
            raise ValueError(f"incomplete semantic review: {group_id}")
        if item.get("semantics_reviewed") is not True:
            raise ValueError(f"semantic review not attested: {group_id}")
        items = item.get("destinations", []) if version == 2 else [item]
        assigned = [facet for destination in items for facet in destination.get("facets", [])]
        if len(assigned) != len(set(assigned)) or set(assigned) != facets:
            raise ValueError(f"destinations must cover each facet exactly once: {group_id}")
        for destination in items:
            if not destination.get("facets"):
                raise ValueError("destination must carry at least one facet")
            verify_destination(
                repo, plugin, reachable, automatic, group_id, destination, version == 2
            )
            destinations.add(destination["path"])
    return {
        "groups": len(expected),
        "facets": sum(map(len, expected.values())),
        "destinations": sorted(destinations),
        "setup_specification_required": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    try:
        record = args.record or args.repo / ".contextlean/bootstrap-transfer.json"
        result = verify(args.repo, json.loads(record.read_text(encoding="utf-8")))
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"bootstrap incomplete: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
