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

## Why Does `11111111` Mean `-1`?

An 8-bit number can store only 8 bits.

Look what happens when we add `1` to `11111111`:

```text
  11111111
+ 00000001
----------
1 00000000

The answer contains 9 bits, but the computer can store only 8.

So it discards the extra bit on the left:

00000000

This means:

11111111 + 1 = 0

Therefore, 11111111 acts like -1, because:

-1 + 1 = 0

That is why an 8-bit signed integer uses:

11111111 = -1

Later, when they understand binary addition well, you can teach the full rule:

> To make a negative number, invert the bits and add `1`.
