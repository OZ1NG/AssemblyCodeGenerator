#include <stdio.h>
#include <stdint.h>

uint32_t calc_func() {
    uint32_t result = {{init_0}};
    {{v_0}};
    {{v_1}};
    {{v_2}};
    
    for (int i = 0; i < {{loop_count_0}}; i++) {
        result += v_0;
        result *= v_1;
        result -= v_2;
    }

    return result;
}

int main() {

    uint32_t result = calc_func();

    printf("%#lx\n", (uint64_t) result);

    return 0;
}

