# Alert Update Pause

status: completed

## Context

Collision alerts are gated so repeated collision frames do not stack duplicate
alerts. While an alert is visible, the accelerometer update loop can still call
`update`, allowing movement and collision calculations to continue behind the
alert. Gameplay updates should pause until the alert is dismissed.

## Objectives

- Return early from `update` while `collisionAlertVisible` is true.
- Preserve the existing alert dismissal reset behavior.
- Extend the static baseline to require the alert pause guard.
- Document the alert pause alongside collision alert and time-delta guardrails.

## Verification

- `make check`
- `git diff --check`
