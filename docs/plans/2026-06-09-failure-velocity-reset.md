# Failure Velocity Reset

status: completed

## Context

Failure collisions send the player back to the starting point before showing the
modal alert. The previous implementation left accumulated accelerometer velocity
intact, so movement could resume with stale speed after the alert pause ended.

## Completed Scope

- Reset horizontal and vertical movement velocity when a failure collision sends
  the player back to the start.
- Kept collision alert gating, alert pause behavior, and frame clock reset
  behavior unchanged.
- Extended the static baseline and docs so failure velocity reset behavior
  remains visible without Xcode.

## Verification

- `make check`
- `git diff --check`
