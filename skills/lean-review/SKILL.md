---
name: lean-review
description: Review the current code change for duplicated behavior, unnecessary abstraction or dependencies, misplaced ownership, dead code, speculative flexibility, and poor architectural locality. Use when asked for a lean review, simplification review, anti-overengineering check, or pre-merge review; remain read-only unless a separate fix is explicitly requested.
---

# Review a change for locality

Run only when the user requests a review. Review only; do not edit files by default. Prefer the current Git diff and relevant repository map. If no diff is available, use the change set or files identified by the user and state that limitation.

## Specialized architecture review

For an explicitly requested review involving ownership, extraction, boundaries,
dependency direction or indirection, read [Architecture and locality review](references/architecture.md).
These details are optional review material, not required ordinary coding context.

## Review workflow

1. Identify the responsibility the change is meant to own and the existing subsystem that should own it.
2. Read the changed code, its immediate callers or dependencies, and the smallest relevant verification.
3. Search before claiming duplication or reimplementation.
4. Check whether the change:
   - duplicates existing behavior;
   - adds an abstraction, dependency, forwarding wrapper, compatibility path, or configuration surface without a current need;
   - retains dead or obsolete code;
   - reimplements the language standard library or framework;
   - assigns a new responsibility to the wrong module;
   - spreads a cohesive feature across unnecessary unrelated files;
   - patches a symptom instead of the responsible root cause.
5. Report findings in priority order with paths, evidence, impact, and the smallest behavior-preserving alternative. If there are no material findings, say so directly and note any verification gap.

Do not equate fewer lines or smaller files with better code. A large cohesive file can be correct; many tiny files can make a change less local. The primary criterion is whether one responsibility can be understood and modified from the smallest reasonable coherent set of files.

Never trade away correctness, security, trust-boundary validation, data-loss prevention, readability, maintainability, accessibility, or explicitly requested behavior for apparent simplicity.
