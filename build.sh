#!/bin/sh

set -eu

if ! command -v xcodebuild >/dev/null 2>&1; then
    echo "xcodebuild unavailable; skipping Xcode build on this host."
    exit 0
fi

cleanup_derived_data=0
if [ "${DERIVED_DATA_DIR:-}" = "" ]; then
    DERIVED_DATA_DIR=$(mktemp -d "${TMPDIR:-/tmp}/ios-pacman-derived-data.XXXXXX")
    cleanup_derived_data=1
fi

cleanup() {
    if [ "$cleanup_derived_data" -eq 1 ]; then
        rm -rf -- "$DERIVED_DATA_DIR"
    fi
}
trap cleanup 0

xcodebuild -project "Maze.xcodeproj" \
           -scheme "Maze" \
           -destination "generic/platform=iOS Simulator" \
           -sdk iphonesimulator \
           -configuration "Debug" \
           -derivedDataPath "$DERIVED_DATA_DIR" \
           CODE_SIGNING_ALLOWED=NO \
           build
