"""Session-local runtime controls and an offline effective command-environment probe."""

import json
from pathlib import Path
import shlex
import subprocess


def configure(session, source_env):
    root, temporary = session.root, session.tmp
    bindir = root / "cache/bin"
    startup = root / "cache/shell"
    bindir.mkdir()
    startup.mkdir()
    directories = {
        "HOME": temporary / "home",
        "XDG_CACHE_HOME": temporary / "cache",
        "XDG_CONFIG_HOME": temporary / "config",
        "PYTHONPYCACHEPREFIX": temporary / "pycache",
        "PYTHONUSERBASE": temporary / "python-user",
    }
    for path in directories.values():
        path.mkdir()
    config = root / "cache/gitconfig"
    config.write_text("# No inherited Git configuration.\n")
    session.env = dict(
        source_env,
        **{name: str(path) for name, path in directories.items()},
        PATH=f"{bindir}:/usr/bin:/bin:/usr/sbin:/sbin",
        SHELL=session.runtime["binaries"]["shell"]["path"],
        TMPDIR=str(temporary),
        TMP=str(temporary),
        TEMP=str(temporary),
        CODEX_HOME=str(session.profile),
        CLAUDE_CONFIG_DIR=str(session.profile),
        ZDOTDIR=str(startup),
        ENV=str(startup / "environment"),
        BASH_ENV=str(startup / "environment"),
        GIT_CONFIG_GLOBAL=str(config),
        GIT_EXEC_PATH=session.runtime["binaries"]["git"]["exec_path"],
        PYTHONNOUSERSITE="1",
    )
    # No credential values enter startup files or the provider's tool policy.
    session.tool_env = {k: v for k, v in session.env.items() if k not in session.auth_names}
    exports = "".join(f"export {k}={shlex.quote(v)}\n" for k, v in session.tool_env.items())
    (startup / "environment").write_text(exports)
    # /etc/zshenv is always read by zsh. Disable subsequent global startup
    # files before /etc/zprofile can run path_helper; no host files are edited.
    (startup / ".zshenv").write_text("unsetopt GLOBAL_RCS\n" + exports)
    # bash/sh login shells read the isolated HOME, following /etc/profile.
    for name in [".bash_profile", ".profile"]:
        (directories["HOME"] / name).write_text(exports)
    for name, record in session.runtime["binaries"].items():
        target = bindir / name
        target.write_text(f'#!/bin/sh\nexec {shlex.quote(record["path"])} "$@"\n')
        target.chmod(0o755)
    (bindir / "python").write_text(
        f'#!/bin/sh\nexec {shlex.quote(session.runtime["binaries"]["python3"]["path"])} "$@"\n'
    )
    (bindir / "python").chmod(0o755)


def shell_command(session, script):
    return [session.runtime["binaries"]["shell"]["path"], "-lc", script]


def probe(session, boundary):
    """Run command-v in a login shell through the real provider command boundary.

    This is the exposed offline native-command mechanism, not a model/tool turn.
    The same environment policy and permission profile are supplied to exec.
    """
    script = (
        "environment_names = "
        + repr(list(session.tool_env))
        + r"""
import json, os, pathlib, subprocess, sys
observed = {"binaries": {}, "environment": {k: os.environ.get(k) for k in environment_names},
            "shell": {"identity": sys.argv[1], "version": sys.argv[2]}}
for name, path in zip(["python3", "git", "rg"], sys.argv[3:]):
    result = subprocess.run([name, "--version"], capture_output=True, text=True)
    observed["binaries"][name] = {"path": path, "version": result.stdout.strip(),
        "exit_code": result.returncode, "stderr": result.stderr}
observed["python_executable"] = sys.executable
result = subprocess.run(["git", "config", "--show-origin", "--list"],
                        capture_output=True, text=True)
observed["git_config"] = {"stdout": result.stdout, "stderr": result.stderr,
                          "exit_code": result.returncode}
observed["cache_writes"] = {}
for name in ["HOME", "TMPDIR", "XDG_CACHE_HOME", "XDG_CONFIG_HOME",
             "PYTHONPYCACHEPREFIX", "PYTHONUSERBASE"]:
    path = pathlib.Path(os.environ[name]) / "runtime-cache-probe"
    path.write_text("session-local")
    path.unlink()
    observed["cache_writes"][name] = True
print(json.dumps(observed))
"""
    )
    command = shell_command(
        session,
        "python3 -c "
        + shlex.quote(script)
        + ' "$0" "${ZSH_VERSION:-${BASH_VERSION:-}}"'
        + ' "$(command -v python3)" "$(command -v git)" "$(command -v rg)"',
    )
    actual = boundary(command)
    result = subprocess.run(
        actual, cwd=session.repo, env=session.env, capture_output=True, text=True, timeout=30
    )
    observed = None
    errors = []
    if result.returncode or result.stderr:
        errors.append("native runtime probe failed or emitted diagnostics")
    else:
        try:
            observed = json.loads(result.stdout)
            for name in ["python3", "git", "rg"]:
                expected = session.runtime["binaries"][name]
                binary = observed["binaries"][name]
                if binary != {
                    "path": str(session.root / "cache/bin" / name),
                    "version": expected["version"],
                    "exit_code": 0,
                    "stderr": "",
                }:
                    errors.append(f"effective {name} mismatch")
            if Path(observed["python_executable"]).resolve() != Path(
                session.runtime["binaries"]["python3"]["path"]
            ):
                errors.append("effective Python executable mismatch")
            if any(observed["environment"].get(k) != v for k, v in session.tool_env.items()):
                errors.append("effective environment mismatch")
            if observed["shell"]["identity"] != session.runtime["binaries"]["shell"]["path"]:
                errors.append("effective shell mismatch")
            if observed["git_config"]["exit_code"] or observed["git_config"]["stderr"]:
                errors.append("effective Git configuration probe failed")
            if observed["git_config"]["stdout"].strip() != getattr(
                session, "git_config_expected", None
            ):
                errors.append("effective Git configuration mismatch")
        except (ValueError, KeyError, TypeError):
            errors.append("invalid effective runtime output")
    # Retain controlled values only: do not publish CLI-added credentials/env.
    if observed:
        observed["environment"] = {k: observed["environment"].get(k) for k in session.tool_env}
    return {
        "passed": not errors,
        "requested": session.runtime,
        "effective": observed,
        "invocation": actual,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "errors": errors,
        "scope": "offline CLI-native login-shell command path; no model request",
    }
