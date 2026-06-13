# Location-Independent Pacman Verification

status: completed

## Context

Absolute Makefile invocations previously resolved both the Python checker and
`build.sh` relative to the caller instead of the checkout, so documented
verification aliases failed outside the repository directory.

## Scope

1. Derive the checkout root from the loaded Makefile.
2. Invoke the checker by absolute path and enter the checkout before `build.sh`.
3. Add exact Makefile, completed-plan, external-run, and guidance contracts.
4. Preserve Objective-C gameplay, project metadata, resources, and workflow
   policy.

## Verification Plan

- Run all four Make gates from the checkout and through an absolute Makefile
  path from a temporary directory.
- Run checker compilation, build-script syntax, project metadata parsing, and
  diff checks.
- Reject root-derivation, checker-invocation, build-script-invocation,
  plan-status, plan-evidence, and documentation mutations independently.
- Inspect intended paths, secret patterns, conflict markers, and generated
  artifacts before commit.

## Work Completed

- Derived the checkout root from the loaded Makefile, invoked the checker by
  absolute path, and entered the checkout before running `build.sh`.
- Added exact Makefile, completed-plan, external-run, and synchronized guidance
  contracts without changing gameplay, project, resources, or workflow files.

## Verification Completed

- All four Make gates passed from the checkout.
- All four Make gates passed from `/tmp` through the absolute Makefile path.
- `python3 -m py_compile scripts/check-baseline.py`, `sh -n build.sh`, and
  project metadata parsing passed; `git diff --check` passed.
- Local validation reported that `xcodebuild` was unavailable, so the static
  iOS baseline ran and the build script skipped the Xcode build.
- Six isolated hostile mutations were rejected: root derivation, checker
  invocation, build-script invocation, plan status, plan evidence, and
  documentation guidance.

## Risk And Rollback

This changes verification path resolution only. Rollback restores the relative
recipes and removes their checker, plan, and documentation contracts.
