## iOS Pacman Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

iOS Pacman is an Objective-C iOS game sample inspired by classic maze gameplay.

The repository is useful as a compact older iOS game project with image assets,
an XIB-based view controller, a screenshot, and a build script. Project context
lives in [`README.md`](README.md).

The goal is to keep the game playable, buildable, and easy to inspect.

The current focus is:

Priority:

- Preserve the maze gameplay and asset references
- Keep the screenshot and README aligned with app behavior
- Maintain the build script and Xcode project structure
- Keep accelerometer updates bounded to the live controller lifecycle
- Gate collision alerts so repeated frames do not stack modal alerts
- Reset movement velocity after failure collisions send the player to start
- Reset the frame clock when alert pause ends
- Clamp frame time delta before applying motion velocity
- Avoid broad rewrites without gameplay verification
- Keep `scripts/check-baseline.py` passing for shell syntax, asset/XIB
  references, Xcode metadata, Objective-C source inventory, and local-only gameplay
- Keep `make lint`, `make test`, `make build`, and `make check` available as
  local verification gates

Next priorities:

- Add manual gameplay verification steps
- Modernize Objective-C/project settings only in a dedicated pass
- Document asset provenance for future replacements

Contribution rules:

- One PR = one focused gameplay, asset, build, or documentation change.
- Verify the game launches after Xcode or asset changes.
- Keep generated build products and signing files out of git.
- Include notes for visible gameplay changes.

## Security

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

This is a local game sample. Future networking, accounts, or analytics should be
opt-in and documented.

Current baseline: `make lint`, `make test`, `make build`, and `make check` run
`scripts/check-baseline.py` without Xcode. It verifies `build.sh`,
plist/XIB/scheme XML, image resources, Xcode project references, accelerometer
lifecycle guardrails, frame time delta clamping, collision alert gating, failure
velocity reset behavior, and alert pause behavior, with local-only gameplay and
alert frame clock reset behavior, with no debug logging, network, analytics,
upload, or persistence behavior.
It also verifies that motion callbacks avoid strongly retaining the controller.

## What We Will Not Merge (For Now)

- Asset replacements without purpose or provenance
- Analytics or tracking features
- Broad project migration bundled with gameplay changes
- Build changes that make the sample harder to open

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
