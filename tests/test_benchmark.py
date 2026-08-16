import datetime as dt
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/benchmark/scripts/benchmark.py"
FIXTURES = ROOT / "tests/fixtures/benchmark"
SPEC = importlib.util.spec_from_file_location("contextlean_benchmark", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load benchmark module")
benchmark = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(benchmark)


def fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def successful_run(variant: str, task: int, repeat: int, *, scale: int = 1) -> dict:
    return {
        "variant": variant,
        "task_index": task,
        "repeat_index": repeat,
        "success": True,
        "duration_seconds": 1.5 * scale,
        "commands": 2 * scale,
        "web_searches": 0,
        "usage": {
            "input_tokens": 1000 * scale,
            "cached_input_tokens": 400 * scale,
            "output_tokens": 200 * scale,
            "reasoning_output_tokens": 100 * scale,
        },
    }


class JsonlParsingTests(unittest.TestCase):
    def test_parses_turn_usage_and_unique_item_counts(self) -> None:
        result = benchmark.parse_jsonl(fixture("success.jsonl"))

        self.assertTrue(result["success"])
        self.assertEqual(result["thread_id"], "thread-success")
        self.assertEqual(result["usage"]["input_tokens"], 1000)
        self.assertEqual(result["usage"]["cached_input_tokens"], 400)
        self.assertEqual(result["usage"]["output_tokens"], 200)
        self.assertEqual(result["usage"]["reasoning_output_tokens"], 100)
        self.assertEqual(result["commands"], 1)
        self.assertEqual(result["web_searches"], 1)

    def test_failed_turn_is_not_successful(self) -> None:
        result = benchmark.parse_jsonl(fixture("failed.jsonl"))

        self.assertFalse(result["success"])
        self.assertIsNone(result["usage"])
        self.assertIn("turn.completed", result["error"])

    def test_invalid_cached_usage_is_rejected(self) -> None:
        result = benchmark.parse_jsonl(fixture("invalid-usage.jsonl"))

        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "cached_input_tokens exceeds input_tokens")

    def test_malformed_jsonl_is_a_run_error(self) -> None:
        result = benchmark.parse_jsonl(fixture("success.jsonl") + "not-json\n")

        self.assertFalse(result["success"])
        self.assertEqual(result["parse_errors"], 1)

    def test_idless_started_and_completed_events_are_not_double_counted(self) -> None:
        stream = "\n".join(
            [
                '{"type":"item.started","item":{"type":"command_execution"}}',
                '{"type":"item.completed","item":{"type":"command_execution"}}',
                '{"type":"turn.completed","usage":{"input_tokens":1,"cached_input_tokens":0,"output_tokens":1,"reasoning_output_tokens":0}}',
            ]
        )
        result = benchmark.parse_jsonl(stream)

        self.assertTrue(result["success"])
        self.assertEqual(result["commands"], 1)


class CalculationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.usage = {
            "input_tokens": 1000,
            "cached_input_tokens": 400,
            "output_tokens": 200,
            "reasoning_output_tokens": 100,
        }
        self.rate = {"input": 100, "cached_input": 10, "output": 200}

    def test_uncached_input_treats_cached_as_subset(self) -> None:
        self.assertEqual(benchmark.uncached_input_tokens(self.usage), 600)

    def test_credit_calculation_does_not_double_count_reasoning(self) -> None:
        self.assertAlmostEqual(benchmark.calculate_credits(self.usage, self.rate), 0.104)

    def test_negative_uncached_input_is_an_error(self) -> None:
        invalid = dict(self.usage, cached_input_tokens=1001)
        with self.assertRaises(benchmark.BenchmarkError):
            benchmark.uncached_input_tokens(invalid)

    def test_percentages(self) -> None:
        self.assertEqual(benchmark.change_percent(100, 80), -20)
        self.assertEqual(benchmark.change_percent(100, 120), 20)
        self.assertEqual(benchmark.change_percent(0, 0), 0)
        self.assertIsNone(benchmark.change_percent(0, 1))

    def test_aggregation_sums_usage_commands_and_elapsed(self) -> None:
        runs = [successful_run("baseline", 0, 0), successful_run("baseline", 1, 0, scale=2)]
        aggregate = benchmark.aggregate_runs(runs, self.rate)

        self.assertEqual(aggregate["successful_runs"], 2)
        self.assertEqual(aggregate["input_tokens"], 3000)
        self.assertEqual(aggregate["cached_input_tokens"], 1200)
        self.assertEqual(aggregate["uncached_input_tokens"], 1800)
        self.assertEqual(aggregate["output_tokens"], 600)
        self.assertEqual(aggregate["reasoning_output_tokens"], 300)
        self.assertEqual(aggregate["commands"], 6)
        self.assertEqual(aggregate["elapsed_seconds"], 4.5)
        self.assertAlmostEqual(aggregate["credit_equivalent"], 0.312)

    def test_pairing_excludes_failed_pairs(self) -> None:
        runs = [
            successful_run("baseline", 0, 0),
            successful_run("optimized", 0, 0),
            successful_run("baseline", 1, 0),
            dict(successful_run("optimized", 1, 0), success=False, usage=None),
        ]
        baseline, optimized = benchmark.paired_successful_runs(runs)

        self.assertEqual(len(baseline), 1)
        self.assertEqual(len(optimized), 1)
        self.assertEqual(baseline[0]["task_index"], 0)

    def test_order_is_balanced_deterministically(self) -> None:
        self.assertEqual(benchmark.variant_order(0, 0), ("baseline", "optimized"))
        self.assertEqual(benchmark.variant_order(1, 0), ("optimized", "baseline"))
        self.assertEqual(benchmark.variant_order(0, 1), ("optimized", "baseline"))

    def test_codex_command_is_explicit_and_never_uses_full_access(self) -> None:
        command = benchmark.codex_command(
            "codex", Path("/tmp/fixture"), "fixture-model", "medium", "fixture task"
        )
        rendered = " ".join(command)

        self.assertIn("--json", command)
        self.assertIn("--ephemeral", command)
        self.assertIn("--ignore-user-config", command)
        self.assertIn("--ignore-rules", command)
        self.assertIn("--strict-config", command)
        self.assertIn("read-only", command)
        self.assertIn('web_search="disabled"', command)
        self.assertNotIn("danger-full-access", rendered)
        self.assertNotIn("project_doc_max_bytes", rendered)


class RateCardTests(unittest.TestCase):
    def test_missing_model_rate_returns_none(self) -> None:
        card = {"models": [{"model": "known", "aliases": []}]}
        self.assertIsNone(benchmark.find_rate(card, "missing"))

    def test_alias_rate_is_found(self) -> None:
        card = {"models": [{"model": "canonical", "aliases": ["alias"]}]}
        self.assertEqual(benchmark.find_rate(card, "alias")["model"], "canonical")

    def test_stale_and_current_rate_cards(self) -> None:
        today = dt.date(2026, 8, 16)
        self.assertFalse(
            benchmark.is_rate_stale({"verified_on": "2026-08-01"}, today=today)
        )
        self.assertTrue(
            benchmark.is_rate_stale({"verified_on": "2026-01-01"}, today=today)
        )
        self.assertTrue(benchmark.is_rate_stale({}, today=today))


class StaticReportTests(unittest.TestCase):
    def test_snapshot_and_bootstrap_report_store_metrics_not_contents(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            (repo / "AGENTS.md").write_text("secret-shaped-text\n", encoding="utf-8")
            baseline_path = repo / ".contextlean/.bootstrap-baseline.json"
            report_path = repo / ".contextlean/bootstrap-report.json"
            benchmark.bootstrap_start(repo, baseline_path, "fixture")
            (repo / "nested").mkdir()
            (repo / "nested/AGENTS.md").write_text("nested map\n", encoding="utf-8")
            report = benchmark.bootstrap_finish(
                repo,
                baseline_path,
                report_path,
                "fixture",
                ["nested/AGENTS.md"],
                ["AGENTS.md"],
                [],
                [],
                [],
            )

            serialized = json.dumps(report)
            self.assertNotIn("secret-shaped-text", serialized)
            self.assertTrue(report["baseline_available"])
            self.assertEqual(report["before"]["project_maps"]["value"], 1)
            self.assertEqual(report["after"]["project_maps"]["value"], 2)
            self.assertFalse(baseline_path.exists())
            self.assertTrue(report_path.is_file())

    def test_current_only_report_explains_missing_baseline(self) -> None:
        report = {
            "baseline_available": False,
            "after": {
                "automatic_instruction_bytes": {"value": 100},
                "automatic_instruction_tokens": {"value": 25},
                "large_mandatory_startup_docs": {"value": 0},
                "project_maps": {"value": 1},
            },
        }
        markdown = benchmark.render_static_report(report)

        self.assertIn("true static before/after is not available", markdown)
        self.assertIn("[exact]", markdown)
        self.assertIn("[estimated]", markdown)
        self.assertIn("[heuristic]", markdown)
        self.assertIn("not measured model-token savings", markdown)

    def test_automatic_suite_is_five_wrapped_read_only_navigation_tasks(self) -> None:
        tasks = benchmark.automatic_tasks(ROOT)
        wrapped = [benchmark.read_only_prompt(task) for task in tasks]

        self.assertEqual(len(tasks), 5)
        self.assertTrue(all("Do not rely only on AGENTS.md" in task for task in tasks))
        self.assertTrue(all(task.startswith("READ-ONLY BENCHMARK TASK") for task in wrapped))


class AbReportTests(unittest.TestCase):
    def report(self, complete: bool = True) -> dict:
        baseline = benchmark.aggregate_runs([successful_run("baseline", 0, 0)])
        optimized = benchmark.aggregate_runs([successful_run("optimized", 0, 0)])
        if complete:
            optimized["input_tokens"] = 800
            optimized["billed_token_volume"] = 1000
        return {
            "model": "fixture-model",
            "reasoning": "medium",
            "codex_cli_version": "codex-cli fixture",
            "tasks": ["Inspect two subsystems."],
            "repeats": 1,
            "authentication": "api",
            "rate_card": None,
            "all_runs": {
                "baseline": {"successful_runs": 1, "failed_runs": 0},
                "optimized": {"successful_runs": int(complete), "failed_runs": int(not complete)},
            },
            "comparison": {
                "paired_runs": int(complete),
                "expected_pairs": 1,
                "baseline": baseline,
                "optimized": optimized,
            },
            "result": benchmark.report_result_statement(baseline, optimized, complete),
            "confidence": "Indicative",
        }

    def test_markdown_reports_regression_or_supported_gain_only(self) -> None:
        report = self.report(complete=True)
        markdown = benchmark.render_ab_report(report)

        self.assertIn("ContextLean reduced measured billed token volume", markdown)
        self.assertIn("API-key authentication detected", markdown)
        self.assertIn("No file-open metric is claimed", markdown)
        self.assertIn("Reproducible task suite", markdown)

    def test_failed_run_suppresses_gain_claim(self) -> None:
        report = self.report(complete=False)
        self.assertIn("No overall gain claim", report["result"])

    def test_json_and_markdown_are_machine_and_human_readable(self) -> None:
        report = self.report(complete=True)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            json_path = root / "benchmark.json"
            markdown_path = root / "benchmark.md"
            benchmark.write_json(json_path, report)
            markdown_path.write_text(benchmark.render_ab_report(report), encoding="utf-8")

            self.assertEqual(json.loads(json_path.read_text(encoding="utf-8"))["model"], "fixture-model")
            self.assertTrue(markdown_path.read_text(encoding="utf-8").startswith("# ContextLean A/B Benchmark"))


if __name__ == "__main__":
    unittest.main()
