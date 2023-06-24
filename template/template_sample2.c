#include <stdio.h>
#include <stdint.h>

{{return_type}} calc_func() {
    {{return_type}} result = {{init_0}};
{{code}}
    return result;
}

int main() {

    {{return_type}} result = calc_func();

    printf("%#lx\n", (uint64_t) result);

    return 0;
}

