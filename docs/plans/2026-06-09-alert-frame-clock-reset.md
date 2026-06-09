# Alert Frame Clock Reset

status: completed

## Context

Gameplay updates pause while collision alerts are visible. During that pause,
`lastUpdateTime` can still point at the frame before the alert appeared. Resetting
the frame clock when the alert dismisses keeps resumed movement tied to a fresh
timestamp instead of hidden alert duration.

## Objectives

- Reset `lastUpdateTime` when a collision alert dismisses.
- Preserve the existing alert visibility reset.
- Keep frame time delta clamping as a second guardrail.
- Extend the static baseline so the alert dismissal clock reset remains visible
  without Xcode.
- Document the frame clock reset alongside alert pause and collision alert
  guardrails.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
