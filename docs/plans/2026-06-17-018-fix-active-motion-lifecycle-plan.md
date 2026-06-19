---
title: Active-App Motion Lifecycle
type: fix
date: 2026-06-17
---

# Active-App Motion Lifecycle

## Summary

Tie accelerometer delivery to the app's active lifecycle instead of starting it
once in `viewDidLoad` and stopping only during controller teardown. Invalidate
queued samples across each stop/restart boundary so inactive or stale motion
cannot update gameplay.

## Problem Frame

The root gameplay controller remains alive when the app loses focus or enters
the background, so `dealloc` does not stop CoreMotion. Sensor and operation-queue
work can continue while gameplay is inactive, and a callback queued before the
pause can arrive after a later resume.

Apple documents `UIApplicationWillResignActiveNotification` as the loss-of-focus
boundary and `applicationDidBecomeActive:` as the point where active work may
resume. `CMMotionManager` remains active between its start and stop calls.

## Requirements

- R1. Start accelerometer updates when the application becomes active, not from
  one-time view loading.
- R2. Stop accelerometer updates when the application will resign active and
  during controller teardown or terminal win completion.
- R3. Make start and stop idempotent so repeated lifecycle callbacks do not
  duplicate handlers or corrupt state.
- R4. Invalidate queued callbacks with a generation token across every stop and
  restart boundary before assigning acceleration or updating gameplay.
- R5. Reset the frame clock when motion resumes so inactive time cannot produce
  a stale integration interval.
- R6. Preserve finite-sample validation, weak capture, main-thread handoff,
  collision behavior, velocity policy, assets, and project metadata.
- R7. Add mutation-sensitive static contracts and synchronized lifecycle
  guidance, with the hosted macOS build as the Objective-C compile boundary.

## Key Technical Decisions

- **App delegate drives active-state ownership:** the existing pre-scene app
  delegate already receives active/inactive callbacks and owns the root
  controller.
- **Controller owns CoreMotion implementation:** public lifecycle methods hide
  the handler, queue, clock, and generation details from the app delegate.
- **Generation guards queued work:** a captured generation must still match on
  the main queue, preventing pre-stop samples from crossing a pause or resume.
- **Terminal wins remain terminal:** active-state callbacks must not restart
  motion after the game has completed.

## Implementation Units

### U1. Encapsulate motion start and stop

- **Goal:** Move handler registration into idempotent controller lifecycle
  methods and preserve finite, weak, main-thread sample handling.
- **Files:** `Maze/APPViewController.h`, `Maze/APPViewController.m`
- **Verification:** Static ordering checks cover generation capture, stale
  rejection, clock reset, duplicate-start guard, stop invalidation, win stop,
  and teardown stop.
- **Covers:** R1, R2, R3, R4, R5, R6.

### U2. Connect application lifecycle callbacks

- **Goal:** Stop before the app loses active status and restart after it becomes
  active.
- **Files:** `Maze/APPAppDelegate.m`
- **Patterns:** Reuse the existing root-controller property without adding
  notification observers or scene APIs to this legacy app.
- **Covers:** R1, R2, R3.

### U3. Lock verification and guidance

- **Goal:** Extend the canonical checker and maintenance documentation with the
  active-app motion lifecycle contract.
- **Files:** `scripts/check-baseline.py`, `README.md`, `SECURITY.md`, `VISION.md`,
  `CHANGES.md`
- **Verification:** Root and external Make gates plus isolated mutations of app
  lifecycle wiring, generation invalidation, restart guards, docs, and checker
  enforcement.
- **Covers:** R7.

## Risks And Mitigations

- A stop can race a previously queued main-thread block; generation comparison
  rejects that block even if motion restarts before it executes.
- Repeated active callbacks can otherwise register duplicate handlers; check
  `isAccelerometerActive` before starting.
- Linux cannot compile UIKit/CoreMotion Objective-C; keep source contracts local
  and require both hosted macOS event paths on the exact head.

## Scope Boundaries

- Do not change acceleration math, velocity reset semantics, collisions, alerts,
  ghost animation, win behavior, assets, XIB wiring, dependencies, or project
  settings.
- Do not migrate the legacy app to scenes, notifications, or a new motion
  abstraction.
- Do not add background motion execution or permissions.

## Verification

- Run the executable C motion-validation harness.
- Run `make lint`, `make test`, `make build`, and `make check` from the checkout.
- Run the absolute-path Make gate from an external directory.
- Compile the Python checker, validate `build.sh`, and run `git diff --check`.
- Reject isolated mutations covering app lifecycle calls, duplicate-start
  protection, generation invalidation, stale callback rejection, clock reset,
  documentation, and checker enforcement.
- Audit intended files for generated artifacts and credential-shaped content.

## References

- [UIApplicationWillResignActiveNotification](https://developer.apple.com/documentation/uikit/uiapplication/willresignactivenotification?language=objc)
- [UIApplicationDelegate applicationDidBecomeActive:](https://developer.apple.com/documentation/uikit/uiapplicationdelegate)
- [CMMotionManager stopAccelerometerUpdates](https://developer.apple.com/documentation/coremotion/cmmotionmanager/stopaccelerometerupdates%28%29)
