"""Reconcile and regrade compact-final public evidence without model calls."""

import hashlib
import importlib.util
import json
from pathlib import Path
import stat
import tempfile
import zipfile


DATA = Path(__file__).resolve().parent
KEYS = (
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "total_tokens",
    "duration_seconds",
    "command_calls",
)


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extract(name, destination):
    with zipfile.ZipFile(DATA / name) as archive:
        for member in archive.infolist():
            path = Path(member.filename)
            assert not path.is_absolute() and ".." not in path.parts
            assert not stat.S_ISLNK(member.external_attr >> 16)
            assert not any(
                part in {".DS_Store", "__pycache__", ".ruff_cache", ".venv"} for part in path.parts
            )
        archive.extractall(destination)


def main():
    checksums = read(DATA / "checksums.json")
    observed = {
        p.relative_to(DATA).as_posix(): sha(p)
        for p in DATA.rglob("*")
        if p.is_file() and p.name != "checksums.json" and "__pycache__" not in p.parts
    }
    assert checksums == observed, "Artifact set/checksum mismatch"
    report, review = read(DATA / "summary.json"), read(DATA / "measurement-review.json")
    assert report["product_commit"] == "90ed9a4a049af519a40c36424ed1ff8b6acefe48"
    assert report["model"] == "gpt-5.6-terra" and report["reasoning"] == "low"
    assert report["new_live_runs"] == 8 and report["bug_fix_reruns"] == 0 and report["repeats"] == 1
    assert len(report["runs"]) == 10 and len(review["regrading"]) == 10
    assert len(read(DATA / "call-journal.json")) == 8
    imported = read(DATA / "bug-fix/provenance.json")["imported_raw_sha256"]
    for name, expected in imported.items():
        assert sha(DATA / name) == expected
    with tempfile.TemporaryDirectory(prefix="compact-offline-evidence-") as temporary:
        root = Path(temporary)
        source, solutions, fixtures = root / "source", root / "solutions", root / "fixtures"
        for name, target in (
            ("source-snapshot.zip", source),
            ("solutions.zip", solutions),
            ("fixtures.zip", fixtures),
        ):
            extract(name, target)
        selection = read(DATA / "source-selection.json")
        retained = {
            p.relative_to(source).as_posix(): sha(p) for p in source.rglob("*") if p.is_file()
        }
        assert retained == selection["retained_files"]
        assert all(
            selection["frozen_commit_files"][name] == value for name, value in retained.items()
        )
        runner = load("frozen_evidence_runner", source / "benchmarks/run_benchmark.py")
        core, prep = runner.core, runner.preparation
        original_digest = core.tree_digest

        def product_digest(repo, ignore_instructions=False):
            if not ignore_instructions:
                return original_digest(repo)
            digest = hashlib.sha256()
            for path in core.iter_project_files(repo):
                relative = core.relative(path, repo)
                if path.name in core.INSTRUCTION_NAMES or relative == "PROJECT_REFERENCE.md":
                    continue
                digest.update(relative.encode() + b"\0" + path.read_bytes() + b"\0")
            return digest.hexdigest()

        core.tree_digest = product_digest
        core.execute_run = lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("Model calls forbidden during evidence verification")
        )
        tasks = read(source / "benchmarks/tasks/suite.json")["tasks"]
        assert report["tasks"] == [
            {**task, "executed_prompt": runner.task_prompt(task)} for task in tasks
        ]
        assert sha(source / "benchmarks/tasks/suite.json") == report["task_suite_digest"]
        assert sha(source / "benchmarks/evaluate.py") == report["evaluator_digest"]
        expected_pairs = {
            (task["id"], condition) for task in tasks for condition in ("vanilla", "contextlean")
        }
        assert {(r["task"], r["condition"]) for r in report["runs"]} == expected_pairs
        transfer = load(
            "frozen_evidence_transfer", source / "skills/bootstrap/scripts/verify_transfer.py"
        )
        for task in tasks:
            task_id = task["id"]
            directory = (
                DATA / "bug-fix" if task_id == "bug-fix" else DATA / "preparations" / task_id
            )
            fixture = fixtures / task_id / "contextlean"
            evidence = read(directory / "preflight.json")
            record = read(directory / "preparation.json")
            assert sha(directory / "preparation.json") == evidence["preparation_sha256"]
            assert prep.validate_frozen(fixture, directory / "preparation.json") == record
            assert (
                transfer.verify(fixture, read(directory / "transfer.json"), source)
                == evidence["transfer"]
            )
            assert evidence["transfer"]["facets"] == 71
            for condition in ("vanilla", "contextlean"):
                initial = fixtures / task_id / condition
                assert core.tree_digest(initial) == evidence["fixtures"][condition]["digest"]
                for name in evidence["fixtures"][condition]["mapped_paths"]:
                    prep.local_path(initial, name)
                assert core.tree_digest(initial, True) == record["baseline_non_instruction_digest"]
        thread_ids = set()
        for run in report["runs"]:
            task_id, condition = run["task"], run["condition"]
            raw = DATA / run["raw_directory"]
            parsed = core.parse_jsonl((raw / "events.jsonl").read_text())
            raw_record = read(raw / "run.json")
            for key in KEYS:
                assert raw_record["metrics"][key] == run["metrics"][key]
            for key, value in parsed["usage"].items():
                if key != "cache_write_input_tokens":
                    assert run["metrics"][key] == value
            assert parsed["success"] == run["execution_success"]
            assert parsed["commands"] == run["metrics"]["command_calls"]
            assert (
                run["metrics"]["total_tokens"]
                == run["metrics"]["input_tokens"] + run["metrics"]["output_tokens"]
            )
            assert all(
                run["metrics"][key] is None
                for key in ("tool_calls", "file_reads", "unique_files_inspected")
            )
            for event in [
                json.loads(line) for line in (raw / "events.jsonl").read_text().splitlines() if line
            ]:
                if event.get("type") == "thread.started":
                    assert event["thread_id"] not in thread_ids
                    thread_ids.add(event["thread_id"])
            fixture = fixtures / task_id / condition
            runner.FIXTURE = fixtures / task_id / "contextlean"
            solution = solutions / f"{task_id}-1-{condition}" / "solution"
            assert core.tree_digest(solution) == run["solution_digest"]
            if task_id == "navigation":
                assert core.tree_digest(solution) == core.tree_digest(fixture)
            for name in ("AGENTS.md", "CLAUDE.md", "PROJECT_REFERENCE.md", "data/sample.csv"):
                if (fixture / name).exists():
                    assert (solution / name).read_bytes() == (fixture / name).read_bytes()
                else:
                    assert not (solution / name).exists()
            graded = runner.grade(
                {"id": task_id}, solution, parsed, root / "regrade" / f"{task_id}-{condition}"
            )
            assert graded == run["evaluation"] == run["offline_regrade"]
        assert len(thread_ids) == 10
        for condition in ("vanilla", "contextlean"):
            selected = [r for r in report["runs"] if r["condition"] == condition]
            for key in KEYS:
                assert (
                    sum(r["metrics"][key] for r in selected)
                    == review["aggregate"][condition][key]
                    == report["aggregate"][condition][key]
                )
        rate = core.find_rate(review["rate_card"], report["model"])
        assert (
            abs(
                sum(core.calculate_credits(r["metrics"], rate) for r in report["runs"])
                - review["total_compact_credit_equivalent"]
            )
            < 1e-10
        )
        assert (
            abs(
                sum(
                    core.calculate_credits(r["metrics"], rate)
                    for r in report["runs"]
                    if r["task"] != "bug-fix"
                )
                - review["new_eight_credit_equivalent"]
            )
            < 1e-10
        )
        for task in tasks:
            pair = {r["condition"]: r["metrics"] for r in report["runs"] if r["task"] == task["id"]}
            expected = [
                key
                for key in ("total_tokens", "duration_seconds", "command_calls")
                if pair["contextlean"][key] > pair["vanilla"][key]
            ]
            assert expected == review["negative_cases"][task["id"]]
        assert review["headline_eligible"] == all(
            r["evaluation"]["task_success"] for r in report["runs"]
        )
        assert read(DATA / "comparison.json")["datasets_pooled"] is False
    print(
        f"PASS: {len(checksums)} checksums, frozen source/fixtures/71 facets, ten unique conversations, all metrics, costs and ten independent offline regrades; zero model calls."
    )


if __name__ == "__main__":
    main()
