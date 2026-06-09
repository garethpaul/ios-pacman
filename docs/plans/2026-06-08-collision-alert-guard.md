# Collision Alert Guard Plan

status: completed

## Context

The Objective-C game shows modal alerts when the player reaches the exit or hits
a hazard. Collision checks can run across repeated frames while an alert is still
visible, so those paths should not stack duplicate modal prompts.

## Objectives

- Add explicit collision-alert visibility state to the view controller.
- Gate win and failure alert creation while an alert is already visible.
- Reset the visibility state when the alert is dismissed.
- Extend the static baseline so the guard remains visible without Xcode.
- Document the collision-alert guard alongside the existing accelerometer and
  frame time delta guardrails.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `./build.sh`
- `git diff --check`
