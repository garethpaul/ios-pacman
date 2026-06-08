## iOS Pacman Vision

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
- Avoid broad rewrites without gameplay verification

Next priorities:

- Add README setup and Xcode version notes
- Add manual gameplay verification steps
- Modernize Objective-C/project settings only in a dedicated pass
- Document asset provenance for future replacements

Contribution rules:

- One PR = one focused gameplay, asset, build, or documentation change.
- Verify the game launches after Xcode or asset changes.
- Keep generated build products and signing files out of git.
- Include notes for visible gameplay changes.

## Security

This is a local game sample. Future networking, accounts, or analytics should be
opt-in and documented.

## What We Will Not Merge For Now

- Asset replacements without purpose or provenance
- Analytics or tracking features
- Broad project migration bundled with gameplay changes
- Build changes that make the sample harder to open
