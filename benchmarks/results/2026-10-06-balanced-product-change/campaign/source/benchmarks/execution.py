"""Provider execution strategies and offline native-command compatibility gates.

This module never invokes a model. Codex probes use its local `sandbox` command.
Claude has no exposed equivalent in the supported CLI: retain a primitive-only
diagnostic and fail closed rather than claiming its native path was verified.
"""

import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile


class ExecutionError(ValueError):
    pass


def strategy(provider):
    if provider in {"codex", "claude"}:
        return {
            "execution_strategy": "provider-native",
            "provider_native_sandbox": True,
            "outer_os_sandbox": False,
        }
    if provider == "external":
        return {
            "execution_strategy": "harness-outer",
            "provider_native_sandbox": False,
            "outer_os_sandbox": True,
        }
    raise ExecutionError("unsupported provider execution strategy")


def validate_strategy(policy):
    if policy.get("provider_native_sandbox") and policy.get("outer_os_sandbox"):
        raise ExecutionError("nested provider-native/outer OS sandbox composition is unsupported")
    if policy.get("execution_strategy") != strategy(policy["provider"])["execution_strategy"]:
        raise ExecutionError("execution strategy does not match provider capabilities")
    if {k: policy.get(k) for k in strategy(policy["provider"])} != strategy(policy["provider"]):
        raise ExecutionError("required sandbox was disabled or unsupported composition selected")


def toml(value):
    if isinstance(value, dict):
        return "{" + ",".join(json.dumps(k) + "=" + toml(v) for k, v in value.items()) + "}"
    if isinstance(value, (str, bool, int, list)):
        return json.dumps(value, ensure_ascii=False)
    raise ExecutionError("unsupported permission configuration value")


def codex_options(session, policy):
    """One named profile for exec and sandbox; never mix legacy --sandbox flags."""
    filesystem = {":root": "deny", ":minimal": "read"}
    # Provider driver stays outside the command sandbox. Its fresh profile can
    # be read by child shells, but commands cannot write to the control areas.
    roots = {
        Path(sys.base_prefix).resolve(),
        session.profile,
        session.root / "cache/bin",
        session.root / "cache/shell",
        session.root / "cache/gitconfig",
    }
    roots.update(Path(v["path"]).parent for v in session.runtime["binaries"].values())
    roots.add(Path(session.runtime["binaries"]["git"]["exec_path"]))
    # Homebrew's dynamic libraries live outside individual executable prefixes.
    if platform.system() == "Darwin" and Path("<package-manager>").is_dir():
        roots.add(Path("<package-manager>"))
    filesystem.update({str(p): "read" for p in sorted(roots)})
    filesystem[str(session.output)] = "deny"
    filesystem[str(session.repo)] = "read" if policy["sandbox"] == "read-only" else "write"
    filesystem[str(session.repo / ".git")] = "read"
    filesystem[str(session.tmp)] = "write"
    # Root-deny already protects all evidence, earlier sessions, shared temp,
    # and unrelated host state. No profile inheritance of shared tmp writes.
    profile = {
        "filesystem": filesystem,
        "network": {"enabled": False},
    }
    return [
        "--config",
        'default_permissions="contextlean-session"',
        "--config",
        "permissions.contextlean-session=" + toml(profile),
        "--config",
        'approval_policy="never"',
        "--config",
        'web_search="disabled"',
        "--config",
        "shell_environment_policy="
        + toml(
            {
                "inherit": "none",
                "set": session.tool_env,
                "experimental_use_profile": False,
            }
        ),
    ]


def native_command(session, policy, command):
    validate_strategy(policy)
    if policy["provider"] != "codex":
        raise ExecutionError("provider has no exposed offline native-command sandbox probe")
    return [
        session.runtime["binaries"]["cli"]["path"],
        "sandbox",
        "--permission-profile",
        "contextlean-session",
        "--include-managed-config",
        "--cd",
        str(session.repo),
        *codex_options(session, policy),
        "--",
        *command,
    ]


def model_command(policy, command):
    validate_strategy(policy)
    if policy["provider"] == "claude":
        raise ExecutionError("Claude native CLI probe unavailable; model execution remains blocked")
    if (
        not policy.get("native_preflight")
        or not policy.get("permission_probe", {}).get("passed")
        or not policy.get("effective_runtime", {}).get("passed")
        or (
            policy["provider_native_sandbox"] and policy.get("native_sandbox_available") is not True
        )
    ):
        raise ExecutionError("successful provider compatibility preflight required")
    return command


def permission_probe(session, policy, output, outer_command):
    """Probe the actual CLI path, not a Python process under a substitute wrapper."""
    validate_strategy(policy)
    policy.update(
        native_sandbox_available=None,
        probe_scope="provider CLI native-command path",
        permission_probe={"passed": False, "exit_code": None},
    )
    with tempfile.TemporaryDirectory(prefix="contextlean-forbidden-probe-") as temporary:
        marker = output / "permission-read-probe"
        marker.write_text("private benchmark evidence")
        targets = [
            session.repo / ".permission-probe",
            session.tmp / "probe",
            session.root / "parent-probe",
            Path(temporary) / "outside",
        ]
        outside_marker = Path(temporary) / "other-session-scratch"
        outside_marker.write_text("unrelated scratch must not be readable")
        script = (
            "import pathlib,sys,json; r=[]\n"
            "for s in sys.argv[1:-2]:\n"
            " try:\n  p=pathlib.Path(s);p.write_text('probe');p.unlink();r.append(True)\n"
            " except PermissionError:r.append(False)\n"
            "for s in sys.argv[-2:]:\n"
            " try:\n  pathlib.Path(s).read_bytes();r.append(True)\n"
            " except (PermissionError,FileNotFoundError):r.append(False)\n"
            "print(json.dumps(r))\n"
        )
        command = [
            session.runtime["binaries"]["python3"]["path"],
            "-c",
            script,
            *map(str, targets),
            str(marker),
            str(outside_marker),
        ]
        try:
            if policy["provider"] == "claude":
                # This tests the documented OS primitive only. It cannot stand
                # in for Claude's native Bash configuration or built-in tools.
                policy["probe_scope"] = (
                    "OS primitive only; actual Claude native tool path unverified"
                )
                diagnostic = dict(policy, backend=policy["primitive_backend"])
                actual = outer_command(session, diagnostic, command, output)
            elif policy["provider_native_sandbox"]:
                actual = native_command(session, policy, command)
            else:
                actual = outer_command(session, policy, command, output)
            result = subprocess.run(
                actual,
                cwd=session.repo,
                env=session.env,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            expected = [policy["sandbox"] != "read-only", True, False, False, False, False]
            observed = json.loads(result.stdout) if result.returncode == 0 else None
            passed = result.returncode == 0 and observed == expected
            policy["permission_probe"] = {
                "passed": passed and policy["provider"] != "claude",
                "primitive_passed": passed if policy["provider"] == "claude" else None,
                "invocation": actual,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "operations": dict(
                    zip(
                        [
                            "repo_write",
                            "tmp_write",
                            "parent_write",
                            "outside_write",
                            "evidence_read",
                            "outside_read",
                        ],
                        observed,
                    )
                )
                if observed
                else None,
                "operation_exit_codes": {
                    name: None
                    for name in [
                        "repo_write",
                        "tmp_write",
                        "parent_write",
                        "outside_write",
                        "evidence_read",
                        "outside_read",
                    ]
                },
                "operation_result_scope": "each operation reports allowed/denied; exit code belongs to the enclosing CLI probe",
            }
            if policy["provider"] == "claude":
                raise ExecutionError(
                    "Claude has no offline native-command CLI probe; primitive-only diagnostic cannot authorize execution"
                )
            policy["native_sandbox_available"] = (
                result.returncode == 0 if policy["provider_native_sandbox"] else False
            )
            if not passed:
                raise ExecutionError(
                    "provider sandbox compatibility preflight failed: " + result.stderr
                )
            policy["native_preflight"] = policy["permission_probe"]["operations"]
        finally:
            marker.unlink()
    return policy
