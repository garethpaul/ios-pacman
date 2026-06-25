# Pause Motion During Collision Alerts

status: completed

## Context

`update` returned while a collision alert was visible, but the accelerometer
stream continued producing callbacks. A ghost collision therefore consumed
sensor and queue work behind a modal prompt, and app activation could restart
motion before that prompt was dismissed.

Apple's Core Motion guidance says to call `stopAccelerometerUpdates` when motion
data is no longer needed. The existing alert delegate provides the matching
post-dismissal boundary for a guarded restart.

## Design

- Add `collisionAlertVisible` to `startMotionUpdates` rejection conditions.
- Mark the ghost alert visible, then call `stopMotionUpdates` before presenting
  it so generation invalidation rejects already queued callbacks.
- On dismissal, clear visibility, refresh the frame clock, and call
  `startMotionUpdates`; its completed-game and capability guards remain the
  authority for whether motion can resume.

## Test First

The static baseline was extended before source implementation. It failed for
the missing startup guard, missing failure-path stop, and missing dismissal
restart.

## Verification

- `python3 scripts/check-baseline.py`
- `/usr/bin/make check`
- Isolated hostile mutations removing the alert guard, stop, or restart
- `git diff --check`
- Local `xcodebuild` is unavailable; hosted macOS CI is authoritative.

## Scope Boundaries

- Motion math, finite-sample validation, collision geometry, assets, XIB
  wiring, deployment target, signing, and terminal win behavior are unchanged.
- `UIAlertView` remains for compatibility with the legacy sample; modernizing
  modal presentation is outside this fix.

## References

- https://developer.apple.com/documentation/coremotion/cmmotionmanager
- https://developer.apple.com/documentation/uikit/uialertviewdelegate
