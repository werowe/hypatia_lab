

#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

/*

Here we will not define a circuit.  Instead we will just write logic that shows how to turn on a LED by turning on
the base.  Remember when the base is on the power can flow from the collector to the emitter.  The emitter goes to ground
and the collector goes to the LED.  Both the LED and the base have a resistor.  When the base is on the LED is on.
*/

#define ON  1
#define OFF 0

// C does not have classes.  It has structs.  This is a convention way to use a meaningful name for 
// some item.  So you can think of like a Python dictionary if you want with keys and values

struct Transistor {
    bool base_on;
    bool conducting;
};

// this function receives a pointer to a struct Transistor
void update_transistor(struct Transistor *transistor)
{

    // Follow the pointer to the structure at that address, then access one of its members

    // when the base turns on the transistor turns on.  that means the collector-to-emitter circuit is conducting
    transistor->conducting = transistor->base_on;
}

int main(int argc, char *argv[])
{
    // argc is argument count
    // argv is argument vector or the list of argumenrs.  The first argument is the name of the program

    if (argc != 2) {
        printf("Usage: %s 1\n", argv[0]);
        printf("       %s 0\n", argv[0]);
        return 1;
    }

    // convert the string to an integer
    int input = atoi(argv[1]);

    // && is booleans AND   
    if (input != ON && input != OFF) {
        printf("Enter 1 for ON or 0 for OFF.\n");
        return 1;
    }

    // this instantiates the transistor meaning give the items in the struct a value
    struct Transistor transistor = {
        .base_on = false,
        .conducting = false
    };

    // this is shorthand for if input is ON then True. so transistor.base_on = true

    transistor.base_on = input == ON;

    // we pass the address of the transistor to the update_transistor function
    // in C we cannot pass a struct, so we pass the address of the struct
    
    update_transistor(&transistor);

    if (transistor.conducting) {
        printf("Base: ON\n");
        printf("Collector-to-emitter path: conducting\n");
    } else {
        printf("Base: OFF\n");
        printf("Collector-to-emitter path: blocked\n");
    }

    return 0;
}

