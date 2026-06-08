# Changes

## 2026-06-08

- Made `build.sh` compatible with its `/bin/sh` shebang by removing bash-only function syntax.
- Made `build.sh` skip cleanly on hosts without Xcode.
- Ignored unavailable accelerometer samples and stopped motion updates during controller teardown.
- Added `make check` and a static Objective-C/Xcode baseline for shell syntax, plist/XIB/scheme XML, image resources, project wiring, and local-only gameplay guardrails.
- Documented the legacy Xcode project, build script, asset inventory, and static verification workflow.
