# Frame Delta Clamp Plan

status: completed

## Context

`APPViewController` integrates accelerometer velocity using time elapsed since the last draw. If the app stalls or resumes after a pause, that elapsed time can be large enough to move the player by an oversized step.

## Objectives

- Clamp negative or oversized frame time deltas before velocity integration.
- Preserve the existing accelerometer movement model.
- Extend the static baseline so the clamp remains visible without Xcode.
- Document the motion-update guardrail.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `sh -n build.sh`
- `./build.sh`
- `git diff --check`
