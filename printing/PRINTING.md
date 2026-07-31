````markdown
# Printing Values in C with `printf()`

C uses the `printf()` function to display text and values.

`printf()` is provided by the standard input/output library:

```
#include <stdio.h>
```

A simple program looks like this:

```
#include <stdio.h>

int main(void)
{
    printf("Hello, world!\n");

    return 0;
}
```

Output:

```text
Hello, world!
```

---

# Printing Text

Text that appears between double quotation marks is printed directly:

```c
printf("Hello, Elene!\n");
```

Output:

```text
Hello, Elene!
```

The text inside the quotation marks is called the **format string**.

```c
printf("Hello, Elene!\n");
       // ^^^^^^^^^^^^^^
       // Format string
```

---

# Printing Variables

To print a variable, place a **format specifier** inside the format string.

A format specifier begins with `%`.

For example:

```c
int age = 16;

printf("Age: %d\n", age);
```

Output:

```text
Age: 16
```

In this example:

```text
%d
```

tells `printf()` to print the value as a signed decimal integer.

The variable is supplied after the format string:

```c
printf("Age: %d\n", age);
```

---

# Common `printf()` Format Specifiers

| Format | Used for | Example type |
|---|---|---|
| `%d` | Signed decimal integer | `int` |
| `%i` | Signed decimal integer | `int` |
| `%u` | Unsigned decimal integer | `unsigned int` |
| `%f` | Floating-point number | `double` |
| `%e` | Scientific notation | `double` |
| `%g` | Shorter form of `%f` or `%e` | `double` |
| `%c` | One character | `char` |
| `%s` | A string | `char[]` or `char *` |
| `%x` | Unsigned hexadecimal, lowercase | `unsigned int` |
| `%X` | Unsigned hexadecimal, uppercase | `unsigned int` |
| `%o` | Unsigned octal | `unsigned int` |
| `%p` | Memory address | pointer |
| `%zu` | Unsigned value of type `size_t` | `size_t` |
| `%%` | A literal percent sign | no argument |

---

# `%d` — Signed Decimal Integer

Use `%d` to print an `int` as a normal decimal integer.

```c
int temperature = -5;

printf("%d\n", temperature);
```

Output:

```text
-5
```

Another example:

```c
int age = 16;

printf("Elene is %d years old.\n", age);
```

Output:

```text
Elene is 16 years old.
```

---

# `%i` — Signed Decimal Integer

With `printf()`, `%i` and `%d` do the same thing.

```c
int number = 42;

printf("%d\n", number);
printf("%i\n", number);
```

Output:

```text
42
42
```

Both print a signed `int` in decimal notation.

For `printf()`:

```text
%d and %i behave the same
```

However, `%d` and `%i` behave differently with `scanf()` when reading input.

For beginning programs, `%d` is usually the clearest choice for decimal integers.

---

# `%u` — Unsigned Integer

Use `%u` for an `unsigned int`.

```c
unsigned int count = 250;

printf("%u\n", count);
```

Output:

```text
250
```

An unsigned integer cannot represent negative values.

For a typical 32-bit `unsigned int`, the range is:

```text
0 to 4,294,967,295
```

Use a matching format specifier:

```c
unsigned int number = 100;

printf("%u\n", number);
```

Do not use `%d` for an `unsigned int`.

---

# `%c` — One Character

Use `%c` to print one character.

```c
char letter = 'E';

printf("%c\n", letter);
```

Output:

```text
E
```

Remember:

```c
'E'
```

is one character.

```c
"E"
```

is a string containing:

```text
'E' '\0'
```

You can also print one character from a string:

```c
char name[] = "Elene";

printf("%c\n", name[0]);
```

Output:

```text
E
```

---

# `%s` — A String

Use `%s` to print a null-terminated string.

```c
char name[] = "Elene";

printf("%s\n", name);
```

Output:

```text
Elene
```

The character array must end with `'\0'`.

```text
'E' 'l' 'e' 'n' 'e' '\0'
```

`printf()` starts at the first character and continues until it finds the null terminator.

---

# `%f` — Floating-Point Number

Use `%f` to print a floating-point value.

```c
float temperature = 25.5f;

printf("%f\n", temperature);
```

Output:

```text
25.500000
```

By default, `%f` prints six digits after the decimal point.

You can also print a `double` using `%f`:

```c
double price = 19.95;

printf("%f\n", price);
```

Output:

```text
19.950000
```

When passed to `printf()`, a `float` is automatically promoted to `double`.

Therefore, `%f` is used for both:

```text
float
double
```

---

# Controlling Decimal Places

Place a period and a number between `%` and `f`.

```c
double price = 19.9567;

printf("%.2f\n", price);
```

Output:

```text
19.96
```

The `2` means:

```text
Print two digits after the decimal point
```

Examples:

```c
double value = 3.14159265;

printf("%.0f\n", value);
printf("%.1f\n", value);
printf("%.2f\n", value);
printf("%.4f\n", value);
```

Output:

```text
3
3.1
3.14
3.1416
```

`printf()` rounds the displayed result.

It does not change the value stored in the variable.

---

# `%e` — Scientific Notation

Use `%e` to print a floating-point number using scientific notation.

```c
double distance = 1234567.0;

printf("%e\n", distance);
```

Output:

```text
1.234567e+06
```

The uppercase version uses an uppercase `E`:

```c
printf("%E\n", distance);
```

Output:

```text
1.234567E+06
```

Scientific notation is useful for extremely large or extremely small values.

```c
double tiny = 0.00000125;

printf("%e\n", tiny);
```

Output:

```text
1.250000e-06
```

---

# `%g` — Compact Floating-Point Output

`%g` chooses between normal decimal notation and scientific notation.

It removes unnecessary trailing zeros.

```c
double number = 25.500000;

printf("%g\n", number);
```

Output:

```text
25.5
```

Another example:

```c
double number = 123456789.0;

printf("%g\n", number);
```

Depending on the value, `printf()` may use scientific notation.

The uppercase version is:

```c
%G
```

---

# `%x` — Hexadecimal

Use `%x` to print an unsigned integer in hexadecimal.

```c
unsigned int number = 255;

printf("%x\n", number);
```

Output:

```text
ff
```

Use `%X` for uppercase hexadecimal letters:

```c
printf("%X\n", number);
```

Output:

```text
FF
```

To include the `0x` prefix, use `#`:

```c
printf("%#x\n", number);
```

Output:

```text
0xff
```

Uppercase:

```c
printf("%#X\n", number);
```

Output:

```text
0XFF
```

Hexadecimal is especially useful in embedded programming.

```c
unsigned int register_value = 255;

printf("Register: 0x%02X\n", register_value);
```

Output:

```text
Register: 0xFF
```

---

# `%o` — Octal

Use `%o` to print an unsigned integer in base 8.

```c
unsigned int number = 64;

printf("%o\n", number);
```

Output:

```text
100
```

To include the octal prefix, use `#`:

```c
printf("%#o\n", number);
```

Output:

```text
0100
```

Octal is less common in modern application code, but it still appears in areas such as Unix file permissions.

---

# `%p` — Memory Address

Use `%p` to print a pointer or memory address.

```c
int number = 42;

printf("%p\n", (void *)&number);
```

Possible output:

```text
0x16f3a6abc
```

The exact address changes between computers and program runs.

`&number` means:

```text
the address of number
```

The cast to `void *` is the correct portable type for `%p`:

```c
(void *)&number
```

Example:

```c
char letter = 'A';

printf("Value: %c\n", letter);
printf("Address: %p\n", (void *)&letter);
```

---

# `%zu` — Values of Type `size_t`

Functions such as `strlen()` return a value of type `size_t`.

Use `%zu` to print a `size_t`.

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    char name[] = "Elene";
    size_t length = strlen(name);

    printf("%zu\n", length);

    return 0;
}
```

Output:

```text
5
```

`sizeof` also produces a value of type `size_t`.

```c
int number = 42;

printf("%zu\n", sizeof number);
```

On a typical system, the output might be:

```text
4
```

Use `%zu`, not `%d`, for a `size_t`.

---

# Printing a Percent Sign

A single `%` begins a format specifier.

To print an actual percent sign, use two percent signs:

```c
printf("Battery: 75%%\n");
```

Output:

```text
Battery: 75%
```

No additional argument is required for `%%`.

---

# Printing Multiple Values

A single `printf()` call can contain several format specifiers.

```c
char name[] = "Elene";
int age = 16;
double score = 92.5;

printf("%s is %d years old and scored %.1f.\n",
       name,
       age,
       score);
```

Output:

```text
Elene is 16 years old and scored 92.5.
```

The arguments must appear in the same order as the format specifiers.

```text
%s  matches name
%d  matches age
%f  matches score
```

---

# Format Specifiers Must Match the Arguments

This is correct:

```c
int age = 16;

printf("%d\n", age);
```

This is incorrect:

```c
int age = 16;

printf("%s\n", age);
```

`%s` expects a pointer to a string, but `age` is an integer.

Using the wrong format specifier causes undefined behavior.

A compiler with warnings enabled may report mistakes such as:

```text
format specifies type 'char *' but the argument has type 'int'
```

Useful compiler flags include:

```bash
clang \
    -Wall \
    -Wextra \
    -Wpedantic \
    -std=c17 \
    program.c \
    -o program
```

---

# Field Width

You can specify the minimum number of character positions to use.

```c
int number = 42;

printf("|%5d|\n", number);
```

Output:

```text
|   42|
```

The number is right-aligned in a field that is at least five characters wide.

Examples:

```c
printf("|%3d|\n", 42);
printf("|%5d|\n", 42);
printf("|%8d|\n", 42);
```

Output:

```text
| 42|
|   42|
|      42|
```

Field width does not cut off a value that is too large.

```c
printf("|%3d|\n", 12345);
```

Output:

```text
|12345|
```

---

# Left Alignment

Use `-` to left-align a value.

```c
printf("|%-5d|\n", 42);
```

Output:

```text
|42   |
```

Compare:

```c
printf("|%5d|\n", 42);
printf("|%-5d|\n", 42);
```

Output:

```text
|   42|
|42   |
```

---

# Padding with Zeros

Use `0` before the width to pad a number with zeros.

```c
int number = 42;

printf("%05d\n", number);
```

Output:

```text
00042
```

This is useful for clocks, counters, and binary or hexadecimal displays.

```c
int hours = 9;
int minutes = 5;

printf("%02d:%02d\n", hours, minutes);
```

Output:

```text
09:05
```

For hexadecimal:

```c
unsigned int value = 10;

printf("%02X\n", value);
```

Output:

```text
0A
```

---

# Always Displaying a Sign

Use `+` to display a sign for both positive and negative values.

```c
printf("%+d\n", 5);
printf("%+d\n", -5);
```

Output:

```text
+5
-5
```

This can also be used with floating-point values:

```c
printf("%+.2f\n", 3.5);
```

Output:

```text
+3.50
```

---

# Adding a Space for Positive Values

A space flag leaves one leading space for positive values.

```c
printf("% d\n", 5);
printf("% d\n", -5);
```

Output:

```text
 5
-5
```

This can help align positive and negative numbers.

---

# Precision with Strings

Precision can limit the number of characters printed from a string.

```c
char name[] = "Elene";

printf("%.3s\n", name);
```

Output:

```text
Ele
```

The string itself is not changed.

Only the first three characters are printed.

---

# Width and Precision Together

You can combine field width and decimal precision.

```c
double number = 3.14159265;

printf("|%8.2f|\n", number);
```

Output:

```text
|    3.14|
```

This means:

```text
8    Minimum total field width
2    Digits after the decimal point
```

Left alignment:

```c
printf("|%-8.2f|\n", number);
```

Output:

```text
|3.14    |
```

---

# Length Modifiers

Some integer types require an additional letter before the main format character.

Common length modifiers include:

| Type | Format |
|---|---|
| `short int` | `%hd` |
| `unsigned short int` | `%hu` |
| `long int` | `%ld` |
| `unsigned long int` | `%lu` |
| `long long int` | `%lld` |
| `unsigned long long int` | `%llu` |
| `size_t` | `%zu` |

---

## Printing a `short`

```c
short int number = -100;

printf("%hd\n", number);
```

---

## Printing a `long`

```c
long int population = 1000000L;

printf("%ld\n", population);
```

---

## Printing a `long long`

```c
long long int huge_number = 9000000000LL;

printf("%lld\n", huge_number);
```

---

## Printing Unsigned Long Types

```c
unsigned long int value = 1000000UL;

printf("%lu\n", value);
```

```c
unsigned long long int value = 9000000000ULL;

printf("%llu\n", value);
```

---

# Printing Fixed-Width Integer Types

The `<stdint.h>` header provides integer types with known widths:

```c
#include <stdint.h>
```

Examples include:

```c
int8_t
uint8_t
int16_t
uint16_t
int32_t
uint32_t
int64_t
uint64_t
```

For portable printing, include:

```c
#include <inttypes.h>
```

Then use macros such as:

```c
PRId8
PRIu8
PRId16
PRIu16
PRId32
PRIu32
PRId64
PRIu64
```

Example:

```c
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

int main(void)
{
    int32_t temperature = -25;
    uint32_t counter = 4000000000U;

    printf("%" PRId32 "\n", temperature);
    printf("%" PRIu32 "\n", counter);

    return 0;
}
```

For small fixed-width types such as `uint8_t`, integer promotion occurs when they are passed to `printf()`.

For simple classroom examples, this is often used:

```c
uint8_t value = 255;

printf("%u\n", (unsigned int)value);
```

---

# Printing Binary

Standard C `printf()` does not provide a `%b` format specifier.

This is not standard C:

```c
printf("%b\n", number);
```

To print binary, you can write a loop:

```c
#include <stdio.h>
#include <stdint.h>

void print_binary8(uint8_t value)
{
    for (int bit = 7; bit >= 0; bit--) {
        printf("%u", (unsigned int)((value >> bit) & 1U));
    }
}

int main(void)
{
    uint8_t value = 42;

    print_binary8(value);
    printf("\n");

    return 0;
}
```

Output:

```text
00101010
```

The loop begins with bit 7 and moves toward bit 0.

---

# Escape Sequences

A backslash introduces a special character inside a string.

| Escape sequence | Meaning |
|---|---|
| `\n` | New line |
| `\t` | Horizontal tab |
| `\\` | Backslash |
| `\"` | Double quotation mark |
| `\'` | Single quotation mark |
| `\0` | Null character |
| `\r` | Carriage return |
| `\b` | Backspace |

---

## `\n` — New Line

```c
printf("First line\nSecond line\n");
```

Output:

```text
First line
Second line
```

---

## `\t` — Tab

```c
printf("Name\tAge\n");
printf("Elene\t16\n");
```

Possible output:

```text
Name    Age
Elene   16
```

Tabs move the cursor to the next tab position.

They do not always create exactly the same number of spaces.

---

## `\\` — Backslash

```c
printf("C:\\Users\\Elene\n");
```

Output:

```text
C:\Users\Elene
```

A single backslash begins an escape sequence, so two backslashes are needed to print one.

---

## `\"` — Double Quotation Mark

```c
printf("She said, \"Hello.\"\n");
```

Output:

```text
She said, "Hello."
```

---

## Printing a Table

Field widths can be used to align columns.

```c
#include <stdio.h>

int main(void)
{
    printf("%-10s %5s %8s\n", "Name", "Age", "Score");
    printf("%-10s %5d %8.1f\n", "Elene", 16, 92.5);
    printf("%-10s %5d %8.1f\n", "Ilias", 17, 88.0);

    return 0;
}
```

Output:

```text
Name         Age    Score
Elene         16     92.5
Ilias         17     88.0
```

Explanation:

```text
%-10s   Left-align a string in a field 10 characters wide
%5d     Right-align an integer in a field 5 characters wide
%8.1f   Right-align a number in a field 8 characters wide
         and print one digit after the decimal point
```

---

# `printf()` Return Value

`printf()` returns the number of characters successfully printed.

```c
int result = printf("Hello\n");

printf("Characters printed: %d\n", result);
```

The first call prints six characters:

```text
H e l l o \n
```

Therefore, `result` will normally be:

```text
6
```

A negative return value indicates an output error.

---

# Important Difference Between `printf()` and `scanf()`

The format specifiers used by `printf()` and `scanf()` are similar, but they are not always identical.

For `printf()`:

```c
double value = 3.14;

printf("%f\n", value);
```

For `scanf()`:

```c
double value;

scanf("%lf", &value);
```

With `printf()`:

```text
%f prints a double
```

With `scanf()`:

```text
%f  reads a float
%lf reads a double
```

Also, with `printf()`:

```text
%d and %i both print decimal integers
```

With `scanf()`:

```text
%d reads decimal input
%i detects decimal, octal, or hexadecimal input
```

This page focuses primarily on `printf()`.

---

# Common Mistakes

## Mistake 1: Using `%c` for a string

Incorrect:

```c
char name[] = "Elene";

printf("%c\n", name);
```

`name` is not one character.

Correct:

```c
printf("%s\n", name);
```

To print only the first character:

```c
printf("%c\n", name[0]);
```

---

## Mistake 2: Using `%s` for one character

Incorrect:

```c
char letter = 'E';

printf("%s\n", letter);
```

Correct:

```c
printf("%c\n", letter);
```

---

## Mistake 3: Using `%d` for `size_t`

Incorrect:

```c
printf("%d\n", strlen(name));
```

Correct:

```c
printf("%zu\n", strlen(name));
```

---

## Mistake 4: Forgetting an argument

Incorrect:

```c
printf("Age: %d\n");
```

The format string contains `%d`, but no integer argument was supplied.

Correct:

```c
int age = 16;

printf("Age: %d\n", age);
```

---

## Mistake 5: Supplying arguments in the wrong order

Incorrect:

```c
char name[] = "Elene";
int age = 16;

printf("%s is %d years old.\n", age, name);
```

Correct:

```c
printf("%s is %d years old.\n", name, age);
```

---

## Mistake 6: Using `%b`

Standard C does not define `%b`.

Incorrect:

```c
printf("%b\n", number);
```

Write a binary-printing function instead.

---

# Complete Example

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    char name[] = "Elene";
    char initial = name[0];

    int age = 16;
    unsigned int students = 25;

    double score = 92.567;
    unsigned int register_value = 255;

    printf("Name: %s\n", name);
    printf("Initial: %c\n", initial);
    printf("Age: %d\n", age);
    printf("Students: %u\n", students);
    printf("Score: %.2f\n", score);
    printf("Hexadecimal: 0x%02X\n", register_value);
    printf("Name length: %zu\n", strlen(name));
    printf("Address of age: %p\n", (void *)&age);
    printf("Completion: 100%%\n");

    return 0;
}
```

Possible output:

```text
Name: Elene
Initial: E
Age: 16
Students: 25
Score: 92.57
Hexadecimal: 0xFF
Name length: 5
Address of age: 0x16f123abc
Completion: 100%
```

The memory address will vary.

---

# Summary

A format specifier tells `printf()` how to interpret and display a value.

Common format specifiers include:

```text
%d    signed decimal int
%i    signed decimal int
%u    unsigned int
%f    floating-point value
%e    scientific notation
%g    compact floating-point output
%c    one character
%s    string
%x    lowercase hexadecimal
%X    uppercase hexadecimal
%o    octal
%p    pointer
%zu   size_t
%%    percent sign
```

The format specifier must match the type of the argument.

Examples:

```c
printf("%d\n", age);
printf("%u\n", count);
printf("%.2f\n", price);
printf("%c\n", letter);
printf("%s\n", name);
printf("%zu\n", strlen(name));
printf("%p\n", (void *)&age);
```

Useful formatting options include:

```text
%5d      Minimum width of 5
%-5d     Left-align in a width of 5
%05d     Pad with zeros
%+d      Always show the sign
%.2f     Two digits after the decimal point
%8.2f    Width of 8 and two decimal places
%.3s     Print at most three string characters
%#x      Include the hexadecimal prefix
```

Using compiler warnings helps detect mismatched format specifiers:

```bash
clang \
    -Wall \
    -Wextra \
    -Wpedantic \
    -std=c17 \
    program.c \
    -o program
```
````
