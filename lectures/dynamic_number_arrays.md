# Class 7: Dynamic Arrays of Numbers

A normal array has a size fixed at its declaration:

```c
int scores[5];
```

When the required length is learned at runtime, allocate the array on the heap.

```c
int *scores = malloc(length * sizeof *scores);
```

`scores` points to the first element. We can use normal array indexing:

```c
scores[0] = 90;
printf("%d\n", scores[0]);
```

---

## Length chosen at runtime

Create `dynamic_array.c`:

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    size_t length;

    printf("number of scores: ");

    if (scanf("%zu", &length) != 1 || length == 0 || length > 10000)
    {
        printf("invalid length\n");
        return 1;
    }

    int *scores = malloc(length * sizeof *scores);

    if (scores == NULL)
    {
        printf("allocation failed\n");
        return 1;
    }

    for (size_t i = 0; i < length; i++)
    {
        printf("score %zu: ", i + 1);

        if (scanf("%d", &scores[i]) != 1)
        {
            printf("invalid score\n");
            free(scores);
            return 1;
        }
    }

    long long total = 0;

    for (size_t i = 0; i < length; i++)
    {
        total += scores[i];
    }

    double average = (double) total / length;

    printf("total: %lld\n", total);
    printf("average: %.2f\n", average);

    free(scores);

    return 0;
}
```

The allocation calculation is:

```text
number of elements * bytes per element
```

Writing `sizeof *scores` keeps the element type and allocation in agreement.

The valid indexes are `0` through `length - 1`, so the loop uses `i < length`.

---

## A pointer does not know the array length

These variables carry different information:

```c
int *scores;   // where the array starts
size_t length; // how many elements it contains
```

The pointer alone does not record the length. Keep the length with the pointer
and pass both to functions.

```c
void printNumbers(const int numbers[], size_t length)
{
    for (size_t i = 0; i < length; i++)
    {
        printf("%d\n", numbers[i]);
    }
}
```

---

## When the final length is truly unknown

Sometimes values arrive until a sentinel or end-of-file. Track both:

```c
size_t count = 0;    // elements currently used
size_t capacity = 4; // elements that currently fit
```

When `count == capacity`, grow the allocation with `realloc()`.

This program reads nonnegative integers until the user enters `-1`:

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    size_t count = 0;
    size_t capacity = 4;
    int *numbers = malloc(capacity * sizeof *numbers);

    if (numbers == NULL)
    {
        return 1;
    }

    printf("enter nonnegative integers; -1 stops\n");

    while (1)
    {
        int value;

        if (scanf("%d", &value) != 1)
        {
            printf("invalid input\n");
            free(numbers);
            return 1;
        }

        if (value == -1)
        {
            break;
        }

        if (count == capacity)
        {
            size_t newCapacity = capacity * 2;
            int *larger = realloc(
                numbers,
                newCapacity * sizeof *numbers
            );

            if (larger == NULL)
            {
                printf("could not grow array\n");
                free(numbers);
                return 1;
            }

            numbers = larger;
            capacity = newCapacity;
        }

        numbers[count] = value;
        count++;
    }

    printf("stored %zu numbers\n", count);

    for (size_t i = 0; i < count; i++)
    {
        printf("%d\n", numbers[i]);
    }

    free(numbers);

    return 0;
}
```

The capacities grow `4, 8, 16, 32, ...`. Doubling avoids requesting a new
block after every value.

`-1` is the sentinel. It ends input and is not stored.

---

## The safe `realloc()` pattern

Do not overwrite the original pointer before checking the result:

```c
// Dangerous if realloc fails:
numbers = realloc(numbers, newSize);
```

On failure, `realloc()` returns `NULL` and leaves the old block unchanged.
Assigning directly to `numbers` would lose the old block's address.

Use a temporary pointer:

```c
int *larger = realloc(numbers, newSize);

if (larger == NULL)
{
    free(numbers);
    return 1;
}

numbers = larger;
```

---

## `count` versus `capacity`

Suppose five numbers are stored in an eight-element allocation:

```text
count:     5
capacity:  8
```

Indexes `0` through `4` contain values. Indexes `5` through `7` are available
but do not yet contain valid data.

Use `count` when processing stored values. Use `capacity` only when deciding
whether the allocation must grow.

---

## Arduino note

Repeated heap allocation can fragment the Arduino Uno's small RAM. When a
reasonable maximum is known, use a fixed array and a count:

```c
int readings[100];
size_t count = 0;

if (count < 100)
{
    readings[count] = newReading;
    count++;
}
```

Dynamic arrays are common on desktop systems. Fixed maximums are usually more
predictable on small microcontrollers.

---

## Common mistakes

```c
malloc(length);                  // wrong: length bytes
malloc(length * sizeof *scores); // correct: length integers

for (size_t i = 0; i <= length; i++) // wrong: one past the end
for (size_t i = 0; i < length; i++)  // correct
```

Also remember to check `malloc()` and `realloc()`, preserve the original
pointer until `realloc()` succeeds, and call `free()` exactly once.

---

## Exercises

1. Allocate an array for a runtime-selected number of temperatures, read the
   values, and print their average.
2. Add minimum and maximum calculations to the scores program.
3. Put the total calculation in a function that accepts an array and its
   length.
4. Change the growing array's starting capacity from 4 to 2 and print each new
   capacity when growth occurs.
5. Change the sentinel from `-1` to `0`. Decide whether zero should be stored.

---

## Summary

- `malloc(length * sizeof *pointer)` allocates a runtime-sized array.
- The pointer and length must be tracked separately.
- Valid indexes end at `length - 1`.
- `count` is used elements; `capacity` is available elements.
- `realloc()` changes an allocation's size.
- Store `realloc()`'s result in a temporary pointer until it succeeds.
- Release the final allocation with `free()`.
- Prefer fixed-capacity storage on an Arduino when practical.
