````markdown
# Pointers in C

A pointer is a variable that stores a **memory address**.

A normal variable stores a value:

```c
int number = 42;
```

A pointer can store the address where that value is located:

```c
int *pointer = &number;
```

In this example:

```text
number   stores the integer value 42
pointer  stores the memory address of number
```

---

# Variables and Memory

When a variable is created, the computer reserves space for it in memory.

```c
int number = 42;
```

Conceptually, memory might look like this:

```text
Memory address     Value
0x1000             42
```

The exact address is chosen by the computer and will usually be different each time the program runs.

The variable name:

```c
number
```

refers to the value stored at that location.

The expression:

```c
&number
```

means:

```text
the memory address of number
```

---

# Declaring a Pointer

A pointer declaration uses the `*` symbol:

```c
int *pointer;
```

This means:

```text
pointer can store the address of an int
```

A pointer should normally be initialized when it is declared:

```c
int number = 42;
int *pointer = &number;
```

Now `pointer` stores the address of `number`.

---

# The Address Operator: `&`

The `&` operator obtains the address of a variable.

```c
int number = 42;

printf("%p\n", (void *)&number);
```

Possible output:

```text
0x16f7a2abc
```

The actual address will vary.

This expression:

```c
&number
```

means:

```text
the address of number
```

The type of `&number` is:

```c
int *
```

because it is the address of an `int`.

---

# The Dereference Operator: `*`

When `*` is used with a pointer expression, it accesses the value stored at the pointed-to address.

```c
int number = 42;
int *pointer = &number;

printf("%d\n", *pointer);
```

Output:

```text
42
```

Here:

```text
pointer   is the address of number
*pointer  is the value stored at that address
```

Therefore:

```c
number
```

and:

```c
*pointer
```

refer to the same integer value.

---

# The Two Meanings of `*`

The `*` symbol has two related uses with pointers.

## Use 1: Declaring a pointer

```c
int *pointer;
```

This means:

```text
pointer is a pointer to an int
```

## Use 2: Dereferencing a pointer

```c
printf("%d\n", *pointer);
```

This means:

```text
read the int stored at the address inside pointer
```

The meaning depends on where `*` appears.

---

# A Complete Pointer Example

```c
#include <stdio.h>

int main(void)
{
    int number = 42;
    int *pointer = &number;

    printf("Value of number: %d\n", number);
    printf("Address of number: %p\n", (void *)&number);
    printf("Value stored in pointer: %p\n", (void *)pointer);
    printf("Value found through pointer: %d\n", *pointer);

    return 0;
}
```

Possible output:

```text
Value of number: 42
Address of number: 0x16f7a2abc
Value stored in pointer: 0x16f7a2abc
Value found through pointer: 42
```

Notice that these addresses match:

```c
&number
pointer
```

That is because `pointer` stores the address of `number`.

---

# Changing a Variable Through a Pointer

A pointer can be used to change the value stored at an address.

```c
#include <stdio.h>

int main(void)
{
    int number = 42;
    int *pointer = &number;

    *pointer = 100;

    printf("%d\n", number);

    return 0;
}
```

Output:

```text
100
```

This line:

```c
*pointer = 100;
```

means:

```text
go to the address stored in pointer
and place the value 100 there
```

Because `pointer` points to `number`, this changes `number`.

---

# Visualizing a Pointer

Consider:

```c
int number = 42;
int *pointer = &number;
```

Conceptually:

```text
pointer
+----------------+
| address 0x1000 | ──────────┐
+----------------+            |
                              v
                    number at address 0x1000
                    +----------------+
                    |       42       |
                    +----------------+
```

The pointer does not contain `42`.

It contains the address where `42` is stored.

Dereferencing the pointer follows the address and accesses the value.

---

# Pointer Types

A pointer type describes the type of value located at the address.

```c
int *integer_pointer;
char *character_pointer;
float *float_pointer;
double *double_pointer;
```

Examples:

```c
int age = 16;
int *age_pointer = &age;
```

```c
char letter = 'E';
char *letter_pointer = &letter;
```

```c
double price = 19.95;
double *price_pointer = &price;
```

The pointer type should match the type of the variable being pointed to.

Correct:

```c
int number = 42;
int *pointer = &number;
```

Incorrect:

```c
int number = 42;
double *pointer = &number;
```

A compiler with warnings enabled should report the incompatible pointer types.

---

# Printing Pointer Addresses

Use `%p` to print a pointer.

The argument should be converted to `void *`:

```c
printf("%p\n", (void *)pointer);
```

To print the address of a normal variable:

```c
printf("%p\n", (void *)&number);
```

Example:

```c
#include <stdio.h>

int main(void)
{
    int number = 42;
    int *pointer = &number;

    printf("&number: %p\n", (void *)&number);
    printf("pointer: %p\n", (void *)pointer);

    return 0;
}
```

The two printed addresses should be the same.

---

# A Pointer Must Point Somewhere Valid

This declaration creates a pointer, but does not give it a valid address:

```c
int *pointer;
```

The pointer contains an indeterminate value.

Dereferencing it is dangerous:

```c
*pointer = 42;
```

This causes undefined behavior because the pointer does not point to valid storage.

A pointer should point to a real object:

```c
int number = 42;
int *pointer = &number;
```

Or it should be initialized to `NULL`:

```c
int *pointer = NULL;
```

---

# The Null Pointer

`NULL` represents a pointer that does not currently point to a valid object.

```c
int *pointer = NULL;
```

Before dereferencing a pointer, you can check whether it is `NULL`:

```c
if (pointer != NULL) {
    printf("%d\n", *pointer);
}
```

This is commonly written more simply as:

```c
if (pointer) {
    printf("%d\n", *pointer);
}
```

A null pointer must not be dereferenced.

This is invalid:

```c
int *pointer = NULL;

printf("%d\n", *pointer);
```

It may cause the program to crash.

---

# Passing Values to Functions

C normally passes function arguments **by value**.

This means the function receives a copy.

```c
#include <stdio.h>

void change_number(int number)
{
    number = 100;
}

int main(void)
{
    int value = 42;

    change_number(value);

    printf("%d\n", value);

    return 0;
}
```

Output:

```text
42
```

The function changed only its local copy.

It did not change the original variable in `main()`.

---

# Passing an Address to a Function

To allow a function to change the original variable, pass its address.

```c
#include <stdio.h>

void change_number(int *number)
{
    *number = 100;
}

int main(void)
{
    int value = 42;

    change_number(&value);

    printf("%d\n", value);

    return 0;
}
```

Output:

```text
100
```

The call:

```c
change_number(&value);
```

passes the address of `value`.

The function parameter:

```c
int *number
```

receives that address.

Inside the function:

```c
*number = 100;
```

changes the value stored at that address.

---

# Understanding a Pointer Function Step by Step

Consider this function:

```c
void update_transistor(struct transistor *transistor)
{
    transistor->collector = transistor->base;
}
```

And this call:

```c
update_transistor(&transistor);
```

The call passes:

```c
&transistor
```

which means:

```text
the address of the transistor variable
```

The function receives that address using:

```c
struct transistor *transistor
```

which means:

```text
transistor is a pointer to a struct transistor
```

The function can then change the original structure through the pointer.

---

# Changing Two Variables with Pointers

Pointers allow a function to change more than one variable.

```c
#include <stdio.h>

void set_values(int *first, int *second)
{
    *first = 10;
    *second = 20;
}

int main(void)
{
    int a = 0;
    int b = 0;

    set_values(&a, &b);

    printf("a = %d\n", a);
    printf("b = %d\n", b);

    return 0;
}
```

Output:

```text
a = 10
b = 20
```

Without pointers, a function normally returns only one value directly.

---

# Swapping Two Values

A classic pointer example is swapping two variables.

```c
#include <stdio.h>

void swap(int *first, int *second)
{
    int temporary = *first;

    *first = *second;
    *second = temporary;
}

int main(void)
{
    int a = 10;
    int b = 20;

    swap(&a, &b);

    printf("a = %d\n", a);
    printf("b = %d\n", b);

    return 0;
}
```

Output:

```text
a = 20
b = 10
```

The function receives the addresses of `a` and `b`, so it can change both original variables.

---

# Pointers and Arrays

The name of an array is closely related to a pointer to its first element.

```c
int numbers[] = {10, 20, 30};
```

In most expressions:

```c
numbers
```

is converted to a pointer to:

```c
numbers[0]
```

Therefore:

```c
numbers
```

and:

```c
&numbers[0]
```

refer to the same starting address.

Example:

```c
#include <stdio.h>

int main(void)
{
    int numbers[] = {10, 20, 30};

    printf("%p\n", (void *)numbers);
    printf("%p\n", (void *)&numbers[0]);

    return 0;
}
```

The printed addresses should match.

---

# Array Indexing and Pointer Arithmetic

These two expressions access the same array element:

```c
numbers[i]
```

and:

```c
*(numbers + i)
```

Example:

```c
#include <stdio.h>

int main(void)
{
    int numbers[] = {10, 20, 30};

    printf("%d\n", numbers[1]);
    printf("%d\n", *(numbers + 1));

    return 0;
}
```

Output:

```text
20
20
```

The expression:

```c
numbers + 1
```

points to the next `int` in the array.

Dereferencing it:

```c
*(numbers + 1)
```

reads that integer.

---

# Pointer Arithmetic

When a pointer is increased, it moves by the size of the type it points to.

```c
int numbers[] = {10, 20, 30};
int *pointer = numbers;
```

Initially:

```c
*pointer
```

is:

```text
10
```

After:

```c
pointer++;
```

the pointer moves to the next `int`.

Now:

```c
*pointer
```

is:

```text
20
```

Example:

```c
#include <stdio.h>

int main(void)
{
    int numbers[] = {10, 20, 30};
    int *pointer = numbers;

    printf("%d\n", *pointer);

    pointer++;

    printf("%d\n", *pointer);

    return 0;
}
```

Output:

```text
10
20
```

If an `int` occupies four bytes, increasing an `int *` by one moves the address forward by four bytes.

You do not manually add four.

C automatically scales pointer arithmetic according to the pointed-to type.

---

# Looping Through an Array with a Pointer

You can loop through an array using pointer arithmetic:

```c
#include <stdio.h>

int main(void)
{
    int numbers[] = {10, 20, 30, 40};
    size_t length = sizeof numbers / sizeof numbers[0];

    for (size_t i = 0; i < length; i++) {
        printf("%d\n", *(numbers + i));
    }

    return 0;
}
```

Output:

```text
10
20
30
40
```

The usual indexed version is often easier to read:

```c
for (size_t i = 0; i < length; i++) {
    printf("%d\n", numbers[i]);
}
```

Both versions access the same elements.

---

# Pointers and Strings

A C string is an array of characters ending with `'\0'`.

```c
char name[] = "Elene";
```

In most expressions, `name` becomes a pointer to the first character.

```text
name points to name[0]
```

Therefore:

```c
printf("%s\n", name);
```

passes the address of the first character to `printf()`.

`printf()` continues reading characters until it finds `'\0'`.

---

# A Character Pointer

A pointer can point to a character:

```c
char letter = 'E';
char *pointer = &letter;
```

Example:

```c
#include <stdio.h>

int main(void)
{
    char letter = 'E';
    char *pointer = &letter;

    printf("%c\n", letter);
    printf("%c\n", *pointer);

    return 0;
}
```

Output:

```text
E
E
```

---

# Character Arrays and String Literals

This creates a modifiable character array:

```c
char name[] = "Elene";
```

You can change its characters:

```c
name[0] = 'A';
```

This creates a pointer to a string literal:

```c
const char *name = "Elene";
```

The string literal should not be modified:

```c
name[0] = 'A';  // Incorrect
```

Using `const` tells the compiler that the characters must not be changed.

For a string that needs to be modified, use an array:

```c
char name[] = "Elene";
```

For a fixed string that will only be read, use:

```c
const char *name = "Elene";
```

---

# Pointer to Pointer

A pointer can also store the address of another pointer.

```c
int number = 42;
int *pointer = &number;
int **pointer_to_pointer = &pointer;
```

The types are:

```text
number              int
pointer             pointer to int
pointer_to_pointer  pointer to pointer to int
```

Values can be accessed at different levels:

```c
number
*pointer
**pointer_to_pointer
```

All three produce:

```text
42
```

Example:

```c
#include <stdio.h>

int main(void)
{
    int number = 42;
    int *pointer = &number;
    int **pointer_to_pointer = &pointer;

    printf("%d\n", number);
    printf("%d\n", *pointer);
    printf("%d\n", **pointer_to_pointer);

    return 0;
}
```

---

# Structures and Pointers

Suppose we have this structure:

```c
struct transistor {
    int base;
    int collector;
    int emitter;
};
```

A normal structure variable uses the dot operator:

```c
struct transistor t;

t.base = 1;
```

A pointer to the structure can use the arrow operator:

```c
struct transistor *pointer = &t;

pointer->base = 1;
```

This:

```c
pointer->base
```

is equivalent to:

```c
(*pointer).base
```

The arrow operator is easier to read.

---

# Structure Pointer Example

```c
#include <stdio.h>
#include <stdbool.h>

struct transistor {
    bool base;
    bool collector;
    bool emitter;
};

void update_transistor(struct transistor *transistor)
{
    transistor->collector = transistor->base;
    transistor->emitter = transistor->collector;
}

int main(void)
{
    struct transistor transistor = {
        .base = true,
        .collector = false,
        .emitter = false
    };

    update_transistor(&transistor);

    printf("Base: %d\n", transistor.base);
    printf("Collector: %d\n", transistor.collector);
    printf("Emitter: %d\n", transistor.emitter);

    return 0;
}
```

The function receives the address of the original structure, so it can modify the structure in `main()`.

---

# The `const` Keyword with Pointers

`const` can be used to prevent a function from changing a pointed-to value.

```c
void print_number(const int *number)
{
    printf("%d\n", *number);
}
```

Inside this function, the following would be invalid:

```c
*number = 100;
```

The pointer can read the value, but cannot change it through that pointer.

Example:

```c
#include <stdio.h>

void print_number(const int *number)
{
    printf("%d\n", *number);
}

int main(void)
{
    int value = 42;

    print_number(&value);

    return 0;
}
```

Using `const` is useful when a function only needs to inspect data.

---

# Dynamic Memory with `malloc()`

Sometimes the amount of memory needed is decided while the program is running.

The `malloc()` function allocates memory dynamically.

It is declared in:

```c
#include <stdlib.h>
```

Example:

```c
int *number = malloc(sizeof *number);
```

This asks for enough memory to store one `int`.

`malloc()` returns a pointer to the allocated memory.

---

# Checking the Result of `malloc()`

Memory allocation can fail.

Always check whether `malloc()` returned `NULL`.

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int *number = malloc(sizeof *number);

    if (number == NULL) {
        fprintf(stderr, "Memory allocation failed.\n");
        return 1;
    }

    *number = 42;

    printf("%d\n", *number);

    free(number);

    return 0;
}
```

Output:

```text
42
```

---

# Releasing Memory with `free()`

Memory created with `malloc()` remains allocated until it is released.

Use:

```c
free(pointer);
```

Example:

```c
int *number = malloc(sizeof *number);

if (number == NULL) {
    return 1;
}

*number = 42;

free(number);
```

After calling `free()`, the pointer no longer points to valid allocated memory.

It is often a good idea to assign `NULL` afterward:

```c
free(number);
number = NULL;
```

---

# Allocating an Array with `malloc()`

To allocate space for several integers:

```c
size_t length = 5;

int *numbers = malloc(length * sizeof *numbers);
```

This allocates enough memory for five integers.

Complete example:

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    size_t length = 5;

    int *numbers = malloc(length * sizeof *numbers);

    if (numbers == NULL) {
        fprintf(stderr, "Memory allocation failed.\n");
        return 1;
    }

    for (size_t i = 0; i < length; i++) {
        numbers[i] = (int)(i * 10);
    }

    for (size_t i = 0; i < length; i++) {
        printf("%d\n", numbers[i]);
    }

    free(numbers);
    numbers = NULL;

    return 0;
}
```

Output:

```text
0
10
20
30
40
```

---

# Why Use `sizeof *pointer`?

This is a common allocation pattern:

```c
int *numbers = malloc(length * sizeof *numbers);
```

It means:

```text
allocate length elements,
each the size of the object that numbers points to
```

You could write:

```c
malloc(length * sizeof(int))
```

but:

```c
malloc(length * sizeof *numbers)
```

automatically stays correct if the pointer type changes.

For example:

```c
double *numbers = malloc(length * sizeof *numbers);
```

Now the allocation automatically uses the size of `double`.

---

# Allocating Memory for a String

To store up to nine visible characters plus `'\0'`:

```c
char *name = malloc(10 * sizeof *name);
```

Because `sizeof(char)` is always `1`, this could also be written:

```c
char *name = malloc(10);
```

However, this style is more consistent:

```c
char *name = malloc(10 * sizeof *name);
```

Complete example:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    size_t capacity = 10;

    char *name = malloc(capacity * sizeof *name);

    if (name == NULL) {
        fprintf(stderr, "Memory allocation failed.\n");
        return 1;
    }

    strcpy(name, "Elene");

    printf("%s\n", name);

    free(name);
    name = NULL;

    return 0;
}
```

The allocated memory has room for:

```text
9 visible characters + '\0'
```

---

# `calloc()`

`calloc()` allocates memory for several elements and initializes all bytes to zero.

```c
int *numbers = calloc(5, sizeof *numbers);
```

This creates space for five integers.

Conceptually, the initial values are:

```text
0 0 0 0 0
```

Complete example:

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    size_t length = 5;

    int *numbers = calloc(length, sizeof *numbers);

    if (numbers == NULL) {
        fprintf(stderr, "Memory allocation failed.\n");
        return 1;
    }

    for (size_t i = 0; i < length; i++) {
        printf("%d\n", numbers[i]);
    }

    free(numbers);

    return 0;
}
```

---

# `realloc()`

`realloc()` changes the size of previously allocated memory.

```c
int *temporary = realloc(numbers, new_length * sizeof *numbers);
```

Use a temporary pointer because `realloc()` can fail.

```c
if (temporary == NULL) {
    free(numbers);
    return 1;
}

numbers = temporary;
```

Example:

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    size_t length = 3;

    int *numbers = malloc(length * sizeof *numbers);

    if (numbers == NULL) {
        return 1;
    }

    numbers[0] = 10;
    numbers[1] = 20;
    numbers[2] = 30;

    size_t new_length = 5;

    int *temporary =
        realloc(numbers, new_length * sizeof *numbers);

    if (temporary == NULL) {
        free(numbers);
        return 1;
    }

    numbers = temporary;

    numbers[3] = 40;
    numbers[4] = 50;

    for (size_t i = 0; i < new_length; i++) {
        printf("%d\n", numbers[i]);
    }

    free(numbers);

    return 0;
}
```

---

# Common Pointer Errors

## Error 1: Dereferencing an uninitialized pointer

Incorrect:

```c
int *pointer;

*pointer = 42;
```

The pointer does not point to valid storage.

Correct:

```c
int number;
int *pointer = &number;

*pointer = 42;
```

---

## Error 2: Dereferencing `NULL`

Incorrect:

```c
int *pointer = NULL;

printf("%d\n", *pointer);
```

Check first:

```c
if (pointer != NULL) {
    printf("%d\n", *pointer);
}
```

---

## Error 3: Using memory after `free()`

Incorrect:

```c
int *pointer = malloc(sizeof *pointer);

free(pointer);

*pointer = 42;
```

The allocated memory is no longer valid.

This is called a **use-after-free** error.

A safer pattern is:

```c
free(pointer);
pointer = NULL;
```

---

## Error 4: Forgetting to call `free()`

```c
int *pointer = malloc(sizeof *pointer);
```

If the memory is never released, the program has a **memory leak**.

Correct:

```c
free(pointer);
```

---

## Error 5: Freeing the same memory twice

Incorrect:

```c
free(pointer);
free(pointer);
```

This is called a **double free** and causes undefined behavior.

After freeing:

```c
free(pointer);
pointer = NULL;
```

Calling:

```c
free(NULL);
```

is safe.

---

## Error 6: Returning the address of a local variable

Incorrect:

```c
int *create_number(void)
{
    int number = 42;

    return &number;
}
```

The local variable stops existing when the function returns.

The returned pointer becomes invalid.

This is called a **dangling pointer**.

---

## Error 7: Going beyond an array

```c
int numbers[3] = {10, 20, 30};

int *pointer = numbers;

printf("%d\n", *(pointer + 3));
```

Valid indexes are:

```text
0, 1, 2
```

Index `3` is outside the array.

Accessing it causes undefined behavior.

---

## Error 8: Confusing a pointer with the pointed-to value

```c
int number = 42;
int *pointer = &number;
```

These are different:

```c
pointer
```

is an address.

```c
*pointer
```

is the integer stored at that address.

Use `%p` for the pointer:

```c
printf("%p\n", (void *)pointer);
```

Use `%d` for the pointed-to integer:

```c
printf("%d\n", *pointer);
```

---

# Pointer Declaration Style

All of these declare a pointer to `int`:

```c
int *pointer;
```

```c
int* pointer;
```

```c
int * pointer;
```

A common C style is:

```c
int *pointer;
```

This helps show that `*` belongs to the variable declaration.

Be careful when declaring several variables on one line:

```c
int *first, second;
```

This declares:

```text
first   pointer to int
second  int
```

It does not make both variables pointers.

To declare two pointers:

```c
int *first;
int *second;
```

This is often clearer than declaring both on one line.

---

# Pointers and `sizeof`

The size of a pointer is not necessarily the size of the type it points to.

```c
int number = 42;
int *pointer = &number;

printf("%zu\n", sizeof number);
printf("%zu\n", sizeof pointer);
```

On a typical 64-bit computer, possible output is:

```text
4
8
```

This means:

```text
int          4 bytes
int pointer  8 bytes
```

A `char *`, `int *`, and `double *` commonly have the same pointer size on one system:

```c
printf("%zu\n", sizeof(char *));
printf("%zu\n", sizeof(int *));
printf("%zu\n", sizeof(double *));
```

The pointed-to objects may have different sizes, but the pointers themselves store memory addresses.

---

# Pointers Are Not Physical Memory Addresses

An address printed with `%p` is the address used by the process.

Modern operating systems normally use **virtual memory**.

```c
printf("%p\n", (void *)&number);
```

The result is generally a virtual address, not a direct physical RAM address.

The operating system and processor translate virtual addresses to physical memory locations.

This provides:

- process isolation;
- memory protection;
- flexible memory management;
- support for paging and swapping;
- address-space randomization.

For introductory C programming, it is sufficient to think of the pointer as the address of an object in the program's memory.

---

# Important Pointer Rules

## Rule 1: A pointer stores an address

```c
int *pointer = &number;
```

## Rule 2: `&` obtains an address

```c
&number
```

means:

```text
the address of number
```

## Rule 3: `*` dereferences a pointer

```c
*pointer
```

means:

```text
the value stored at the address inside pointer
```

## Rule 4: Pointer types should match

```c
int number = 42;
int *pointer = &number;
```

## Rule 5: Do not dereference an invalid pointer

```c
int *pointer = NULL;
```

Do not use:

```c
*pointer
```

until the pointer refers to a valid object.

## Rule 6: Use `%p` to print addresses

```c
printf("%p\n", (void *)pointer);
```

## Rule 7: Pass an address when a function must change a variable

```c
change_number(&value);
```

## Rule 8: Release dynamically allocated memory

```c
free(pointer);
```

## Rule 9: Do not use memory after freeing it

```c
free(pointer);
pointer = NULL;
```

## Rule 10: Stay within array bounds

For:

```c
int numbers[3];
```

the valid indexes are:

```text
0, 1, 2
```

---

# Complete Example

```c
#include <stdio.h>
#include <stdlib.h>

void double_value(int *value)
{
    if (value != NULL) {
        *value = *value * 2;
    }
}

int main(void)
{
    int number = 21;
    int *pointer = &number;

    printf("Original value: %d\n", number);
    printf("Address: %p\n", (void *)pointer);
    printf("Value through pointer: %d\n", *pointer);

    double_value(&number);

    printf("New value: %d\n", number);

    size_t length = 3;

    int *numbers = malloc(length * sizeof *numbers);

    if (numbers == NULL) {
        fprintf(stderr, "Memory allocation failed.\n");
        return 1;
    }

    numbers[0] = 10;
    numbers[1] = 20;
    numbers[2] = 30;

    for (size_t i = 0; i < length; i++) {
        printf("numbers[%zu] = %d\n", i, numbers[i]);
    }

    free(numbers);
    numbers = NULL;

    return 0;
}
```

Possible output:

```text
Original value: 21
Address: 0x16f123abc
Value through pointer: 21
New value: 42
numbers[0] = 10
numbers[1] = 20
numbers[2] = 30
```

The address will vary between systems and program runs.

---

# Summary

A pointer is a variable that stores a memory address.

```c
int number = 42;
int *pointer = &number;
```

The most important pointer operators are:

```text
&   get the address of a variable
*   access the value stored at an address
```

Therefore:

```c
&number
```

means:

```text
the address of number
```

and:

```c
*pointer
```

means:

```text
the value found at the address stored in pointer
```

Pointers are used for:

- changing variables inside functions;
- working with arrays and strings;
- passing large structures efficiently;
- dynamic memory allocation;
- building linked data structures;
- accessing hardware registers;
- memory-mapped input and output;
- embedded systems programming.

The central idea is:

```text
A normal variable stores a value.

A pointer stores the address where a value is located.
```
````
