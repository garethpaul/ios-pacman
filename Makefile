.PHONY: build check lint test

CC ?= cc
ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

lint test build: check

check:
	CC="$(CC)" "$(ROOT)/scripts/run-motion-validation-tests.sh"
	python3 "$(ROOT)/scripts/check-baseline.py"
	cd "$(ROOT)" && ./build.sh
