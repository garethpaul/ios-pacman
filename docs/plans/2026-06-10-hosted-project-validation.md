# Hosted Project Validation

status: completed

## Completed Scope

- Run pinned, read-only `macos-15` CI through `make check`.
- Parse `Maze.xcodeproj` when Xcode is available.
- Keep accelerometer input, alerts, rendering, gameplay, and signing outside CI.

## Verification

- `make check`
- workflow YAML parse
- `git diff --check`
