# Main-Thread Motion Handoff

status: planned

## Context

Core Motion invokes the accelerometer handler on the controller's operation
queue. The current handler writes the `CMAcceleration` property on that queue
and separately schedules `update` on the main thread. Gameplay therefore reads
a multi-value motion sample on a different thread from the one that wrote it,
and a newer callback can replace the sample before an older queued update runs.

## Scope

- Dispatch each valid accelerometer sample to the main queue.
- Resolve the weak controller reference inside the main-queue block.
- Assign the sample and run the gameplay update together on the main thread.
- Extend the static baseline and project documentation with this invariant.
- Mutation-test that moving the assignment outside the main-queue block is
  rejected.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `python3 -m py_compile scripts/check-baseline.py`
- `git diff --check`
