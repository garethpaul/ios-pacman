# CI Baseline

status: completed

## Context

The repository had a local `make check` baseline for the Objective-C game, but
no hosted workflow ran the static checks and unsigned simulator build for pushes
and pull requests.

## Changes

- Added a bounded, read-only macOS workflow with immutable checkout and Python
  3.12 setup actions, with checkout credential persistence disabled.
- Runs `make check`, including static checks and the unsigned generic-simulator
  app build.
- Extended the checker and docs so the hosted CI and gameplay contracts remain
  visible.

## Verification

- `make check`
