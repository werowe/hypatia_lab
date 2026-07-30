# DATA TYPES

## Concepts

Add explanations of the main concepts here.

## Programs

Add a list of the example programs in this folder.

## Compile

```bash
clang -Wall -Wextra -Wpedantic -std=c17 source.c -o program
```

## Run

```bash
./program
```

## int


```
## Signed and Unsigned 8-Bit Integers

For an **8-bit integer**:

* An unsigned integer ranges from **0 to 255**
* A signed integer ranges from **-128 to 127**

### Unsigned Integers

With an unsigned integer, all 8 bits represent the value.

```text
11111111
```

This equals:

```text
2^7 + 2^6 + 2^5 + 2^4 + 2^3 + 2^2 + 2^1 + 2^0
```

```text
128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 = 255
```

Therefore, the largest unsigned 8-bit integer is:

```text
11111111 = 255
```

### Signed Integers

Modern computers normally represent signed integers using **two's complement**.

The first bit indicates whether the number is non-negative or negative:

```text
0xxxxxxx = non-negative
1xxxxxxx = negative
```

Therefore:

* A leading `0` means the number is non-negative.
* A leading `1` means the number is negative.

For example:

```text
01111111
```

This equals:

```text
64 + 32 + 16 + 8 + 4 + 2 + 1 = 127
```

Therefore:

```text
01111111 = 127
```

Some important signed 8-bit values are:

```text
00000000 = 0
00000001 = 1
01111111 = 127
11111111 = -1
10000000 = -128
```

The signed range is:

```text
-128 to 127
```

There are:

* 128 negative values: `-128` through `-1`
* 128 non-negative values: `0` through `127`

The range is not `-127` to `127` because zero also requires its own bit pattern.

```c
// An 8-bit unsigned integer ranges from 0 to 255.
//
// An 8-bit signed integer using two's complement
// ranges from -128 to 127.
//
// In a signed value, a leading 0 indicates a
// non-negative number, while a leading 1
// indicates a negative number.
```

```


## Why `11111111` Means `-1`

Yes—this is similar to **9's complement or 10's complement subtraction** in decimal.

Two's complement allows a computer to perform subtraction by using addition and then discarding the extra overflow bit.

For an 8-bit number, arithmetic wraps around at:

```text
2^8 = 256

The bit pattern for -1 is the value that becomes zero when you add 1 and discard anything beyond 8 bits:

  11111111
+ 00000001
----------
1 00000000

An 8-bit register can store only 8 bits, so the extra bit on the left is discarded:

00000000

Therefore:

11111111 + 1 = 00000000

This means that 11111111 behaves like -1.

Signed and Unsigned Interpretations

The same bits can have different meanings depending on whether the number is signed or unsigned:

11111111 = 255   unsigned
11111111 = -1    signed two's complement

The bits do not change. Only their interpretation changes.

Modular Arithmetic Explanation

In 8-bit arithmetic:

-1 ≡ 255 (mod 256)

This is because:

-1 + 256 = 255

Since 8-bit arithmetic wraps around after 255, the values -1 and 255 use the same bit pattern.

Creating -1 Using Two's Complement

Start with positive 1:

00000001

Invert every bit:

11111110

Then add 1:

  11111110
+ 00000001
----------
  11111111

Therefore:

-1 = 11111111
Subtraction Using Addition

To calculate:

5 - 1

the computer can instead calculate:

5 + (-1)

In binary:

  00000101    5
+ 11111111   -1
-----------
1 00000100

Discard the extra carry bit:

00000100

This equals:

4

So:

5 + (-1) = 4

Two's complement lets the computer perform subtraction using the same circuitry it uses for addition.



## double 
is floating point number



## Strings and Char

