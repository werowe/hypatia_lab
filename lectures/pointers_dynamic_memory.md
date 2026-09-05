# Class 5: Pointers and Dynamic Memory

Every variable is stored somewhere in memory.

```c
int score = 90;
```

`score` names the value. The `&` operator gives its memory address.

```c
printf("%p\n", (void *) &score);
```

The exact address varies each time the program runs.

---

## Declaring a pointer

A pointer stores an address.

```c
int score = 90;
int *scorePointer = &score;
```

Read `int *scorePointer` as:

> `scorePointer` points to an `int`.

The types must agree. An `int *` points to an `int`; a `char *` points to a
`char`.

```c
char letter = 'A';
char *letterPointer = &letter;
```

---

## Dereferencing a pointer

The `*` operator accesses the value at an address.

```c
int score = 90;
int *scorePointer = &score;

printf("%d\n", *scorePointer); // 90
```

It can also change that value:

```c
*scorePointer = 100;
printf("%d\n", score); // 100
```

Two uses of `*` appear here:

```c
int *scorePointer; // declaration: pointer to int
*scorePointer      // expression: value being pointed to
```

---

## Complete pointer example

Create `pointers.c`:

```c
#include <stdio.h>

int main(void)
{
    int score = 90;
    int *scorePointer = &score;

    printf("score: %d\n", score);
    printf("address: %p\n", (void *) scorePointer);
    printf("value through pointer: %d\n", *scorePointer);

    *scorePointer += 5;

    printf("new score: %d\n", score);

    return 0;
}
```

Changing `*scorePointer` changes `score` because both refer to the same memory.

---

## Arrays and pointers

In most expressions, an array name gives the address of its first element.

```c
int numbers[] = {10, 20, 30};
int *pointer = numbers;
```

These expressions access the same values:

```c
numbers[0] == *pointer
numbers[1] == *(pointer + 1)
numbers[2] == *(pointer + 2)
```

Array notation is usually easier to read, even when the array was obtained
through a pointer:

```c
printf("%d\n", pointer[1]); // 20
```

---

## Passing an address to a function

C normally passes a copy of an argument. Pass a pointer when a function must
change the caller's variable.

```c
#include <stdio.h>

void addPoint(int *score)
{
    (*score)++;
}

int main(void)
{
    int score = 9;

    addPoint(&score);
    printf("%d\n", score); // 10

    return 0;
}
```

Parentheses in `(*score)++` ensure that the pointed-to integer is incremented.

---

## Stack and heap

Local variables normally live on the **stack**:

```c
int score = 90;
char name[40];
```

Their storage is managed automatically and disappears when the function
returns.

The **heap** is memory requested while the program runs. Use `malloc()` to
request it and `free()` to release it.

```c
#include <stdlib.h>

int *number = malloc(sizeof *number);

if (number == NULL)
{
    return 1;
}

*number = 42;
free(number);
```

`malloc()` returns `NULL` if the request fails. Never dereference a pointer
until you know it is not `NULL`.

---

## Allocating several elements

Multiply the element count by the size of one element.

```c
size_t length = 10;
int *numbers = malloc(length * sizeof *numbers);
```

For a string, include one element for `\0`:

```c
size_t visibleCharacters = 20;
char *text = malloc((visibleCharacters + 1) * sizeof *text);
```

Writing `sizeof *numbers` is safer than repeating the type name. If the pointer
type changes later, the size calculation still matches it.

---

## Ownership and lifetime

After a successful `malloc()`, the program owns the returned block.

```text
malloc -> check -> use -> free
```

Rules:

- Call `free()` exactly once for each successful allocation.
- Do not read or write the block after `free()`.
- Do not call `free()` on ordinary local arrays or string literals.
- Do not lose the only pointer to an allocated block.

Forgetting the pointer without calling `free()` creates a **memory leak**.

```c
int *value = malloc(sizeof *value);
value = NULL; // leak: the allocated block can no longer be found
```

---

## Arduino note

An Arduino Uno has very little RAM. Fixed arrays are often preferable because
their memory use is predictable. Repeated heap allocation can also fragment
the available memory.

You still need pointers for Arduino work: arrays, strings, functions, hardware
registers, and library interfaces all use them.

---

## Exercises

1. Create an `int`, point to it, and print the value both directly and through
   the pointer.
2. Change a `char` by dereferencing a `char *`.
3. Write a function `doubleValue(int *value)` that changes the caller's value.
4. Allocate one `double`, check the allocation, store a value, print it, and
   free it.
5. Explain why dereferencing `NULL` and using memory after `free()` are errors.

---

## Summary

- `&value` produces an address.
- A pointer stores an address.
- `*pointer` accesses the pointed-to value.
- Array names and pointers are closely related, but a pointer does not remember
  an array's length.
- Local variables normally use automatic stack storage.
- `malloc()` requests heap memory and `free()` releases it.
- Check every allocation for `NULL`.
- Each successful allocation needs exactly one later `free()`.

Next: applying dynamic memory to strings.
