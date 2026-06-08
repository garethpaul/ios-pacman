# iOS Pacman Objective-C Game Baseline Plan

status: completed

## Context

`ios-pacman` is a legacy Objective-C iOS game sample with XIB layout, image assets, accelerometer motion, an Xcode scheme, and a small CI build script. This Linux host does not provide Xcode, so local verification needs a static baseline while full app builds remain a macOS/Xcode responsibility.

## Objectives

- Fix the checked-in shell build script so it is valid for its `/bin/sh` shebang.
- Add a local `make check` baseline for shell syntax, Xcode metadata, plist/XIB/scheme XML, image resources, source inventory, and local-only gameplay guardrails.
- Keep the game dependency-free and free of network, analytics, account, or upload behavior.
- Document legacy Xcode verification expectations and non-macOS static checks.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `sh -n build.sh`
- `git diff --check`
