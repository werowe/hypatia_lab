
#include <cmath>
#include <stdio.h>
#include <limits.h>
#include <stdint.h>

/*
&
AND on each bit
1100 & 1010 = 1000  

*/

/* 

bitwise operators

& AND
| OR
^ XOR
<< left shift
>> right shift
-   one's complement
*/


void print_bits(unsigned int value)
{
    // multiply by 8 to get the number of bits
    int bits = sizeof(value) * CHAR_BIT;

    for (int i = bits - 1; i >= 0; i--) {
        unsigned int bit = (value >> i) & 1u;
        printf("%u", bit);
    }

    printf("\n");
}






int main() {

    unsigned int x = 0b1100;  // 2**3 + 2**2 = 12
    unsigned int y = 0b1010;  // 2**3 + 2**1 = 10

 
    // set to zero all but the lower order bits of n

    // 0177 octal = 127 decimal = 2^7 - 1 = 01111111
    // extract the lower 7 bits of n.  e.g. to ensure a value
    // is within the range 0-127 (ASCII characters)

    /*
Bitwise AND (&) compares two numbers one bit at a time.
A result bit is 1 only when both input bits are 1.

Example:
  1100
& 1010
------
  1000
*/


    int n = 257;

    printf("before");
    print_bits(n);
    n = n & 0177;
    printf("n = %d\n", n);
    printf("after");
    print_bits(n);

    int x = 0b100;
    int y = 0b011;
    unsigned int z = 0b111;

    // bitwise OR
    // 1100 | 1010 = 1110
    // useful for chaning individual bits
    // Common use: setting several hardware-control bits without changing the others.
    

    x = x | y;

    printf("x = ");
    print_bits(x);
    printf("y = ");
    print_bits(y);

    printf("z = ");
    print_bits(z);

    




}