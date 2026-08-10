# STRUCTS

A `struct` groups several related values — possibly of different types —
into a single named unit. C doesn't have classes like Python or Java, but
`struct` gives you the same basic idea: a bundle of named fields that
belong together.

```c
struct point {
    int x;
    int y;
};
```

This defines a new type, `struct point`, with two members: `x` and `y`.
Defining the struct does not create a variable yet — it just describes the
shape.

---

## 1. Declaring and Using a Struct Variable

```c
#include <stdio.h>

struct point {
    int x;
    int y;
};

int main(void)
{
    struct point pt;

    pt.x = 3;
    pt.y = 2;

    printf("point x=%d y=%d\n", pt.x, pt.y);

    return 0;
}
```

Output:

```text
point x=3 y=2
```

The `.` (dot operator) accesses a member of a struct variable.

---

## 2. Initializing at Declaration

```c
struct point pt = {3, 2};   // pt.x = 3, pt.y = 2, in member order
```

Designated initializers name each member explicitly, which is clearer and
doesn't depend on remembering the member order:

```c
struct point pt = {
    .x = 3,
    .y = 2
};
```

---

## 3. Walkthrough: `structs.c`

This course's [`structs/structs.c`](structs.c) shows a function that
**returns** a struct:

```c
#include <stdio.h>

struct point {
    int x;
    int y;
};

struct point makepoint(int x, int y)
{
    struct point temp;

    temp.x = x;
    temp.y = y;

    return temp;
}

int main()
{
    struct point pt = makepoint(3, 2);

    printf("point x=%d y=%d\n", pt.x, pt.y);
}
```

Output:

```text
point x=3 y=2
```

`makepoint()` builds a temporary `struct point`, fills in its members, and
returns the whole thing by value — `pt` in `main()` gets its own independent
copy. This is a common way to construct a struct: one function whose only
job is to build and return it correctly, so you never repeat that setup
code everywhere you need a `struct point`.

---

## 4. A Struct With `bool` Members

Struct members don't have to be numbers. This example, used elsewhere in
the course to model a transistor switch, uses `bool` members (from
`<stdbool.h>`, see [Data Types](../misc/DATATYPES.md)):

```c
#include <stdbool.h>

struct transistor {
    bool base;
    bool collector;
    bool emitter;
};
```

```c
struct transistor t = {
    .base = true,
    .collector = false,
    .emitter = false
};

printf("%d\n", t.base);   // 1
```

See [`electronics/transistor.c`](../electronics/transistor.c) for the full
program this comes from, walked through in
[Electronics](../electronics/ELECTRONICS.md).

---

## 5. Structs and Pointers

Passing a large struct into a function by value copies the *entire* struct.
For a small struct like `struct point` that's fine, but as structs grow, or
when a function needs to *change* the caller's struct, you pass a pointer
to it instead — using `->` instead of `.` to access members through the
pointer.

```c
void update_transistor(struct transistor *transistor)
{
    transistor->collector = transistor->base;
}
```

```c
struct transistor t = { .base = true };

update_transistor(&t);

printf("%d\n", t.collector);   // 1
```

This is exactly the pattern used in
[`electronics/transistor.c`](../electronics/transistor.c). The full
explanation of `->`, `&`, and pointers to structs is in
[Pointers](../pointers/POINTERS.md).

---

## 6. Arrays of Structs

A struct can be an element of an array, letting you manage many of the same
kind of "thing" at once.

```c
#include <stdio.h>

struct point {
    int x;
    int y;
};

int main(void)
{
    struct point path[3] = {
        {0, 0},
        {1, 2},
        {3, 4}
    };

    for (int i = 0; i < 3; i++) {
        printf("%d, %d\n", path[i].x, path[i].y);
    }

    return 0;
}
```

Output:

```text
0, 0
1, 2
3, 4
```

See [Arrays](../arrays/ARRAYS.md).

---

## 7. `typedef struct` — Dropping the `struct` Keyword

Normally, every declaration of a struct variable needs the `struct`
keyword:

```c
struct point pt;
```

`typedef` gives the struct a shorter alias, so you can drop it:

```c
typedef struct {
    int x;
    int y;
} Point;

Point pt = {3, 2};
```

See the `typedef` section of [Data Types](../misc/DATATYPES.md) for more
examples.

---

## Summary

```text
struct name { type member1; type member2; ... };   define the shape
struct name variable;                               declare a variable
variable.member                                      access a member
pointer->member                                      access a member through a pointer
```

Rules to remember:

* Defining a `struct` only describes its shape — it doesn't create a
  variable by itself.
* Use `.` on a struct variable, `->` on a pointer to a struct.
* A function receives a *copy* of a struct passed by value; pass a pointer
  if the function needs to modify the caller's original struct.
* `typedef` lets you drop the repeated `struct` keyword.

---

## Programs

* [`structs.c`](structs.c) — defines `struct point` and a `makepoint()`
  function that builds and returns one. Walked through in section 3 above.

## Compile

```bash
clang -Wall -Wextra -Wpedantic -std=c17 structs.c -o structs
```

## Run

```bash
./structs
```
