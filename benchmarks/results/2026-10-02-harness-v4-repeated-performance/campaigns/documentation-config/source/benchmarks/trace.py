"""Extract exposed provider evidence without estimating hidden work or costs."""

import hashlib
import json
import re


COVERAGE_PARSER_VERSION = 2


def normalize_usage(raw, claude=False):
    if not isinstance(raw, dict):
        return None
    keys = ["input_tokens", "output_tokens"] + (
        ["cache_creation_input_tokens", "cache_read_input_tokens"]
        if claude
        else ["cached_input_tokens"]
    )
    if any(type(raw.get(k)) is not int or raw[k] < 0 for k in keys):
        return None
    ordinary = raw["input_tokens"]
    cached = raw["cache_read_input_tokens"] if claude else raw["cached_input_tokens"]
    total_input = ordinary + raw["cache_creation_input_tokens"] + cached if claude else ordinary
    if cached > total_input:
        return None
    return {
        "input_tokens": total_input,
        "cached_input_tokens": cached,
        "uncached_input_tokens": total_input - cached,
        "output_tokens": raw["output_tokens"],
        "total_tokens": total_input + raw["output_tokens"],
        "reasoning_output_tokens": raw.get("reasoning_output_tokens")
        if not claude
        else raw.get("output_tokens_details", {}).get("thinking_tokens"),
    }


def coverage(command, text):
    if not re.search(
        r"(?:\bunittest\b|\bpytest\b|\b(?:npm|cargo|go)\s+(?:run\s+)?test\b)", command
    ):
        return None
    tests = re.findall(
        r"^([\w.]+) \(([^)]+)\) \.\.\. (ok|FAIL|ERROR|expected failure|unexpected success|skipped[^\n]*)$",
        text,
        re.M,
    )
    # Python 3.9 prints method (module.Class); newer versions include the
    # method inside the parentheses too. Both expose the full identity.
    names = sorted(
        {
            (identity if identity.endswith("." + method) else identity + "." + method).removeprefix(
                "tests."
            )
            for method, identity, _ in tests
        }
    )
    counts = re.findall(r"^Ran (\d+) tests?\b", text, re.M)
    discovered = int(counts[-1]) if len(counts) == 1 else None
    passed = sum(status == "ok" for _, _, status in tests) if tests else None
    failed = sum(status == "FAIL" for _, _, status in tests) if tests else None
    errors = sum(status == "ERROR" for _, _, status in tests) if tests else None
    skipped = sum(status.startswith("skipped") for _, _, status in tests) if tests else None
    expected_failures = (
        sum(status == "expected failure" for _, _, status in tests) if tests else None
    )
    unexpected_successes = (
        sum(status == "unexpected success" for _, _, status in tests) if tests else None
    )
    complete = discovered is not None and len(names) == len(tests) == discovered and discovered > 0
    counts_complete = complete
    count_scope = "exposed status rows only"
    summaries = re.findall(r"^(OK|FAILED)(?: \(([^\n]*)\))?\s*$", text, re.M)
    if discovered is not None and len(summaries) == 1:
        fields = {
            name.strip(): value for name, value in re.findall(r"([a-z ]+)=(\d+)", summaries[0][1])
        }
        supported = {"failures", "errors", "skipped", "expected failures", "unexpected successes"}
        if set(fields) <= supported:
            failed, errors, skipped, expected_failures, unexpected_successes = (
                int(fields.get(name, 0))
                for name in [
                    "failures",
                    "errors",
                    "skipped",
                    "expected failures",
                    "unexpected successes",
                ]
            )
            passed = (
                discovered - failed - errors - skipped - expected_failures - unexpected_successes
            )
            counts_complete = passed >= 0 and (
                (summaries[0][0] == "OK") == (failed == errors == unexpected_successes == 0)
            )
            count_scope = "single unittest footer; no identities inferred"
    if not tests and discovered is None:
        pytest = re.search(r"(\d+) passed", text)
        passed = int(pytest[1]) if pytest else None
        failure = re.search(r"(\d+) failed", text)
        failed = int(failure[1]) if failure else None
        if pytest:
            discovered = passed + (failed or 0)
    return {
        "coverage_parser_version": COVERAGE_PARSER_VERSION,
        "command": command,
        "discovered_count": discovered,
        "passed_count": passed,
        "failed_count": failed,
        "error_count": errors,
        "skipped_count": skipped,
        "expected_failure_count": expected_failures,
        "unexpected_success_count": unexpected_successes,
        "status_counts_complete": counts_complete,
        "status_count_scope": count_scope,
        "test_names": names,
        "test_list_complete": complete,
        "normalized_test_list_sha256": hashlib.sha256("\n".join(names).encode()).hexdigest()
        if complete
        else None,
        "passed": complete
        and counts_complete
        and passed + skipped + expected_failures == discovered
        and failed == errors == unexpected_successes == 0,
        "identity_scope": "exposed test output only; hidden coverage unavailable",
    }


def parse(text, provider, cwd):
    events, errors = [], []
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError("non-object event")
            events.append((line_number, value))
        except ValueError:
            errors.append(line_number)
    calls, by_id, usage_records, message_ids = [], {}, [], {}
    verifications, changes = [], []
    results, completions, failures = [], [], []
    init, session_ids, requests = {}, set(), set()

    def new_call(identifier, line, name, inputs, timestamp=None):
        if identifier in by_id:
            return by_id[identifier]
        call = {
            "sequence": len(calls) + 1,
            "event_line": line,
            "id": identifier,
            "tool": name,
            "input": inputs,
            "command": inputs.get("command") if isinstance(inputs, dict) else None,
            "cwd": cwd,
            "cwd_scope": "session cwd; shell may change cwd internally",
            "timestamp": timestamp,
            "exit_code": None,
            "status": "unknown",
            "executed": None,
            "denied": False,
            "denial_reason": None,
            "duration_seconds": None,
            "stdout_bytes": None,
            "stderr_bytes": None,
            "returned_content_bytes": None,
            "files_changed_afterward": None,
            "file_change_scope": "unavailable unless provider explicitly exposes changes",
        }
        calls.append(call)
        by_id[identifier] = call
        return call

    def verify(call, output, line):
        item = coverage(call.get("command") or "", output)
        if not item:
            return
        item.update(
            event_line=line,
            command_sequence=call["sequence"],
            equivalent_previous_pass=None,
            intervening_relevant_change=None,
        )
        if item["passed"]:
            previous = next(
                (
                    v
                    for v in reversed(verifications)
                    if v["passed"]
                    and v["normalized_test_list_sha256"] == item["normalized_test_list_sha256"]
                ),
                None,
            )
            if previous:
                item["equivalent_previous_pass"] = previous["command_sequence"]
                changed = any(previous["event_line"] < c < line for c in changes)
                uncertain = any(
                    previous["event_line"] < c["event_line"] < line
                    and c["sequence"] != call["sequence"]
                    and c["tool"]
                    in {"Bash", "command_execution", "mcp_tool_call", "dynamic_tool_call"}
                    for c in calls
                )
                item["intervening_relevant_change"] = (
                    True if changed else None if uncertain else False
                )
        item["change_scope"] = "exposed changes only; no hidden-state inference"
        verifications.append(item)

    for line, event in events:
        kind = event.get("type")
        if event.get("session_id"):
            session_ids.add(event["session_id"])
        if event.get("request_id"):
            requests.add(event["request_id"])
        if kind == "thread.started":
            session_ids.add(event["thread_id"])
        if kind == "system" and event.get("subtype") == "init":
            init = event
        if kind == "result":
            results.append(event)
        if kind == "turn.completed":
            completions.append(event)
            usage_records.append(
                {
                    "event_line": line,
                    "scope": "top-level turn aggregate",
                    "raw": event.get("usage"),
                    "normalized": normalize_usage(event.get("usage")),
                }
            )
        if kind in {"turn.failed", "error"}:
            failures.append(event)
        if kind == "assistant":
            message = event.get("message", {})
            identifier = message.get("id")
            if identifier:
                message_ids.setdefault(identifier, line)
                usage_records.append(
                    {
                        "event_line": line,
                        "message_id": identifier,
                        "request_id": event.get("request_id"),
                        "scope": "message-stream report; partial/duplicate reports retained and never summed",
                        "raw": message.get("usage"),
                        "normalized": normalize_usage(message.get("usage"), True),
                    }
                )
            for block in message.get("content", []):
                if block.get("type") == "tool_use":
                    call = new_call(
                        block["id"],
                        line,
                        block["name"],
                        block.get("input", {}),
                        event.get("timestamp"),
                    )
                    if block["name"] in {"Edit", "Write"}:
                        # An attempt is not yet a successful mutation.
                        call["mutation_attempt"] = True
        if kind == "system" and event.get("subtype") == "permission_denied":
            call = by_id.get(event.get("tool_use_id"))
            if call:
                call.update(
                    status="denied",
                    denied=True,
                    executed=False,
                    denial_reason=event.get("decision_reason") or event.get("message"),
                    denial_reason_type=event.get("decision_reason_type"),
                )
        if kind == "user":
            result = event.get("tool_use_result")
            for block in event.get("message", {}).get("content", []):
                if block.get("type") != "tool_result":
                    continue
                call = by_id.get(block.get("tool_use_id"))
                if not call:
                    continue
                content = block.get("content", "")
                content = (
                    content if isinstance(content, str) else json.dumps(content, ensure_ascii=False)
                )
                call["returned_content_bytes"] = len(content.encode())
                call["result"] = result
                if not call["denied"]:
                    call["status"] = "error" if block.get("is_error") else "completed"
                    call["executed"] = True if isinstance(result, dict) else None
                match = re.search(r"Exit code (\d+)", content)
                if match:
                    call.update(exit_code=int(match[1]), executed=True)
                if isinstance(result, dict):
                    if "stdout" in result:
                        call.update(
                            stdout_bytes=len(result["stdout"].encode()),
                            stderr_bytes=len(result.get("stderr", "").encode()),
                        )
                    if "file" in result:
                        file = result["file"]
                        call["displayed_file"] = {
                            "path": file.get("filePath"),
                            "bytes": len(file.get("content", "").encode()),
                            "lines": file.get("numLines"),
                        }
                    if call.get("mutation_attempt") and not block.get("is_error"):
                        changes.append(line)
                        call["files_changed_afterward"] = True
                verify(call, content, line)
        if kind in {"item.started", "item.completed"}:
            item = event.get("item", {})
            if item.get("type") == "command_execution":
                call = new_call(item["id"], line, "command_execution", {"command": item["command"]})
                if kind == "item.completed":
                    output = item.get("aggregated_output", "")
                    # Codex merges stdout/stderr: do not invent their split.
                    call.update(
                        exit_code=item.get("exit_code"),
                        status=item.get("status", "unknown"),
                        combined_output_bytes=len(output.encode()),
                        result=output,
                        duration_seconds=item.get("duration_seconds"),
                    )
                    denied = item.get("status") == "denied"
                    call.update(
                        denied=denied,
                        executed=False
                        if denied
                        else True
                        if item.get("exit_code") is not None
                        else None,
                        denial_reason=item.get("denial_reason"),
                    )
                    verify(call, output, line)
            if item.get("type") == "file_change" and kind == "item.completed":
                call = new_call(item["id"], line, "file_change", item.get("changes", []))
                call.update(
                    status=item.get("status"),
                    executed=item.get("status") == "completed",
                    files_changed_afterward=True if item.get("status") == "completed" else None,
                )
                if item.get("status") == "completed":
                    changes.append(line)
            if item.get("type") in {"mcp_tool_call", "dynamic_tool_call", "web_search"}:
                call = new_call(item["id"], line, item["type"], item, event.get("timestamp"))
                if kind == "item.completed":
                    call.update(status=item.get("status", "unknown"), result=item)
    final = results[-1] if results else None
    raw_usage = (
        final.get("usage") if final else completions[-1].get("usage") if completions else None
    )
    usage = normalize_usage(raw_usage, provider == "claude")
    reported_model = init.get("model")
    model_usage = final.get("modelUsage", {}) if final else {}
    auxiliary = (
        {k: v for k, v in model_usage.items() if k != reported_model} if reported_model else {}
    )
    primary = model_usage.get(reported_model) if reported_model else None
    if provider == "claude":
        success = bool(
            final and final.get("subtype") == "success" and not final.get("is_error") and usage
        )
        error = (
            json.dumps(final.get("errors") or final.get("result", ""))
            if final and not success
            else None
        )
        response = final.get("result", "") if final else ""
    else:
        success = bool(completions and not failures and usage)
        error = json.dumps(failures) if failures else None
        messages = [
            e["item"].get("text", "")
            for _, e in events
            if e.get("type") == "item.completed"
            and e.get("item", {}).get("type") == "agent_message"
        ]
        response = messages[-1] if messages else ""
    return {
        "success": success,
        "usage": usage,
        "raw_usage": raw_usage,
        "error": error,
        "final_response": response,
        "commands": sum(c["tool"] in {"Bash", "command_execution"} for c in calls),
        "event_count": len(events),
        "parse_error_lines": errors,
        "calls": calls,
        "verification": verifications,
        "usage_records": usage_records,
        "usage_scope": "primary-model result aggregate"
        if provider == "claude"
        else "top-level turn aggregate; internal request usage unavailable",
        "primary_model_usage": primary,
        "auxiliary_model_usage": auxiliary,
        "unclassified_model_usage": model_usage if not reported_model else {},
        "auxiliary_scope": "exposed modelUsage; role and chronology unavailable"
        if auxiliary
        else "unavailable",
        "reported_model": reported_model,
        "reported_permission_mode": init.get("permissionMode"),
        "session_identifiers": sorted(session_ids),
        "request_identifiers": sorted(requests),
        "reported_turn_count": final.get("num_turns") if final else len(completions),
        "assistant_message_count": len(message_ids) if message_ids else None,
        "output_byte_totals": {
            k: sum(c[k] for c in calls if c.get(k) is not None)
            if any(c.get(k) is not None for c in calls)
            else None
            for k in [
                "stdout_bytes",
                "stderr_bytes",
                "combined_output_bytes",
                "returned_content_bytes",
            ]
        },
        "output_byte_scope": "original exposed UTF-8 strings before sanitization; merged outputs are not counted again as stdout/stderr",
        "cache_state": "uncontrolled",
        "provider_result": final,
    }
