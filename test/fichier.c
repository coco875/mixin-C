#include "mixin.h"

int function1(int a, int b) {
    return a+b;
}

int function2(int a, int b) {
    return a*b;
}

OVERWRITE(function1)
int function3(int a, int b) {
    return a-b;
}