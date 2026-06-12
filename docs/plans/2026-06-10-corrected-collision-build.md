# Corrected Collision Build

status: completed

## Problem

Gameplay outcome checks use the pacman view's previous frame before boundary and
wall constraints are resolved. A winning exit collision also falls through to
ghost collision handling in the same update. The hosted gate parses the Xcode
project but does not compile the Objective-C target.

## Scope

- Resolve boundaries and walls before evaluating exit and ghost outcomes.
- Evaluate outcomes against one candidate frame derived from the corrected
  gameplay position.
- Stop outcome evaluation after the game is completed.
- Build the unsigned app for a generic iOS simulator in hosted CI.
- Raise project and target deployment settings to iOS 12 for current Xcode.
- Extend the static baseline to guard these contracts.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `./build.sh` on macOS with Xcode
- `git diff --check`
