#include "APPMotionValidation.h"

#include <float.h>
#include <math.h>
#include <stdio.h>

static int failure_count = 0;

static void expect_true(bool value, const char *message) {
    if (!value) {
        fprintf(stderr, "FAIL: %s: expected true\n", message);
        failure_count += 1;
    }
}

static void expect_false(bool value, const char *message) {
    if (value) {
        fprintf(stderr, "FAIL: %s: expected false\n", message);
        failure_count += 1;
    }
}

int main(void) {
    expect_true(APPMotionComponentsAreFinite(0.0, 0.0, 0.0), "zero sample is finite");
    expect_true(APPMotionComponentsAreFinite(0.25, -0.5, 1.0), "normal sample is finite");
    expect_true(APPMotionComponentsAreFinite(DBL_MAX, -DBL_MAX, DBL_MIN), "finite boundaries are accepted");

    expect_false(APPMotionComponentsAreFinite(NAN, 0.0, 0.0), "NaN x is rejected");
    expect_false(APPMotionComponentsAreFinite(0.0, NAN, 0.0), "NaN y is rejected");
    expect_false(APPMotionComponentsAreFinite(0.0, 0.0, NAN), "NaN z is rejected");
    expect_false(APPMotionComponentsAreFinite(INFINITY, 0.0, 0.0), "positive infinity is rejected");
    expect_false(APPMotionComponentsAreFinite(0.0, -INFINITY, 0.0), "negative infinity is rejected");

    if (failure_count != 0) {
        return 1;
    }

    puts("APPMotionValidation behavioral tests passed");
    return 0;
}
