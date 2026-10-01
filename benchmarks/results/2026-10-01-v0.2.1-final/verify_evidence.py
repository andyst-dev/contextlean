#!/usr/bin/env python3
"""Reconcile this public evidence offline. Optional --regrade never starts a model."""

import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

BASE = Path(__file__).resolve().parent
GUIDANCE = {"AGENTS.md", "CLAUDE.md", "PROJECT_REFERENCE.md"}


def read(path):
    return json.loads(path.read_text())


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extract(path, destination):
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            member = Path(info.filename)
            assert not member.is_absolute() and ".." not in member.parts
            assert ((info.external_attr >> 16) & 0o170000) != 0o120000
        archive.extractall(destination)


def reconcile(regrade=False):
    checks = read(BASE / "checksums.json")
    observed = {
        p.relative_to(BASE).as_posix()
        for p in BASE.rglob("*")
        if p.is_file() and p.name != "checksums.json" and "__pycache__" not in p.parts
    }
    assert observed == set(checks)
    for name, expected in checks.items():
        assert hashlib.sha256((BASE / name).read_bytes()).hexdigest() == expected, name
    for item in read(BASE / "patch-compression.json").values():
        content = gzip.decompress((BASE / item["stored_as"]).read_bytes())
        assert hashlib.sha256(content).hexdigest() == item["uncompressed_sha256"]
    report = read(BASE / "summary.json")
    preflight = read(BASE / "preparation.json")
    assert report["release_commit"] == "44ee6f227dfead62406326a1306f897358f1778f"
    assert (
        report["expected_sessions"]
        == report["completed_sessions"]
        == len(report["runs"])
        == len(read(BASE / "call-ledger.json"))
        == 18
    )
    assert len({(r["provider"], r["task"], r["condition"]) for r in report["runs"]}) == 18
    assert len(preflight["pairs"]) == 9
    assert [r["sequence"] for r in report["runs"]] == list(range(1, 19))
    with tempfile.TemporaryDirectory(prefix="contextlean-evidence-check-") as tmp:
        tmp = Path(tmp)
        source, solutions, preparation = [
            tmp / name for name in ["source", "solutions", "preparation"]
        ]
        extract(BASE / "source-snapshot.zip", source)
        extract(BASE / "solutions.zip", solutions)
        extract(BASE / "preparation.zip", preparation)
        assert {
            p.relative_to(source).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in source.rglob("*")
            if p.is_file()
        } == read(BASE / "source-hashes.json")
        runner = load("frozen_campaign_runner", source / "benchmarks/run_benchmark.py")
        core, prep = runner.core, runner.preparation
        original_digest = core.tree_digest

        def digest(root, ignore_instructions=False):
            if not ignore_instructions:
                return original_digest(root)
            h = hashlib.sha256()
            for p in core.iter_project_files(root):
                name = core.relative(p, root)
                if name in GUIDANCE or p.name in core.INSTRUCTION_NAMES:
                    continue
                h.update(name.encode() + b"\0" + p.read_bytes() + b"\0")
            return h.hexdigest()

        core.tree_digest = digest
        transfer = load(
            "frozen_campaign_transfer", source / "skills/bootstrap/scripts/verify_transfer.py"
        )
        for pair in preflight["pairs"]:
            base = preparation / f"{pair['provider']}-{pair['task']['id']}"
            assert read(base / "preflight.json") == pair
            assert (
                hashlib.sha256((base / "preparation.json").read_bytes()).hexdigest()
                == pair["preparation_sha256"]
            )
            prep.validate_frozen(base / "validated-contextlean", base / "preparation.json")
            assert (
                transfer.verify(base / "fixtures/contextlean", read(base / "transfer.json"))
                == pair["transfer"]
            )
            assert (
                pair["transfer"]["facets"] == 71
                and pair["transfer"]["setup_specification_required"] is False
            )
            assert runner.task_prompt(pair["task"]) == (base / "prompt.txt").read_text()
            for condition in ["vanilla", "contextlean"]:
                fixture = base / "fixtures" / condition
                state = pair["fixtures"][condition]
                assert (
                    digest(fixture) == state["digest"]
                    and digest(fixture, True) == state["product_digest"]
                )
                assert (fixture / ".git").is_dir()
                for args, expected in [
                    (["status", "--short"], ""),
                    (["diff", "--"], ""),
                    (["diff", "--", "expense_report/report.py", "tests/test_expenses.py"], ""),
                    (["rev-parse", "HEAD"], state["git"]["head"]),
                    (["rev-parse", "HEAD^{tree}"], state["git"]["tree"]),
                ]:
                    actual = subprocess.check_output(
                        ["git", "-c", "safe.directory=*", *args], cwd=fixture, text=True
                    ).strip()
                    assert actual == expected
        for run in report["runs"]:
            out = BASE / run["raw_directory"]
            assert read(out / "run.json") == run
            execution = read(out / "execution.json")
            events = [json.loads(line) for line in (out / "events.jsonl").read_text().splitlines()]
            if run["provider"] == "claude":
                result = next(e for e in reversed(events) if e["type"] == "result")
                usage = result["usage"]
                parsed = {
                    "input_tokens": usage["input_tokens"]
                    + usage.get("cache_creation_input_tokens", 0)
                    + usage.get("cache_read_input_tokens", 0),
                    "cached_input_tokens": usage.get("cache_read_input_tokens", 0),
                    "output_tokens": usage["output_tokens"],
                }
                calls = {
                    b["id"]: b
                    for e in events
                    if e.get("type") == "assistant"
                    for b in e.get("message", {}).get("content", [])
                    if b.get("type") == "tool_use"
                }
                commands = sum(b["name"] == "Bash" for b in calls.values())
                assert (
                    result["total_cost_usd"]
                    == execution["reported_cost_usd"]
                    == run["reported_cost_usd"]
                )
                assert run["metrics"]["file_read_tool_calls"] == sum(
                    b["name"] == "Read" for b in calls.values()
                )
                assert run["metrics"]["total_tool_calls"] == len(calls)
            else:
                parsed_result = core.parse_jsonl((out / "events.jsonl").read_text())
                parsed, commands = parsed_result["usage"], parsed_result["commands"]
                assert parsed_result["success"] == execution["success"]
                assert (
                    run["metrics"]["file_read_tool_calls"] is None
                    and run["metrics"]["total_tool_calls"] is None
                )
            assert parsed == execution["usage"]
            metrics = run["metrics"]
            assert commands == execution["commands"] == metrics["command_calls"]
            assert metrics["duration_seconds"] == execution["duration_seconds"]
            if parsed:
                for key in ["input_tokens", "cached_input_tokens", "output_tokens"]:
                    assert metrics[key] == parsed[key]
                assert metrics["total_tokens"] == parsed["input_tokens"] + parsed["output_tokens"]
                assert (
                    metrics["uncached_input_tokens"]
                    == parsed["input_tokens"] - parsed["cached_input_tokens"]
                )
            else:
                assert run["sequence"] == 9 and not run["execution_success"]
                assert all(
                    metrics[key] is None
                    for key in [
                        "input_tokens",
                        "cached_input_tokens",
                        "uncached_input_tokens",
                        "output_tokens",
                        "total_tokens",
                    ]
                )
                assert any(
                    e.get("type") == "turn.failed"
                    and "usage limit" in e.get("error", {}).get("message", "")
                    for e in events
                )
            assert (
                run["offline_regrade"]
                == read(BASE / run["offline_regrade_directory"] / "result.json")
                == run["evaluation"]
            )
            solution = solutions / run["solution_archive_directory"]
            assert digest(solution) == run["solution_digest"]
            if regrade:
                pair = next(
                    p
                    for p in preflight["pairs"]
                    if p["provider"] == run["provider"] and p["task"]["id"] == run["task"]
                )
                runner.FIXTURE = (
                    preparation / f"{run['provider']}-{run['task']}" / "fixtures" / run["condition"]
                )
                grade = runner.grade(
                    pair["task"], solution, execution, tmp / "regrade" / solution.name
                )
                assert grade == run["offline_regrade"]
            assert run["offline_regrade"]["task_success"] == bool(
                run["execution_success"]
                and run["offline_regrade"]["tests_passed"]
                and run["offline_regrade"]["agent_tests_passed"]
                and run["offline_regrade"]["acceptance_passed"]
            )
        assert sum(r["offline_regrade"]["task_success"] for r in report["runs"]) == 17
        assert not report["all_grades_pass"]
        for provider, groups in report["aggregates"].items():
            for condition, total in groups.items():
                selected = [
                    r
                    for r in report["runs"]
                    if r["provider"] == provider and r["condition"] == condition
                ]
                for key in [
                    "input_tokens",
                    "cached_input_tokens",
                    "uncached_input_tokens",
                    "output_tokens",
                    "total_tokens",
                    "duration_seconds",
                    "command_calls",
                ]:
                    expected = (
                        sum(r["metrics"][key] for r in selected)
                        if all(r["metrics"][key] is not None for r in selected)
                        else None
                    )
                    assert total[key] == expected
        assert len([r for r in report["runs"] if r["provider"] == "terra"]) == 10
        assert len([r for r in report["runs"] if r["provider"] == "claude"]) == 4
        assert len([r for r in report["runs"] if r["provider"] == "sol"]) == 4
    return {
        "sessions": 18,
        "valid_usage_sessions": 17,
        "provider_failed_sessions": [9],
        "solution_test_checks": "18/18 all three checks",
        "overall_success": "17/18",
        "checksums": len(checks),
        "fresh_git_pairs": 9,
        "facet_preservation": "71/71",
        "regraded_again": regrade,
        "model_calls": 0,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--regrade",
        action="store_true",
        help="Independently rerun frozen offline graders on saved solutions",
    )
    args = parser.parse_args()
    print(json.dumps(reconcile(args.regrade), indent=2))


if __name__ == "__main__":
    main()
