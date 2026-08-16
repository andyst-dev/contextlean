# Existing Claude guidance

This service receives names from an import queue and normalizes them before storage.
The queue contract, retry policy, deployment notes, incident history, and manual
recovery steps below are useful project knowledge, but they are too detailed for
automatic startup context. A bootstrap must preserve them in an optional reference
and replace this file with a lightweight `@AGENTS.md` wrapper.

## Queue contract

Inputs are UTF-8 strings. Blank values are rejected by the caller. Normalization is
owned by `src/index.ts`; callers must not implement parallel normalization rules.

## Retry policy

Transient queue failures are retried by infrastructure. Application code must not
introduce its own unbounded retry loop.

## Deployment notes

The fixture has no real deployment. These notes intentionally represent substantial
existing knowledge that a bootstrap must preserve rather than overwrite.

## Incident history

Previous failures came from callers trimming values inconsistently. Keep the shared
normalization owner explicit in repository guidance.

## Manual recovery

Verify the queue input, run the existing test command, and inspect normalized output.
Do not change production behavior as part of repository-guidance bootstrap.

## Additional operational context

The remaining paragraphs deliberately make this fixture larger than a normal wrapper.
They model a repository where useful Claude-specific notes accumulated over time.
ContextLean should move such detail behind a targeted reference, link it from the
project map, and keep the automatically loaded wrapper small.

The import queue is logically separate from normalization. Configuration belongs to
the deployment layer, transformation belongs to the source module, and verification
belongs to the test suite. A future agent should be able to locate each owner without
loading the entire incident history.

Recovery is always read-only until the operator explicitly authorizes a mutation.
Credentials, provider configuration, and user-global settings are outside the scope
of repository bootstrap. The fixture includes these statements to ensure useful
boundaries survive migration into optional documentation.
