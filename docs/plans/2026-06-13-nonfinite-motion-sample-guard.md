# Non-Finite Motion Sample Guard

status: completed

## Context

The accelerometer callback checks for an error and missing data, then copies all
three acceleration components into gameplay state. A non-finite sensor value
can propagate through velocity, position, collision rectangles, and rotation,
leaving the local game in an invalid geometry state.

## Priority

Core Motion is an external numeric boundary. Gameplay should fail closed for an
invalid sample instead of allowing NaN or infinity to contaminate persistent
controller state and later frame calculations.

## Requirements

- R1. Reject any accelerometer sample whose x, y, or z component is not finite.
- R2. Perform validation before scheduling work on the main queue.
- R3. Preserve assignment and `update` together on the main queue for valid
  samples, including weak/strong controller lifetime handling.
- R4. Preserve update cadence, delta clamping, velocities, collision ordering,
  alerts, terminal win behavior, assets, and local-only gameplay.
- R5. Add callback-scoped static contracts and completed verification evidence.

## Implementation Units

### U1. Validate the sensor boundary

- **File:** `Maze/APPViewController.m`
- Include the standard finite-number predicate and return before dispatch when
  any acceleration component is invalid.

### U2. Enforce validation ordering

- **File:** `scripts/check-baseline.py`
- Require error/data validation, three-component finite validation, main-queue
  dispatch, controller resolution, assignment, and update in that order.

### U3. Document the motion guardrail

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Record that invalid sensor samples cannot enter gameplay state.

## Scope Boundaries

- Do not alter valid acceleration values, sampling interval, movement scale,
  time-delta clamp, wall/exit/ghost collision behavior, or animation timing.
- Do not add networking, analytics, telemetry, persistence, or logging.
- Do not claim device or simulator motion validation without Xcode and a motion
  input source.

## Work Completed

- Rejected accelerometer samples with a non-finite x, y, or z component before
  main-queue dispatch.
- Preserved weak controller capture and kept valid-sample assignment and update
  together on the main thread.
- Extended the static baseline with callback-scoped validation and ordering
  contracts and documented the sensor boundary.

## Verification Completed

- All four Make gates, `make lint`, `make test`, `make build`, and `make check`,
  passed against the complete static baseline.
- `python3 -m py_compile scripts/check-baseline.py`, plist parsing, XIB, scheme,
  workspace, and SVG XML parsing, workflow YAML parsing, PNG signature/type
  checks, `sh -n build.sh`, and `git diff --check` passed.
- Ten hostile mutations removing any component predicate, the math import,
  the finite predicate, early return, validation-before-dispatch ordering, or
  main-queue dispatch, or falsifying plan status or verification evidence were
  rejected.
- The local environment did not provide `xcodebuild` or a motion input source,
  so device/simulator gameplay and accelerometer execution were not claimed.
