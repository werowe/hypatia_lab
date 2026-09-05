# Class 6: Strings and Dynamic Memory

A C string is a `char` array ending with `\0`.

```c
char name[] = "Diana";
```

The compiler creates six elements:

```text
'D' 'i' 'a' 'n' 'a' '\0'
```

The visible length is 5. The required storage is 6.

---

## Length and capacity

Length and capacity are different.

```c
char message[100];
```

This array always has a capacity of 100 `char` values. It can store strings
from 0 through 99 visible characters because one position is needed for `\0`.

A fixed array already accepts varying-length text:

```c
if (fgets(message, sizeof message, stdin) != NULL)
{
    printf("%s", message);
}
```

Use a fixed array when a reasonable maximum is known. Use dynamic memory when
the required capacity is learned while the program runs.

---

## Pointers and `malloc()`

`malloc()` reserves a requested number of bytes and returns their address.

```c
#include <stdlib.h>

char *text = malloc(100 * sizeof *text);
```

`text` is a pointer to `char`. It stores the address of the first allocated
character.

Always check whether the request succeeded:

```c
if (text == NULL)
{
    printf("allocation failed\n");
    return 1;
}
```

Release the memory when finished:

```c
free(text);
```

The basic pattern is:

```text
malloc -> check -> use -> free
```

---

## Capacity chosen at runtime

Create `dynamic_string.c`:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    size_t maximumLength;

    printf("maximum visible characters: ");

    if (scanf("%zu", &maximumLength) != 1 ||
        maximumLength == 0 || maximumLength > 10000)
    {
        printf("invalid length\n");
        return 1;
    }

    char *text = malloc((maximumLength + 1) * sizeof *text);

    if (text == NULL)
    {
        printf("allocation failed\n");
        return 1;
    }

    int character;
    while ((character = getchar()) != '\n' && character != EOF)
    {
        // Remove the rest of the scanf input line.
    }

    printf("enter text: ");

    if (fgets(text, maximumLength + 1, stdin) == NULL)
    {
        printf("input failed\n");
        free(text);
        return 1;
    }

    text[strcspn(text, "\n")] = '\0';

    printf("length: %zu\n", strlen(text));
    printf("text: %s\n", text);

    free(text);

    return 0;
}
```

If the user requests 40 visible characters, the program allocates 41 `char`
values. The extra position holds `\0`.

`size_t` is an unsigned integer type used for sizes. Its `printf()` and
`scanf()` marker is `%zu`.

---

## Allocating an exact-size copy

If a string already exists, allocate `strlen(string) + 1` bytes and copy it.

```c
char original[200];

if (fgets(original, sizeof original, stdin) == NULL)
{
    return 1;
}

original[strcspn(original, "\n")] = '\0';

size_t length = strlen(original);
char *copy = malloc((length + 1) * sizeof *copy);

if (copy == NULL)
{
    return 1;
}

strcpy(copy, original);
printf("%s\n", copy);

free(copy);
```

The allocation fits the current text exactly. The temporary `original` array
still limits input to 199 visible characters.

---

## Why not use `scanf("%s", text)`?

Plain `%s` stops at the first whitespace, so it cannot read a complete sentence.
Without a width limit, it can also write beyond the allocated memory.

`fgets()` reads spaces and receives the destination capacity:

```c
fgets(text, maximumLength + 1, stdin);
```

The size passed to `fgets()` includes the position reserved for `\0`.

---

## Ownership rules

After a successful `malloc()`, the program owns the allocated block.

- Call `free()` exactly once when the block is no longer needed.
- Do not use the pointer after `free()`.
- Do not call `free()` on an ordinary array or a string literal.

```c
char fixed[20];
char *dynamic = malloc(20);

free(dynamic); // correct
// free(fixed); // wrong
```

Forgetting `free()` causes a **memory leak**.

---

## Arduino note

An Arduino Uno has only a small amount of RAM. Dynamic allocation can also
fragment its heap over time. Prefer a fixed maximum when practical:

```c
char command[32];
```

Dynamic memory is still important C knowledge and is common in desktop
programs where input sizes vary widely.

---

## Exercises

1. Allocate space for a user-selected maximum city-name length, then read and
   print the city.
2. Explain why 25 visible characters require 26 `char` values.
3. Read text into a 100-character temporary array and allocate an exact-size
   copy.
4. Add a second dynamically allocated string and free both allocations.
5. Identify the errors:

   ```c
   char *name = malloc(strlen(input));
   strcpy(name, input);
   free(name);
   printf("%s\n", name);
   ```

---

## Summary

- A string's length and its storage capacity are different.
- A string needs one extra `char` for `\0`.
- `malloc()` allocates a runtime-sized block and returns a pointer.
- Check for `NULL` before using allocated memory.
- `fgets()` reads text within a supplied capacity.
- `strlen()` returns visible length; `strcpy()` copies a string.
- Every successful allocation needs one later `free()`.
- Fixed arrays are usually preferable on an Arduino Uno.

Next: dynamic arrays of numbers.
