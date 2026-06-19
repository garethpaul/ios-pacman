#ifndef APPMotionValidation_h
#define APPMotionValidation_h

#include <stdbool.h>

#define APPMotionMaximumAccelerationComponent 16.0

bool APPMotionComponentsAreSafeForIntegration(double x, double y, double z);

#endif
