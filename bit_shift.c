
#include <stdio.h>
#include <limits.h>

/*
&
AND on each bit
1100 & 1010 = 1000  

*/


void print_bits(unsigned int value)
{
    int bits = sizeof(value) * CHAR_BIT;

    for (int i = bits - 1; i >= 0; i--) {
        unsigned int bit = (value >> i) & 1u;
        printf("%u", bit);
    }

    printf("\n");
}


int main() {

    int x = 0b1100;  // 2**3 + 2**2 = 12
    int y = 0b1010;  // 2**3 + 2**1 = 10

 

    print_bits(x);
    print_bits(y);
    
    
   
    printf("x & y = %d\n", x & y);




}