"""Versioned, dependency-free graded benchmark isolation and evidence controls.

No import-time execution. CLI version probes and sandbox probes are offline; only
execute_session starts a model. Historical and packaged measurement code stays
independent of this development harness.
"""

from contextlib import contextmanager
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time


VERSION = 3
EXECUTION_SPEC = importlib.util.spec_from_file_location(
    "benchmark_execution", Path(__file__).with_name("execution.py")
)
execution = importlib.util.module_from_spec(EXECUTION_SPEC)
EXECUTION_SPEC.loader.exec_module(execution)
GUIDANCE = frozenset({"AGENTS.md", "CLAUDE.md", "PROJECT_REFERENCE.md"})
GIT_SETTINGS = {
    "user.name": "Benchmark fixture",
    "user.email": "fixture@example.invalid",
    "commit.gpgsign": "false",
    "core.autocrlf": "false",
    "core.filemode": "false",
    "core.ignorecase": "false",
    "core.precomposeunicode": "false",
    "core.logallrefupdates": "false",
    "core.hooksPath": "/dev/null",
}
AUTH_NAMES = {
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "CLAUDE_CODE_OAUTH_TOKEN",
}
PUBLIC_ENV = {"LANG", "LC_ALL", "TZ", "TERM", "PYTHONDONTWRITEBYTECODE"}


class HarnessError(ValueError):
    pass


def digest(value):
    return hashlib.sha256(value).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def inventory(root):
    """Include every fixture file, not just extensions understood by the task."""
    records = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise HarnessError("symlink in fixture or session evidence")
        if path.is_file() and ".git" not in path.relative_to(root).parts:
            data = path.read_bytes()
            records[path.relative_to(root).as_posix()] = {
                "sha256": digest(data),
                "size": len(data),
            }
    return records


def local_path(root, name):
    path = Path(name)
    if path.is_absolute() or ".." in path.parts or not name or name == ".":
        raise HarnessError("path must stay inside its root")
    target = root / path
    if any(p.is_symlink() for p in [target, *target.parents] if p != root.parent):
        # The session root is resolved; no link may redirect an approved path.
        raise HarnessError("symlink in approved path")
    if not target.resolve().is_relative_to(root.resolve()):
        raise HarnessError("path escaped its root")
    return target


def fixture_manifest(vanilla, contextlean, vanilla_prompt, contextlean_prompt):
    if vanilla_prompt != contextlean_prompt:
        raise HarnessError("task prompt bytes differ")
    v, c = inventory(vanilla), inventory(contextlean)
    rows = []
    for name in sorted(set(v) | set(c)):
        different = v.get(name) != c.get(name)
        if different and name not in GUIDANCE:
            raise HarnessError(f"undeclared fixture difference: {name}")
        if name in GUIDANCE and (name in v or name not in c):
            raise HarnessError("Vanilla must omit all declared guidance files")
        rows.append(
            {
                "path": name,
                "vanilla": v.get(name),
                "contextlean": c.get(name),
                "condition_specific": name in GUIDANCE,
                "status": "contextlean-guidance" if name in GUIDANCE else "identical",
            }
        )
    return {
        "benchmark_harness_version": VERSION,
        "files": rows,
        "prompt_sha256": digest(vanilla_prompt),
        "prompt_size": len(vanilla_prompt),
    }


def make_conditions(canonical, destination, copier):
    original = inventory(canonical)  # Fail on links, including ignored/generated input.
    for condition in ["vanilla", "contextlean"]:
        copier(canonical, destination / condition)
        compare_receipts(original, inventory(destination / condition), "canonical copy")
    for name in GUIDANCE:
        path = destination / "vanilla" / name
        if path.exists():
            path.unlink()
    return destination / "vanilla", destination / "contextlean"


def copy_fixture(source, destination):
    """Omit only Git metadata; don't silently drop runtime or ignored files."""
    original = inventory(source)
    shutil.copytree(source, destination, ignore=lambda directory, names: {".git"} & set(names))
    compare_receipts(original, inventory(destination), "fixture copy")


def schedule(tasks, repeats):
    return [
        {"sequence": index + 1, "task": task, "repeat": repetition + 1, "condition": condition}
        for index, (task, repetition, condition) in enumerate(
            (task, repetition, condition)
            for task_index, task in enumerate(tasks)
            for repetition in range(repeats)
            for condition in (
                ["vanilla", "contextlean"]
                if (task_index + repetition) % 2 == 0
                else ["contextlean", "vanilla"]
            )
        )
    ]


def pin_runtime(cli, shell=None):
    """Resolve once, record versions/content hashes; children use pinned aliases."""
    binaries = {
        "python3": sys.executable,
        "git": "git",
        "rg": "rg",
        "cli": cli,
        "shell": shell or os.environ.get("SHELL", "/bin/sh"),
    }
    resolved = {}
    for name, executable in binaries.items():
        path = shutil.which(executable)
        if not path:
            raise HarnessError(f"required runtime unavailable: {name}")
        path = Path(path).resolve()
        result = subprocess.run(
            [str(path), "--version"], capture_output=True, text=True, timeout=15, check=False
        )
        version = (result.stdout or result.stderr).strip() if result.returncode == 0 else None
        if name != "shell" and not version:
            raise HarnessError(f"runtime version unavailable: {name}")
        resolved[name] = {
            "path": str(path),
            "version": version,
            "sha256": digest(path.read_bytes()),
        }
    return {
        "os": platform.system(),
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "binaries": resolved,
        "dependency_environment": "standard-library-only; dependencies are not installed",
    }


def validate_runtime(runtime):
    for entry in runtime["binaries"].values():
        path = Path(entry["path"])
        if not path.is_file() or digest(path.read_bytes()) != entry["sha256"]:
            raise HarnessError("pinned runtime changed")


def environment_source(provider, inherited=None):
    source = dict(os.environ if inherited is None else inherited)
    env = {k: source[k] for k in PUBLIC_ENV if k in source}
    env.update(
        LANG=env.get("LANG", "C.UTF-8"),
        TZ="UTC",
        TERM="dumb",
        PYTHONDONTWRITEBYTECODE="1",
        GIT_CONFIG_NOSYSTEM="1",
        GIT_CONFIG_GLOBAL=os.devnull,
        GIT_ATTR_NOSYSTEM="1",
        GIT_AUTHOR_NAME="Benchmark fixture",
        GIT_COMMITTER_NAME="Benchmark fixture",
        GIT_AUTHOR_EMAIL="fixture@example.invalid",
        GIT_COMMITTER_EMAIL="fixture@example.invalid",
        GIT_AUTHOR_DATE="2000-01-01T00:00:00Z",
        GIT_COMMITTER_DATE="2000-01-01T00:00:00Z",
    )
    names = (
        {"OPENAI_API_KEY"}
        if provider == "codex"
        else {"ANTHROPIC_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN"}
    )
    env.update({k: source[k] for k in names if source.get(k)})
    # Nothing else is inherited: proxy/provider overrides, Python paths, Git
    # paths, injected shell startup and user configuration cannot leak in.
    return env


def environment_receipt(env, normalize):
    receipt = {
        k: ({"present": bool(v)} if k in AUTH_NAMES else {"present": True, "value": normalize(v)})
        for k, v in sorted(env.items())
    }
    for name in AUTH_NAMES:
        receipt.setdefault(name, {"present": False})
    return receipt


def compare_receipts(left, right, label):
    if left != right:
        raise HarnessError(f"{label} receipts differ")


class Sanitizer:
    """Sanitize public data recursively; never sanitize the private raw trace."""

    def __init__(self, root=None, replacements=None, secrets=()):
        self.replacements = dict(replacements or {})
        if root:
            self.replacements[str(root)] = "<session-root>"
        self.replacements[str(Path.home())] = "<home>"
        self.secrets = sorted({s for s in secrets if s}, key=len, reverse=True)

    def text(self, text):
        for secret in self.secrets:
            text = text.replace(secret, "<redacted>")
        for source, placeholder in sorted(
            self.replacements.items(), key=lambda item: len(item[0]), reverse=True
        ):
            text = text.replace(source, placeholder)
        text = re.sub(
            r"(?:/Users/|/home/|/private/tmp/|/tmp/|/private/var/folders/|/var/folders/)[^\s\"'<>]*",
            "<host-path>",
            text,
        )
        text = re.sub(r"\b(?:sk-[A-Za-z0-9_-]+|Bearer\s+[^\s\"']+)", "<redacted>", text)
        text = re.sub(r"(?i)(?:[A-Z]:\\Users\\)[^\s\"<>]+", "<host-path>", text)
        return text

    def value(self, value, key=""):
        if re.search(
            r"(?i)(?:api.?key|auth.?token|access.?token|refresh.?token|credential|account.?id|user.?id|org(?:anization)?.?id|tenant.?id|subscription.?id|email)",
            key,
        ):
            # Preserve presence-only receipts, never values or account IDs.
            return (
                {"present": value.get("present", True)} if isinstance(value, dict) else "<redacted>"
            )
        if isinstance(value, dict):
            return {self.text(k): self.value(v, k) for k, v in value.items()}
        if isinstance(value, list):
            return [self.value(v) for v in value]
        return self.text(value) if isinstance(value, str) else value


class Session:
    def __init__(self, root, runtime, source_env, output):
        self.root, self.runtime, self.output = root, runtime, output.resolve()
        for name in ["repo", "tmp", "cache", "artifacts", "receipts"]:
            (root / name).mkdir()
        self.repo = root / "repo"
        self.tmp = root / "tmp"
        self.profile = root / "cache/profile"
        self.profile.mkdir()
        bindir = root / "cache/bin"
        bindir.mkdir()
        for name, record in runtime["binaries"].items():
            (bindir / name).symlink_to(record["path"])
        (bindir / "python").symlink_to(runtime["binaries"]["python3"]["path"])
        self.env = dict(
            source_env,
            HOME=str(self.profile),
            PATH=f"{bindir}:/usr/bin:/bin:/usr/sbin:/sbin",
            SHELL=runtime["binaries"]["shell"]["path"],
            TMPDIR=str(self.tmp),
            TMP=str(self.tmp),
            TEMP=str(self.tmp),
            XDG_CACHE_HOME=str(root / "cache"),
            CODEX_HOME=str(self.profile),
            CLAUDE_CONFIG_DIR=str(self.profile),
            ZDOTDIR=str(self.profile),
            ENV="",
            BASH_ENV="",
            PYTHONNOUSERSITE="1",
        )
        self.sanitizer = Sanitizer(
            root, {str(output): "<evidence>"}, [self.env[k] for k in AUTH_NAMES if k in self.env]
        )
        self.cleanup_verified = False

    def auth(self, provider):
        # Auth-only profile: no user settings, memories, plugins or history.
        source = Path.home() / (
            ".codex/auth.json" if provider == "codex" else ".claude/.credentials.json"
        )
        if not any(self.env.get(k) for k in AUTH_NAMES) and source.is_file():
            target = self.profile / source.name
            shutil.copyfile(source, target)
            target.chmod(0o600)

            def auth_strings(value):
                if isinstance(value, dict):
                    return [s for item in value.values() for s in auth_strings(item)]
                if isinstance(value, list):
                    return [s for item in value for s in auth_strings(item)]
                return [value] if isinstance(value, str) and len(value) > 6 else []

            self.sanitizer.secrets.extend(auth_strings(json.loads(source.read_text())))
        return {
            "source": "environment"
            if any(self.env.get(k) for k in AUTH_NAMES)
            else "auth-only-profile",
            "present": any(self.env.get(k) for k in AUTH_NAMES) or any(self.profile.iterdir()),
        }


@contextmanager
def session_root(runtime, env, output):
    root = Path(tempfile.mkdtemp(prefix=f"contextlean-session-v{VERSION}-")).resolve()
    session = None
    try:
        session = Session(root, runtime, env, output)
        yield session
    finally:
        shutil.rmtree(root)  # No ignore_errors: cleanup failure stops the campaign.
        if root.exists():
            raise HarnessError("session root cleanup failed")
        if session:
            session.cleanup_verified = True


def git(session, *args):
    command = [session.runtime["binaries"]["git"]["path"], *args]
    result = subprocess.run(
        command,
        cwd=session.repo,
        env=session.env,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if result.returncode:
        raise HarnessError("Git normalization failed: " + result.stderr)
    return result.stdout.strip()


def initialize_git(session):
    if (session.repo / ".git").exists():
        raise HarnessError("inherited repository metadata")
    template = session.root / "receipts/empty-git-template"
    template.mkdir()
    git(session, "init", "--initial-branch=main", f"--template={template}")
    for key, value in GIT_SETTINGS.items():
        git(session, "config", "--local", key, value)
    git(session, "add", "--force", ".")
    git(session, "commit", "-m", "Untouched benchmark task baseline")
    receipt = git_state(session)
    # A unique disposable file probes ordinary diff semantics, then is removed.
    tracked = git(session, "ls-files").splitlines()[0]
    target = session.repo / tracked
    original = target.read_bytes()
    try:
        target.write_bytes(original + b"\nbenchmark offline diff probe\n")
        if "diff --git " not in git(session, "diff", "--", tracked):
            raise HarnessError("normal Git diff failed")
    finally:
        target.write_bytes(original)
    if git_state(session) != receipt:
        raise HarnessError("Git probe changed baseline")
    return receipt


def git_state(session):
    status = git(session, "status", "--porcelain")
    return {
        "version": session.runtime["binaries"]["git"]["version"],
        "baseline_commit": git(session, "rev-parse", "HEAD"),
        "tree": git(session, "rev-parse", "HEAD^{tree}"),
        "clean": not status,
        "status": status,
        "branch": git(session, "branch", "--show-current"),
        "config": git(session, "config", "--local", "--list"),
        "remotes": git(session, "remote"),
        "hooks": list((session.repo / ".git/hooks").glob("*"))
        if (session.repo / ".git/hooks").exists()
        else [],
    }


def permission_policy(session, provider, sandbox):
    if sandbox not in {"workspace-write", "read-only"}:
        raise HarnessError("unsupported task permission mode")
    selected = execution.strategy(provider)
    primitive = None
    if platform.system() == "Darwin" and Path("/usr/bin/sandbox-exec").is_file():
        primitive = "sandbox-exec"
    elif platform.system() == "Linux" and shutil.which("bwrap"):
        primitive = "bwrap"
    if not primitive and (selected["outer_os_sandbox"] or provider == "claude"):
        raise HarnessError("no supported native filesystem boundary available")
    policy = {
        **selected,
        "benchmark_harness_version": VERSION,
        "platform": platform.platform(),
        "os": platform.system(),
        "backend": provider + "-native" if selected["provider_native_sandbox"] else primitive,
        "primitive_backend": primitive,
        "provider": provider,
        "cli_version": session.runtime["binaries"]["cli"]["version"],
        "sandbox": sandbox,
        "permission_mode": "acceptEdits" if provider == "claude" else "approval-never",
        "effective_writable_roots": ["<session-root>/repo", "<session-root>/tmp"]
        if sandbox != "read-only"
        else ["<session-root>/tmp"],
        "cli_control_writable": [
            "<session-root>/cache",
            "<session-root>/artifacts",
            "<session-root>/receipts",
        ],
        "cwd_policy": "isolated session repository",
        "environment_policy": "allowlisted environment; session-local home/temp/cache; pinned PATH",
        "evidence_readable": False,
        "shared_tmp_writable": False,
        "native_preflight": None,
        "task_control_writable": selected["outer_os_sandbox"],
    }
    if selected["outer_os_sandbox"]:
        policy["effective_writable_roots"] += policy["cli_control_writable"]
    return policy


def outer_command(session, policy, command, output):
    output = output.resolve()
    if policy["backend"] == "sandbox-exec":
        roots = [
            session.tmp,
            session.root / "cache",
            session.root / "artifacts",
            session.root / "receipts",
        ]
        if policy["sandbox"] != "read-only":
            roots.append(session.repo)
        profile = session.root / "receipts/filesystem.sb"
        rules = [
            "(version 1)",
            "(allow default)",
            "(deny file-write*)",
            '(allow file-write* (literal "/dev/null"))',
            f"(deny file-read* (subpath {json.dumps(str(output))}))",
        ]
        rules += [f"(allow file-write* (subpath {json.dumps(str(p))}))" for p in roots]
        scratch_parents = {
            Path("/tmp"),
            Path("/private/tmp"),
            Path(tempfile.gettempdir()).resolve(),
        }
        rules += [
            f"(deny file-read* (subpath {json.dumps(str(p))}))" for p in sorted(scratch_parents)
        ]
        rules += [f"(allow file-read* (subpath {json.dumps(str(session.root))}))"]
        rules += [
            f"(allow file-read-metadata (literal {json.dumps(str(p))}))"
            for p in session.root.parents
        ]

        profile.write_text("\n".join(rules) + "\n")
        return ["/usr/bin/sandbox-exec", "-f", str(profile), *command]
    empty = session.root / "receipts/hidden-evidence"
    empty.mkdir(exist_ok=True)
    arguments = [
        shutil.which("bwrap"),
        "--die-with-parent",
        "--unshare-user",
        "--unshare-pid",
        "--ro-bind",
        "/",
        "/",
        "--dev",
        "/dev",
        "--proc",
        "/proc",
    ]
    # Mask shared scratch before rebinding this session's own locations.
    for parent in sorted({Path("/tmp"), Path("/var/tmp"), Path(tempfile.gettempdir()).resolve()}):
        if parent.is_dir():
            arguments += ["--tmpfs", str(parent)]
    arguments += ["--ro-bind", str(session.repo), str(session.repo)]
    for name in ["tmp", "cache", "artifacts", "receipts"]:
        arguments += ["--bind", str(session.root / name), str(session.root / name)]
    if policy["sandbox"] != "read-only":
        arguments += ["--bind", str(session.repo), str(session.repo)]
    return [*arguments, "--ro-bind", str(empty), str(output), "--", *command]


def boundary_command(session, policy, command, output):
    """Offline task commands follow the same provider sandbox path as real tools."""
    try:
        execution.validate_strategy(policy)
        if policy["provider_native_sandbox"]:
            return execution.native_command(session, policy, command)
        return outer_command(session, policy, command, output)
    except execution.ExecutionError as error:
        raise HarnessError(str(error)) from error


def execution_command(session, policy, command, output):
    """Do not put a native-sandbox provider driver inside a second OS sandbox."""
    try:
        execution.model_command(policy, command)
        return (
            command
            if policy["provider_native_sandbox"]
            else outer_command(session, policy, command, output)
        )
    except execution.ExecutionError as error:
        raise HarnessError(str(error)) from error


def permission_preflight(session, policy, output):
    """Preserve successful and failed compatibility receipts before cleanup."""
    try:
        return execution.permission_probe(session, policy, output, outer_command)
    except (execution.ExecutionError, OSError, ValueError, subprocess.SubprocessError) as error:
        policy["preparation_failure"] = str(error)
        raise HarnessError(str(error)) from error
    finally:
        private = output / "private/preflight"
        private.mkdir(parents=True, exist_ok=True, mode=0o700)
        private.chmod(0o700)
        raw = private / (session.root.name + "-permission.json")
        write_json(raw, policy)
        raw.chmod(0o600)
        write_json(
            output / "preflight" / (session.root.name + "-permission.json"),
            session.sanitizer.value(policy),
        )


def invocation(session, provider, model, reasoning, sandbox, policy=None):
    policy = policy or permission_policy(session, provider, sandbox)
    cli = session.runtime["binaries"]["cli"]["path"]
    if provider == "codex":
        return [
            cli,
            "exec",
            "--json",
            "--ephemeral",
            "--ignore-user-config",
            "--ignore-rules",
            "--strict-config",
            "--model",
            model,
            "--config",
            f'model_reasoning_effort="{reasoning}"',
            *execution.codex_options(session, policy),
            "--cd",
            str(session.repo),
            "-",
        ]
    return [
        cli,
        "--print",
        "--verbose",
        "--output-format",
        "stream-json",
        "--no-session-persistence",
        "--model",
        model,
        "--effort",
        reasoning,
        "--setting-sources",
        "project,local",
        "--strict-mcp-config",
        "--mcp-config",
        '{"mcpServers":{}}',
        "--settings",
        json.dumps(
            {
                "sandbox": {
                    "enabled": True,
                    "failIfUnavailable": True,
                    "allowUnsandboxedCommands": False,
                }
            }
        ),
        "--permission-mode",
        "acceptEdits",
        "--add-dir",
        str(session.tmp),
        "--tools",
        "Bash,Read,Edit,Write,Glob,Grep",
        "--allowedTools",
        "Read",
        "Edit",
        "Write",
        "Glob",
        "Grep",
        *[
            f"Bash({name} *)"
            for name in [
                "python3",
                "python",
                "rg",
                "ls",
                "cat",
                "sed",
                "head",
                "tail",
                "wc",
                "find",
            ]
        ],
        "Bash(pwd*)",
        "Bash(git status*)",
        "Bash(git diff*)",
        "Bash(git log*)",
    ]


def execute_session(session, command, prompt, timeout, policy, output):
    if not policy.get("native_preflight"):
        raise HarnessError("permission preflight required before invocation")
    private = output / "private" / getattr(session, "evidence_name", session.root.name)
    private.mkdir(parents=True, exist_ok=True, mode=0o700)
    private.chmod(0o700)
    started = time.perf_counter()
    try:
        result = subprocess.run(
            execution_command(session, policy, command, output),
            input=prompt.encode("utf-8"),
            cwd=session.repo,
            env=session.env,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        stdout, stderr, exit_code, error = result.stdout, result.stderr, result.returncode, None
    except (subprocess.TimeoutExpired, OSError) as failure:
        stdout, stderr = (
            getattr(failure, "stdout", b"") or b"",
            getattr(failure, "stderr", b"") or b"",
        )
        exit_code, error = None, type(failure).__name__
    for name, content in [("events.jsonl", stdout), ("events.stderr.txt", stderr)]:
        path = private / name
        path.write_bytes(content)
        path.chmod(0o600)
    return {
        "stdout": stdout.decode("utf-8", errors="replace"),
        "stderr": stderr.decode("utf-8", errors="replace"),
        "stdout_bytes": len(stdout),
        "stderr_bytes": len(stderr),
        "exit_code": exit_code,
        "error": error,
        "duration_seconds": time.perf_counter() - started,
    }


def control_inventory(root):
    """Record control-area mutations without reading auth values or following links."""
    return {
        p.relative_to(root).as_posix(): {"kind": "symlink"}
        if p.is_symlink()
        else {"kind": "file", "size": p.stat().st_size}
        for p in sorted(root.rglob("*"))
        if p.is_symlink() or p.is_file()
    }


def sanitize_tree(root, sanitizer):
    """Text exports are sanitized; binary originals remain private, never published."""
    omitted = []
    for file in sorted(root.rglob("*")):
        if file.is_symlink():
            raise HarnessError("symlink in public evidence")
        if file.is_file():
            try:
                content = file.read_bytes().decode("utf-8")
            except UnicodeDecodeError:
                omitted.append(file.relative_to(root).as_posix())
                file.unlink()
            else:
                file.write_text(sanitizer.text(content), encoding="utf-8")
    return omitted


def failure_category(result, evaluation=None):
    error = str(result.get("error") or "") + str(result.get("stderr") or "")
    if result.get("harness_error"):
        return "harness-preparation-failure"
    if re.search(r"usage.limit|quota|rate.limit|limit.reached", error, re.I):
        return "provider-usage-limit-interruption"
    if not result.get("success") or not result.get("usage"):
        return "provider-network-failure"
    if evaluation and not evaluation.get("task_success"):
        return "model-task-failure"
    return None


def distribution(values):
    return (
        {
            "observations": values,
            "count": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
            "range": max(values) - min(values),
            "sample_standard_deviation": statistics.stdev(values) if len(values) > 1 else None,
        }
        if values
        else None
    )


def paired_metrics(runs, tasks, repeats):
    output = []
    for task in tasks:
        record = {"task": task, "pairs": [], "differences": {}}
        for repetition in range(1, repeats + 1):
            pair = {
                r["condition"]: r for r in runs if r["task"] == task and r["repeat"] == repetition
            }
            complete = set(pair) == {"vanilla", "contextlean"} and all(
                r.get("measurement_complete", True) for r in pair.values()
            )
            differences = {}
            for metric in [
                "input_tokens",
                "cached_input_tokens",
                "uncached_input_tokens",
                "output_tokens",
                "total_tokens",
                "duration_seconds",
                "command_calls",
            ]:
                values = (
                    [pair[c]["metrics"].get(metric) for c in ["vanilla", "contextlean"]]
                    if complete
                    else [None, None]
                )
                differences[metric] = (
                    values[1] - values[0] if all(v is not None for v in values) else None
                )
            record["pairs"].append(
                {"repeat": repetition, "complete": complete, "differences": differences}
            )
        for metric in record["pairs"][0]["differences"]:
            values = [p["differences"][metric] for p in record["pairs"]]
            record["differences"][metric] = (
                distribution(values) if all(v is not None for v in values) else None
            )
        output.append(record)
    return output
