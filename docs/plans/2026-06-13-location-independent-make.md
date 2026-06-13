# Location-Independent Pacman Verification

status: in progress

## Context

Absolute Makefile invocations resolve both the Python checker and `build.sh`
relative to the caller instead of the checkout, so documented verification
aliases fail outside the repository directory.

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

## Risk And Rollback

This changes verification path resolution only. Rollback restores the relative
recipes and removes their checker, plan, and documentation contracts.
