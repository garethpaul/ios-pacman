# Changes

## 2026-06-26 - P2 - Refresh wall collision geometry

### Summary
Recomputed Pac-Man's candidate frame after each wall rollback so subsequent
walls are evaluated against corrected geometry instead of the stale incoming
frame.

### Work completed
- Preserved the existing rollback axis and damped velocity behavior.
- Added a portable source contract for post-rollback frame refresh ordering.
- Synchronized gameplay, security, and maintenance guidance.

### Validation
- The new contract failed before implementation on the single captured frame.
- Local and hosted validation evidence is recorded in the completed plan.

### Bugs / findings
- P2: one update overlapping multiple wall images could apply later collision
  responses using geometry captured before the first rollback.

### Blockers
- Local `xcodebuild` is unavailable; hosted macOS CI remains authoritative for
  Objective-C compilation.

### Next action
- Merge only after exact-head review and hosted checks pass.

## 2026-06-25 05:18 - P2 - Pause motion delivery during collision alerts

### Summary
Stopped Core Motion delivery while a ghost collision alert owns the game screen
and resumed only after dismissal clears the alert guard.

### Work completed
- Added collision-alert visibility to the motion startup guard.
- Invalidated and stopped the active accelerometer stream before failure alerts.
- Restarted non-terminal motion after alert dismissal and clock refresh.

### Threads
- Started: none — work completed directly in the current repository.
- Continued: none.
- Stopped: none.

### Files changed
- `Maze/APPViewController.m` — enforced alert-scoped motion ownership.
- `scripts/check-baseline.py` — added ordered pause/resume source contracts.
- Documentation and plan files — recorded behavior, evidence, and boundaries.

### Validation
- `python3 scripts/check-baseline.py` — failed in three expected lifecycle
  contracts before implementation and passed afterward.
- `/usr/bin/make check` — passed the executable C harness, static baseline, and
  conditional build gate; Xcode was unavailable locally.
- Three isolated hostile mutations removing the guard, stop, or restart were
  rejected by their focused contracts.
- `python3 -m py_compile scripts/check-baseline.py`, shell syntax checks, and
  `git diff --check` — passed.
- Hosted Xcode and CodeQL checks — pending PR verification.

### Bugs / findings
- P2: modal collision alerts paused gameplay state updates but left the 60 Hz
  accelerometer stream and callback dispatch active behind the prompt.

### Blockers
- `xcodebuild` is unavailable locally; hosted macOS CI remains authoritative for
  Objective-C, UIKit, and Core Motion compilation.

### Next action
- Open a PR and complete Codex plus hosted review before merge.

## 2026-06-18

- Kept Xcode build artifacts temp-scoped through `build.sh`, stopped motion on
  background and termination lifecycle callbacks, and rejected overflow-prone
  finite accelerometer samples before gameplay integration.
- Added an accelerometer availability guard before motion generation, clock,
  capture, or handler startup state changes.

## 2026-06-17

- Tied accelerometer start and stop to the active app lifecycle and rejected
  stale queued motion across pause/resume boundaries.

## 2026-06-16

- Added executable C tests for finite accelerometer samples using the same
  predicate as the CoreMotion callback.

## 2026-06-13

- Made all Make verification aliases location-independent when invoked through
  an absolute Makefile path.
- Rejected non-finite motion samples before main-thread gameplay assignment and
  update.

## 2026-06-12

- Assigned each Core Motion sample and advanced gameplay together on the main
  thread, avoiding cross-thread acceleration state races and stale queued reads.

## 2026-06-10

- Resolved boundaries and walls before outcome collisions, evaluated exit and
  ghost intersections against the corrected candidate frame, and stopped ghost
  checks after a win.
- Raised deployment settings to iOS 12 and upgraded pinned macOS CI from project
  parsing to an unsigned generic-simulator app build.
- Initialized the previous position to the starting position so first-frame wall
  collision rollback does not use the zero-value point.
- Added pinned, read-only macOS GitHub Actions CI with Python 3.12 and no
  persisted checkout credentials; `make check` compiles the unsigned app.

## 2026-06-09

- Added local `make lint`, `make test`, and `make build` gate aliases for the
  static Objective-C game baseline.
- Added a failure velocity reset so returning to the start after a ghost
  collision does not preserve stale movement speed.
- Added a win completion update guard so movement stays stopped after the exit
  alert appears.

## 2026-06-08

- Made `build.sh` compatible with its `/bin/sh` shebang by removing bash-only function syntax.
- Made `build.sh` skip cleanly on hosts without Xcode.
- Ignored unavailable accelerometer samples and stopped motion updates during controller teardown.
- Avoided strongly retaining the controller from the accelerometer callback by using weak capture.
- Guarded collision alerts so repeated collision frames do not stack duplicate alerts.
- Added alert pause behavior so gameplay updates stop while collision alerts are visible.
- Reset the frame clock when collision alerts dismiss so movement resumes from a fresh timestamp.
- Clamped frame time delta before applying accelerometer velocity to avoid oversized movement steps.
- Added `make check` and a static Objective-C/Xcode baseline for shell syntax, plist/XIB/scheme XML, image resources, project wiring, and local-only gameplay guardrails.
- Documented the legacy Xcode project, build script, asset inventory, and static verification workflow.
