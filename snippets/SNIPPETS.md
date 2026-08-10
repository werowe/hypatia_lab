# SNIPPETS

A collection of short, standalone C programs — quick references for
patterns you'll use constantly, rather than full lessons of their own. For
the full explanation behind any pattern here, follow the link to its
proper page.

---

## `hello_world.c`

The traditional first program in any language.

```c
#include <stdio.h>

int main() {

    printf("Hello World!");
    return 0;
}
```

```bash
clang -Wall -Wextra -Wpedantic -std=c17 hello_world.c -o hello_world
./hello_world
```

Output:

```text
Hello World!
```

See [Printing](../printing/PRINTING.md) for everything `printf()` can do.

---

## `copy.c`

Reads every character typed at the keyboard and prints it right back out,
one at a time, until the input ends.

```c
#include <stdio.h>

int main() {

    int c;

    while ((c = getchar()) != EOF) {
        putchar(c);
    }

    return 0;
}
```

```bash
clang -Wall -Wextra -Wpedantic -std=c17 copy.c -o copy
./copy
```

`getchar()` reads one character at a time; `putchar()` prints one
character. `EOF` ("end of file") is what `getchar()` returns once there's
nothing left to read — press **Ctrl+D** (macOS/Linux) to signal that from
the keyboard. See section 9 of [Loops](../loops/LOOPS.md) for the full
explanation of this exact pattern.

---

## `bit_shift.c`

Demonstrates bitwise `&` and `|`, and a helper function that prints any
integer in binary, one bit at a time.

```c
#include <stdio.h>
#include <limits.h>
#include <stdint.h>

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

    unsigned int x = 0b1100;  // 12
    unsigned int y = 0b1010;  // 10

    int n = 257;

    printf("before");
    print_bits(n);
    n = n & 0177;             // keep only the lowest 7 bits
    printf("n = %d\n", n);
    printf("after");
    print_bits(n);

    x = x | y;

    printf("x = ");
    print_bits(x);
    printf("y = ");
    print_bits(y);
}
```

See [Bits and Bitwise Operations](../bits/BITS.md) for a full explanation
of `&`, `|`, `^`, `~`, `<<`, `>>`, and `print_bits()`.

> **Heads up — this file won't compile as written.** Further down in the
> same function, it declares `int x` and `int y` a *second* time, in the
> same scope as the `unsigned int x` and `unsigned int y` above. C does not
> allow redeclaring a variable in the same scope — this is a great
> "predict the compiler error" exercise: try compiling it as-is, read what
> `clang` reports, then fix it by renaming the second pair (or removing the
> first) before running it. It also `#include <cmath>`, a **C++** header —
> a `.c` file compiled as C should use `<math.h>` instead.

---

## `class_1.c`

A short demo mixing `printf()` and `sprintf()`.

```c
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
```

`sprintf()` works like `printf()`, but instead of printing to the screen,
it writes the formatted text into a `char` array (`buffer`) that you can
use later. See [Printing](../printing/PRINTING.md) and
[Strings](../strings/STRINGS.md).

> **Heads up — this file won't compile as written, either.** `int x` is
> declared twice in `main()`'s scope: once as `5`, then again as `42`. Just
> like in `bit_shift.c` above, that's a redefinition error in C. Try
> compiling it, read the error `clang` gives you, and fix it by giving the
> second variable its own name (for example, `y`) before running it.

---

## Quick Reference

A few common patterns, with links to where they're explained in full:

```c
// Loop over an array
for (size_t i = 0; i < length; i++) {
    printf("%d\n", numbers[i]);
}
```
See [Arrays](../arrays/ARRAYS.md).

```c
// Compare two strings
if (strcmp(name1, name2) == 0) {
    printf("Equal\n");
}
```
See [Strings](../strings/STRINGS.md).

```c
// Swap two variables using pointers
void swap(int *first, int *second)
{
    int temporary = *first;
    *first = *second;
    *second = temporary;
}
```
See [Pointers](../pointers/POINTERS.md).

```c
// Set, clear, and check one bit
value |=  (1u << n);            // set
value &= ~(1u << n);            // clear
unsigned int bit = (value >> n) & 1u;   // check
```
See [Bits](../bits/BITS.md).

---

## Programs

* [`hello_world.c`](hello_world.c) — the classic first program.
* [`copy.c`](copy.c) — echoes keyboard input back out, character by character.
* [`bit_shift.c`](bit_shift.c) — bitwise `&`/`|` and a binary-printing helper. *(currently has a compile error — see above)*
* [`class_1.c`](class_1.c) — `printf()` and `sprintf()` demo. *(currently has a compile error — see above)*

## Compile

```bash
clang -Wall -Wextra -Wpedantic -std=c17 <filename>.c -o <program-name>
```

## Run

```bash
./<program-name>
```
