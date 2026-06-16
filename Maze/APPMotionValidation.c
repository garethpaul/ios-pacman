#include "APPMotionValidation.h"

#include <math.h>

bool APPMotionComponentsAreFinite(double x, double y, double z) {
    return isfinite(x) && isfinite(y) && isfinite(z);
}
