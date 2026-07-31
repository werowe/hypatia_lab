## How `char` and `int` Are Related in C

`char` and `int` are not exactly the same type, but both are **integer types** in C.

A `char` stores a small integer value. We often interpret that value as a character.

```c
char letter = 'A';

Internally, 'A' is stored as a number. On systems using ASCII:

'A' = 65

So these are closely related:

char letter = 'A';
int number = letter;

printf("%c\n", letter);  // A
printf("%d\n", letter);  // 65
printf("%d\n", number);  // 65

The same value can be printed in different ways:

%c interprets the value as a character.
%d interprets the value as an integer.

For example:

char letter = 66;

printf("%c\n", letter);  // B
printf("%d\n", letter);  // 66
The Main Difference Is Size

A char is exactly one byte:

sizeof(char) == 1

An int is usually larger, commonly four bytes:

sizeof(int) == 4

The exact size of int depends on the computer and compiler.

A typical system might have:

char:  8 bits
int:  32 bits

So a char can hold a much smaller range of numbers than an int.

Character Literals Are Integers

An important detail in C is that a character literal such as:

'A'

has type int, not char.

So:

printf("%zu\n", sizeof('A'));

will commonly print:

4

because 'A' is an int value representing the character code for A.

It can still be stored in a char:

char letter = 'A';

because the value 65 fits inside a char.

Automatic Promotion

When a char is used in an arithmetic expression, C usually promotes it to int.

char letter = 'A';

int result = letter + 1;

printf("%c\n", result);  // B
printf("%d\n", result);  // 66

C effectively treats this as:

65 + 1 = 66
A Useful Way to Explain It

A char is a small integer that is often used to store a character code.

So:

char letter = 'A';

does not store a drawing of the letter A. It stores the numerical code associated with A.
