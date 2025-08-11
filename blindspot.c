#include <stdio.h>

#define FILTER_SIZE 5
static float leftHistory[FILTER_SIZE] = {0};
static float rightHistory[FILTER_SIZE] = {0};
static int indexPos = 0;

// Function to smooth distance readings (moving average)
float smoothReading(float history[], float newReading) {
    history[indexPos] = newReading;
    float sum = 0.0;
    for (int i = 0; i < FILTER_SIZE; i++) {
        sum += history[i];
    }
    return sum / FILTER_SIZE;
}

// Function to check if object is in blind spot
int detectBlindSpot(float leftDistance, float rightDistance) {
    float leftSmoothed = smoothReading(leftHistory, leftDistance);
    float rightSmoothed = smoothReading(rightHistory, rightDistance);

    indexPos = (indexPos + 1) % FILTER_SIZE;

    // Blind spot range: 0.5m to 3.0m
    if ((leftSmoothed >= 0.5 && leftSmoothed <= 3.0) ||
        (rightSmoothed >= 0.5 && rightSmoothed <= 3.0)) {
        return 1; // Warning triggered
    }
    return 0; // No warning
}
