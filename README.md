# ios-pacman

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/ios-pacman` is a legacy Objective-C iOS Pac-Man game with a small
shared C motion-validation component.

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: Objective-C (3), C (2), C/C++ headers (3), shell (2).

## Repository Contents

- `CHANGES.md` - concise history of maintenance changes
- `Makefile` - local verification entry point
- `README.md` - project overview and local usage notes
- `build.sh`
- `Maze` - source or example code
- `Maze.xcodeproj` - Xcode project file
- `SECURITY.md` - security reporting and disclosure guidance
- `scripts/check-baseline.py` - static Objective-C/Xcode project verifier
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: Maze
- Dependency and build manifests: none detected
- Entry points or build surfaces: `make check`, build.sh, Maze.xcodeproj
- Executable test: `Tests/APPMotionValidationTests.c`, compiled and run by
  `make check` through `scripts/run-motion-validation-tests.sh`

## Getting Started

### Prerequisites

- Git
- macOS with Xcode for building Apple platform projects
- Python 3 for local static verification on non-macOS hosts

### Setup

```bash
git clone https://github.com/garethpaul/ios-pacman.git
cd ios-pacman
make lint
make test
make build
make check
```

The checked-in project has no external dependency manifest. Use Xcode for full builds and `make check` for static verification on hosts without Xcode.

## Running or Using the Project

- Open `Maze.xcodeproj` in Xcode, choose the sole shared `Maze` scheme, and run
  it on a compatible simulator or device.
- Run `./build.sh` when the required platform toolchain is installed. On hosts without Xcode, the script exits cleanly after reporting that the Xcode build was skipped. Xcode DerivedData stays in a temp directory unless `DERIVED_DATA_DIR` is set.
- This is a local game sample with XIB-wired image assets and CoreMotion movement. The accelerometer availability guard rejects unsupported hardware before motion startup state changes. Non-finite or overflow-prone motion samples are rejected before each valid accelerometer sample is assigned and integrated together on the main thread. Gameplay updates clamp the frame time delta before applying accelerometer velocity, refresh candidate geometry after each wall rollback, resolve boundary and wall constraints before evaluating the corrected outcome frame, stop outcome checks after a win, gate collision alerts while visible, and reset the frame clock after alerts. Do not add accounts, analytics, persistence, upload, or network behavior without a dedicated design and security review.

## Testing and Verification

Run the local static baseline:

```bash
make lint
make test
make build
make check
```

The `lint`, `test`, and `build` targets intentionally alias the static baseline
on hosts without the legacy Xcode toolchain, so the standard local gate commands
stay available while preserving the single source of truth.

The baseline first compiles and runs executable C tests against the same finite
motion-sample predicate used by the CoreMotion callback. It then runs
`scripts/check-baseline.py`, validates POSIX shell syntax for `build.sh`, parses
plist/XIB/scheme XML, checks PNG resources, verifies Xcode project references,
checks corrected collision ordering, per-wall candidate-frame refresh, accelerometer
lifecycle and main-thread handoff, collision alert gating, failure velocity
reset behavior, previous position initialization, win completion update guards,
alert pause behavior, alert frame clock reset behavior, frame time delta
clamping, and weak callback capture guardrails, and guards against debug
logging, network, analytics, upload, or persistence behavior.

`Tests/APPMotionValidationTests.c` is a standalone C behavioral harness rather
than an Xcode test target. The shared `Maze` scheme has no Xcode testable
references, so use `make check` for the executable tests and Xcode Build or
`./build.sh` for the app target.

Pinned `macos-15` CI runs `make check` and compiles the unsigned app for a
generic iOS simulator. It does not exercise accelerometer input, alerts,
rendering, or gameplay.

GitHub Actions runs the same `make check` static baseline with Python 3.12 for
pushes and pull requests.

For full legacy build verification on macOS, run `./build.sh` or build the
`Maze` scheme in Xcode with an appropriate destination. `build.sh` directs
DerivedData to a temp directory by default.

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.

## Security and Privacy Notes

- Review changes touching network requests, sockets, or service endpoints; examples from the scan include Maze/Maze-Info.plist.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include Maze/APPViewController.m, Maze/Maze-Info.plist.
- Resource changes should keep image files, XIB outlets, screenshot, and Xcode project references aligned.
- Accelerometer callbacks should not strongly retain the controller. Non-finite
  or overflow-prone motion samples should be rejected, updates should follow the
  active app lifecycle, and stale queued motion should not cross pause/resume
  boundaries.
- Ghost collision alerts stop accelerometer delivery while the modal prompt is
  visible. Dismissal clears the alert guard, refreshes the frame clock, and then
  resumes motion; terminal win alerts remain stopped.
- Wall collision rollback refreshes the candidate frame before later walls are
  evaluated, preventing stale geometry from applying extra collision responses.
- `build.sh` should stay valid for `/bin/sh` because CI and local shells may not invoke bash.

## Maintenance Notes

- This is a self-contained Objective-C/C Xcode project with no external
  dependency manifest. Xcode and deployment target compatibility may still
  reflect the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-09-alert-update-pause.md` for the alert pause guardrail.
- See `docs/plans/2026-06-09-alert-frame-clock-reset.md` for the alert frame clock reset guardrail.
- See `docs/plans/2026-06-09-failure-velocity-reset.md` for the failure velocity reset guardrail.
- See `docs/plans/2026-06-09-win-completion-update-guard.md` for the win completion update guardrail.
- See `docs/plans/2026-06-10-previous-point-initialization.md` for the previous position initialization guardrail.
- See `docs/plans/2026-06-13-nonfinite-motion-sample-guard.md` for the sensor
  value guardrail.
- See `docs/plans/2026-06-16-executable-motion-validation-tests.md` for the
  shared finite-sample predicate and executable C behavioral gate.
- See `docs/plans/2026-06-17-018-fix-active-motion-lifecycle-plan.md` for active
  app lifecycle ownership and stale queued motion rejection.
- See `docs/plans/2026-06-25-pause-motion-during-alerts.md` for collision-alert
  sensor suspension and guarded dismissal resume behavior.
- See `docs/plans/2026-06-26-refresh-wall-collision-frame.md` for per-wall
  corrected-frame evaluation.
- See `docs/plans/2026-06-10-ci-baseline.md` for the GitHub Actions static
  baseline.
- See `docs/plans/2026-06-09-make-gate-aliases.md` for the local gate alias guardrail.
- Run `make lint`, `make test`, `make build`, and `make check` before pushing changes to Objective-C sources, plist/XIB files, image assets, Xcode metadata, `build.sh`, or gameplay/security documentation.
- The same gates may be invoked through an absolute Makefile path from another
  directory; verification resolves both commands relative to the checkout.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
