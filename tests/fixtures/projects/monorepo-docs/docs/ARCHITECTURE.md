# Detailed fixture architecture

This document represents a large optional architecture reference in a monorepo. The
root package owns workspace orchestration. `apps/web` owns the user-facing entry
point. `packages/shared` owns stable identifiers shared by applications.

## Workspace boundaries

Applications may depend on shared packages. Shared packages must not import from
applications. This direction keeps reusable logic independent from delivery layers.

## Web application

The web application assembles user-facing behavior. It should remain thin and defer
stable identifier construction to the shared package.

## Shared package

The shared package exposes the smallest useful interface. Callers should not copy its
prefixing logic or depend on internal implementation details.

## Verification

Workspace-level changes require the root checks. A change isolated to one package can
begin with its targeted verification before broader checks are considered.

## Historical notes

These details are intentionally optional. They model a long architecture document
that future agents should search by topic and read selectively, not load at startup.
The project map needs only the ownership boundaries and verified commands.

Repeated rediscovery of workspace layout wastes context. Repeating this entire
document in root instructions also wastes context. The useful outcome is a concise
map that points to this reference only when deeper history is relevant.
