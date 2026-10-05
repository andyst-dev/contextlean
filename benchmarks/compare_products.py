#!/usr/bin/env python3
"""Guided product comparison adapter v1; delegates all execution to harness v4.

The public Vanilla/ContextLean condition constructor and manifest remain unchanged.
This entry point freezes two committed generators' output, never current guidance.
"""

import argparse
import importlib.util
import io
from pathlib import Path
import re
import subprocess
import sys
import tarfile


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "product_runner", ROOT / "benchmarks/run_benchmark.py"
)
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)
h = runner.harness
ADAPTER_VERSION = 1
REVISIONS = {
    "old": "ae8653b123bdb4c686ee36825c80db851c8595ea",
    "balanced": "1a6e67fb9e5c3d5a91ca89a9f5466d2fa037ea52",
}
ORDER = ("old", "balanced", "balanced", "old", "old", "balanced")
UNCHANGED = (
    "benchmarks/harness.py",
    "benchmarks/execution.py",
    "benchmarks/runtime.py",
    "benchmarks/trace.py",
    "benchmarks/prepare_fixture.py",
    "benchmarks/evaluate.py",
    "benchmarks/tasks/suite.json",
    "skills/benchmark/scripts/benchmark.py",
)
# Source evidence for the unchanged, independently reviewed sample owners.
MAP_EVIDENCE = {
    "expense_report/cli.py": 'args.currency or config["currency"]',
    "expense_report/storage.py": 'Decimal(row["amount"])',
    "expense_report/filters.py": 'if normalize_category(expense["category"]) == category',
    "expense_report/report.py": 'categories[key] = categories.get(key, Decimal("0"))',
    "config.json": '{"currency": "USD"}',
    "tests/test_expenses.py": "def test_configured_default(self):",
    "data/sample.csv": "Food,12.50",
    "README.md": "python3 -m unittest discover -s tests -v",
}


def product_inventory(path):
    return {k: v for k, v in h.inventory(path).items() if k not in h.GUIDANCE}


def archive_revision(repo, revision, destination):
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise h.HarnessError("full immutable product SHA required")
    resolved = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "--verify", revision + "^{commit}"], text=True
    ).strip()
    if resolved != revision:
        raise h.HarnessError("product revision did not resolve exactly")
    # Export committed inputs, never a worktree copy. Historical results are not needed.
    paths = [
        "tests/bootstrap_fixture.py",
        "tests/fixtures",
        "skills/bootstrap",
        "skills/lean-review",
        "benchmarks/fixtures/expense-report",
        *UNCHANGED,
    ]
    data = subprocess.check_output(["git", "-C", str(repo), "archive", revision, "--", *paths])
    destination.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        for member in archive.getmembers():
            if member.issym() or member.islnk() or not (member.isfile() or member.isdir()):
                raise h.HarnessError("unexpected non-file in committed product inputs")
        archive.extractall(destination, filter="data")
    return h.inventory(destination)


def generate(source, destination, condition):
    """Run the committed fixture generator in a separate, bytecode-free interpreter."""
    program = """import importlib.util, pathlib, sys
source, target, condition = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
generator = load("frozen_generator", source / "tests/bootstrap_fixture.py")
if condition == "old":
    transfer = load("frozen_transfer", source / "skills/bootstrap/scripts/verify_transfer.py")
    generator.generate(target, transfer)
    (target / "transfer.json").unlink()
else:
    generator.generate(target)
"""
    subprocess.run(
        [sys.executable, "-I", "-B", "-c", program, str(source), str(destination), condition],
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )


class GuidedComparison:
    """Only product artifacts, condition identity and comparison-specific assertions."""

    def __init__(self, repo, inputs):
        self.inputs = Path(inputs).resolve()
        if self.inputs.exists():
            raise h.HarnessError("comparison inputs must use a fresh directory")
        self.paths, self.sources, self.records, self.reviews = {}, {}, {}, {}
        self.revisions = dict(REVISIONS)
        if len(set(self.revisions.values())) != 2:
            raise h.HarnessError("two distinct product revisions required")
        for name, revision in self.revisions.items():
            source = self.inputs / "sources" / name
            self.sources[name] = archive_revision(repo, revision, source)
            for relative in UNCHANGED:
                if (source / relative).read_bytes() != (ROOT / relative).read_bytes():
                    raise h.HarnessError(f"validated shared input changed: {relative}")
            target = self.inputs / "conditions" / name
            h.copy_fixture(source / "benchmarks/fixtures/expense-report", target)
            for relative in h.GUIDANCE:
                (target / relative).unlink(missing_ok=True)
            generate(source, target, name)
            h.compare_receipts(
                product_inventory(source / "benchmarks/fixtures/expense-report"),
                product_inventory(target),
                "generator product preservation",
            )
            self.paths[name] = target
            self.records[name] = h.inventory(target)
            entries = runner.preparation.project_map(target)
            if set(entries) != set(MAP_EVIDENCE):
                raise h.HarnessError("unexpected project map owners")
            self.reviews[name] = {
                "semantics_reviewed": True,
                "entries": {
                    path: {
                        "responsibility": description,
                        "evidence": [{"path": path, "contains": MAP_EVIDENCE[path]}],
                    }
                    for path, description in entries.items()
                },
            }
        self.fixture = self.paths["old"]
        self.tasks = self.inputs / "refactor.json"
        task = next(
            t
            for t in runner.load_suite(self.inputs / "sources/old/benchmarks/tasks/suite.json")
            if t["id"] == "refactor"
        )
        h.write_json(self.tasks, {"tasks": [task]})
        self.task_bytes = self.tasks.read_bytes()
        self.frozen = self.validate()
        h.write_json(self.inputs / "products.json", self.frozen)

    def identity(self, name):
        if name not in self.revisions:
            raise h.HarnessError("unknown guided condition")
        files = {p: value for p, value in self.records[name].items() if p in h.GUIDANCE}
        return {
            "condition_kind": "guided_product_revision",
            "condition_name": name,
            "product_revision": self.revisions[name],
            "guidance_files": files,
            "automatic_guidance_bytes": sum(files[p]["size"] for p in ("AGENTS.md", "CLAUDE.md")),
        }

    def manifest(self, paths, first_prompt, second_prompt):
        if first_prompt != second_prompt:
            raise h.HarnessError("task prompt bytes differ")
        inventories = {}
        for name in self.revisions:
            inventories[name] = h.inventory(paths[name])
            guidance = set(inventories[name]) & h.GUIDANCE
            required = h.GUIDANCE if name == "old" else {"AGENTS.md", "CLAUDE.md"}
            if guidance != required or any(inventories[name][p]["size"] == 0 for p in required):
                raise h.HarnessError(f"{name} requires exact nonempty committed guidance")
            h.compare_receipts(self.records[name], inventories[name], f"{name} frozen fixture")
        h.compare_receipts(
            product_inventory(paths["old"]),
            product_inventory(paths["balanced"]),
            "non-guidance fixture",
        )
        if inventories["old"]["AGENTS.md"] == inventories["balanced"]["AGENTS.md"]:
            raise h.HarnessError("product guidance must differ")
        return {
            "comparison_adapter_version": ADAPTER_VERSION,
            "benchmark_harness_version": h.VERSION,
            "condition_kind": "guided_product_revision",
            "conditions": {name: self.identity(name) for name in self.revisions},
            "files": [
                {
                    "path": p,
                    "condition_specific": p in h.GUIDANCE,
                    **{name: inventories[name].get(p) for name in self.revisions},
                }
                for p in sorted(set(inventories["old"]) | set(inventories["balanced"]))
            ],
            "prompt_sha256": h.digest(first_prompt),
            "prompt_size": len(first_prompt),
        }

    def validate(self, expected=None):
        for name in self.revisions:
            source = self.inputs / "sources" / name
            h.compare_receipts(self.sources[name], h.inventory(source), "committed source inputs")
            # Reuse the existing map/command/import/source-review validator. Its
            # legacy condition-labelled digest fields are not serialized as identities.
            runner.preparation.validate(self.paths[name], self.reviews[name])
        if self.tasks.read_bytes() != self.task_bytes:
            raise h.HarnessError("frozen Refactor task changed")
        record = self.manifest(
            self.paths,
            runner.task_prompt(runner.load_suite(self.tasks)[0]).encode(),
            runner.task_prompt(runner.load_suite(self.tasks)[0]).encode(),
        )
        record["source_inputs"] = self.sources
        record["reviews"] = self.reviews
        if expected is not None:
            h.compare_receipts(expected, record, "product preparation")
        return record

    def make_conditions(self, destination):
        paths = {name: destination / name for name in self.revisions}
        for name, path in paths.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            h.copy_fixture(self.paths[name], path)
        return paths

    def schedule(self, tasks, args):
        if (
            tasks != runner.load_suite(self.tasks)
            or args.tasks_file != self.tasks
            or args.repeat != 3
            or args.provider != "codex"
            or args.model != "gpt-5.6-sol"
            or args.reasoning != "high"
        ):
            raise h.HarnessError("comparison requires the exact six-slot Refactor contract")
        return [
            dict(
                sequence=i + 1,
                task="refactor",
                repeat=i // 2 + 1,
                condition=name,
                **self.identity(name),
            )
            for i, name in enumerate(ORDER)
        ]

    def check_runtime(self, runtime):
        required = {
            "python3": r"Python 3\.14\.4",
            "git": r"git version 2\.54\.0(?: \(.+\))?",
            "rg": r"ripgrep 15\.2\.0(?: \(.+\))?",
        }
        for name, pattern in required.items():
            version = runtime["binaries"][name]["version"].splitlines()[0]
            if not re.fullmatch(pattern, version):
                raise h.HarnessError(f"comparison runtime mismatch: {name} {version}")
        if h.VERSION != 4 or runner.trace.COVERAGE_PARSER_VERSION != 2:
            raise h.HarnessError("requires harness v4 and coverage parser v2")

    def input_hashes(self):
        return {"benchmarks/compare_products.py": h.digest(Path(__file__).read_bytes())}

    def report_metadata(self):
        return {
            "kind": "contextlean-guided-product-validation",
            "comparison_adapter_version": ADAPTER_VERSION,
            "conditions": list(self.revisions),
            "products": {n: self.identity(n) for n in self.revisions},
            "paired_label": "Paired differences (Balanced minus Old):",
            "retries": 0,
        }

    def paired_metrics(self, runs):
        # Product comparison aggregation only; all measurements come from v4.
        metrics = ("total_tokens", "duration_seconds", "command_calls")
        pairs = []
        for repetition in range(1, 4):
            pair = {r["condition"]: r for r in runs if r["repeat"] == repetition}
            complete = set(pair) == set(self.revisions) and all(
                r["measurement_complete"] for r in pair.values()
            )
            differences = {
                m: pair["balanced"]["metrics"][m] - pair["old"]["metrics"][m]
                if complete and all(pair[n]["metrics"].get(m) is not None for n in self.revisions)
                else None
                for m in metrics
            }
            old_tokens = pair.get("old", {}).get("metrics", {}).get("total_tokens")
            pairs.append(
                {
                    "repeat": repetition,
                    "complete": complete,
                    "differences": differences,
                    "token_percentage": 100 * differences["total_tokens"] / old_tokens
                    if differences["total_tokens"] is not None and old_tokens
                    else None,
                }
            )
        return [
            {
                "task": "refactor",
                "pairs": pairs,
                "differences": {
                    m: h.distribution([p["differences"][m] for p in pairs])
                    if all(p["differences"][m] is not None for p in pairs)
                    else None
                    for m in metrics
                },
            }
        ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, required=True)
    launch = parser.add_mutually_exclusive_group(required=True)
    launch.add_argument("--preflight-only", action="store_true")
    launch.add_argument(
        "--live", action="store_true", help="Requires a separate explicit user request"
    )
    parser.add_argument("--codex", default="codex")
    parser.add_argument("--shell")
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    if output.exists():
        parser.error("output must be a new directory; no retries or resuming")
    output.mkdir(parents=True)
    try:
        comparison = GuidedComparison(args.repo, output / "inputs")
        args.tasks_file = comparison.tasks
        args.output_dir = output / "campaign"
        args.model, args.reasoning, args.provider = "gpt-5.6-sol", "high", "codex"
        args.repeat, args.experiment_kind = 3, "product-change-validation"
        report = runner.run(args, comparison=comparison)
        (output / "report.md").write_text(runner.render(report) + "\n")
        print(runner.render(report))
        success = report["status"] == "preflight-passed" or (
            report["status"] == "complete"
            and all(run["evaluation"].get("task_success") is True for run in report["runs"])
        )
        return 0 if success else 2
    except (
        h.HarnessError,
        runner.core.BenchmarkError,
        OSError,
        ValueError,
        subprocess.SubprocessError,
    ) as error:
        h.write_json(output / "adapter-error.json", h.Sanitizer().value({"error": str(error)}))
        print(f"Product comparison stopped: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
