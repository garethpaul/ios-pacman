# Hosted Project Validation

status: completed

## Completed Scope

- Run pinned, credential-free, read-only `macos-15` CI with Python 3.12 through
  `make check`.
- Compile the unsigned app for a generic iOS simulator when Xcode is available.
- Keep accelerometer input, alerts, rendering, gameplay, and signing outside CI.

## Verification

- `make check`
- workflow YAML parse
- `git diff --check`
