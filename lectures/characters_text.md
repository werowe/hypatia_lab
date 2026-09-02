# Class 2: Characters and Strings in C

In the previous class, we used `int` to store whole numbers.

```c
int age = 15;
```

Programs also need to store letters, symbols, words, and sentences.

In this class, we will learn how C stores characters and text.

---

## One character

A character is one letter, digit, punctuation mark, or symbol.

Examples include:

```text
A
b
7
?
!
```

In C, we use the `char` data type to store one character.

```c
char grade = 'A';
```

This creates a variable with:

- Data type: `char`
- Name: `grade`
- Value: `'A'`

A single character uses **single quotation marks**:

```c
'A'
```

---

## Printing a character

Create a file named:

```text
characters.c
```

Enter this program:

```c
#include <stdio.h>

int main(void)
{
    char grade = 'A';

    printf("%c\n", grade);

    return 0;
}
```

The output is:

```text
A
```

The `%c` tells `printf()` to print one character.

---

## Printing text and a character

```c
#include <stdio.h>

int main(void)
{
    char grade = 'A';

    printf("Grade: %c\n", grade);

    return 0;
}
```

The output is:

```text
Grade: A
```

The `%c` is replaced by the value of `grade`.

---

## More character examples

```c
char firstLetter = 'H';
char answer = 'Y';
char symbol = '?';
char digit = '7';
```

Each variable stores exactly one character.

Notice this example:

```c
char digit = '7';
```

It stores the character `'7'`.

It does not store the integer `7`.

Compare these variables:

```c
int number = 7;
char digit = '7';
```

The first variable stores a number.

The second variable stores a character.

---

## Changing a character

The value of a character variable can change.

```c
#include <stdio.h>

int main(void)
{
    char answer = 'N';

    printf("First answer: %c\n", answer);

    answer = 'Y';

    printf("Second answer: %c\n", answer);

    return 0;
}
```

The output is:

```text
First answer: N
Second answer: Y
```

---

## Words and sentences

A `char` variable stores only one character.

This is correct:

```c
char letter = 'A';
```

This is not correct:

```c
char name = 'Anna';
```

`Anna` contains four characters, not one.

To store text, we can write:

```c
char name[] = "Anna";
```

Text uses **double quotation marks**:

```c
"Anna"
```

---

## Single and double quotation marks

This is an important rule:

```c
char letter = 'A';
char name[] = "Anna";
```

Use:

- Single quotation marks for one character: `'A'`
- Double quotation marks for text: `"Anna"`

Another example:

```c
char answer = 'Y';
char message[] = "Yes";
```

---

## Printing a string

Text stored in C is called a **string**.

Create a file named:

```text
strings.c
```

Enter this program:

```c
#include <stdio.h>

int main(void)
{
    char name[] = "Anna";

    printf("%s\n", name);

    return 0;
}
```

The output is:

```text
Anna
```

The `%s` tells `printf()` to print a string.

---

## Printing text before a string

```c
#include <stdio.h>

int main(void)
{
    char name[] = "Anna";

    printf("Name: %s\n", name);

    return 0;
}
```

The output is:

```text
Name: Anna
```

The `%s` is replaced by the text stored in `name`.

---

## Three data types

This program uses integers, characters, and strings:

```c
#include <stdio.h>

int main(void)
{
    char studentName[] = "Anna";
    int studentAge = 14;
    char studentGroup = 'A';

    printf("Name: %s\n", studentName);
    printf("Age: %d\n", studentAge);
    printf("Group: %c\n", studentGroup);

    return 0;
}
```

The output is:

```text
Name: Anna
Age: 14
Group: A
```

The program uses three kinds of information:

| Information | Example |
|---|---|
| Whole number | `int studentAge = 14;` |
| One character | `char studentGroup = 'A';` |
| Text | `char studentName[] = "Anna";` |

It also uses three different `printf()` markers:

| Marker | Prints |
|---|---|
| `%d` | An integer |
| `%c` | One character |
| `%s` | A string |

---

## Numbers and text are different

This stores an integer:

```c
int value = 10;
```

It can be used in a calculation:

```c
value = value + 5;
```

This stores text:

```c
char word[] = "10";
```

The characters `"10"` look like a number, but C treats them as text.

---

## Example: Student information

```c
#include <stdio.h>

int main(void)
{
    char name[] = "Danylo";
    int age = 15;
    char group = 'B';

    printf("Student information\n");
    printf("-------------------\n");

    printf("Name: %s\n", name);
    printf("Age: %d\n", age);
    printf("Group: %c\n", group);

    return 0;
}
```

Change the values so the program prints your information.

---

## Exercise 1

Create a character variable named `firstLetter`.

Store the first letter of your name and print it.

Example:

```c
char firstLetter = 'A';
```

Use `%c` to print it.

---

## Exercise 2

Create a variable named `name` that stores your name.

Example:

```c
char name[] = "Anna";
```

Use `%s` to print it.

---

## Exercise 3

Create these three variables:

```text
name
age
group
```

Use:

- A string for the name
- An integer for the age
- One character for the group

Print all three values.

---

## Exercise 4

Which lines are correct?

```c
char letter = 'B';
char letter = "B";
char name[] = "Bohdan";
int age = 15;
int age = "15";
```

Explain why each incorrect line is wrong.

---

## Exercise 5

Correct the mistakes:

```c
char grade = "A";
char studentName = 'Olena';
int age = "14";
```

---

## Exercise 6

Complete the `printf()` instructions:

```c
#include <stdio.h>

int main(void)
{
    char name[] = "Olena";
    int age = 14;
    char group = 'B';

    printf("Name: ___\n", name);
    printf("Age: ___\n", age);
    printf("Group: ___\n", group);

    return 0;
}
```

Replace each blank with `%s`, `%d`, or `%c`.

---

## Summary

In this class, we learned:

- `int` stores a whole number.
- `char` stores one character.
- One character uses single quotation marks.
- A string stores text.
- A string uses double quotation marks.
- `%d` prints an integer.
- `%c` prints one character.
- `%s` prints a string.

Examples:

```c
int age = 15;
char grade = 'A';
char name[] = "Anna";
```

In the next class, we will look inside a string and see how its characters are stored.
