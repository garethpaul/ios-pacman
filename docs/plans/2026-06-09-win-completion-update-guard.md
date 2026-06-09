# Win Completion Update Guard

status: completed

## Context

The exit collision path stopped accelerometer updates before showing the win
alert, but alert dismissal cleared the same visibility flag used by the update
loop. A terminal completion state makes the win path explicit and keeps any
queued or future update calls from moving the player after completion.

## Completed Scope

- Added `gameCompleted` state to the view controller.
- Marked win completion and reset movement velocity before showing the exit
  alert.
- Updated the movement loop to pause while an alert is visible or the game is
  completed.
- Extended the static baseline and docs so win completion remains a terminal
  update guard.

## Verification

- `make check`
- `git diff --check`
