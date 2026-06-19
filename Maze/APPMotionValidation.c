#include "APPMotionValidation.h"

#include <math.h>

static bool APPMotionComponentIsSafeForIntegration(double value) {
    return isfinite(value) && fabs(value) <= APPMotionMaximumAccelerationComponent;
}

bool APPMotionComponentsAreSafeForIntegration(double x, double y, double z) {
    return APPMotionComponentIsSafeForIntegration(x)
        && APPMotionComponentIsSafeForIntegration(y)
        && APPMotionComponentIsSafeForIntegration(z);
}
