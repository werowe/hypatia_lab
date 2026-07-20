#include <stdio.h>

int main() {
    int x = 5;

    // Print the value of x
    // %d is a placeholder for an integer

    printf("x = %d\n", x);
    
    int x = 42;
char buffer[20];
sprintf(buffer, "%d", x);
printf("%s", buffer); 
    
    return 0;
}

