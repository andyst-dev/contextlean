# Provider-aware sandbox composition correction — harness v3

This is benchmark infrastructure only. ContextLean remains 0.2.1; packaged Skills,
product behavior, task acceptance and historical evidence are unchanged. Harness
and future summary schema advance from 2 to 3 because effective permission strategy
and receipts changed. Historical receipts keep their original versions.

## Exact observed failure

On macOS 27.0 arm64, with codex-cli 0.147.0, v2 built this process chain:

```text
harness subprocess.run(cwd=<session-root>/repo, env=normalized session environment)
  /usr/bin/sandbox-exec -f <session-root>/receipts/filesystem.sb
    <pinned-codex-cli> exec ... --sandbox workspace-write ...
      Codex native command sandbox (macOS Seatbelt)
        task shell/command
```

The outer profile allowed default operations, denied filesystem writes except
session repo/tmp/cache/artifacts/receipts and /dev/null, and denied reads of the
exported evidence directory. Synthetic Python permission probes passed under it.
They did not exercise Codex's own sandbox initialization.

The deterministic reproducer, without any model request, replaces `exec` with:

```text
<pinned-codex-cli> sandbox
  --config model_reasoning_effort="high"
  --config approval_policy="never"
  --config web_search="disabled"
  --config sandbox_workspace_write.exclude_slash_tmp=true
  --config sandbox_workspace_write.exclude_tmpdir_env_var=true
  --config sandbox_mode="workspace-write"
  -- <pinned-python> -c "print('offline nested sandbox probe')"
```

That invocation alone exits 0. Inside the exact v2 outer profile it exits **71**
with **`sandbox_apply: Operation not permitted`**, before Python prints anything.
The invalid boundary is the second Seatbelt sandbox initialization inside an
already sandboxed provider process. This establishes the observed composition
conflict, not an undocumented explanation of Apple's kernel internals. It is not
a task-path, prompt, model or grading failure. The stopped Refactor campaign made
zero model calls and its original evidence is preserved.

The regression reproduces the same failure using the new named profile as well.
No equivalent Linux failure has been observed here; Linux retains a real native
CLI gate rather than inheriting a macOS compatibility claim. Claude documents
Seatbelt on macOS and Bubblewrap on Linux for its optional Bash sandbox. We did
not reproduce a nested Claude CLI failure: its installed CLI has no exposed offline
native-command mechanism, and invoking a model to explore it is unauthorized.

## Corrected execution

The harness owns unique roots, deterministic fixture/Git preparation, controlled
cwd/environment/PATH/runtime, session-local scratch/cache/profile, receipts,
evidence capture and verified lifecycle cleanup. Codex owns command sandboxing.
Its driver is launched directly; there is no outer Seatbelt or Bubblewrap wrapper.
Native sandboxing is enabled explicitly, never bypassed.

Codex `sandbox` and `exec` receive the same named `contextlean-session` permissions
profile. It starts with `:root = "deny"` and `:minimal = "read"`, adds pinned runtime
reads and local profile reads, allows repo/tmp writes for edit tasks, protects
`.git`, explicitly denies evidence and disables task-command networking. No legacy
`--sandbox` or `sandbox_workspace_write` override is mixed into named permissions.
Managed requirements are included in the offline sandbox probe; unsupported
configuration or constraints fail preparation. The driver can write its own
session control areas; sandboxed task commands cannot write them.

The offline gate is `codex sandbox --permission-profile contextlean-session
--include-managed-config --cd <repo> --config ... -- <python> -c <permission-probe>`.
The same CLI path also runs canonical verbose regression tests. Receipts distinguish
actual native-command verification from configuration intent. They retain exact
private invocations, public normalized policies, enclosing exit codes and individual
allowed/denied results. Separate per-operation exit codes are null, not estimated.

Native and outer strategies are mutually exclusive and validated before launch.
An explicitly non-native runner may use the harness outer boundary where supported.
No automatic fallback or retry switches a failed native provider to unrestricted
execution. Both conditions must have identical normalized policy receipts.

## Claude limitation and security scope

For Claude 2.1.233, only `--help`/`--version` and OS-primitive diagnostics are used
offline. There is no documented native-command sandbox subcommand. Settings require
`sandbox.enabled`, `sandbox.failIfUnavailable` and prohibit
`sandbox.allowUnsandboxedCommands`. Nevertheless, an OS-primitive diagnostic cannot
prove the actual Claude Bash wrapper or its separate built-in file tool policies.
Its native availability is recorded as unverified and execution is blocked as a
harness/preparation failure. This is deliberately an unsupported gate, not a
successful Claude-native validation or a claim that Claude is inherently incompatible.

Tests check allowed repo/tmp writes, forbidden parent/outside writes and evidence/unrelated scratch
reads, read-only task policy, Vanilla/ContextLean receipt parity, concurrent
cross-session scratch denial, scratch removal and later invisibility, cleanup on
failure, strategy downgrades/nesting and failed receipt preservation. The provider
driver is trusted to enforce its native tool policy; an offline command probe does
not establish every opaque provider tool's behavior. Runtime directories are readable
and not fully hermetic. Credentials are confined to an auth-only session profile;
raw receipts contain no credential values and public evidence is sanitized.

Provider documentation:
[Codex permissions](https://learn.chatgpt.com/docs/permissions),
[Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference),
[Claude sandboxing](https://code.claude.com/docs/en/sandboxing).
