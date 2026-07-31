# STRINGS

# Strings in C

C does not have a built-in `string` data type.

Instead, a string is stored as an **array of characters**.

For example:

```c
char name[] = "Elene";
```

The array contains:

```text
'E' 'l' 'e' 'n' 'e' '\0'
```

The final character, `'\0'`, is called the **null terminator**.

It tells C where the string ends.

---

## A Character Versus a String

A single character is stored using `char` and single quotation marks:

```c
char letter = 'E';
```

A string uses an array of characters and double quotation marks:

```c
char name[] = "Elene";
```

These are different:

```c
'E'     // One character
"Elene" // A string
```

This is also a string:

```c
"E"
```

It contains two values:

```text
'E' '\0'
```

---

## How Much Space Does a String Need?

The word `"Elene"` contains five visible characters:

```text
E l e n e
```

However, C also needs space for the null terminator:

```text
E l e n e \0
```

Therefore, the array requires six elements:

```c
char name[6] = "Elene";
```

You can also let the compiler calculate the size:

```c
char name[] = "Elene";
```

This is usually the simplest option when the string is known at the time of declaration.

---

## Printing a String

Use `%s` to print a string:

```c
#include <stdio.h>

int main(void)
{
    char name[] = "Elene";

    printf("%s\n", name);

    return 0;
}
```

Output:

```text
Elene
```

Use `%c` to print one character:

```c
printf("%c\n", name[0]);
```

Output:

```text
E
```

---

## Accessing Individual Characters

A string is an array, so its characters can be accessed using indexes.

Indexes begin at zero:

```text
Index:       0   1   2   3   4    5
Character:  'E' 'l' 'e' 'n' 'e' '\0'
```

Example:

```c
char name[] = "Elene";

printf("%c\n", name[0]); // E
printf("%c\n", name[1]); // l
printf("%c\n", name[4]); // e
```

---

## Changing Individual Characters

You can change characters by assigning values to individual array elements:

```c
char name[] = "Elene";

name[0] = 'A';

printf("%s\n", name);
```

Output:

```text
Alene
```

Remember that individual characters use single quotation marks:

```c
name[0] = 'E';  // Correct
```

This is incorrect:

```c
name[0] = "E";  // Incorrect
```

`'E'` is one character.

`"E"` is a string containing `'E'` and `'\0'`.

---

## Building a String One Character at a Time

You can write each element individually:

```c
char name[6];

name[0] = 'E';
name[1] = 'l';
name[2] = 'e';
name[3] = 'n';
name[4] = 'e';
name[5] = '\0';
```

The null terminator is essential.

Without it, functions such as `printf()` do not know where the string ends.

```c
printf("%s\n", name);
```

---

# The `string.h` Header

The standard C library provides useful string functions in:

```c
#include <string.h>
```

Some commonly used functions are:

```text
strlen()   Find the length of a string
strcpy()   Copy one string into another
strcmp()   Compare two strings
strcat()   Join two strings
```

These functions work with null-terminated character arrays.

---

## `strlen()` — Find the Length

`strlen()` returns the number of visible characters in a string.

It does not count the null terminator.

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    char name[] = "Elene";

    printf("%zu\n", strlen(name));

    return 0;
}
```

Output:

```text
5
```

Although the array contains six elements, `strlen()` returns five:

```text
'E' 'l' 'e' 'n' 'e' '\0'
```

The return type of `strlen()` is `size_t`.

Therefore, use `%zu` when printing its result:

```c
printf("%zu\n", strlen(name));
```

`%zu` means strlen(name) is size_t.  

>  **size_t**
>
> `size_t` is iand unsigned integer.  We use size_t instead of int because the size of varies by the platform.  And you
> want your code to work on all platforms.  On an 8 bit microcontroller, the size of an integer is 8 bits.  On a 64 bit
> CPU is it 32 or 64 bits.  


> **type safe** 
>
> the `printf` function is not type safe.  We an illustrate this like this:
> 
> #include <stdio.h>
>
> int main(void) {
>    size_t big_number = 9999999999;  // needs 64 bits
>    printf("%d\n", big_number);      // told it to expect a 32-bit int
>    return 0;
>}
> 
> This compiles. No error. But it's wrong: printf reads only 4 bytes off the argument (because %d means "int"), while big_number actually occupies 8 bytes. The output will be garbage — some truncated, essentially random-looking numbe
---

## Looping Through a String

You can use `strlen()` in a loop:

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    char name[] = "Elene";
    size_t length = strlen(name);

    for (size_t i = 0; i < length; i++) {
        printf("%c\n", name[i]);
    }

    return 0;
}
```

Output:

```text
E
l
e
n
e
```

It is better to calculate the length once:

```c
size_t length = strlen(name);
```

rather than repeatedly calling `strlen()` inside the loop.

You can also loop until the null terminator:

```c
for (size_t i = 0; name[i] != '\0'; i++) {
    printf("%c\n", name[i]);
}
```

---

## `strcpy()` — Copy a String

An array cannot be assigned a new string using `=` after it has been declared.

This is incorrect:

```c
char name[20];

name = "Elene";
```

Instead, use `strcpy()`:

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    char name[20];

    strcpy(name, "Elene");

    printf("%s\n", name);

    return 0;
}
```

`strcpy()` copies the characters and the null terminator into the destination array.

The destination must be large enough.

This is dangerous:

```c
char name[4];

strcpy(name, "Elene");
```

The array has only four elements, but `"Elene"` requires six.

Writing beyond the end of an array causes undefined behavior.

---

## A Safer Way to Copy a String

For simple formatted copying, `snprintf()` can limit the number of characters written:

```c
#include <stdio.h>

int main(void)
{
    char name[10];

    snprintf(name, sizeof name, "%s", "Elene");

    printf("%s\n", name);

    return 0;
}
```

`sizeof name` gives the total size of the array.

`snprintf()` will not write more than that amount.

---

## `strcmp()` — Compare Two Strings

You cannot reliably compare strings using `==`.

This does not compare the characters:

```c
if (name1 == name2) {
    // Incorrect string comparison
}
```

For character arrays, `==` compares addresses, not the contents of the strings.

Use `strcmp()` instead:

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    char name1[] = "Elene";
    char name2[] = "Elene";

    if (strcmp(name1, name2) == 0) {
        printf("The strings are equal.\n");
    }

    return 0;
}
```

`strcmp()` returns:

```text
0               The strings are equal
Less than 0     The first string comes before the second
Greater than 0  The first string comes after the second
```

Example:

```c
if (strcmp(name, "Elene") == 0) {
    printf("Hello, Elene!\n");
}
```

---

## `strcat()` — Join Strings

`strcat()` adds one string to the end of another.

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    char message[30] = "Hello, ";

    strcat(message, "Elene");

    printf("%s\n", message);

    return 0;
}
```

Output:

```text
Hello, Elene
```

The destination array must have enough unused space for:

- the original string;
- the added string;
- the final null terminator.

This would be too small:

```c
char message[8] = "Hello, ";

strcat(message, "Elene");
```

---

## Reading a String with `fgets()`

You can read a string from the keyboard using `fgets()`:

```c
#include <stdio.h>

int main(void)
{
    char name[20];

    printf("Enter your name: ");

    if (fgets(name, sizeof name, stdin) == NULL) {
        printf("Input error.\n");
        return 1;
    }

    printf("Hello, %s", name);

    return 0;
}
```

`fgets()` reads at most:

```text
array size - 1
```

characters.

It reserves the final element for `'\0'`.

Unlike `scanf("%s", name)`, `fgets()` can also read spaces.

For example:

```text
Elene Menabde
```

---

## Removing the Newline Added by `fgets()`

When the user presses Enter, `fgets()` usually stores the newline character:

```text
'E' 'l' 'e' 'n' 'e' '\n' '\0'
```

You can remove it using `strcspn()` from `string.h`:

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    char name[20];

    printf("Enter your name: ");

    if (fgets(name, sizeof name, stdin) == NULL) {
        return 1;
    }

    name[strcspn(name, "\n")] = '\0';

    printf("Hello, %s!\n", name);

    return 0;
}
```

This line finds the newline and replaces it with the null terminator:

```c
name[strcspn(name, "\n")] = '\0';
```

---

## Strings and Pointers

When an array is passed to a function, it is normally treated as a pointer to its first element.

```c
char name[] = "Elene";
```

In many expressions, `name` refers to the address of:

```c
name[0]
```

These values refer to the same location:

```c
name
&name[0]
```

That is why `%s` expects a pointer to the first character of a null-terminated string:

```c
printf("%s\n", name);
```

---

## A String Stored Using `malloc()`

When the required size is decided while the program is running, memory can be allocated dynamically.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    size_t size = 20;

    char *name = malloc(size * sizeof *name);

    if (name == NULL) {
        fprintf(stderr, "Memory allocation failed.\n");
        return 1;
    }

    strcpy(name, "Elene");

    printf("%s\n", name);

    free(name);

    return 0;
}
```

`malloc()` creates the storage.

`name` points to the first character in that storage.

The memory must later be released with:

```c
free(name);
```

For beginners, fixed-size arrays are usually easier:

```c
char name[20];
```

Dynamic memory is more useful when the required size is not known until runtime.

---

## Important Rules

### Rule 1: A C string is a character array

```c
char name[] = "Elene";
```

### Rule 2: A string must end with `'\0'`

```text
'E' 'l' 'e' 'n' 'e' '\0'
```

### Rule 3: Use single quotes for one character

```c
char letter = 'E';
```

### Rule 4: Use double quotes for a string

```c
char name[] = "Elene";
```

### Rule 5: Leave space for the null terminator

```c
char name[6] = "Elene";
```

### Rule 6: Use `%c` for one character

```c
printf("%c\n", name[0]);
```

### Rule 7: Use `%s` for a string

```c
printf("%s\n", name);
```

### Rule 8: Use `strcmp()` to compare strings

```c
strcmp(name1, name2)
```

### Rule 9: Make sure destination arrays are large enough

Functions such as `strcpy()` and `strcat()` do not automatically enlarge arrays.

---

## Complete Example

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    char first_name[20];
    char message[40] = "Hello, ";

    printf("Enter your first name: ");

    if (fgets(first_name, sizeof first_name, stdin) == NULL) {
        fprintf(stderr, "Could not read input.\n");
        return 1;
    }

    first_name[strcspn(first_name, "\n")] = '\0';

    strcat(message, first_name);

    printf("%s\n", message);
    printf("Your name contains %zu characters.\n", strlen(first_name));

    return 0;
}
```

Example output:

```text
Enter your first name: Elene
Hello, Elene
Your name contains 5 characters.
```

---

## Summary

C does not provide a special string type.

A string is:

```text
an array of characters ending with '\0'
```

The `string.h` header provides functions for working with strings:

```c
strlen()   // Find the length
strcpy()   // Copy a string
strcmp()   // Compare strings
strcat()   // Join strings
strcspn()  // Find characters such as '\n'
```

These functions are useful, but the programmer must still make sure that every destination array has enough space.
