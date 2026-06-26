# Active Motion Start Guard

Status: Completed

## Goal

Make active application state an invariant of the controller-owned motion
startup boundary rather than an assumption of individual callers.

## Scope

- Reject startup unless `UIApplicationStateActive` owns the screen.
- Keep the check before generation, clock, queue, and handler side effects.
- Preserve availability, duplicate-start, alert, and terminal-game guards.
- Keep app delegate and alert dismissal callers unchanged.

## Verification

- Prove the missing guard with the static baseline.
- Run `make check` and isolated hostile mutations.
- Run hosted Xcode build and CodeQL before merge.
- Run `git diff --check` and exact-head review.

## Outcome

Every motion restart path now fails closed while the application is inactive.
