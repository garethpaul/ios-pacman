# Changes

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
