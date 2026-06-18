# Accelerometer Availability Guard

status: planned

## Context

`startMotionUpdates` rejects completed games and duplicate active streams, but
it does not check whether the current device exposes accelerometer data. An
unsupported environment can therefore advance the motion generation, reset the
frame clock, and request a stream that Core Motion cannot provide.

## Priority

Treat sensor capability as part of the motion lifecycle boundary. Rejecting an
unavailable accelerometer before startup side effects keeps generation and
timing state aligned with real stream ownership while preserving the existing
active-app lifecycle and stale-callback defenses.

## Requirements

- R1. Motion startup must require `isAccelerometerAvailable` in addition to a
  non-terminal game and an inactive accelerometer stream.
- R2. Capability rejection must occur before generation changes, frame-clock
  reset, handler capture, or `startAccelerometerUpdatesToQueue`.
- R3. Supported devices must retain the existing generation token, finite
  sample validation, weak capture, main-thread handoff, and update behavior.
- R4. Stop, inactive-app, teardown, and terminal-win behavior must remain
  unchanged.
- R5. Portable static contracts must reject a missing, inverted, or late
  availability check and incomplete plan or guidance evidence.

## Implementation Units

### U1. Guard motion capability

**File:** `Maze/APPViewController.m`

Extend the idempotent startup guard with `isAccelerometerAvailable`, ahead of
all startup state mutation and Core Motion registration.

### U2. Portable regression contracts

**File:** `scripts/check-baseline.py`

Parse the startup method and require the availability predicate, its ordering
before generation and clock state, and its position before handler startup.

### U3. Maintained evidence

**Files:** `AGENTS.md`, `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`,
and this plan.

Document accelerometer availability as part of the existing local-only motion
lifecycle without changing gameplay, assets, dependencies, or project metadata.

## Test Scenarios

- A completed game rejects motion startup.
- An unavailable accelerometer rejects startup before generation or clock
  changes.
- An already active stream rejects duplicate startup.
- An available inactive stream preserves the existing handler and stale-sample
  generation contract.
- Existing executable motion-validation and lifecycle contracts remain green.

## Scope Boundaries

- Do not change acceleration math, collision behavior, alerts, ghost animation,
  win behavior, assets, XIB wiring, dependencies, or project settings.
- Do not add fallback controls, background motion, permissions, or a new motion
  abstraction.
- Do not claim local UIKit or Core Motion execution when Xcode is unavailable.

## Verification

- Run the executable C motion-validation harness through all four Make gates.
- Run the absolute-path Make gate from an external directory.
- Compile the Python checker, validate `build.sh` and the C runner shell, and
  run `git diff --check`.
- Reject isolated mutations for availability presence, predicate polarity,
  ordering, guidance, and completed plan evidence.
- Audit intended files for generated artifacts, protected metadata, and
  credential-shaped additions.

## Work Completed

Pending implementation.

## Verification Completed

Pending implementation and validation.
