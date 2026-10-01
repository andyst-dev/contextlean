#!/usr/bin/env python3
"""Harness v3: opt-in, isolated graded Codex/Claude benchmark; offline preflight."""

import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
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
HARNESS_SPEC = importlib.util.spec_from_file_location(
    "benchmark_harness_v3", ROOT / "benchmarks/harness.py"
)
harness = importlib.util.module_from_spec(HARNESS_SPEC)
HARNESS_SPEC.loader.exec_module(harness)
TRACE_SPEC = importlib.util.spec_from_file_location(
    "benchmark_trace_v2", ROOT / "benchmarks/trace.py"
)
trace = importlib.util.module_from_spec(TRACE_SPEC)
TRACE_SPEC.loader.exec_module(trace)
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


def capture(command, workspace, timeout=60, env=None):
    try:
        result = subprocess.run(
            command,
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env if env is not None else dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
        )
        if env is not None and result.returncode not in {0, 1}:
            raise harness.HarnessError("grader process failed: " + result.stderr)
        return result.returncode == 0, result.stdout + result.stderr
    except (subprocess.TimeoutExpired, OSError) as error:
        if env is not None:
            raise
        return False, type(error).__name__


def grade(task, workspace, result, artifact_dir, session=None):
    # Evaluate another copy, with original tests restored. Agent edits cannot weaken
    # the regression suite, and evaluation cannot contaminate measured artifacts.
    with tempfile.TemporaryDirectory(prefix="contextlean-evaluation-") as temporary:
        python = session.runtime["binaries"]["python3"]["path"] if session else sys.executable
        options = {"env": session.env} if session else {}
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
            [python, "-m", "unittest", "discover", "-s", "tests", "-v"], evaluation, **options
        )
        shutil.rmtree(evaluation / "tests", ignore_errors=True)
        shutil.copytree(FIXTURE / "tests", evaluation / "tests")
        response = Path(temporary) / "response.txt"
        response.write_text(result.get("final_response", ""), encoding="utf-8")
        regression, regression_log = capture(
            [python, "-m", "unittest", "discover", "-s", "tests", "-v"], evaluation, **options
        )
        accepted, acceptance_log = capture(
            [
                python,
                str(ROOT / "benchmarks/evaluate.py"),
                task["id"],
                str(evaluation),
                str(response),
            ],
            evaluation,
            **options,
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
    return harness.distribution(values)


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
                "uncached_input_tokens",
                "output_tokens",
                "total_tokens",
                "command_calls",
                "duration_seconds",
            ):
                values = [
                    run["metrics"][key]
                    for run in selected
                    if run["metrics"].get(key) is not None and run.get("measurement_complete", True)
                ]
                metrics[key] = distribution(values)
            entry[condition] = {
                "runs": len(selected),
                "expected_runs": repeats,
                "task_successes": sum(
                    run["evaluation"].get("task_success") is True for run in selected
                ),
                "task_failures": sum(
                    run["evaluation"].get("task_success") is False for run in selected
                ),
                "unevaluated_runs": sum(
                    run["evaluation"].get("task_success") is None for run in selected
                ),
                "measurements_complete": len(selected) == repeats
                and all(
                    run.get("measurement_complete", True)
                    and run["metrics"].get("total_tokens") is not None
                    for run in selected
                ),
                "metrics": metrics,
            }
        summary.append(entry)
    return summary


def render(report):
    lines = [
        "# ContextLean benchmark validation batch",
        "",
        f"Harness v{report.get('benchmark_harness_version', 1)} · {report.get('experiment_kind', 'compatibility-smoke')}. No statistical significance claim.",
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
        duration = metric.get("duration_seconds")
        seconds = "unavailable" if duration is None else f"{duration:.2f}"
        lines.append(
            f"| {run['task']} | {run['condition']} | {'pass' if evaluation.get('task_success') is True else 'fail' if evaluation.get('task_success') is False else 'unavailable'} | {'pass' if evaluation.get('tests_passed') else 'unavailable' if 'tests_passed' not in evaluation else 'fail'} | {fields} | {seconds} |"
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
            "All exposed tool attempts, coverage identities and output sizes are in execution.json; hidden actions remain unavailable.",
            "Command calls count unique Bash/command_execution attempts, including denials. No inferred file counts are presented.",
            "Cached input is a subset of input. Total is input + output. Missing reasoning-token fields remain null.",
            "One repetition cannot establish variance or statistical confidence.",
            "",
        ]
    )
    lines.extend(
        [
            "## Token statistics",
            "",
            "| Task | Condition | Mean | Sample SD | Range |",
            "|---|---|---:|---:|---:|",
        ]
    )
    for task in report["summary"]:
        for condition in ("vanilla", "contextlean"):
            stats = task[condition]["metrics"]["total_tokens"]
            if stats:
                sd = stats["sample_standard_deviation"]
                lines.append(
                    f"| {task['task']} | {condition} | {stats['mean']:.2f} | {'unavailable' if sd is None else f'{sd:.2f}'} | {stats['range']} |"
                )
    lines.extend(["", "Paired differences (ContextLean minus Vanilla):", ""])
    for item in report.get("paired_differences", []):
        stats = item["differences"]["total_tokens"]
        lines.append(
            f"- {item['task']}: "
            + (
                "unavailable; incomplete pair measurements"
                if stats is None
                else f"observations {stats['observations']}; mean {stats['mean']:.2f}; median {stats['median']:.2f}; range {stats['range']}; sample SD {stats['sample_standard_deviation']}"
            )
        )
    return "\n".join(lines)


def run(args):
    tasks = load_suite(args.tasks_file)
    mode = getattr(args, "experiment_kind", "compatibility-smoke")
    provider = getattr(args, "provider", "codex")
    if args.repeat < 1 or args.timeout < 1 or (mode == "performance" and args.repeat < 3):
        raise core.BenchmarkError(
            "positive timeout/repeats required; performance requires at least 3 repetitions (5 preferred)"
        )
    output = args.output_dir.resolve()
    if output.is_relative_to(FIXTURE.resolve()) or (output.exists() and any(output.iterdir())):
        raise core.BenchmarkError("output must be new and outside the fixture")
    prepared = preparation.validate_frozen(FIXTURE, args.preparation_record)
    if not getattr(args, "live", False) and not getattr(args, "preflight_only", False):
        raise core.BenchmarkError("explicit --live or --preflight-only required")
    if any(
        p.name.startswith("requirements") or p.name in {"pyproject.toml", "uv.lock", "poetry.lock"}
        for p in FIXTURE.rglob("*")
    ):
        raise core.BenchmarkError(
            "this fixture requires a separately pinned dependency environment; standard-library harness will not install dependencies"
        )
    source_digest = core.tree_digest(FIXTURE)
    canonical_inventory = harness.inventory(FIXTURE)
    # Canonical preparation and map validation precede even CLI version probes.
    runtime = harness.pin_runtime(
        args.codex if provider == "codex" else args.claude, getattr(args, "shell", None)
    )
    source_env = harness.environment_source(provider)
    plan = harness.schedule([t["id"] for t in tasks], args.repeat)
    output.mkdir(parents=True, exist_ok=True)
    (output / "private").mkdir(mode=0o700)
    clean = harness.Sanitizer(
        replacements={str(ROOT): "<contextlean>", str(output): "<evidence>"},
        secrets=[source_env[k] for k in harness.AUTH_NAMES if k in source_env],
    )

    def save(path, value):
        harness.write_json(path, clean.value(value))

    save(
        output / "schedule.json",
        {
            "benchmark_harness_version": harness.VERSION,
            "generated_at": core.utc_now(),
            "order": plan,
            "method": "deterministic counterbalanced task/repetition parity",
        },
    )
    inputs = {
        name: harness.digest((ROOT / name).read_bytes())
        for name in [
            "benchmarks/evaluate.py",
            "benchmarks/tasks/suite.json",
            "benchmarks/run_benchmark.py",
            "benchmarks/harness.py",
            "benchmarks/execution.py",
            "benchmarks/trace.py",
            "benchmarks/prepare_fixture.py",
            "skills/benchmark/scripts/benchmark.py",
        ]
    }
    tasks_sha = harness.digest(args.tasks_file.read_bytes())
    compile((ROOT / "benchmarks/evaluate.py").read_bytes(), "grader", "exec")
    # Canonical source and task/grader bytes, not the host checkout/private files.
    for name in inputs:
        target = output / "source" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(clean.text((ROOT / name).read_text()), encoding="utf-8")
        private_source = output / "private/source" / name
        private_source.parent.mkdir(parents=True, exist_ok=True)
        private_source.write_bytes((ROOT / name).read_bytes())
    harness.copy_fixture(FIXTURE, output / "private/canonical-fixture")
    (output / "private/tasks.json").write_bytes(args.tasks_file.read_bytes())
    report = {
        "schema_version": harness.VERSION,
        "benchmark_harness_version": harness.VERSION,
        "kind": "contextlean-graded-validation",
        "experiment_kind": mode,
        "status": "preparing",
        "contextlean_version": core.CONTEXTLEAN_VERSION,
        "started_at": core.utc_now(),
        "model": args.model,
        "provider": provider,
        "reasoning": args.reasoning,
        "repeats": args.repeat,
        "expected_runs": len(plan),
        "schedule": plan,
        "runtime": runtime,
        "fixture_digest": source_digest,
        "input_hashes": inputs,
        "tasks_file_sha256": tasks_sha,
        "quota": {"state": "unknown", "reliable_check_available": False},
        "cache_state": "uncontrolled",
        "tasks": [{**t, "executed_prompt": task_prompt(t)} for t in tasks],
        "runs": [],
        "limitations": [
            "Model stochasticity, cache/service load and hidden provider implementation are uncontrolled.",
            "Only exposed command/usage/coverage events are captured; no per-action token estimates.",
            "Native filesystem boundary is required; unavailable or failed boundaries block execution.",
        ],
    }
    save(output / "preparation.json", prepared)
    save(output / "summary.json", report)
    reference_receipts = {}
    reference_git = {}
    with tempfile.TemporaryDirectory(
        prefix=f"contextlean-canonical-v{harness.VERSION}-"
    ) as temporary:
        canonical = Path(temporary) / "conditions"
        vanilla, contextlean = harness.make_conditions(FIXTURE, canonical, harness.copy_fixture)
        manifest = harness.fixture_manifest(vanilla, contextlean, b"", b"")
        manifest.pop("prompt_sha256")
        manifest.pop("prompt_size")
        manifest["task_prompts"] = {
            t["id"]: {
                "sha256": harness.digest(task_prompt(t).encode()),
                "size": len(task_prompt(t).encode()),
                "pair_bytes_equal": True,
            }
            for t in tasks
        }
        save(output / "fixture-manifest.json", manifest)
        condition_paths = {"vanilla": vanilla, "contextlean": contextlean}
        for condition, path in condition_paths.items():
            harness.copy_fixture(path, output / "fixtures" / condition)
            omitted = harness.sanitize_tree(output / "fixtures" / condition, clean)
            save(
                output / "fixtures" / f"{condition}-export.json", {"omitted_binary_paths": omitted}
            )

        def prepare_session(session, item):
            task = next(t for t in tasks if t["id"] == item["task"])
            preparation.validate_frozen(FIXTURE, args.preparation_record, prepared)
            harness.compare_receipts(
                canonical_inventory, harness.inventory(FIXTURE), "canonical input"
            )
            if (
                tasks_sha != harness.digest(args.tasks_file.read_bytes())
                or source_digest != core.tree_digest(FIXTURE)
                or any(harness.digest((ROOT / n).read_bytes()) != h for n, h in inputs.items())
            ):
                raise harness.HarnessError("frozen input changed during campaign")
            harness.validate_runtime(runtime)
            source = condition_paths[item["condition"]]
            # Session creates empty repo; copier requires a missing destination.
            session.repo.rmdir()
            harness.copy_fixture(source, session.repo)
            harness.compare_receipts(
                harness.inventory(source), harness.inventory(session.repo), "source fixture"
            )
            prompt = task_prompt(task).encode("utf-8")
            pair_manifest = harness.fixture_manifest(vanilla, contextlean, prompt, prompt)
            baseline = harness.initialize_git(session)
            if not baseline["clean"] or baseline["remotes"] or baseline["hooks"]:
                raise harness.HarnessError("unclean or inherited Git baseline")
            git_key = (task["id"], item["condition"])
            if git_key in reference_git:
                harness.compare_receipts(reference_git[git_key], baseline, "Git baseline")
            else:
                reference_git[git_key] = baseline
            auth = session.auth(provider)
            if not auth["present"]:
                raise harness.HarnessError("provider authentication unavailable")
            sandbox = "read-only" if task["id"] == "navigation" else "workspace-write"
            policy = harness.permission_preflight(
                session, harness.permission_policy(session, provider, sandbox), output
            )
            # Canonical tests run in the exact environment and filesystem boundary.
            command = [
                runtime["binaries"]["python3"]["path"],
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-v",
            ]
            tested = subprocess.run(
                harness.boundary_command(session, policy, command, output),
                cwd=session.repo,
                env=session.env,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            test_coverage = trace.coverage(
                "python3 -m unittest discover -s tests -v", tested.stdout + tested.stderr
            )
            if tested.returncode or not test_coverage or not test_coverage["passed"]:
                raise harness.HarnessError("canonical tests are not runnable")
            if harness.git_state(session) != baseline:
                raise harness.HarnessError("canonical tests changed baseline")
            receipt = {
                "benchmark_harness_version": harness.VERSION,
                "runtime": runtime,
                "cwd": "<session-root>/repo",
                "environment": harness.environment_receipt(session.env, session.sanitizer.text),
                "permission": session.sanitizer.value(policy),
                "auth": auth,
                "git": baseline,
                "prompt_sha256": pair_manifest["prompt_sha256"],
                "prompt_size": len(prompt),
                "preflight_coverage": test_coverage,
                "grader_sha256": inputs["benchmarks/evaluate.py"],
                "git_policy": {
                    k: baseline[k] for k in ["config", "branch", "clean", "remotes", "hooks"]
                },
                "quota": report["quota"],
            }
            comparison = {
                k: receipt[k]
                for k in [
                    "runtime",
                    "environment",
                    "permission",
                    "auth",
                    "prompt_sha256",
                    "grader_sha256",
                    "git_policy",
                ]
            }
            key = task["id"]
            if key in reference_receipts:
                harness.compare_receipts(reference_receipts[key], comparison, "execution")
            else:
                reference_receipts[key] = comparison
            return task, prompt.decode(), baseline, policy, receipt

        # Gate every planned task/condition before the first paid call. Each dry
        # preparation gets its own root and is cleaned, just like a measured run.
        try:
            for item in plan:
                with harness.session_root(runtime, source_env, output) as session:
                    _, _, _, _, receipt = prepare_session(session, item)
                    save(output / "preflight" / f"{item['sequence']}.json", receipt)
                if not session.cleanup_verified:
                    raise harness.HarnessError("preflight cleanup unverified")
        except (harness.HarnessError, OSError, ValueError, subprocess.SubprocessError) as error:
            report.update(status="harness-preparation-failure", error=str(error), model_calls=0)
            save(output / "summary.json", report)
            raise
        report["status"] = "preflight-passed"
        save(output / "summary.json", report)
        if getattr(args, "preflight_only", False):
            report.update(
                result="Deterministic preflight passed; zero model calls.",
                summary=[],
                model_calls=0,
            )
            save(output / "summary.json", report)
            return clean.value(report)

        for item in plan:
            name = f"{item['task']}-{item['repeat']}-{item['condition']}"
            artifacts = output / "raw" / name
            artifacts.mkdir(parents=True)
            run_record = dict(
                item, benchmark_harness_version=harness.VERSION, timestamp=core.utc_now()
            )
            session = None
            try:
                with harness.session_root(runtime, source_env, output) as session:
                    task, prompt, baseline, policy, receipt = prepare_session(session, item)
                    command = harness.invocation(
                        session, provider, args.model, args.reasoning, policy["sandbox"], policy
                    )
                    receipt["provider"] = {
                        "provider": provider,
                        "requested_model": args.model,
                        "reasoning_effort": args.reasoning,
                        "timeout_seconds": args.timeout,
                        "cli_version": runtime["binaries"]["cli"]["version"],
                        "cwd": str(session.repo),
                        "invocation": command,
                    }
                    harness.write_json(
                        session.root / "receipts/preflight.json", session.sanitizer.value(receipt)
                    )
                    before = harness.inventory(session.repo)
                    control_before = harness.control_inventory(session.root / "cache")
                    session.evidence_name = name
                    private = output / "private" / name
                    private.mkdir(mode=0o700)
                    private_receipt = dict(
                        receipt,
                        cwd=str(session.repo),
                        environment=harness.environment_receipt(session.env, lambda value: value),
                    )
                    harness.write_json(private / "session.json", private_receipt)
                    (private / "session.json").chmod(0o600)
                    print(f"Session {item['sequence']}/{len(plan)}: {name}", flush=True)
                    run_record.update(
                        model_invocation_attempted=True, started_at=core.utc_now(), receipt=receipt
                    )
                    save(artifacts / "run.json", session.sanitizer.value(run_record))
                    execution = harness.execute_session(
                        session, command, prompt, args.timeout, policy, output
                    )
                    run_record["finished_at"] = core.utc_now()
                    parsed = trace.parse(execution["stdout"], provider, str(session.repo))
                    parsed["success"] = bool(
                        parsed["success"]
                        and execution["exit_code"] == 0
                        and not parsed["parse_error_lines"]
                    )
                    parsed.update(
                        duration_seconds=execution["duration_seconds"],
                        exit_code=execution["exit_code"],
                        raw_stdout_bytes=execution.get("stdout_bytes"),
                        raw_stderr_bytes=execution.get("stderr_bytes"),
                        raw_stdout_sha256=harness.digest(execution["stdout"].encode()),
                        raw_digest_scope="decoded UTF-8 trace; byte-exact private stream retained separately",
                    )
                    parsed["error"] = execution.get("error") or parsed.get("error")
                    parsed["stderr"] = execution["stderr"]
                    receipt["provider"].update(
                        reported_model=parsed["reported_model"],
                        reported_permission_mode=parsed["reported_permission_mode"],
                        session_identifiers=parsed["session_identifiers"],
                        request_identifiers=parsed["request_identifiers"],
                        auxiliary_model_usage=parsed["auxiliary_model_usage"],
                    )
                    reported_mode = parsed["reported_permission_mode"]
                    if (
                        provider == "claude"
                        and reported_mode is not None
                        and reported_mode != "acceptEdits"
                    ):
                        raise harness.HarnessError("provider reported a different permission mode")
                    sanitizer = session.sanitizer
                    # Public snapshots are separate from original private evidence.
                    private = output / "private" / name
                    private.mkdir(parents=True, exist_ok=True, mode=0o700)
                    private.chmod(0o700)
                    private_receipt = dict(
                        receipt,
                        cwd=str(session.repo),
                        environment=harness.environment_receipt(session.env, lambda value: value),
                    )
                    harness.write_json(private / "session.json", private_receipt)
                    (private / "session.json").chmod(0o600)
                    harness.copy_fixture(session.repo, private / "solution")
                    harness.copy_fixture(session.repo, artifacts / "solution")
                    omitted = harness.sanitize_tree(artifacts / "solution", sanitizer)
                    for filename, text in [
                        ("events.jsonl", execution["stdout"]),
                        ("events.stderr.txt", execution["stderr"]),
                    ]:
                        # JSON-aware sanitization also removes account fields, preserving line order.
                        if filename.endswith(".jsonl") and not parsed["parse_error_lines"]:
                            text = (
                                "\n".join(
                                    json.dumps(
                                        sanitizer.value(core.json.loads(line)), ensure_ascii=False
                                    )
                                    for line in text.splitlines()
                                    if line.strip()
                                )
                                + "\n"
                            )
                        else:
                            text = sanitizer.text(text)
                        (artifacts / filename).write_text(text, encoding="utf-8")
                    try:
                        evaluation = grade(task, session.repo, parsed, artifacts, session=session)
                        category = harness.failure_category(parsed, evaluation)
                    except (
                        harness.HarnessError,
                        OSError,
                        ValueError,
                        subprocess.SubprocessError,
                    ) as error:
                        evaluation = {"task_success": None, "error": str(error)}
                        category = "grading-failure"
                    if category in {
                        "provider-usage-limit-interruption",
                        "provider-network-failure",
                    }:
                        evaluation["task_success"] = None
                    after = harness.inventory(session.repo)
                    preserved = all(
                        before.get(n) == after.get(n)
                        for n in harness.GUIDANCE | {"data/sample.csv"}
                    )
                    post_git = harness.git_state(session)
                    if category not in {
                        "provider-usage-limit-interruption",
                        "provider-network-failure",
                        "grading-failure",
                    } and (
                        not preserved
                        or post_git["baseline_commit"] != baseline["baseline_commit"]
                        or (task["id"] == "navigation" and before != after)
                    ):
                        evaluation["task_success"] = False
                        category = "model-task-failure"
                    parsed["file_changes"] = {
                        n: {"before": before.get(n), "after": after.get(n)}
                        for n in set(before) | set(after)
                        if before.get(n) != after.get(n)
                    }
                    post = {
                        "git": post_git,
                        "repo_changes": parsed["file_changes"],
                        "tmp_files": harness.inventory(session.tmp),
                        "unexpected_root_entries": sorted(
                            p.name
                            for p in session.root.iterdir()
                            if p.name not in {"repo", "tmp", "cache", "artifacts", "receipts"}
                        ),
                        "outside_approved_visibility": "native write boundary; external hidden side effects unavailable",
                        "cache_before": control_before,
                        "cache_after": harness.control_inventory(session.root / "cache"),
                        "control_artifacts": harness.control_inventory(session.root / "artifacts"),
                        "control_receipts": harness.control_inventory(session.root / "receipts"),
                        "omitted_binary_paths": omitted,
                        "evidence_complete": not parsed["parse_error_lines"]
                        and all(
                            (artifacts / filename).is_file()
                            for filename in ["events.jsonl", "events.stderr.txt"]
                        ),
                    }
                    if post["unexpected_root_entries"]:
                        category = "harness-preparation-failure"
                        evaluation["task_success"] = None
                    usage = parsed["usage"] or {}
                    metrics = {
                        k: usage.get(k)
                        for k in [
                            "input_tokens",
                            "cached_input_tokens",
                            "uncached_input_tokens",
                            "output_tokens",
                            "reasoning_output_tokens",
                            "total_tokens",
                        ]
                    }
                    metrics.update(
                        command_calls=parsed["commands"],
                        duration_seconds=execution["duration_seconds"],
                    )
                    run_record.update(
                        metrics=metrics,
                        evaluation=evaluation,
                        failure_category=category,
                        execution_success=parsed["success"],
                        error=parsed["error"],
                        exit_code=execution["exit_code"],
                        raw_directory=f"raw/{name}",
                        measurement_complete=bool(
                            usage
                            and parsed["success"]
                            and post["evidence_complete"]
                            and category
                            not in {
                                "provider-usage-limit-interruption",
                                "provider-network-failure",
                                "harness-preparation-failure",
                                "grading-failure",
                            }
                        ),
                        receipt=receipt,
                        post_run=post,
                    )
                    for filename, data in [
                        ("execution.json", parsed),
                        ("session.json", receipt),
                        ("post-run.json", post),
                    ]:
                        harness.write_json(artifacts / filename, sanitizer.value(data))
                    # Grader may contain temporary paths; sanitize its public log too.
                    log = artifacts / "evaluation.txt"
                    if log.exists():
                        log.write_text(sanitizer.text(log.read_text()), encoding="utf-8")
                    run_record = sanitizer.value(run_record)
                run_record["cleanup_verified"] = session.cleanup_verified
            except (harness.HarnessError, OSError, ValueError, subprocess.SubprocessError) as error:
                run_record.update(
                    failure_category="harness-preparation-failure",
                    error=str(error),
                    evaluation={"task_success": None},
                    metrics={},
                    cleanup_verified=bool(session and session.cleanup_verified),
                    measurement_complete=False,
                )
                if session:
                    run_record = session.sanitizer.value(run_record)
            report["runs"].append(run_record)
            save(artifacts / "run.json", run_record)
            save(output / "summary.json", report)
            if run_record["failure_category"] in {
                "provider-usage-limit-interruption",
                "provider-network-failure",
                "harness-preparation-failure",
                "grading-failure",
            }:
                break  # No retries; scheduled, unattempted observations remain incomplete.
    report.update(
        finished_at=core.utc_now(),
        summary=summarize(report["runs"], tasks, args.repeat),
        paired_differences=harness.paired_metrics(
            report["runs"], [t["id"] for t in tasks], args.repeat
        ),
    )
    complete = len(report["runs"]) == len(plan) and all(
        r["measurement_complete"] for r in report["runs"]
    )
    report["status"] = "complete" if complete else "incomplete"
    report["model_calls"] = sum(r.get("model_invocation_attempted", False) for r in report["runs"])
    correct = complete and all(r["evaluation"].get("task_success") is True for r in report["runs"])
    report["result"] = (
        "All observations retained; no statistical significance or universal gain claim."
        if correct
        else "No gain claim: failed or incomplete campaign; unavailable pairs have no comparison aggregate."
    )
    public = clean.value(report)
    save(output / "summary.json", report)
    (output / "report.md").write_text(render(public), encoding="utf-8")
    checksums = {
        p.relative_to(output).as_posix(): harness.digest(p.read_bytes())
        for p in sorted(output.rglob("*"))
        if p.is_file()
        and "private" not in p.relative_to(output).parts
        and p.name != "checksums.json"
    }
    harness.write_json(output / "checksums.json", checksums)
    return public


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--provider", choices=["codex", "claude"], default="codex")
    parser.add_argument("--claude", default="claude")
    parser.add_argument("--shell")
    parser.add_argument(
        "--experiment-kind",
        choices=["compatibility-smoke", "performance"],
        default="compatibility-smoke",
    )
    launch = parser.add_mutually_exclusive_group(required=True)
    launch.add_argument("--live", action="store_true", help="Explicitly authorize model execution")
    launch.add_argument(
        "--preflight-only", action="store_true", help="Offline gates only; no model calls"
    )
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
            if args.preflight_only
            or (
                len(report["runs"]) == report["expected_runs"]
                and all(run["evaluation"]["task_success"] for run in report["runs"])
            )
            else 2
        )
    except (
        core.BenchmarkError,
        harness.HarnessError,
        OSError,
        ValueError,
        subprocess.SubprocessError,
    ) as error:
        print(f"benchmark error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
