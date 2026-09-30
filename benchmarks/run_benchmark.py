#!/usr/bin/env python3
"""Opt-in, graded Codex benchmark on an offline public sample repository."""

import argparse
import hashlib
import importlib.util
import os
from pathlib import Path
import platform
import shutil
import statistics
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "contextlean_benchmark", ROOT / "skills/benchmark/scripts/benchmark.py"
)
core = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(core)
PREPARATION_SPEC = importlib.util.spec_from_file_location(
    "fixture_preparation", ROOT / "benchmarks/prepare_fixture.py"
)
preparation = importlib.util.module_from_spec(PREPARATION_SPEC)
PREPARATION_SPEC.loader.exec_module(preparation)
# Share the existing copier/digests/error type with the suite's measurement helper.
preparation.core = core
FIXTURE = ROOT / "benchmarks/fixtures/expense-report"
TASKS = ROOT / "benchmarks/tasks/suite.json"


def load_suite(path):
    suite = core.read_json(path)
    tasks = suite.get("tasks", [])
    ids = [task.get("id") for task in tasks]
    allowed = {"navigation", "bug-fix", "feature", "refactor", "documentation-config"}
    if not tasks or len(ids) != len(set(ids)) or any(task_id not in allowed for task_id in ids):
        raise core.BenchmarkError("suite must contain unique supported task ids")
    if any(not isinstance(task.get("prompt"), str) or not task["prompt"].strip() for task in tasks):
        raise core.BenchmarkError("every task requires a nonempty prompt")
    return tasks


def task_prompt(task):
    return (
        "Work only in this local sample repository. Do not use network services, "
        "install dependencies or change agent guidance. "
        "Use the existing standard-library tests.\n\n" + task["prompt"]
    )


def capture(command, workspace, timeout=60):
    try:
        result = subprocess.run(
            command,
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
        )
        return result.returncode == 0, result.stdout + result.stderr
    except (subprocess.TimeoutExpired, OSError) as error:
        return False, type(error).__name__


def grade(task, workspace, result, artifact_dir):
    # Evaluate another copy, with original tests restored. Agent edits cannot weaken
    # the regression suite, and evaluation cannot contaminate measured artifacts.
    with tempfile.TemporaryDirectory(prefix="contextlean-evaluation-") as temporary:
        evaluation = Path(temporary) / "repo"
        if any(path.is_symlink() for path in workspace.rglob("*")):
            return {
                "tests_passed": False,
                "acceptance_passed": False,
                "task_success": False,
                "error": "unexpected symlink in measured workspace",
            }
        core.copy_repository(workspace, evaluation)
        agent_tests, agent_log = capture(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], evaluation
        )
        shutil.rmtree(evaluation / "tests", ignore_errors=True)
        shutil.copytree(FIXTURE / "tests", evaluation / "tests")
        response = Path(temporary) / "response.txt"
        response.write_text(result.get("final_response", ""), encoding="utf-8")
        regression, regression_log = capture(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], evaluation
        )
        accepted, acceptance_log = capture(
            [
                sys.executable,
                str(ROOT / "benchmarks/evaluate.py"),
                task["id"],
                str(evaluation),
                str(response),
            ],
            evaluation,
        )

        def clean(text):
            return (
                text.replace(str(evaluation), "<workspace>")
                .replace(str(ROOT), "<contextlean>")
                .replace(str(Path.home()), "<home>")
            )

        artifact_dir.mkdir(parents=True, exist_ok=True)
        (artifact_dir / "evaluation.txt").write_text(
            clean(agent_log + "\n" + regression_log + "\n" + acceptance_log), encoding="utf-8"
        )
        return {
            "tests_passed": regression,
            "agent_tests_passed": agent_tests,
            "acceptance_passed": accepted,
            "task_success": bool(result["success"] and regression and agent_tests and accepted),
        }


def distribution(values):
    return (
        {
            "median": statistics.median(values),
            "mean": statistics.mean(values),
            "min": min(values),
            "max": max(values),
        }
        if values
        else None
    )


def summarize(runs, tasks, repeats):
    summary = []
    for task in tasks:
        entry = {"task": task["id"], "category": task["category"]}
        for condition in ("vanilla", "contextlean"):
            selected = [
                run for run in runs if run["task"] == task["id"] and run["condition"] == condition
            ]
            metrics = {}
            for key in (
                "input_tokens",
                "cached_input_tokens",
                "output_tokens",
                "total_tokens",
                "command_calls",
                "duration_seconds",
            ):
                values = [
                    run["metrics"][key] for run in selected if run["metrics"].get(key) is not None
                ]
                metrics[key] = distribution(values)
            entry[condition] = {
                "runs": len(selected),
                "expected_runs": repeats,
                "task_successes": sum(run["evaluation"]["task_success"] for run in selected),
                "metrics": metrics,
            }
        summary.append(entry)
    return summary


def render(report):
    lines = [
        "# ContextLean benchmark validation batch",
        "",
        "Validation only. Not a published performance benchmark.",
        "",
        f"Model: `{report['model']}` · reasoning: `{report['reasoning']}` · repeats: {report['repeats']}",
        f"Completed runs: {len(report['runs'])}/{report['expected_runs']}",
        "",
        "| Task | Condition | Task success | Regression tests | Input | Cached | Output | Total | Commands | Seconds |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for run in report["runs"]:
        metric, evaluation = run["metrics"], run["evaluation"]
        values = [
            metric.get(key)
            for key in (
                "input_tokens",
                "cached_input_tokens",
                "output_tokens",
                "total_tokens",
                "command_calls",
            )
        ]
        fields = " | ".join("unavailable" if value is None else str(value) for value in values)
        lines.append(
            f"| {run['task']} | {run['condition']} | {'pass' if evaluation['task_success'] else 'fail'} | {'pass' if evaluation['tests_passed'] else 'fail'} | {fields} | {metric['duration_seconds']:.2f} |"
        )
    lines.extend(
        [
            "",
            report["result"],
            "",
            "## Per-task medians and ranges",
            "",
            "Every run is retained, including incorrect solutions and failed executions.",
            "",
            "| Task | Condition | Successes / runs | Total tokens median [min, max] | Seconds median [min, max] |",
            "|---|---|---:|---:|---:|",
        ]
    )
    for task in report["summary"]:
        for condition in ("vanilla", "contextlean"):
            item = task[condition]

            def span(key):
                value = item["metrics"][key]
                return (
                    "unavailable"
                    if value is None
                    else f"{value['median']:.2f} [{value['min']:.2f}, {value['max']:.2f}]"
                )

            lines.append(
                f"| {task['task']} | {condition} | {item['task_successes']}/{item['runs']} | {span('total_tokens')} | {span('duration_seconds')} |"
            )
    lines.extend(
        [
            "",
            "File reads, unique files inspected and total tool calls: unavailable from the current CLI event contract.",
            "Command calls are unique command_execution events, not all tool calls. No inferred file counts are presented.",
            "Cached input is a subset of input. Total is input + output. Missing reasoning-token fields remain null.",
            "One repetition cannot establish variance or statistical confidence.",
            "",
        ]
    )
    return "\n".join(lines)


def run(args):
    tasks = load_suite(args.tasks_file)
    if args.repeat < 1 or args.timeout < 1:
        raise core.BenchmarkError("repeat and timeout must be positive")
    output = args.output_dir.resolve()
    if output.is_relative_to(FIXTURE):
        raise core.BenchmarkError("reports must be outside the source fixture")
    if output.exists() and any(output.iterdir()):
        raise core.BenchmarkError(
            "output directory must be empty; prior runs must not be overwritten"
        )
    # Fail before CLI probing, snapshots or any paid model call.
    prepared_record = preparation.validate_frozen(
        FIXTURE, getattr(args, "preparation_record", None)
    )
    source_digest = core.tree_digest(FIXTURE)
    suite_digest = hashlib.sha256(args.tasks_file.read_bytes()).hexdigest()
    version_ok, version = capture([args.codex, "--version"], ROOT)
    if not version_ok:
        raise core.BenchmarkError("Codex CLI is not available")
    _, commit = capture(["git", "rev-parse", "HEAD"], ROOT)
    _, dirty = capture(["git", "status", "--porcelain"], ROOT)
    # Snapshot the full candidate for reproducing validation before it is committed.
    output.mkdir(parents=True, exist_ok=True)
    snapshot = output / "candidate"
    shutil.copytree(
        ROOT,
        snapshot,
        ignore=lambda directory, names: {
            name
            for name in names
            if name in core.COPY_SKIP_NAMES or (Path(directory) / name).resolve() == output
        },
    )
    preparation.validate_frozen(
        snapshot / "benchmarks/fixtures/expense-report", args.preparation_record, prepared_record
    )
    core.write_json(output / "preparation.json", prepared_record)
    report = {
        "schema_version": 1,
        "kind": "contextlean-graded-validation",
        "status": "validation-only",
        "contextlean_version": core.CONTEXTLEAN_VERSION,
        "started_at": core.utc_now(),
        "model": args.model,
        "reasoning": args.reasoning,
        "repeats": args.repeat,
        "expected_runs": len(tasks) * args.repeat * 2,
        "codex_cli_version": version.strip(),
        "git_commit": commit.strip(),
        "candidate_has_uncommitted_changes": bool(dirty.strip()),
        "candidate_digest": core.tree_digest(snapshot),
        "fixture_digest": source_digest,
        "task_suite_digest": suite_digest,
        "evaluator_digest": hashlib.sha256(
            (ROOT / "benchmarks/evaluate.py").read_bytes()
        ).hexdigest(),
        "environment": {
            "system": platform.system(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
        "configuration": {
            "ephemeral": True,
            "ignore_user_config": True,
            "ignore_rules": True,
            "web_search": "disabled",
            "approval_policy": "never",
            "service_tier": "default",
            "sandbox": "read-only for navigation; workspace-write for edits",
        },
        "tasks": [{**task, "executed_prompt": task_prompt(task)} for task in tasks],
        "runs": [],
        "limitations": [
            "Synthetic small Python repository; not representative of all projects.",
            "Guidance produced by bootstrap procedure and frozen; only instruction files differ.",
            "Plugin excluded from both conditions; this isolates generated guidance, not skill invocation.",
            "Provider caching and service load are uncontrolled; ordering alternates by task/repetition.",
            "Both conditions use the same commit and candidate snapshot; SHA alone cannot reproduce uncommitted validation changes.",
            "Costs and file inspection counts are unavailable unless separately supported by provider evidence.",
        ],
    }
    abort = False
    with tempfile.TemporaryDirectory(prefix="contextlean-suite-") as temporary:
        for task_index, task in enumerate(tasks):
            for repetition in range(args.repeat):
                for variant in core.variant_order(task_index, repetition):
                    condition = "vanilla" if variant == "baseline" else "contextlean"
                    workspace = Path(temporary) / "repo"
                    shutil.rmtree(workspace, ignore_errors=True)
                    core.copy_repository(FIXTURE, workspace)
                    preparation.validate_frozen(workspace, args.preparation_record, prepared_record)
                    neutralized = (
                        core.neutralize_instructions(workspace) if condition == "vanilla" else []
                    )
                    if core.tree_digest(workspace, True) != core.tree_digest(FIXTURE, True):
                        raise core.BenchmarkError("conditions differ outside instruction files")
                    initial = core.tree_digest(workspace)
                    name = f"{task['id']}-{repetition + 1}-{condition}"
                    artifacts = output / "raw" / name
                    sandbox = "read-only" if task["id"] == "navigation" else "workspace-write"
                    print(
                        f"Run {len(report['runs']) + 1}/{report['expected_runs']}: {name}",
                        flush=True,
                    )
                    result = core.execute_run(
                        args.codex,
                        workspace,
                        args.model,
                        args.reasoning,
                        task_prompt(task),
                        args.timeout,
                        sandbox,
                        artifacts / "events.jsonl",
                    )
                    core.copy_repository(workspace, artifacts / "solution")
                    evaluation = grade(task, workspace, result, artifacts)
                    sample = workspace / "data/sample.csv"
                    if (
                        not sample.is_file()
                        or sample.read_bytes() != (FIXTURE / "data/sample.csv").read_bytes()
                    ):
                        evaluation["task_success"] = False
                        evaluation["error"] = "sample input changed during run"
                    if task["id"] == "navigation" and initial != core.tree_digest(workspace):
                        evaluation["task_success"] = False
                        evaluation["error"] = "read-only task changed the workspace"
                    expected_guidance = (
                        {"AGENTS.md", "CLAUDE.md"} if condition == "contextlean" else set()
                    )
                    observed_guidance = {
                        core.relative(path, workspace) for path in core.instruction_files(workspace)
                    }
                    if observed_guidance != expected_guidance or any(
                        (workspace / path).read_bytes() != (FIXTURE / path).read_bytes()
                        for path in expected_guidance & observed_guidance
                    ):
                        evaluation["task_success"] = False
                        evaluation["error"] = "agent guidance changed during run"
                    usage = result.get("usage") or {}
                    metrics = {
                        key: usage.get(key)
                        for key in (
                            "input_tokens",
                            "cached_input_tokens",
                            "output_tokens",
                            "reasoning_output_tokens",
                        )
                    }
                    metrics.update(
                        {
                            "total_tokens": usage["input_tokens"] + usage["output_tokens"]
                            if usage
                            else None,
                            "command_calls": result.get("commands")
                            if result.get("event_count")
                            else None,
                            "duration_seconds": result["duration_seconds"],
                            "tool_calls": None,
                            "file_reads": None,
                            "unique_files_inspected": None,
                            "estimated_cost": None,
                        }
                    )
                    run_record = {
                        "task": task["id"],
                        "condition": condition,
                        "repeat": repetition + 1,
                        "sequence": len(report["runs"]) + 1,
                        "timestamp": core.utc_now(),
                        "initial_digest": initial,
                        "initial_non_instruction_digest": core.tree_digest(FIXTURE, True),
                        "neutralized_instructions": neutralized,
                        "metrics": metrics,
                        "evaluation": evaluation,
                        "execution_success": result["success"],
                        "exit_code": result["exit_code"],
                        "error": result.get("error"),
                        "raw_directory": f"raw/{name}",
                    }
                    report["runs"].append(run_record)
                    core.write_json(artifacts / "run.json", run_record)
                    core.write_json(output / "summary.json", report)
                    if not result["success"] and not usage:
                        abort = True
                        break
                if abort:
                    break
            if abort:
                break
    if source_digest != core.tree_digest(FIXTURE):
        raise core.BenchmarkError("source fixture changed during benchmark")
    report["finished_at"] = core.utc_now()
    report["summary"] = summarize(report["runs"], tasks, args.repeat)
    complete = len(report["runs"]) == report["expected_runs"]
    correct = complete and all(run["evaluation"]["task_success"] for run in report["runs"])
    report["result"] = (
        "All tasks passed; this validation batch is eligible for measurement review, not a performance claim."
        if correct
        else "No gain claim: one or more runs failed, were incorrect, or were not completed."
    )
    core.write_json(output / "summary.json", report)
    (output / "report.md").write_text(render(report), encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--reasoning", required=True)
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--tasks-file", type=Path, default=TASKS)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--preparation-record", type=Path, required=True)
    parser.add_argument("--codex", default="codex")
    args = parser.parse_args()
    try:
        report = run(args)
        print(render(report))
        return (
            0
            if len(report["runs"]) == report["expected_runs"]
            and all(run["evaluation"]["task_success"] for run in report["runs"])
            else 2
        )
    except (core.BenchmarkError, OSError, ValueError) as error:
        print(f"benchmark error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
