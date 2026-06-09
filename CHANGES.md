# Changes

## 2026-06-09

- Added a failure velocity reset so returning to the start after a ghost
  collision does not preserve stale movement speed.

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
