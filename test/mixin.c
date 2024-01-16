#include "mixin.h"

ADD_END(function1)
int function4(int a) {
    return a+1;
}

ADD_END(function2, function1, funciton4)
int function5(int a) {
    return a-1;
}