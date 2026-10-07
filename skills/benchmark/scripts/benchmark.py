#!/usr/bin/env python3
"""Local, dependency-free ContextLean static and Codex A/B benchmark runner."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from typing import Any, Iterable


CONTEXTLEAN_VERSION = "0.3.1"
SCHEMA_VERSION = 1
TOKEN_CHARS_ESTIMATE = 4
LARGE_DOC_BYTES = 10_000
RATE_FRESH_DAYS = 90
SKIP_DIRS = {
    ".git",
    ".contextlean",
    ".hg",
    ".svn",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "coverage",
    "__pycache__",
}
INSTRUCTION_NAMES = {"AGENTS.md", "AGENTS.override.md", "CLAUDE.md", "CLAUDE.local.md"}
COPY_SKIP_NAMES = {".git", ".contextlean", "__pycache__", ".DS_Store", ".ruff_cache", ".venv"}
MANDATORY_WORDS = re.compile(
    r"\b(must|always|required|before (?:starting|doing|anything)|read completely|load)\b",
    re.IGNORECASE,
)
PATH_TOKEN = re.compile(r"(?:`|\[)[^`\]\n]*?(?P<path>[\w./-]+\.md)(?:`|\])")


class BenchmarkError(RuntimeError):
    """Expected, user-facing benchmark failure."""


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def iter_project_files(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(name for name in dirs if name not in SKIP_DIRS)
        current_path = Path(current)
        for name in sorted(files):
            yield current_path / name


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def instruction_files(root: Path) -> list[Path]:
    return [path for path in iter_project_files(root) if path.name in INSTRUCTION_NAMES]


def estimated_tokens(byte_count: int) -> int:
    return math.ceil(byte_count / TOKEN_CHARS_ESTIMATE)


def resolve_doc_reference(root: Path, instruction: Path, token: str) -> Path | None:
    candidates = (instruction.parent / token, root / token)
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
            resolved.relative_to(root.resolve())
        except (OSError, ValueError):
            continue
        if resolved.is_file():
            return resolved
    return None


def heuristic_large_mandatory_docs(root: Path, files: list[Path]) -> list[dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    for instruction in files:
        try:
            text = instruction.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            if not MANDATORY_WORDS.search(line):
                continue
            for match in PATH_TOKEN.finditer(line):
                target = resolve_doc_reference(root, instruction, match.group("path"))
                if target is None:
                    continue
                size = target.stat().st_size
                if size < LARGE_DOC_BYTES:
                    continue
                target_rel = relative(target, root)
                found[target_rel] = {
                    "path": target_rel,
                    "bytes": size,
                    "referenced_by": relative(instruction, root),
                    "line": line_number,
                    "classification": "heuristic",
                }
    return [found[key] for key in sorted(found)]


def static_snapshot(root: Path, project_type: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    files = instruction_files(root)
    records = [
        {
            "path": relative(path, root),
            "bytes": path.stat().st_size,
            "classification": "exact",
        }
        for path in files
    ]
    total = sum(record["bytes"] for record in records)
    maps = [record["path"] for record in records if Path(record["path"]).name == "AGENTS.md"]
    mandatory = heuristic_large_mandatory_docs(root, files)
    return {
        "captured_at": utc_now(),
        "project_type": project_type or detect_project_type(root),
        "instruction_files": records,
        "automatic_instruction_bytes": {
            "value": total,
            "unit": "bytes",
            "classification": "exact",
        },
        "automatic_instruction_tokens": {
            "value": estimated_tokens(total),
            "unit": "tokens",
            "classification": "estimated",
            "method": f"ceil(bytes/{TOKEN_CHARS_ESTIMATE})",
        },
        "large_mandatory_startup_docs": {
            "value": len(mandatory),
            "classification": "heuristic",
            "threshold_bytes": LARGE_DOC_BYTES,
            "documents": mandatory,
        },
        "project_maps": {
            "value": len(maps),
            "classification": "exact",
            "paths": maps,
        },
        "agents_hierarchy": maps,
        "measurement_scope": "inventory across agents and subtrees, not the context loaded by any one session",
    }


def detect_project_type(root: Path) -> str:
    markers = [
        ("pyproject.toml", "Python"),
        ("package.json", "JavaScript/TypeScript"),
        ("Cargo.toml", "Rust"),
        ("go.mod", "Go"),
        ("pom.xml", "Java/Maven"),
        ("build.gradle", "Java/Gradle"),
        ("Gemfile", "Ruby"),
    ]
    detected = [label for marker, label in markers if (root / marker).is_file()]
    return ", ".join(detected) if detected else "repository"


def bootstrap_start(repo: Path, output: Path, project_type: str | None) -> dict[str, Any]:
    snapshot = {
        "schema_version": SCHEMA_VERSION,
        "contextlean_version": CONTEXTLEAN_VERSION,
        "kind": "bootstrap-baseline",
        "snapshot": static_snapshot(repo, project_type),
    }
    write_json(output, snapshot)
    return snapshot


def bootstrap_finish(
    repo: Path,
    baseline_path: Path,
    output: Path,
    project_type: str | None,
    created: list[str],
    modified: list[str],
    moved: list[str],
    exclusions: list[str],
    limits: list[str],
    keep_baseline: bool = False,
) -> dict[str, Any]:
    if not baseline_path.is_file():
        raise BenchmarkError(f"bootstrap baseline not found: {baseline_path}")
    baseline = read_json(baseline_path)
    if baseline.get("kind") != "bootstrap-baseline":
        raise BenchmarkError("invalid bootstrap baseline file")
    report = {
        "schema_version": SCHEMA_VERSION,
        "contextlean_version": CONTEXTLEAN_VERSION,
        "kind": "contextlean-bootstrap-report",
        "generated_at": utc_now(),
        "project_type": project_type
        or baseline["snapshot"].get("project_type")
        or detect_project_type(repo),
        "baseline_available": True,
        "before": baseline["snapshot"],
        "after": static_snapshot(repo, project_type),
        "changes": {
            "classification": "exact",
            "source": "bootstrap action log",
            "created": sorted(set(created)),
            "modified": sorted(set(modified)),
            "moved_or_renamed": sorted(set(moved)),
            "exclusions_installed": sorted(set(exclusions)),
        },
        "measurement_limits": [
            "Static structure is not measured model-token usage or model quality.",
            "Token values are byte-based estimates, never tokenizer measurements.",
            "Mandatory startup documents are detected heuristically from instruction wording and paths.",
            "No repository contents or secrets are copied into this report.",
            *limits,
        ],
    }
    write_json(output, report)
    if not keep_baseline:
        expected_name = ".bootstrap-baseline.json"
        if baseline_path.name == expected_name and baseline_path.parent.name == ".contextlean":
            baseline_path.unlink(missing_ok=True)
    return report


def metric_value(snapshot: dict[str, Any], name: str) -> Any:
    return snapshot[name]["value"]


def change_percent(baseline: float, optimized: float) -> float | None:
    if baseline == 0:
        return 0.0 if optimized == 0 else None
    return (optimized - baseline) / baseline * 100.0


def format_change(value: float | None) -> str:
    return "n/a" if value is None else f"{value:+.1f}%"


def render_static_report(report: dict[str, Any]) -> str:
    before = report.get("before")
    after = report["after"]
    lines = ["# ContextLean Static Report", ""]
    if before is None or not report.get("baseline_available", False):
        lines.extend(
            [
                "No ContextLean bootstrap baseline exists. Only the current state is shown; a true static before/after is not available.",
                "",
                "## Instruction file inventory [exact]",
                "",
                f"Current: {metric_value(after, 'automatic_instruction_bytes'):,} bytes",
                "",
                "## Estimated instruction tokens [estimated]",
                "",
                f"Current: {metric_value(after, 'automatic_instruction_tokens'):,} estimated tokens (ceil(bytes/{TOKEN_CHARS_ESTIMATE}))",
                "",
                "## Large mandatory startup docs [heuristic]",
                "",
                f"Current: {metric_value(after, 'large_mandatory_startup_docs')}",
                "",
                "## Project maps [exact]",
                "",
                f"Current: {metric_value(after, 'project_maps')}",
                "",
            ]
        )
    else:
        rows = [
            ("Instruction file inventory [exact, bytes]", "automatic_instruction_bytes"),
            ("Estimated instruction tokens [estimated]", "automatic_instruction_tokens"),
            ("Large mandatory startup docs [heuristic]", "large_mandatory_startup_docs"),
            ("Project maps [exact]", "project_maps"),
        ]
        for title, key in rows:
            before_value = metric_value(before, key)
            after_value = metric_value(after, key)
            lines.extend(
                [
                    f"## {title}",
                    "",
                    f"Before: {before_value:,}",
                    f"After: {after_value:,}",
                    f"Change: {format_change(change_percent(before_value, after_value))}",
                    "",
                ]
            )
    lines.extend(
        [
            "These are static structural metrics, not measured model-token savings.",
            "The inventory spans agents and subtrees; it is not the context loaded by any one session.",
            "",
            "Classifications: exact = directly counted; estimated = byte approximation; heuristic = rule-based detection.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def parse_jsonl(text: str) -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    parse_errors = 0
    for raw in text.splitlines():
        if not raw.strip():
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            parse_errors += 1
            continue
        if isinstance(event, dict):
            events.append(event)
        else:
            parse_errors += 1

    completed = [event for event in events if event.get("type") == "turn.completed"]
    failed_events = [event for event in events if event.get("type") in {"turn.failed", "error"}]
    usage: dict[str, int] | None = None
    validation_error: str | None = None
    if completed:
        raw_usage = completed[-1].get("usage")
        required = ("input_tokens", "cached_input_tokens", "output_tokens")
        if isinstance(raw_usage, dict) and all(
            type(raw_usage.get(key)) is int and raw_usage[key] >= 0 for key in required
        ):
            usage = {key: raw_usage[key] for key in required}
            reasoning = raw_usage.get("reasoning_output_tokens")
            usage["reasoning_output_tokens"] = (
                reasoning if type(reasoning) is int and reasoning >= 0 else None
            )
            if usage["cached_input_tokens"] > usage["input_tokens"]:
                validation_error = "cached_input_tokens exceeds input_tokens"
        else:
            validation_error = "turn.completed usage is missing or invalid"
    else:
        validation_error = "turn.completed event missing"

    commands: set[str] = set()
    searches: set[str] = set()
    command_fallback_started = 0
    command_fallback_completed = 0
    search_fallback_started = 0
    search_fallback_completed = 0
    for event in events:
        if not str(event.get("type", "")).startswith("item."):
            continue
        item = event.get("item")
        if not isinstance(item, dict):
            continue
        item_type = item.get("type")
        item_id = item.get("id")
        if item_type == "command_execution":
            if item_id is None:
                if event.get("type") == "item.started":
                    command_fallback_started += 1
                elif event.get("type") == "item.completed":
                    command_fallback_completed += 1
            else:
                commands.add(str(item_id))
        if item_type in {"web_search", "web_search_call"}:
            if item_id is None:
                if event.get("type") == "item.started":
                    search_fallback_started += 1
                elif event.get("type") == "item.completed":
                    search_fallback_completed += 1
            else:
                searches.add(str(item_id))

    thread_ids = [
        event.get("thread_id") for event in events if event.get("type") == "thread.started"
    ]
    success = bool(usage) and validation_error is None and not failed_events and parse_errors == 0
    return {
        "success": success,
        "usage": usage,
        "commands": len(commands) + (command_fallback_started or command_fallback_completed),
        "web_searches": len(searches) + (search_fallback_started or search_fallback_completed),
        "parse_errors": parse_errors,
        "error": validation_error or ("Codex emitted a failure event" if failed_events else None),
        "thread_id": thread_ids[-1] if thread_ids else None,
        "event_count": len(events),
        "final_response": next(
            (
                event["item"].get("text", "")
                for event in reversed(events)
                if event.get("type") == "item.completed"
                and isinstance(event.get("item"), dict)
                and event["item"].get("type") == "agent_message"
            ),
            "",
        ),
    }


def uncached_input_tokens(usage: dict[str, int]) -> int:
    value = usage["input_tokens"] - usage["cached_input_tokens"]
    if value < 0:
        raise BenchmarkError("cached_input_tokens cannot exceed input_tokens")
    return value


def calculate_credits(usage: dict[str, int], rate: dict[str, Any]) -> float:
    uncached = uncached_input_tokens(usage)
    return (
        uncached / 1_000_000 * float(rate["input"])
        + usage["cached_input_tokens"] / 1_000_000 * float(rate["cached_input"])
        + usage["output_tokens"] / 1_000_000 * float(rate["output"])
    )


def load_rate_card(path: Path) -> dict[str, Any]:
    card = read_json(path)
    required = {"verified_on", "source_url", "models"}
    if not isinstance(card, dict) or not required.issubset(card):
        raise BenchmarkError(f"invalid rate card: {path}")
    return card


def find_rate(card: dict[str, Any], model: str) -> dict[str, Any] | None:
    for rate in card.get("models", []):
        if model == rate.get("model") or model in rate.get("aliases", []):
            return rate
    return None


def is_rate_stale(
    card: dict[str, Any], today: dt.date | None = None, max_age_days: int = RATE_FRESH_DAYS
) -> bool:
    try:
        verified = dt.date.fromisoformat(card["verified_on"])
    except (KeyError, TypeError, ValueError):
        return True
    current = today or dt.datetime.now(dt.timezone.utc).date()
    return (current - verified).days > max_age_days


def load_tasks(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        tasks = [
            line.strip()
            for line in text.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
    else:
        if isinstance(value, dict):
            value = value.get("tasks")
        if not isinstance(value, list) or not all(isinstance(task, str) for task in value):
            raise BenchmarkError(
                "tasks file must contain a JSON string array, a {tasks: [...]} object, or one task per line"
            )
        tasks = [task.strip() for task in value if task.strip()]
    if not tasks:
        raise BenchmarkError("tasks file contains no tasks")
    return tasks


def automatic_tasks(root: Path) -> list[str]:
    source_hints = [
        relative(path, root)
        for path in sorted(root.iterdir())
        if path.is_dir() and path.name not in SKIP_DIRS and not path.name.startswith(".")
    ][:6]
    hint = ", ".join(source_hints) if source_hints else "the main source directories"
    suffix = " Do not rely only on AGENTS.md; verify the answer in implementation, configuration, or tests and cite the relevant paths."
    return [
        "Identify the implementation owner of the repository's central user-facing behavior and explain why it owns that responsibility."
        + suffix,
        f"Trace one important execution or dependency flow across at least two subsystems (candidate areas: {hint}). Explain the boundary between them."
        + suffix,
        "Find the tests that most directly verify the central behavior, and explain how those tests reach or exercise the implementation."
        + suffix,
        "Locate where project configuration, persisted state, or package metadata is defined and consumed. If there is no runtime persistence, demonstrate that from the repository."
        + suffix,
        "For a hypothetical small extension adjacent to the central behavior, identify the smallest coherent set of implementation, documentation, and test files that would likely need changes, and justify each."
        + suffix,
    ]


def read_only_prompt(task: str) -> str:
    return (
        "READ-ONLY BENCHMARK TASK. Do not modify files, create files, change configuration, "
        "or use network services. Inspect the local repository only and answer with concise path-based evidence.\n\n"
        + task.strip()
    )


def variant_order(task_index: int, repeat_index: int) -> tuple[str, str]:
    return (
        ("baseline", "optimized")
        if (task_index + repeat_index) % 2 == 0
        else ("optimized", "baseline")
    )


def copy_repository(source: Path, destination: Path) -> None:
    def ignore(_directory: str, names: list[str]) -> set[str]:
        return set(names) & COPY_SKIP_NAMES

    shutil.copytree(source, destination, symlinks=True, ignore=ignore)


def neutralize_instructions(root: Path) -> list[str]:
    removed: list[str] = []
    for path in instruction_files(root):
        removed.append(relative(path, root))
        path.unlink()
    return sorted(removed)


def tree_digest(root: Path, ignore_instructions: bool = False) -> str:
    digest = hashlib.sha256()
    for path in iter_project_files(root):
        rel = relative(path, root)
        if ignore_instructions and path.name in INSTRUCTION_NAMES:
            continue
        digest.update(rel.encode("utf-8") + b"\0")
        if path.is_symlink():
            digest.update(b"LINK\0" + os.readlink(path).encode("utf-8"))
        else:
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
        digest.update(b"\0")
    return digest.hexdigest()


def detect_auth_mode(codex: str, requested: str) -> str:
    if requested != "auto":
        return requested
    if os.environ.get("CODEX_API_KEY") or os.environ.get("OPENAI_API_KEY"):
        return "api"
    try:
        result = subprocess.run(
            [codex, "login", "status"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return "unknown"
    status = (result.stdout + "\n" + result.stderr).lower()
    if "chatgpt" in status:
        return "chatgpt"
    if "api key" in status or "api-key" in status:
        return "api"
    return "unknown"


def codex_version(codex: str) -> str | None:
    try:
        result = subprocess.run(
            [codex, "--version"], capture_output=True, text=True, timeout=15, check=False
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value or None


def codex_command(
    codex: str,
    workspace: Path,
    model: str,
    reasoning: str,
    prompt: str,
    sandbox: str = "read-only",
) -> list[str]:
    if sandbox not in {"read-only", "workspace-write"}:
        raise BenchmarkError("benchmark sandbox must be read-only or workspace-write")
    return [
        codex,
        "exec",
        "--json",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--strict-config",
        "--sandbox",
        sandbox,
        "--model",
        model,
        "--config",
        f"model_reasoning_effort={json.dumps(reasoning)}",
        "--config",
        'approval_policy="never"',
        "--config",
        'web_search="disabled"',
        "--cd",
        str(workspace),
        "--skip-git-repo-check",
        prompt,
    ]


def execute_run(
    codex: str,
    workspace: Path,
    model: str,
    reasoning: str,
    prompt: str,
    timeout_seconds: int,
    sandbox: str = "read-only",
    raw_path: Path | None = None,
) -> dict[str, Any]:
    command = codex_command(codex, workspace, model, reasoning, prompt, sandbox)
    started = time.perf_counter()
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        duration = time.perf_counter() - started
    except subprocess.TimeoutExpired as error:
        if raw_path:
            save_raw_run(raw_path, error.stdout or b"", error.stderr or b"", workspace)
        return {
            "success": False,
            "duration_seconds": time.perf_counter() - started,
            "exit_code": None,
            "error": "timeout",
            "usage": None,
            "commands": 0,
            "web_searches": 0,
            "event_count": 0,
            "parse_errors": 0,
        }
    except OSError as error:
        if raw_path:
            save_raw_run(
                raw_path, "", f"could not execute Codex: {error.__class__.__name__}", workspace
            )
        return {
            "success": False,
            "duration_seconds": time.perf_counter() - started,
            "exit_code": None,
            "error": f"could not execute Codex: {error.__class__.__name__}",
            "usage": None,
            "commands": 0,
            "web_searches": 0,
            "event_count": 0,
            "parse_errors": 0,
        }

    if raw_path:
        save_raw_run(raw_path, result.stdout, result.stderr, workspace)
    parsed = parse_jsonl(result.stdout)
    parsed["duration_seconds"] = duration
    parsed["exit_code"] = result.returncode
    if result.returncode != 0:
        parsed["success"] = False
        parsed["error"] = parsed.get("error") or f"codex exited with status {result.returncode}"
    return parsed


def save_raw_run(path: Path, stdout: str | bytes, stderr: str | bytes, workspace: Path) -> None:
    """Retain auditable local logs; replace the temporary workspace and home paths."""

    def clean(value: str | bytes) -> str:
        if isinstance(value, bytes):
            value = value.decode("utf-8", errors="replace")
        return value.replace(str(workspace), "<workspace>").replace(str(Path.home()), "<home>")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(clean(stdout), encoding="utf-8")
    path.with_suffix(".stderr.txt").write_text(clean(stderr), encoding="utf-8")


def paired_successful_runs(
    runs: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    grouped: dict[tuple[int, int], dict[str, dict[str, Any]]] = {}
    for run in runs:
        grouped.setdefault((run["task_index"], run["repeat_index"]), {})[run["variant"]] = run
    baseline: list[dict[str, Any]] = []
    optimized: list[dict[str, Any]] = []
    for key in sorted(grouped):
        pair = grouped[key]
        if set(pair) == {"baseline", "optimized"} and all(
            item["success"] for item in pair.values()
        ):
            baseline.append(pair["baseline"])
            optimized.append(pair["optimized"])
    return baseline, optimized


def aggregate_runs(
    runs: list[dict[str, Any]], rate: dict[str, Any] | None = None
) -> dict[str, Any]:
    successful = [run for run in runs if run["success"] and run.get("usage")]
    usage_keys = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens")
    aggregate: dict[str, Any] = {
        "successful_runs": len(successful),
        "failed_runs": len(runs) - len(successful),
        "elapsed_seconds": sum(float(run["duration_seconds"]) for run in successful),
        "commands": sum(int(run["commands"]) for run in successful),
        "web_searches": sum(int(run["web_searches"]) for run in successful),
    }
    for key in usage_keys:
        values = [run["usage"].get(key) for run in successful]
        aggregate[key] = sum(values) if all(value is not None for value in values) else None
    aggregate["uncached_input_tokens"] = (
        aggregate["input_tokens"] - aggregate["cached_input_tokens"]
    )
    aggregate["billed_token_volume"] = aggregate["input_tokens"] + aggregate["output_tokens"]
    durations = [float(run["duration_seconds"]) for run in successful]
    aggregate["mean_elapsed_seconds"] = statistics.mean(durations) if durations else 0.0
    aggregate["stdev_elapsed_seconds"] = statistics.stdev(durations) if len(durations) > 1 else None
    aggregate["credit_equivalent"] = (
        calculate_credits(aggregate, rate) if rate and successful else None
    )
    return aggregate


def confidence_label(repeat: int, failures: int, paired: int, expected_pairs: int) -> str:
    if failures or paired != expected_pairs or repeat <= 1:
        return "Indicative"
    return "Repeated observations; statistical confidence not established"


def report_result_statement(
    baseline: dict[str, Any],
    optimized: dict[str, Any],
    complete: bool,
    correctness_verified: bool = False,
) -> str:
    if not correctness_verified:
        return "No overall gain claim: task correctness was not evaluated. Turn completion is not task success."
    if not complete:
        return "No overall gain claim: one or more A/B runs failed or were unpaired."
    use_credits = (
        baseline.get("credit_equivalent") is not None
        and optimized.get("credit_equivalent") is not None
    )
    key = "credit_equivalent" if use_credits else "billed_token_volume"
    label = "measured credit-equivalent" if use_credits else "measured billed token volume"
    change = change_percent(float(baseline[key]), float(optimized[key]))
    if change is None:
        return f"No supported overall comparison for {label}: the baseline is zero."
    if change < 0:
        return f"ContextLean reduced {label} by {abs(change):.1f}%."
    if change > 0:
        return f"ContextLean regressed {label} by {change:.1f}%."
    return f"ContextLean produced no measured change in {label}."


def render_ab_report(report: dict[str, Any]) -> str:
    baseline = report["comparison"]["baseline"]
    optimized = report["comparison"]["optimized"]
    rows = [
        ("Input tokens", "input_tokens", ",.0f"),
        ("Cached input", "cached_input_tokens", ",.0f"),
        ("Output tokens", "output_tokens", ",.0f"),
        ("Reasoning output", "reasoning_output_tokens", ",.0f"),
        ("Commands", "commands", ",.0f"),
        ("Elapsed time (s)", "elapsed_seconds", ",.2f"),
    ]
    if baseline.get("credit_equivalent") is not None:
        rows.insert(4, ("Credit-equivalent", "credit_equivalent", ",.4f"))
    lines = [
        "# ContextLean A/B Benchmark",
        "",
        f"Model: {report['model']}",
        f"Reasoning: {report['reasoning']}",
        f"Codex CLI: {report.get('codex_cli_version') or 'unknown'}",
        f"Tasks: {len(report['tasks'])}",
        f"Repeats: {report['repeats']}",
        f"Paired successful runs: {report['comparison']['paired_runs']} / {report['comparison']['expected_pairs']}",
        "",
        "| Metric | BASELINE | OPTIMIZED | CHANGE |",
        "|---|---:|---:|---:|",
    ]
    for label, key, spec in rows:
        if baseline[key] is None or optimized[key] is None:
            lines.append(f"| {label} | unavailable | unavailable | n/a |")
            continue
        before = float(baseline[key])
        after = float(optimized[key])
        lines.append(
            f"| {label} | {format(before, spec)} | {format(after, spec)} | {format_change(change_percent(before, after))} |"
        )
    lines.extend(
        [
            "",
            f"Successful/failed runs — BASELINE: {report['all_runs']['baseline']['successful_runs']}/{report['all_runs']['baseline']['failed_runs']}; OPTIMIZED: {report['all_runs']['optimized']['successful_runs']}/{report['all_runs']['optimized']['failed_runs']}.",
            "",
            f"Result: {report['result']}",
            "",
            f"Confidence: {report['confidence']}",
            "",
        ]
    )
    if report.get("rate_card"):
        lines.extend(
            [
                f"Credit-equivalent using rate card dated {report['rate_card']['verified_on']}; this is not a statement of actual credits spent.",
                "",
            ]
        )
    elif report["authentication"] == "api":
        lines.extend(
            [
                "API-key authentication detected: ChatGPT credits were not applied; token metrics only.",
                "",
            ]
        )
    else:
        lines.extend(["No applicable dated rate card was available; token metrics only.", ""])
    lines.extend(
        [
            "One run per task is indicative; multiple repetitions provide a better estimate of model variance.",
            "Reasoning output tokens are included in output tokens for billing and are not double-counted.",
            "Command counts are exact JSONL event counts. No file-open metric is claimed.",
            "",
            "## Reproducible task suite",
            "",
        ]
    )
    for index, task in enumerate(report["tasks"], 1):
        lines.append(f"{index}. {task}")
    return "\n".join(lines).rstrip() + "\n"


def run_ab(args: argparse.Namespace) -> tuple[dict[str, Any], Path, Path]:
    repo = args.repo.resolve()
    if not repo.is_dir():
        raise BenchmarkError(f"repository not found: {repo}")
    if not any(path.name == "AGENTS.md" for path in instruction_files(repo)):
        raise BenchmarkError("optimized variant requires at least one AGENTS.md")

    task_inputs = list(args.task or [])
    if args.tasks_file:
        if task_inputs:
            raise BenchmarkError("use either --task or --tasks-file, not both")
        task_inputs = load_tasks(args.tasks_file)
    if not task_inputs:
        task_inputs = automatic_tasks(repo)
    tasks = [read_only_prompt(task) for task in task_inputs]
    if args.repeat < 1:
        raise BenchmarkError("--repeat must be at least 1")

    authentication = detect_auth_mode(args.codex, args.billing)
    card: dict[str, Any] | None = None
    rate: dict[str, Any] | None = None
    card_path = args.rate_card or Path(__file__).resolve().parents[1] / "data" / "credit-rates.json"
    if authentication == "chatgpt" and card_path.is_file():
        card = load_rate_card(card_path)
        rate = None if is_rate_stale(card) else find_rate(card, args.model)

    original_digest_before = tree_digest(repo)
    started_at = utc_now()
    runs: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="contextlean-benchmark-") as temporary:
        temporary_root = Path(temporary)
        baseline_root = temporary_root / "baseline"
        optimized_root = temporary_root / "optimized"
        copy_repository(repo, baseline_root)
        copy_repository(repo, optimized_root)
        neutralized = neutralize_instructions(baseline_root)
        if tree_digest(optimized_root) != original_digest_before:
            raise BenchmarkError("optimized copy does not match the working repository content")
        if tree_digest(baseline_root, ignore_instructions=True) != tree_digest(
            optimized_root, ignore_instructions=True
        ):
            raise BenchmarkError("A/B copies differ outside neutralized instruction files")

        sequence = 0
        for task_index, task in enumerate(tasks):
            for repeat_index in range(args.repeat):
                order = variant_order(task_index, repeat_index)
                for variant in order:
                    sequence += 1
                    workspace = baseline_root if variant == "baseline" else optimized_root
                    result = execute_run(
                        args.codex,
                        workspace,
                        args.model,
                        args.reasoning,
                        task,
                        args.timeout,
                    )
                    result.update(
                        {
                            "sequence": sequence,
                            "variant": variant,
                            "task_index": task_index,
                            "repeat_index": repeat_index,
                        }
                    )
                    runs.append(result)

        if tree_digest(baseline_root, ignore_instructions=True) != tree_digest(
            optimized_root, ignore_instructions=True
        ):
            raise BenchmarkError("a measured task changed an A/B repository copy")

    original_digest_after = tree_digest(repo)
    if original_digest_before != original_digest_after:
        raise BenchmarkError("the working repository changed during measured runs")

    baseline_all = [run for run in runs if run["variant"] == "baseline"]
    optimized_all = [run for run in runs if run["variant"] == "optimized"]
    paired_baseline, paired_optimized = paired_successful_runs(runs)
    expected_pairs = len(tasks) * args.repeat
    failures = sum(not run["success"] for run in runs)
    comparison_baseline = aggregate_runs(paired_baseline, rate)
    comparison_optimized = aggregate_runs(paired_optimized, rate)
    complete = len(paired_baseline) == expected_pairs and failures == 0
    report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "contextlean_version": CONTEXTLEAN_VERSION,
        "kind": "contextlean-ab-benchmark",
        "generated_at": utc_now(),
        "started_at": started_at,
        "model": args.model,
        "reasoning": args.reasoning,
        "codex_cli_version": codex_version(args.codex),
        "repeats": args.repeat,
        "tasks": tasks,
        "task_inputs": task_inputs,
        "task_source": "user" if args.task or args.tasks_file else "automatic",
        "authentication": authentication,
        "codex_options": {
            "json": True,
            "ephemeral": True,
            "ignore_user_config": True,
            "ignore_rules": True,
            "strict_config": True,
            "sandbox": "read-only",
            "approval_policy": "never",
            "web_search": "disabled",
        },
        "isolation": {
            "method": "temporary copies with instruction files removed from baseline",
            "neutralized_instruction_files": neutralized,
            "non_instruction_content_match": True,
            "working_repository_unchanged": True,
            "working_repository_digest_before": original_digest_before,
            "working_repository_digest_after": original_digest_after,
        },
        "runs": runs,
        "all_runs": {
            "baseline": aggregate_runs(baseline_all, rate),
            "optimized": aggregate_runs(optimized_all, rate),
        },
        "comparison": {
            "method": "paired successful task/repetition runs only",
            "paired_runs": len(paired_baseline),
            "expected_pairs": expected_pairs,
            "baseline": comparison_baseline,
            "optimized": comparison_optimized,
        },
        "confidence": confidence_label(args.repeat, failures, len(paired_baseline), expected_pairs),
        "measurement_classification": {
            "tokens": "exact Codex turn.completed JSONL fields",
            "commands": "exact unique command_execution JSONL items",
            "elapsed_time": "exact local monotonic process duration",
            "file_opens": "not reported; not reliably measurable from current events",
            "task_success": "unverified; success flags indicate execution and usage availability only",
        },
    }
    report["result"] = report_result_statement(comparison_baseline, comparison_optimized, complete)
    if card and rate:
        report["rate_card"] = {
            "model": rate["model"],
            "verified_on": card["verified_on"],
            "source_url": card["source_url"],
            "stale": is_rate_stale(card),
            "label": f"credit-equivalent using rate card dated {card['verified_on']}",
        }
    else:
        report["rate_card"] = None

    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_dir = (args.output_dir or repo / ".contextlean" / "benchmarks" / stamp).resolve()
    json_path = output_dir / "benchmark.json"
    markdown_path = output_dir / "benchmark.md"
    write_json(json_path, report)
    markdown_path.write_text(render_ab_report(report), encoding="utf-8")
    return report, json_path, markdown_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    estimate = subparsers.add_parser(
        "estimate", help="show static ContextLean metrics without running Codex"
    )
    estimate.add_argument("--repo", type=Path, default=Path.cwd())
    estimate.add_argument("--report", type=Path)

    start = subparsers.add_parser(
        "bootstrap-start", help="capture the pre-bootstrap static baseline"
    )
    start.add_argument("--repo", type=Path, default=Path.cwd())
    start.add_argument("--output", type=Path)
    start.add_argument("--project-type")

    finish = subparsers.add_parser(
        "bootstrap-finish", help="write the verified bootstrap before/after report"
    )
    finish.add_argument("--repo", type=Path, default=Path.cwd())
    finish.add_argument("--baseline", type=Path)
    finish.add_argument("--output", type=Path)
    finish.add_argument("--project-type")
    finish.add_argument("--created", action="append", default=[])
    finish.add_argument("--modified", action="append", default=[])
    finish.add_argument("--moved", action="append", default=[])
    finish.add_argument("--exclusion", action="append", default=[])
    finish.add_argument("--limit", action="append", default=[])
    finish.add_argument("--keep-baseline", action="store_true")

    ab = subparsers.add_parser("ab", help="run a real isolated Codex A/B benchmark")
    ab.add_argument("--repo", type=Path, default=Path.cwd())
    ab.add_argument("--model", required=True)
    ab.add_argument("--reasoning", required=True)
    ab.add_argument("--task", action="append")
    ab.add_argument("--tasks-file", type=Path)
    ab.add_argument("--repeat", type=int, default=1)
    ab.add_argument("--timeout", type=int, default=900)
    ab.add_argument("--output-dir", type=Path)
    ab.add_argument("--codex", default="codex")
    ab.add_argument("--billing", choices=("auto", "chatgpt", "api", "tokens-only"), default="auto")
    ab.add_argument("--rate-card", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "estimate":
            repo = args.repo.resolve()
            report_path = (args.report or repo / ".contextlean" / "bootstrap-report.json").resolve()
            if report_path.is_file():
                report = read_json(report_path)
                if report.get("kind") != "contextlean-bootstrap-report":
                    raise BenchmarkError(f"not a ContextLean bootstrap report: {report_path}")
            else:
                report = {
                    "kind": "contextlean-bootstrap-report",
                    "baseline_available": False,
                    "after": static_snapshot(repo),
                }
            sys.stdout.write(render_static_report(report))
            return 0
        if args.command == "bootstrap-start":
            repo = args.repo.resolve()
            output = (args.output or repo / ".contextlean" / ".bootstrap-baseline.json").resolve()
            bootstrap_start(repo, output, args.project_type)
            print(output)
            return 0
        if args.command == "bootstrap-finish":
            repo = args.repo.resolve()
            baseline = (
                args.baseline or repo / ".contextlean" / ".bootstrap-baseline.json"
            ).resolve()
            output = (args.output or repo / ".contextlean" / "bootstrap-report.json").resolve()
            report = bootstrap_finish(
                repo,
                baseline,
                output,
                args.project_type,
                args.created,
                args.modified,
                args.moved,
                args.exclusion,
                args.limit,
                args.keep_baseline,
            )
            print(output)
            return 0
        if args.command == "ab":
            report, json_path, markdown_path = run_ab(args)
            sys.stdout.write(render_ab_report(report))
            print(f"\nJSON: {json_path}")
            print(f"Markdown: {markdown_path}")
            return 0 if report["comparison"]["paired_runs"] else 2
    except (BenchmarkError, OSError, ValueError, KeyError) as error:
        print(f"benchmark error: {error}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
