# Previous Point Initialization

status: completed

## Context

Wall collisions roll Pacman back to `previousPoint`, but the controller only set
`currentPoint` during startup. Before the first successful movement update,
`previousPoint` could still be the zero-value point, so an immediate wall
collision could roll the player away from the intended starting row.

## Completed Scope

- Initialized `previousPoint` to the starting `currentPoint` in `viewDidLoad`.
- Added static baseline coverage so startup position and rollback position stay
  aligned.
- Updated docs to describe the previous-position guardrail without adding
  networking, persistence, analytics, or account behavior.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
