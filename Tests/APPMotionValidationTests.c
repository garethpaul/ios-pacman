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
    expect_true(APPMotionComponentsAreSafeForIntegration(0.0, 0.0, 0.0), "zero sample is usable");
    expect_true(APPMotionComponentsAreSafeForIntegration(0.25, -0.5, 1.0), "normal sample is usable");
    expect_true(APPMotionComponentsAreSafeForIntegration(APPMotionMaximumAccelerationComponent,
                                                        -APPMotionMaximumAccelerationComponent,
                                                        DBL_MIN),
                "bounded finite sample is usable");

    expect_false(APPMotionComponentsAreSafeForIntegration(NAN, 0.0, 0.0), "NaN x is rejected");
    expect_false(APPMotionComponentsAreSafeForIntegration(0.0, NAN, 0.0), "NaN y is rejected");
    expect_false(APPMotionComponentsAreSafeForIntegration(0.0, 0.0, NAN), "NaN z is rejected");
    expect_false(APPMotionComponentsAreSafeForIntegration(INFINITY, 0.0, 0.0), "positive infinity is rejected");
    expect_false(APPMotionComponentsAreSafeForIntegration(0.0, -INFINITY, 0.0), "negative infinity is rejected");
    expect_false(APPMotionComponentsAreSafeForIntegration(DBL_MAX, 0.0, 0.0), "overflow-prone x is rejected");
    expect_false(APPMotionComponentsAreSafeForIntegration(0.0, -DBL_MAX, 0.0), "overflow-prone y is rejected");
    expect_false(APPMotionComponentsAreSafeForIntegration(0.0, 0.0, APPMotionMaximumAccelerationComponent + 1.0),
                 "out-of-range z is rejected");

    if (failure_count != 0) {
        return 1;
    }

    puts("APPMotionValidation behavioral tests passed");
    return 0;
}
