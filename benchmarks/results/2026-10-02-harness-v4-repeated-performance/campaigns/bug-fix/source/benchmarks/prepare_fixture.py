#!/usr/bin/env python3
"""Offline validation and freezing of agent-authored benchmark guidance."""

import argparse
import importlib.util
import json
from pathlib import Path
import re
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "preparation_core", ROOT / "skills/benchmark/scripts/benchmark.py"
)
core = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(core)


def local_path(repo, name):
    path = Path(name)
    resolved = (repo / path).resolve()
    if path.is_absolute() or ".." in path.parts or not resolved.is_relative_to(repo.resolve()):
        raise core.BenchmarkError(f"map path must stay inside the fixture: {name}")
    if not resolved.exists():
        raise core.BenchmarkError(f"nonexistent mapped path: {name}")
    return resolved


def project_map(repo):
    """Require explicit `path`: responsibility entries, not inferred source paths."""
    text = (repo / "AGENTS.md").read_text(encoding="utf-8")
    match = re.search(r"^## Project map\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not match:
        raise core.BenchmarkError("fixture AGENTS.md requires a Project map section")
    entries = {}
    for line in match[1].splitlines():
        if "`" not in line:
            if line.lstrip().startswith("- "):
                raise core.BenchmarkError("map entries must use `path`: responsibility")
            continue
        pairs = re.findall(r"`([^`]+)`:\s*([^`]+)", line)
        if len(pairs) != len(re.findall(r"`([^`]+)`", line)):
            raise core.BenchmarkError("unparsed path in Project map")
        for name, description in pairs:
            if name in entries or not description.strip(" ;."):
                raise core.BenchmarkError(f"duplicate/empty mapped responsibility: {name}")
            local_path(repo, name)
            entries[name] = description.strip().rstrip("; ")
    if not entries:
        raise core.BenchmarkError("Project map has no explicit paths")
    if (repo / "CLAUDE.md").read_text(encoding="utf-8") != "@AGENTS.md\n":
        raise core.BenchmarkError("fixture Claude wrapper must import canonical AGENTS.md")
    instructions = {core.relative(p, repo) for p in core.instruction_files(repo)}
    if instructions != {"AGENTS.md", "CLAUDE.md"}:
        raise core.BenchmarkError("graded fixture requires only the two root instruction files")
    return entries


def validate(repo, review, baseline=None):
    """Check paths/state and bind the human responsibility review to source evidence.

    Natural-language ownership is reviewed by the preparing agent, not proved by
    this checker. Exact descriptions, evidence snippets and frozen hashes prevent
    silently reusing that review after changing the map or source.
    """
    repo = repo.resolve()
    entries = project_map(repo)
    non_instruction = core.tree_digest(repo, True)
    if baseline is not None and non_instruction != core.tree_digest(baseline.resolve(), True):
        raise core.BenchmarkError("prepared fixture differs outside agent guidance")
    if review.get("semantics_reviewed") is not True or set(review.get("entries", {})) != set(
        entries
    ):
        raise core.BenchmarkError("every mapped responsibility requires an explicit source review")
    for name, description in entries.items():
        item = review["entries"][name]
        if item.get("responsibility") != description or not item.get("evidence"):
            raise core.BenchmarkError(f"missing/changed responsibility review: {name}")
        owner = local_path(repo, name)
        for evidence in item["evidence"]:
            path = local_path(repo, evidence["path"])
            if path != owner and not (owner.is_dir() and path.is_relative_to(owner)):
                raise core.BenchmarkError(f"review evidence is outside mapped owner: {name}")
            snippet = evidence.get("contains")
            if not isinstance(snippet, str) or not snippet or snippet not in path.read_text():
                raise core.BenchmarkError(f"responsibility evidence not found: {name}")
    return {
        "schema_version": 1,
        "contextlean_digest": core.tree_digest(repo),
        "vanilla_digest": non_instruction,
        "baseline_non_instruction_digest": non_instruction,
        "review": review,
    }


def freeze(baseline, prepared, review, output, record_path):
    """Validate before copying; retain only reviewed, equivalent fixture state."""
    if output.exists() or record_path.exists():
        raise core.BenchmarkError("frozen fixture and preparation record must be new paths")
    for source in (baseline, prepared):
        if output.resolve().is_relative_to(
            source.resolve()
        ) or record_path.resolve().is_relative_to(source.resolve()):
            raise core.BenchmarkError("freeze output/record must stay outside preparation inputs")
    record = validate(prepared, review, baseline)
    if record_path.resolve().is_relative_to(output.resolve()):
        raise core.BenchmarkError("preparation record must stay outside measured fixture")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="contextlean-freeze-", dir=output.parent) as tmp:
        frozen = Path(tmp) / "repo"
        core.copy_repository(prepared, frozen)
        if validate(frozen, review, baseline) != record:
            raise core.BenchmarkError("fixture changed while freezing")
        frozen.rename(output)
    core.write_json(record_path, record)
    return record


def validate_frozen(repo, record_path, expected=None):
    if record_path is None:
        raise core.BenchmarkError("offline preparation record required before live execution")
    record = core.read_json(record_path)
    if not isinstance(record, dict):
        raise core.BenchmarkError("preparation record must be a JSON object")
    if expected is not None and record != expected:
        raise core.BenchmarkError("preparation record changed during the batch")
    current = validate(repo, record.get("review", {}))
    if record != current:
        raise core.BenchmarkError("frozen fixture or preparation review has changed")
    return current


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--prepared", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--record", type=Path, required=True)
    args = parser.parse_args()
    try:
        record = freeze(
            args.baseline, args.prepared, core.read_json(args.review), args.output, args.record
        )
        print(json.dumps(record, indent=2))
        return 0
    except (core.BenchmarkError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"preparation rejected: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
