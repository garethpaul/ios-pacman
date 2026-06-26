# Refresh Wall Collision Frame

status: completed

## Problem

`collisionWithWalls` captured one candidate frame before iterating the wall
collection. When one wall rolled the position back, later walls in the same
update still tested the stale pre-rollback frame and could apply an unnecessary
second collision response.

## Scope

- Preserve existing wall ordering, rollback-axis selection, and velocity damping.
- Refresh the candidate frame after each rollback before checking a later wall.
- Keep exit and ghost outcomes on the final corrected frame.
- Add a mutation-sensitive portable source contract.
- Avoid XIB, asset, project-setting, motion, alert, and public API changes.

## Work Completed

- Recomputed `frame` from `currentPoint` after each wall collision response.
- Required the refresh to occur after the vertical or horizontal rollback branch.
- Updated repository guidance for sequential corrected wall geometry.

## Verification Completed

- The new baseline contract failed before implementation with
  `wall collision handling must refresh the candidate frame after rollback before checking later walls`.
- `python3 scripts/check-baseline.py` passed after implementation.
- `/usr/bin/make lint`, `/usr/bin/make test`, `/usr/bin/make build`, and
  `/usr/bin/make check` passed from the checkout and through the absolute
  Makefile path from `/tmp`.
- `python3 -m py_compile scripts/check-baseline.py`,
  `sh -n scripts/run-motion-validation-tests.sh`, `sh -n build.sh`, and
  `git diff --check` passed.
- Three isolated hostile mutations were rejected: removing the refresh, moving
  it before the rollback branch, and moving it outside the collision branch.
- `xcodebuild` was unavailable locally and skipped explicitly; hosted macOS CI
  is the Objective-C compile boundary.

## Scope Boundaries

- No wall layout, collision axis, damping constant, motion sampling, alert
  lifecycle, outcome ordering, persistence, networking, or telemetry changed.
