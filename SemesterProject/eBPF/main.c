#include <stdio.h>

void test_function(int value) {
    if (value > 10) {
        printf("Value is greater than 10.\n");
    } else {
        printf("Value is 10 or less.\n");
    }
}

int main() {
    printf("Starting program...\n");
    test_function(5);
    test_function(15);
    printf("Program finished.\n");
    return 0;
}
