# Main-Thread Motion Handoff

status: completed

## Context

Core Motion invokes the accelerometer handler on the controller's operation
queue. The current handler writes the `CMAcceleration` property on that queue
and separately schedules `update` on the main thread. Gameplay therefore reads
a multi-value motion sample on a different thread from the one that wrote it,
and a newer callback can replace the sample before an older queued update runs.

## Work Completed

- Dispatch each valid accelerometer sample to the main queue.
- Resolve the weak controller reference inside the main-queue block.
- Assign the sample and run the gameplay update together on the main thread.
- Extend the static baseline and project documentation with this invariant.
- Mutation-test that moving the assignment outside the main-queue block is
  rejected.

## Verification Completed

- Local `make check`, `make lint`, `make test`, and `make build` passed. The
  local environment did not provide `xcodebuild`, so `build.sh` reported the
  hosted Xcode requirement after the complete static baseline passed.
- `python3 -m py_compile scripts/check-baseline.py`, `sh -n build.sh`, and
  `git diff --check` passed.
- Hostile mutations changing the plan status, inserting an unfinished-work
  marker, falsifying a run ID, moving the acceleration assignment outside the
  main-queue block, or resolving the controller before dispatch were rejected.
- The implementation push Check run `27395230698` completed successfully for
  commit `6e06f5d1a53d3b471d192b34c2c1af70d16b4b7e`.
- The implementation pull-request Check run `27395235753` completed
  successfully for commit `6e06f5d1a53d3b471d192b34c2c1af70d16b4b7e` and
  built the Objective-C target for the generic iOS simulator on hosted macOS.
- The post-merge push Check run `27395277519` completed successfully for
  commit `0478d9fc14bf406ce0df7d5c8362e9477075951c`.
- The CodeQL setup run `27402323504` completed successfully for commit
  `0478d9fc14bf406ce0df7d5c8362e9477075951c`.
- Motion handling preserves `dispatch_async(dispatch_get_main_queue(), ^{`,
  then `APPViewController *strongSelf = weakSelf;`,
  `strongSelf.acceleration = acceleration;`, and `[strongSelf update];`.
