# Executable Motion Validation Tests

status: completed

## Goal

Replace static-only confidence in accelerometer component validation with
executable tests of the same finite-sample predicate used by the app.

## Implementation

- Move the three-component finite check into portable C source compiled by the
  Maze application target.
- Keep CoreMotion callback ownership and main-thread gameplay handoff unchanged.
- Compile and run a repository-owned C harness through every Make gate before
  static contracts and the optional Xcode build.
- Treat warnings as errors so the portable test boundary remains strict.

## Verification

- Repository and external-directory `make check` passed with executable C
  behavior even when Xcode was unavailable.
- The harness accepts zero, ordinary, and finite boundary samples while
  rejecting NaN and positive or negative infinity in every component.
- Hostile mutations were rejected for runner invocation, application
  delegation, component coverage, compiler warnings, and Xcode membership.
