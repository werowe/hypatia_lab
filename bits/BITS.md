# BITS AND BITWISE OPERATIONS

Every value in a computer is stored as bits — `0`s and `1`s. Most of the
time you don't think about this: `int total = 5 + 3;` just works. But when
you're programming close to the hardware — reading a sensor's raw output,
packing several flags into one byte, or controlling a microcontroller's
pins directly — you need to work with individual bits.

For a refresher on how a number is actually represented in binary, and why
`11111111` means `-1` in a signed 8-bit integer, see
[Integers](../integers/INTEGERS.md).

---

## 1. The Bitwise Operators

| Operator | Name | What it does |
|---|---|---|
| `&` | AND | `1` only where **both** bits are `1` |
| `\|` | OR | `1` where **either** bit is `1` |
| `^` | XOR | `1` where the bits are **different** |
| `~` | NOT | flips every bit |
| `<<` | Left shift | moves bits left, filling with `0` |
| `>>` | Right shift | moves bits right |

Do not confuse these with the *logical* operators `&&`, `||`, `!` from
[Operators](../operators/OPERATORS.md) — those work on whole `true`/`false`
values, while `&`, `|`, `^`, `~` work on individual bits.

---

## 2. `&` — Bitwise AND

Compares two numbers one bit at a time. A result bit is `1` only when
**both** input bits are `1`.

```text
  1100
& 1010
------
  1000
```

```c
#include <stdio.h>

int main(void)
{
    unsigned int x = 0b1100;   // 12
    unsigned int y = 0b1010;   // 10

    printf("%u\n", x & y);     // 8  (0b1000)

    return 0;
}
```

`&` is commonly used with a **mask** to check or isolate specific bits. For
example, to keep only the lowest 7 bits of a number (limiting it to the
range `0`–`127`, the range of standard ASCII):

```c
int n = 257;             // 0b1_0000_0001
n = n & 0177;             // 0177 in octal = 127 decimal = 0b0111_1111

printf("%d\n", n);        // 1
```

---

## 3. `|` — Bitwise OR

A result bit is `1` if **either** input bit is `1`. This is the classic
way to **turn on** specific bits without disturbing the others.

```text
  1100
| 1010
------
  1110
```

```c
unsigned int x = 0b0100;
unsigned int y = 0b0011;

x = x | y;   // 0b0111
```

A common real use: turning on one pin of a hardware register while leaving
every other pin exactly as it was. See [Registers](../registers/REGISTERS.md).

---

## 4. `^` — Bitwise XOR

A result bit is `1` only when the two input bits are **different**.

```text
  1100
^ 1010
------
  0110
```

XOR has a useful property: applying the same value twice cancels out,
which makes it handy for **toggling** a bit (flip it on if it's off, off if
it's on):

```c
unsigned int state = 0b0001;

state = state ^ 0b0001;   // 0b0000 — turned off
state = state ^ 0b0001;   // 0b0001 — turned back on
```

---

## 5. `~` — Bitwise NOT

Flips every bit: every `0` becomes `1`, and every `1` becomes `0`.

```c
unsigned char x = 0b00001111;

printf("%u\n", (unsigned char)~x);   // 0b11110000 = 240
```

`~` is most often used to build a mask for **clearing** specific bits — see
section 7 below.

---

## 6. `<<` and `>>` — Shifting

`<<` shifts every bit to the left, filling the new bits on the right with
`0`. Each left shift by 1 doubles the value (as long as nothing overflows).

```c
unsigned int x = 1;

printf("%u\n", x << 1);   // 2
printf("%u\n", x << 3);   // 8
```

`>>` shifts every bit to the right. Each right shift by 1 halves the value
(dropping any remainder).

```c
unsigned int x = 8;

printf("%u\n", x >> 1);   // 4
printf("%u\n", x >> 3);   // 1
```

`<<` and `>>` are also how a bit at a specific position gets built, which
is used constantly with masks:

```c
unsigned int mask = 1u << 3;   // 0b00001000 — a mask for "bit 3"
```

---

## 7. Setting, Clearing, Toggling, and Checking One Bit

These four operations come up so often in embedded programming that it's
worth memorizing the pattern. Let `n` be the bit position, counting from 0
on the right.

```c
value |=  (1u << n);   // SET bit n to 1
value &= ~(1u << n);   // CLEAR bit n to 0
value ^=  (1u << n);   // TOGGLE bit n
bit    =  (value >> n) & 1u;   // CHECK bit n (0 or 1)
```

```c
#include <stdio.h>

int main(void)
{
    unsigned int value = 0;

    value |= (1u << 3);              // set bit 3
    printf("%u\n", value);           // 8

    value &= ~(1u << 3);             // clear bit 3
    printf("%u\n", value);           // 0

    value ^= (1u << 3);              // toggle bit 3
    printf("%u\n", value);           // 8

    unsigned int bit = (value >> 3) & 1u;
    printf("%u\n", bit);             // 1

    return 0;
}
```

This exact pattern is how Arduino code — and the microcontroller's own
internal registers — turn individual pins on and off. See
[Registers](../registers/REGISTERS.md).

---

## 8. Printing a Number in Binary

C's `printf()` has no `%b` format specifier (see
[Printing](../printing/PRINTING.md)), so printing binary means writing a
small loop that checks one bit at a time, from the highest bit down to the
lowest:

```c
#include <stdio.h>
#include <limits.h>

void print_bits(unsigned int value)
{
    int bits = sizeof(value) * CHAR_BIT;   // number of bits in the type

    for (int i = bits - 1; i >= 0; i--) {
        unsigned int bit = (value >> i) & 1u;
        printf("%u", bit);
    }

    printf("\n");
}

int main(void)
{
    print_bits(12);

    return 0;
}
```

Output (on a system where `unsigned int` is 32 bits):

```text
00000000000000000000000000001100
```

This exact `print_bits()` function is used in
[`snippets/bit_shift.c`](../snippets/bit_shift.c) — see
[Snippets](../snippets/SNIPPETS.md) for the full program.

---

## 9. Why This Matters for Hardware

A microcontroller doesn't give you a friendly `bool` for each pin — it
gives you one register, an integer where each individual bit controls or
reports the state of one physical pin. `digitalWrite(13, HIGH)` in Arduino
is a convenient wrapper around exactly the kind of bit-setting shown above.
See [Registers](../registers/REGISTERS.md) for how to do it directly.

---

## Summary

```text
&    AND    keep bits that are 1 in both
|    OR     turn bits on
^    XOR    toggle bits
~    NOT    flip every bit
<<   shift left   multiply by 2 per shift
>>   shift right  divide by 2 per shift

value |=  (1u << n);   set bit n
value &= ~(1u << n);   clear bit n
value ^=  (1u << n);   toggle bit n
(value >> n) & 1u      read bit n
```

---

## Programs

This folder doesn't have its own example `.c` file yet. See
[`snippets/bit_shift.c`](../snippets/bit_shift.c), described in
[Snippets](../snippets/SNIPPETS.md), for a working program that
demonstrates `&`, `|`, and `print_bits()` together.

## Compile

```bash
clang -Wall -Wextra -Wpedantic -std=c17 bits.c -o bits
```

## Run

```bash
./bits
```
