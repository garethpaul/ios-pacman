# Motion Capture Lifecycle Plan

status: completed

## Context

`ios-pacman` starts accelerometer updates with a block owned by `CMMotionManager`. The controller already stops motion updates during teardown, but a block that strongly captures the controller can prevent teardown from running.

## Objectives

- Keep accelerometer samples ignored when data or errors are unavailable.
- Avoid strongly retaining the view controller from the accelerometer callback.
- Preserve the existing main-thread gameplay update path.
- Extend the static baseline so the motion callback lifecycle remains visible.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `sh -n build.sh`
- `git diff --check`
