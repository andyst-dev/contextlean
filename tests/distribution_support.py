"""Native installation probes: no model requests, credentials or external writes."""

import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import threading


PLUGIN = "contextlean@contextlean-local"


class IsolatedPlatform:
    def __init__(self, root):
        self.root = Path(root).resolve()
        for name in ("home", "codex", "claude", "tmp", "project"):
            (self.root / name).mkdir()
        self.project = self.root / "project"
        # Allowlist environment: never inherit authentication, provider or agent config.
        self.env = {
            "PATH": os.defpath,
            "HOME": str(self.root / "home"),
            "CODEX_HOME": str(self.root / "codex"),
            "CLAUDE_CONFIG_DIR": str(self.root / "claude"),
            "TMPDIR": str(self.root / "tmp"),
            "XDG_CONFIG_HOME": str(self.root / "home/config"),
            "XDG_CACHE_HOME": str(self.root / "home/cache"),
            "XDG_DATA_HOME": str(self.root / "home/data"),
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
            "DISABLE_AUTOUPDATER": "1",
            "DISABLE_TELEMETRY": "1",
            "DISABLE_ERROR_REPORTING": "1",
        }
        self.profile = self.root / "offline.sb"
        self.profile.write_text(
            "(version 1)(allow default)(deny network*)(deny file-write*)"
            f"(allow file-write* (subpath {json.dumps(str(self.root))})"
            ' (literal "/dev/null"))',
            encoding="utf-8",
        )

    def command(self, *args):
        executable = shutil.which(args[0])
        if not executable:
            raise RuntimeError(f"Missing native tool: {args[0]}")
        return ["/usr/bin/sandbox-exec", "-f", str(self.profile), executable, *args[1:]]

    def run(self, *args):
        result = subprocess.run(
            self.command(*args),
            cwd=self.project,
            env=self.env,
            text=True,
            capture_output=True,
            timeout=45,
        )
        if result.returncode:
            raise AssertionError(f"{args}: {result.stdout}\n{result.stderr}")
        return result.stdout

    def codex_skills(self):
        """Only initialize and skills/list; never create a conversation or turn."""
        with subprocess.Popen(
            self.command("codex", "app-server", "--stdio"),
            cwd=self.project,
            env=self.env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        ) as process:
            messages = queue.Queue()

            def read():
                for line in process.stdout:
                    messages.put(json.loads(line))

            reader = threading.Thread(target=read, daemon=True)
            reader.start()

            def request(identifier, method, params):
                process.stdin.write(
                    json.dumps(
                        {
                            "id": identifier,
                            "method": method,
                            "params": params,
                        }
                    )
                    + "\n"
                )
                process.stdin.flush()
                for _ in range(100):
                    message = messages.get(timeout=20)
                    if message.get("id") == identifier:
                        if "error" in message:
                            raise AssertionError(message)
                        return message["result"]
                raise AssertionError("No app-server response")

            try:
                request(
                    1,
                    "initialize",
                    {
                        "clientInfo": {
                            "name": "contextlean_install_test",
                            "version": "0.3.0",
                        }
                    },
                )
                process.stdin.write('{"method":"initialized"}\n')
                process.stdin.flush()
                result = request(
                    2,
                    "skills/list",
                    {
                        "cwds": [str(self.project)],
                        "forceReload": True,
                    },
                )
                entries = result["data"]
                if len(entries) != 1 or entries[0]["errors"]:
                    raise AssertionError(entries)
                return [s for s in entries[0]["skills"] if s["name"].startswith("contextlean:")]
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                reader.join(timeout=5)


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}
