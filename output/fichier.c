#include "mixin.h"

int function1(int a, int b) {
    return function5(function4(a-b));
}

int function2(int a, int b) {
    return function5(a*b);
}

int function3(int a, int b) {
    return a-b;
}
