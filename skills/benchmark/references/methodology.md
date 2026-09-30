# Benchmark methodology

ContextLean exposes two different kinds of evidence. They must never be presented as
equivalent.

## Static estimate

`bootstrap-start` captures instruction paths and byte counts before bootstrap.
`bootstrap-finish` writes the verified before/after data to
`.contextlean/bootstrap-report.json`. `benchmark estimate` reads that report without
running Codex.

Exact filesystem counts are labelled **exact**. The token figure is an explicitly
labelled bytes-per-token approximation. Detection of large mandatory startup
documents is a path-and-language heuristic. Static structure can show that guidance
changed; it cannot prove model-token savings, task quality, or faster completion.

If the pre-bootstrap snapshot is missing, ContextLean reports the current state only.
It never reconstructs or invents a baseline.

## Codex A/B

`benchmark ab` creates temporary baseline and optimized copies outside the working
repository. Only project `AGENTS.md` files and lightweight `CLAUDE.md` wrappers are
removed from the baseline copy. Non-instruction content is hashed to confirm that the
variants otherwise match, and the original repository is hashed before and after the
runs to detect mutation.

Each task runs in a fresh `codex exec --json --ephemeral` conversation with the same
model, reasoning effort, prompt, read-only sandbox, disabled web search, and ignored
user configuration and exec rules. Ordering alternates deterministically between
baseline-first and optimized-first. Reports retain the wrapped tasks, options,
ordering, versions, and digests needed to inspect or repeat the experiment.
`danger-full-access` is never used.

ContextLean reads token usage from
`turn.completed.usage` and counts command events from Codex JSONL. It does not claim a
file-open count because current events do not establish one reliably. Failed or
unpaired runs suppress an overall gain claim. This generic navigation runner has no
answer grader: completion means execution completed with valid usage, not that the
task was solved correctly. It therefore suppresses gain claims even for completed
pairs. Use the [graded sample suite](../../../benchmarks/README.md) for independent
task-success checks and retained raw logs.

Live runs consume the usage of the configured Codex provider. They are opt-in and are
never executed by the default tests.

## Task selection

User-supplied read-only tasks are preferred. Tasks should require realistic
navigation across ownership, flow, tests, configuration, or persistence. They should
be specific enough to verify from source and broad enough that the repository map can
plausibly affect navigation. The exact same wrapped task is used for each A/B pair.

The built-in five-task suite is only a starting point. Results apply to those tasks,
not automatically to every kind of work in the repository.

## Tokens and credit-equivalents

`cached_input_tokens` is treated as part of `input_tokens`. Reasoning tokens are
reported separately but not added to billed output because they are already included
in `output_tokens`.

When ChatGPT authentication and a matching dated official rate card are available,
ContextLean may report a **credit-equivalent**. It is not a statement of actual credits
spent. API-key authentication and unknown or unclassified rates produce token-only
results.

## Limitations

- **Stochasticity:** model choices and outputs vary even with identical inputs.
- **Caching:** provider-side cache state can change observed input composition.
- **Task selection:** a narrow or biased suite can overstate or hide an effect.
- **Model and reasoning dependence:** results for one model and effort do not transfer
  automatically to another.
- **Environment and service load:** process time and tool choices contain noise.
- **Static metrics:** fewer instruction bytes are not the same as token savings or
  better answers.

One repetition is indicative; multiple complete repetitions provide a better view
of variance but do not establish statistical confidence by themselves.

Official implementation references:

- [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)
- [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Codex pricing](https://learn.chatgpt.com/docs/pricing)
- [Reasoning token semantics](https://developers.openai.com/api/docs/guides/reasoning)
