# ARRAYS

An **array** stores a fixed number of values of the same type, one right
after another in memory. Instead of creating `score1`, `score2`, `score3`,
you create one array, `scores`, and access each value by its position.

```c
int scores[5];
```

This reserves room for exactly five `int` values, all named `scores`.

---

## 1. Declaring and Initializing

```c
int scores[5];                              // uninitialized — garbage values
int scores[5] = {88, 92, 79, 65, 100};       // initialized
int scores[] = {88, 92, 79, 65, 100};        // size inferred from the list: 5
```

Letting the compiler count the elements is usually the easiest and safest
option, since the array size and the initializer list can never disagree.

```c
#include <stdio.h>

int main(void)
{
    int scores[] = {88, 92, 79, 65, 100};

    printf("%zu\n", sizeof scores / sizeof scores[0]);

    return 0;
}
```

Output:

```text
5
```

---

## 2. Indexing

Elements are numbered starting at **zero**, not one.

```text
Index:  0   1   2   3   4
Value: 88  92  79  65 100
```

```c
int scores[] = {88, 92, 79, 65, 100};

printf("%d\n", scores[0]);   // 88 — the first element
printf("%d\n", scores[4]);   // 100 — the last element
```

For an array of length `n`, the valid indexes are `0` through `n - 1`.
There is no `scores[5]` in a 5-element array — that index doesn't exist.

### Out-of-Bounds Access Is a Real Danger, Not an Error Message

C does **not** check whether an index is valid. Reading or writing past the
end of an array does not stop the program with a helpful error — it reads
or corrupts whatever happens to be in memory next to the array. This is
called **undefined behavior**, and it's one of the most common sources of
bugs and security vulnerabilities in C programs.

```c
int scores[5] = {88, 92, 79, 65, 100};

scores[5] = 0;   // BUG: index 5 doesn't exist in a 5-element array
```

This may crash immediately, silently corrupt an unrelated variable, or
appear to work fine and fail later — which makes it especially dangerous.
Always double-check your loop bounds.

---

## 3. Changing an Element

```c
int scores[] = {88, 92, 79, 65, 100};

scores[0] = 95;   // replace the first element

printf("%d\n", scores[0]);
```

Output:

```text
95
```

---

## 4. Looping Through an Array

This is the single most common thing you'll do with an array — visit every
element, usually with a `for` loop. See [Loops](../loops/LOOPS.md).

```c
#include <stdio.h>

int main(void)
{
    int scores[] = {88, 92, 79, 65, 100};
    size_t length = sizeof scores / sizeof scores[0];

    for (size_t i = 0; i < length; i++) {
        printf("%d\n", scores[i]);
    }

    return 0;
}
```

`sizeof scores / sizeof scores[0]` means:

```text
total bytes used by the array  ÷  bytes used by one element  =  number of elements
```

This keeps working correctly even if you add or remove elements from the
initializer list later — you never have to remember to update a hardcoded
`5` somewhere else in the code.

### A Common Task: Finding the Total and Average

```c
#include <stdio.h>

int main(void)
{
    int scores[] = {88, 92, 79, 65, 100};
    size_t length = sizeof scores / sizeof scores[0];

    int total = 0;

    for (size_t i = 0; i < length; i++) {
        total += scores[i];
    }

    double average = (double)total / length;

    printf("Total: %d\n", total);
    printf("Average: %.1f\n", average);

    return 0;
}
```

Output:

```text
Total: 424
Average: 84.8
```

The cast `(double)total` forces a floating-point division instead of an
integer one that would truncate the fractional part — see the integer
division note in [Operators](../operators/OPERATORS.md).

---

## 5. Arrays of `char` Are Strings

C doesn't have a separate string type — a string is just an array of `char`
that ends with a special `'\0'` byte. Because this is such a big topic on
its own, it has a dedicated page: [Strings](../strings/STRINGS.md).

```c
char name[] = "Elene";   // an array of 6 char: 'E' 'l' 'e' 'n' 'e' '\0'
```

---

## 6. Two-Dimensional Arrays

An array can have more than one dimension — useful for grids, tables, and
game boards.

```c
int grid[2][3] = {
    {1, 2, 3},
    {4, 5, 6}
};
```

```c
#include <stdio.h>

int main(void)
{
    int grid[2][3] = {
        {1, 2, 3},
        {4, 5, 6}
    };

    for (int row = 0; row < 2; row++) {
        for (int col = 0; col < 3; col++) {
            printf("%d ", grid[row][col]);
        }
        printf("\n");
    }

    return 0;
}
```

Output:

```text
1 2 3
4 5 6
```

---

## 7. Arrays and Functions

When an array is passed to a function, the function receives a pointer to
its first element, not a copy of the whole array. This means the function
can see (and change) the caller's actual array — and it also means the
function has no way to know the array's length on its own. You must pass
the length as a separate argument.

```c
#include <stdio.h>

void print_all(int values[], size_t length)
{
    for (size_t i = 0; i < length; i++) {
        printf("%d\n", values[i]);
    }
}

int main(void)
{
    int scores[] = {88, 92, 79, 65, 100};
    size_t length = sizeof scores / sizeof scores[0];

    print_all(scores, length);

    return 0;
}
```

The full explanation of why this happens — and what `sizeof scores` would
be *inside* `print_all` (a pointer's size, not the array's size, a classic
beginner trap) — is in [Pointers](../pointers/POINTERS.md).

---

## 8. Arrays of Structs

An array can hold structures instead of plain numbers. This will feel very
familiar once you've read [Structs](../structs/STRUCTS.md):

```c
struct point {
    int x;
    int y;
};

struct point path[3] = {
    {0, 0},
    {1, 2},
    {3, 4}
};

printf("%d, %d\n", path[1].x, path[1].y);   // 1, 2
```

---

## 9. A Practical Example: Blinking Several LEDs

```c
const int LED_PINS[] = {2, 3, 4, 5};
const int LED_COUNT = 4;

void setup()
{
    for (int i = 0; i < LED_COUNT; i++) {
        pinMode(LED_PINS[i], OUTPUT);
    }
}

void loop()
{
    for (int i = 0; i < LED_COUNT; i++) {
        digitalWrite(LED_PINS[i], HIGH);
        delay(100);
        digitalWrite(LED_PINS[i], LOW);
    }
}
```

Storing the pin numbers in an array, instead of writing four nearly
identical blocks of code, is a very common Arduino pattern once you're
wiring up more than one or two components. See
[Arduino](../arduino/ARDUINO.md).

---

## Summary

```text
int values[5];                  declare, uninitialized
int values[] = {1, 2, 3};       declare and initialize, size inferred
values[0]                       first element
values[length - 1]              last element
sizeof values / sizeof values[0]  number of elements
```

Rules to remember:

* Indexes start at `0`, not `1`.
* C never checks array bounds for you — going out of bounds is undefined
  behavior, not a helpful error message.
* An array passed to a function decays to a pointer — always pass the
  length alongside it.
* A `char` array ending in `'\0'` is how C represents a string.

---

## Programs

This folder doesn't have an example `.c` file yet. Create `arrays.c` and
try the total/average example above — it's a good first program to write
and run yourself.

## Compile

```bash
clang -Wall -Wextra -Wpedantic -std=c17 arrays.c -o arrays
```

## Run

```bash
./arrays
```
