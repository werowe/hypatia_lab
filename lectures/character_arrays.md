# Class 3: Character Arrays in C

In the previous class, we stored text like this:

```c
char name[] = "Anna";
```

We called this text a string.

In this class, we will look inside the string and see how C stores its characters.

---

## An array stores several values

An array is a group of values stored together.

This is a character array:

```c
char name[] = "Anna";
```

The variable `name` contains several characters.

We can imagine it like this:

| Position | Character |
|---:|:---:|
| 0 | A |
| 1 | n |
| 2 | n |
| 3 | a |

Each character has a numbered position.

The first position is `0`, not `1`.

---

## Printing the entire string

Create a file named:

```text
character_arrays.c
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

The `%s` prints the entire string.

---

## Reading one character

We use square brackets to select one character.

```c
#include <stdio.h>

int main(void)
{
    char name[] = "Anna";

    printf("%c\n", name[0]);

    return 0;
}
```

The output is:

```text
A
```

This expression:

```c
name[0]
```

means:

> Get the character at position 0 in `name`.

Because we selected one character, we print it with `%c`.

---

## Reading every character

```c
#include <stdio.h>

int main(void)
{
    char name[] = "Anna";

    printf("%c\n", name[0]);
    printf("%c\n", name[1]);
    printf("%c\n", name[2]);
    printf("%c\n", name[3]);

    return 0;
}
```

The output is:

```text
A
n
n
a
```

---

## Array positions

Consider this character array:

```c
char word[] = "Arduino";
```

The positions are:

| Position | Character |
|---:|:---:|
| 0 | A |
| 1 | r |
| 2 | d |
| 3 | u |
| 4 | i |
| 5 | n |
| 6 | o |

Examples:

```c
printf("%c\n", word[0]);
printf("%c\n", word[3]);
printf("%c\n", word[6]);
```

The output is:

```text
A
u
o
```

---

## Printing the position and character

We can print the position beside each character:

```c
#include <stdio.h>

int main(void)
{
    char word[] = "Arduino";

    printf("Position 0: %c\n", word[0]);
    printf("Position 1: %c\n", word[1]);
    printf("Position 2: %c\n", word[2]);
    printf("Position 3: %c\n", word[3]);
    printf("Position 4: %c\n", word[4]);
    printf("Position 5: %c\n", word[5]);
    printf("Position 6: %c\n", word[6]);

    return 0;
}
```

---

## Changing one character

We can change a character at a particular position.

```c
#include <stdio.h>

int main(void)
{
    char word[] = "cat";

    printf("Before: %s\n", word);

    word[0] = 'h';

    printf("After: %s\n", word);

    return 0;
}
```

The output is:

```text
Before: cat
After: hat
```

This line:

```c
word[0] = 'h';
```

changes the character at position `0`.

It does not replace the entire array. It changes only one character.

---

## Another example

```c
#include <stdio.h>

int main(void)
{
    char word[] = "car";

    word[2] = 't';

    printf("%s\n", word);

    return 0;
}
```

The output is:

```text
cat
```

The original characters were:

| Position | Character |
|---:|:---:|
| 0 | c |
| 1 | a |
| 2 | r |

We replaced the character at position `2`.

---

## Why it is called a character array

Look at this code:

```c
char name[] = "Anna";
```

It is called a **character array** because it contains several `char` values.

The visible characters are:

```text
A
n
n
a
```

Together, these characters form the string `"Anna"`.

Therefore:

> A string in C is text stored in a character array.

---

## The invisible ending character

C needs to know where a string ends.

It places a special invisible character after the final visible character.

It is written:

```c
'\0'
```

This special character tells C:

> The string ends here.

The word `"cat"` is stored like this:

| Position | Character |
|---:|:---:|
| 0 | c |
| 1 | a |
| 2 | t |
| 3 | `'\0'` |

The final character is not the number zero.

It is a special character that marks the end of the string.

---

## Two ways to create the same string

The normal and easiest way is:

```c
char word[] = "cat";
```

C automatically adds the invisible ending character.

We could also write every character:

```c
char word[] = {'c', 'a', 't', '\0'};
```

Both instructions create the same string.

Normally, we use:

```c
char word[] = "cat";
```

---

## Printing characters with a loop

A loop can print one character at a time.

```c
#include <stdio.h>

int main(void)
{
    char word[] = "Hello";
    int position = 0;

    while (word[position] != '\0')
    {
        printf("%c\n", word[position]);

        position++;
    }

    return 0;
}
```

The output is:

```text
H
e
l
l
o
```

---

## Understanding the loop

We begin at position `0`:

```c
int position = 0;
```

This is the loop condition:

```c
word[position] != '\0'
```

It means:

> Continue while the current character is not the end of the string.

This line moves to the next position:

```c
position++;
```

When the program reaches `'\0'`, the loop stops.

---

## Printing positions with a loop

```c
#include <stdio.h>

int main(void)
{
    char word[] = "Hello";
    int position = 0;

    while (word[position] != '\0')
    {
        printf("Position %d: %c\n", position, word[position]);

        position++;
    }

    return 0;
}
```

The output is:

```text
Position 0: H
Position 1: e
Position 2: l
Position 3: l
Position 4: o
```

This `printf()` instruction prints two variables:

```c
printf("Position %d: %c\n", position, word[position]);
```

The `%d` prints the integer `position`.

The `%c` prints one character from the array.

---

## Complete example

```c
#include <stdio.h>

int main(void)
{
    char studentName[] = "Olena";
    int studentAge = 15;

    printf("Student: %s\n", studentName);
    printf("First character: %c\n", studentName[0]);
    printf("Age: %d\n", studentAge);

    return 0;
}
```

---

## Exercise 1

Create this character array:

```c
char city[] = "Kyiv";
```

Print the entire word using `%s`.

Then print each character separately:

```c
city[0]
city[1]
city[2]
city[3]
```

Use `%c` to print each character.

---

## Exercise 2

Create this character array:

```c
char word[] = "dog";
```

Change one character so the program prints:

```text
dig
```

Which position must you change?

---

## Exercise 3

Start with:

```c
char word[] = "hat";
```

Change it to:

```text
hot
```

Change only one character.

---

## Exercise 4

Consider this array:

```c
char word[] = "Computer";
```

Answer these questions before running the program:

1. What is stored at `word[0]`?
2. What is stored at `word[2]`?
3. What is stored at `word[5]`?
4. At which position is the invisible `'\0'`?

---

## Exercise 5

Write a loop that prints every character in your name on a separate line.

Start with:

```c
char name[] = "YourName";
int position = 0;
```

Continue until the program reaches:

```c
'\0'
```

---

## Exercise 6

Change this program so it prints the position beside every character:

```c
#include <stdio.h>

int main(void)
{
    char word[] = "Programming";
    int position = 0;

    while (word[position] != '\0')
    {
        // Print the position and character here.

        position++;
    }

    return 0;
}
```

---

## Summary

In this class, we learned:

- An array stores several values together.
- A character array stores several characters.
- Array positions begin at `0`.
- Square brackets select one character.
- We can change an individual character.
- A string in C is text stored in a character array.
- C uses `'\0'` to mark the end of a string.
- A loop can process a string one character at a time.

Example:

```c
char name[] = "Anna";
```

C stores:

```text
Position 0: A
Position 1: n
Position 2: n
Position 3: a
Position 4: '\0'
```

The invisible `'\0'` tells C where the string ends.
