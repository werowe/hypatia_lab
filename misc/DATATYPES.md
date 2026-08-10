# DATA TYPES

Every variable in C has a **type**. The type decides three things:

```text
1. How many bytes of memory the variable uses
2. What kind of values it can store
3. What operations are legal on it
```

C's built-in types fall into a small number of families. This page is a map of
all of them, with links to the pages in this course that cover each one in
depth. Where a type does not yet have its own page, the explanation is here.

---

## Overview

| Family | Examples | Covered in |
|---|---|---|
| Integer types | `int`, `short`, `long`, `unsigned int` | [Integers](../integers/INTEGERS.md), below |
| Character type | `char` | [char](../char/CHAR.md) |
| Floating-point types | `float`, `double`, `long double` | below |
| Boolean type | `bool` (`_Bool`) | below |
| `void` | `void`, `void *` | below |
| Arrays | `int numbers[10]` | [Arrays](../arrays/ARRAYS.md), [Strings](../strings/STRINGS.md) |
| Pointers | `int *p` | [Pointers](../pointers/POINTERS.md) |
| Structures | `struct point { ... }` | [Structs](../structs/STRUCTS.md) |
| Unions | `union value { ... }` | below |
| Enumerations | `enum color { ... }` | below |
| `typedef` names | `typedef unsigned char byte;` | below |
| Qualifiers | `const`, `volatile` | below |
| Storage classes | `static`, `extern`, `register` | below |

---

## 1. Integer Types

C gives you several sizes of integer, and each size comes in a **signed**
(can be negative) and an **unsigned** (zero or positive only) version.

```c
int             number;
short int       small_number;
long int        big_number;
long long int   huge_number;

unsigned int            positive_number;
unsigned short int      small_positive_number;
unsigned long int       big_positive_number;
unsigned long long int  huge_positive_number;
```

`short`, `long`, and `long long` are all just bigger or smaller versions of
`int`. Each `unsigned` version stores the same number of bits, but uses all
of them for magnitude instead of reserving one for the sign.

For **how** a signed integer actually represents a negative number in binary
(two's complement), and why the range of an 8-bit signed integer is `-128` to
`127`, see [Integers](../integers/INTEGERS.md).

### Typical sizes

Exact sizes are not guaranteed by the C standard — they depend on the
compiler and platform. These are typical values on a modern 64-bit computer
(macOS or Linux, using `clang` or `gcc`):

| Type | Typical size | Typical range (signed) |
|---|---|---|
| `short int` | 2 bytes | -32,768 to 32,767 |
| `int` | 4 bytes | -2,147,483,648 to 2,147,483,647 |
| `long int` | 8 bytes | very large |
| `long long int` | 8 bytes | very large |

You can always check on your own machine:

```c
#include <stdio.h>

int main(void)
{
    printf("%zu\n", sizeof(short));
    printf("%zu\n", sizeof(int));
    printf("%zu\n", sizeof(long));
    printf("%zu\n", sizeof(long long));

    return 0;
}
```

### Fixed-width integers: `<stdint.h>`

Because `int` and `long` are not a guaranteed size, C also provides types
whose width never changes:

```c
#include <stdint.h>

int8_t   a;   // exactly 8 bits, signed
uint8_t  b;   // exactly 8 bits, unsigned
int16_t  c;   // exactly 16 bits, signed
uint16_t d;   // exactly 16 bits, unsigned
int32_t  e;   // exactly 32 bits, signed
uint32_t f;   // exactly 32 bits, unsigned
int64_t  g;   // exactly 64 bits, signed
uint64_t h;   // exactly 64 bits, unsigned
```

These are the natural types to reach for in embedded and register-level
programming, where you care about the exact number of bits. See
[Printing](../printing/PRINTING.md) for how to print them correctly with the
`PRId32` / `PRIu32`-style macros from `<inttypes.h>`.

### `size_t`

`size_t` is an unsigned integer type used for sizes and array lengths — it is
what `sizeof` and `strlen()` return. Its width changes with the platform, so
it is always the correct type for "how many," and `%zu` is always the
correct format specifier for it. It is explained in detail in
[Strings](../strings/STRINGS.md), in the section on `strlen()`.

---

## 2. The Character Type: `char`

`char` is a one-byte integer type that is normally used to store a
character code. `sizeof(char)` is always `1`.

```c
char letter = 'A';
```

The full relationship between `char` and `int` — including why `'A'` has
type `int` but fits inside a `char` — is covered in [char](../char/CHAR.md).

An array of `char` is how C represents text. See
[Strings](../strings/STRINGS.md).

---

## 3. Floating-Point Types

Floating-point types store numbers with a fractional part.

```c
float       temperature = 25.5f;
double      price       = 19.95;
long double precise_value = 19.95L;
```

| Type | Typical size | Typical precision |
|---|---|---|
| `float` | 4 bytes | about 6–7 significant decimal digits |
| `double` | 8 bytes | about 15–16 significant decimal digits |
| `long double` | 8, 12, or 16 bytes | more than `double` (platform-dependent) |

A few rules to remember:

* A `float` literal needs an `f` suffix, or the compiler treats it as a
  `double`: `25.5f` versus `25.5`.
* When a `float` is passed to `printf()`, it is automatically promoted to
  `double`. That is why `%f` works for printing both.
* `double` is the normal default for floating-point work in C. Use `float`
  only when memory is tight, such as on a small microcontroller.

```c
#include <stdio.h>

int main(void)
{
    float  a = 1.0f / 3.0f;
    double b = 1.0  / 3.0;

    printf("%f\n", a);
    printf("%f\n", b);

    return 0;
}
```

Possible output:

```text
0.333333
0.333333
```

The two look similar when printed with the default precision, but `double`
is storing far more accurate digits internally.

Floating-point values cannot represent every fraction exactly, so never
compare them with `==`:

```c
double result = 0.1 + 0.2;

if (result == 0.3) {   // usually false!
    printf("Equal\n");
}
```

Compare against a small tolerance instead:

```c
#include <math.h>

if (fabs(result - 0.3) < 1e-9) {
    printf("Close enough\n");
}
```

See [Printing](../printing/PRINTING.md) for `%f`, `%e`, `%g`, and controlling
decimal places.

---

## 4. The Boolean Type: `bool`

C did not originally have a true Boolean type. Older code uses `int`, where
`0` means false and any non-zero value means true.

Modern C provides a real Boolean type, `_Bool`, and the header
`<stdbool.h>` gives it the friendlier name `bool`, along with `true` and
`false`:

```c
#include <stdbool.h>

bool is_on = true;
bool is_broken = false;
```

`sizeof(bool)` is typically `1` byte. `bool` is used throughout
[Structs](../structs/STRUCTS.md) and [Pointers](../pointers/POINTERS.md) —
for example, the `transistor` struct example represents each pin's state as
a `bool`.

```c
#include <stdio.h>
#include <stdbool.h>

int main(void)
{
    bool led_on = true;

    if (led_on) {
        printf("LED is on\n");
    }

    return 0;
}
```

---

## 5. `void`

`void` means "no type," and it is used in three different situations.

### A function that returns nothing

```c
void print_greeting(void)
{
    printf("Hello!\n");
}
```

### A function that takes no arguments

```c
int get_number(void)
{
    return 42;
}
```

### A generic pointer: `void *`

A `void *` can point to any type, but it cannot be dereferenced directly —
it must first be converted to a real pointer type. This is exactly the
type that `malloc()` returns, which is why it can be assigned to an `int *`,
a `char *`, or any other pointer type without a cast in C. See
[Pointers](../pointers/POINTERS.md) for the full explanation of `malloc()`,
`calloc()`, and `realloc()`.

```c
int *numbers = malloc(5 * sizeof *numbers);
```

---

## 6. Arrays

An array is a fixed-size sequence of values of the same type, stored
contiguously in memory.

```c
int numbers[5] = {10, 20, 30, 40, 50};
```

Arrays are covered in [Arrays](../arrays/ARRAYS.md). C's most common use of
arrays — the `char` array that forms a string — is covered in
[Strings](../strings/STRINGS.md). How array names decay into pointers is
covered in [Pointers](../pointers/POINTERS.md).

---

## 7. Pointers

A pointer is a variable that stores a memory address rather than a value.

```c
int number = 42;
int *pointer = &number;
```

Pointers get a full page to themselves: [Pointers](../pointers/POINTERS.md).

---

## 8. Structures

A `struct` groups several related values, possibly of different types, into
one variable.

```c
struct transistor {
    bool base;
    bool collector;
    bool emitter;
};
```

See [Structs](../structs/STRUCTS.md), and the structure examples in
[Pointers](../pointers/POINTERS.md) for pointers to structs and the `->`
operator.

---

## 9. Unions

A `union` looks like a `struct`, but all of its members share the **same**
memory instead of each getting their own space. A union is only ever big
enough to hold its largest member, and writing to one member overwrites
whatever was stored in the others.

```c
union value {
    int   as_int;
    float as_float;
    char  as_bytes[4];
};
```

```c
#include <stdio.h>

union value {
    int   as_int;
    float as_float;
};

int main(void)
{
    union value v;

    v.as_int = 42;

    printf("%d\n", v.as_int);

    v.as_float = 3.14f;

    printf("%f\n", v.as_float);
    // v.as_int is no longer valid here —
    // it was overwritten by as_float

    return 0;
}
```

```c
printf("%zu\n", sizeof(union value));  // size of the largest member
```

Unions are less common than structs in beginner code, but they show up when
you need to look at the same bytes in more than one way — for example,
inspecting the individual bytes of a `float`, or reading a hardware register
that packs several small fields into one word. See
[Registers](../registers/REGISTERS.md) and
[Bits and Bitwise Operations](../bits/BITS.md).

---

## 10. Enumerations

An `enum` gives names to a set of related integer constants, which makes
code easier to read than using plain numbers.

```c
enum day {
    MONDAY,
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
    SATURDAY,
    SUNDAY
};
```

By default, the first name is `0` and each following name is one greater:

```text
MONDAY    = 0
TUESDAY   = 1
WEDNESDAY = 2
THURSDAY  = 3
FRIDAY    = 4
SATURDAY  = 5
SUNDAY    = 6
```

```c
#include <stdio.h>

enum day {
    MONDAY,
    TUESDAY,
    WEDNESDAY,
    THURSDAY,
    FRIDAY,
    SATURDAY,
    SUNDAY
};

int main(void)
{
    enum day today = WEDNESDAY;

    printf("%d\n", today);

    return 0;
}
```

Output:

```text
2
```

You can assign specific values, and later names continue counting up from
the last one given:

```c
enum status {
    OK = 0,
    WARNING = 10,
    ERROR,       // 11
    CRITICAL     // 12
};
```

An `enum` is really just an `int` with named values — it does not add any
runtime safety in C, but it makes the intent of the code far clearer than a
"magic number" would.

---

## 11. `typedef` — Naming Your Own Types

`typedef` creates a new name for an existing type. It does not create a new
type, only an alias.

```c
typedef unsigned char byte;

byte flag = 1;
```

This is especially common with `struct`, so you can drop the `struct`
keyword when declaring variables:

```c
typedef struct {
    bool base;
    bool collector;
    bool emitter;
} Transistor;

Transistor t;
```

Without `typedef`, the same declaration requires the `struct` keyword every
time:

```c
struct transistor t;
```

`typedef` is also used with the fixed-width types you saw earlier —
`uint8_t` and `size_t` are themselves `typedef` names for other, more
verbose, underlying types.

---

## 12. Type Qualifiers: `const` and `volatile`

### `const`

`const` tells the compiler that a value must not be changed after it is
initialized. Attempting to change it is a compile error.

```c
const int max_students = 30;

max_students = 31;  // compile error
```

`const` is used heavily with pointers to protect the data a function only
needs to read. This is covered in the `const` section of
[Pointers](../pointers/POINTERS.md).

### `volatile`

`volatile` tells the compiler that a variable's value can change at any
moment for reasons outside the program's own control — for example, because
it is a hardware register being updated by the outside world. Without
`volatile`, the compiler is allowed to assume the value never changes on its
own and to optimize away repeated reads of it, which would be wrong for a
register.

```c
volatile unsigned char *port = (volatile unsigned char *)0x25;
```

`volatile` matters most once you start reading and writing hardware
registers directly — see [Registers](../registers/REGISTERS.md) and
[Bits and Bitwise Operations](../bits/BITS.md).

---

## 13. Storage-Class Specifiers

A storage-class specifier controls a variable's **lifetime** and
**visibility**, not its type.

| Specifier | Meaning |
|---|---|
| `auto` | The default for local variables; rarely written explicitly |
| `static` | Keeps its value between function calls; or limits visibility to one file |
| `extern` | Refers to a variable defined in another file |
| `register` | A hint to keep the variable in a CPU register for speed (mostly obsolete) |

```c
void counter(void)
{
    static int calls = 0;   // keeps its value between calls

    calls++;

    printf("%d\n", calls);
}
```

Called three times, this prints:

```text
1
2
3
```

A normal (non-`static`) local variable would reset to `0` every time.

---

## Summary: Typical Sizes on a 64-Bit System

Sizes are not guaranteed by the C standard, but these are typical on a
64-bit macOS or Linux system:

| Type | Typical size |
|---|---|
| `char` / `_Bool` | 1 byte |
| `short int` | 2 bytes |
| `int` | 4 bytes |
| `long int` | 8 bytes |
| `long long int` | 8 bytes |
| `float` | 4 bytes |
| `double` | 8 bytes |
| `long double` | 8–16 bytes |
| any pointer (`int *`, `char *`, ...) | 8 bytes |

Always confirm with `sizeof` rather than assuming — that is the whole reason
`sizeof` and `size_t` exist.

---

## Where to Go Next

* [Integers](../integers/INTEGERS.md) — signed vs. unsigned, two's complement
* [char](../char/CHAR.md) — how `char` and `int` relate
* [Strings](../strings/STRINGS.md) — `char` arrays, `size_t`, `string.h`
* [Operators](../operators/OPERATORS.md)
* [Arrays](../arrays/ARRAYS.md)
* [Structs](../structs/STRUCTS.md)
* [Pointers](../pointers/POINTERS.md)
* [Memory](../memory/MEMORY.md)
* [Bits and Bitwise Operations](../bits/BITS.md)
* [Registers](../registers/REGISTERS.md)
* [Printing](../printing/PRINTING.md) — the right format specifier for every type above
