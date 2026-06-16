#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
CC=${CC:-cc}
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/ios-pacman-motion-tests.XXXXXX")

cleanup() {
    rm -rf -- "$BUILD_DIR"
}
trap cleanup 0
trap 'exit 129' 1
trap 'exit 130' 2
trap 'exit 143' 15

"$CC" \
    -std=c11 \
    -Wall \
    -Wextra \
    -Werror \
    -I"$ROOT/Maze" \
    "$ROOT/Maze/APPMotionValidation.c" \
    "$ROOT/Tests/APPMotionValidationTests.c" \
    -lm \
    -o "$BUILD_DIR/motion-validation-tests"

"$BUILD_DIR/motion-validation-tests"
