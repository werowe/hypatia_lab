# FUNCTIONS

A **function** is a named, reusable block of code. Instead of copying the
same lines over and over, you write them once inside a function and call
that function wherever you need it.

You've already been using one function in every program in this course:

```c
int main(void)
{
    printf("Hello, world!\n");
    return 0;
}
```

`main()` is a function. `printf()` is a function too — one someone else
already wrote for you, in the standard library.

---

## 1. Declaring and Calling a Function

```c
return_type function_name(parameter_type parameter_name, ...)
{
    // body
    return value;   // only if return_type is not void
}
```

```c
#include <stdio.h>

int add(int a, int b)
{
    return a + b;
}

int main(void)
{
    int result = add(3, 4);

    printf("%d\n", result);

    return 0;
}
```

Output:

```text
7
```

Here:

```text
int      the type of value add() returns
add      the function's name
a, b     the parameters — local variables that receive the caller's values
return   sends a value back to whoever called the function
```

---

## 2. `void` Functions

A function that doesn't need to send a value back uses `void` as its return
type, and simply doesn't use `return value;`.

```c
#include <stdio.h>

void greet(void)
{
    printf("Hello, Elene!\n");
}

int main(void)
{
    greet();
    greet();

    return 0;
}
```

Output:

```text
Hello, Elene!
Hello, Elene!
```

A bare `return;` (with no value) can still be used inside a `void`
function to exit early.

---

## 3. Parameters

Parameters let a function work with different values each time it's
called, instead of always doing the exact same thing.

```c
#include <stdio.h>

void print_squared(int number)
{
    printf("%d\n", number * number);
}

int main(void)
{
    print_squared(3);
    print_squared(10);

    return 0;
}
```

Output:

```text
9
100
```

A function can take any number of parameters, including zero:

```c
int add3(int a, int b, int c)
{
    return a + b + c;
}
```

---

## 4. C Passes Arguments By Value

When you call a function, C copies each argument into the function's
parameters. The function works with its own copy — changes made inside the
function do not affect the caller's original variable.

```c
#include <stdio.h>

void double_it(int number)
{
    number = number * 2;   // only changes the local copy
}

int main(void)
{
    int value = 21;

    double_it(value);

    printf("%d\n", value);   // still 21!

    return 0;
}
```

Output:

```text
21
```

If a function needs to change the caller's variable, it must be given the
variable's **address**, using a pointer parameter. This is one of the main
reasons pointers exist in C — the full explanation, with a working `swap()`
example, is in [Pointers](../pointers/POINTERS.md).

```c
void double_it(int *number)
{
    *number = *number * 2;   // follows the pointer and changes the original
}

double_it(&value);
```

---

## 5. Function Prototypes

If a function is called before it's defined further down the file, the
compiler needs to know its signature in advance. A **prototype** declares
the function's name, return type, and parameter types without its body:

```c
#include <stdio.h>

int add(int a, int b);   // prototype

int main(void)
{
    printf("%d\n", add(2, 3));
    return 0;
}

int add(int a, int b)    // full definition, further down
{
    return a + b;
}
```

Without the prototype, the compiler would reach `add(2, 3)` in `main()`
without yet knowing what `add` is, and refuse to compile.

---

## 6. Local Variables and Scope

A variable declared inside a function only exists inside that function.
This is called its **scope**.

```c
#include <stdio.h>

void set_number(void)
{
    int number = 42;   // local to set_number
    printf("%d\n", number);
}

int main(void)
{
    set_number();
    // number does not exist here — it belongs to set_number
    return 0;
}
```

Two different functions can each have their own local variable with the
same name — they don't interfere with each other:

```c
void first(void)
{
    int x = 1;
    printf("%d\n", x);
}

void second(void)
{
    int x = 2;   // a completely different x
    printf("%d\n", x);
}
```

---

## 7. Returning a `struct`

A function can return a whole structure, not just a single number. This is
exactly how [`structs/structs.c`](../structs/structs.c) works — see
[Structs](../structs/STRUCTS.md) for the full walkthrough:

```c
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
```

```c
struct point pt = makepoint(3, 2);

printf("point x=%d y=%d\n", pt.x, pt.y);
```

---

## 8. Recursion

A function can call itself. This is called **recursion**. Every recursive
function needs a **base case** — a condition where it stops calling itself
— or it will recurse forever and crash the program.

```c
#include <stdio.h>

int factorial(int n)
{
    if (n <= 1) {
        return 1;          // base case
    }

    return n * factorial(n - 1);   // recursive case
}

int main(void)
{
    printf("%d\n", factorial(5));

    return 0;
}
```

Output:

```text
120
```

Tracing it by hand helps it click:

```text
factorial(5) = 5 * factorial(4)
             = 5 * (4 * factorial(3))
             = 5 * (4 * (3 * factorial(2)))
             = 5 * (4 * (3 * (2 * factorial(1))))
             = 5 * (4 * (3 * (2 * 1)))
             = 120
```

Most beginner problems are easier and faster to solve with a plain loop.
Recursion becomes genuinely useful once you get to data structures that are
naturally nested, like trees.

---

## 9. Arduino's Two Special Functions

Every Arduino sketch is built from exactly two functions, and the board
calls them for you — you never call them yourself.

```c
void setup()
{
    // runs once, when the board powers on or resets
}

void loop()
{
    // runs over and over, forever, after setup() finishes
}
```

Everything else you write — your own functions for reading a sensor,
updating a display, or debouncing a button — gets called from inside
`setup()` or `loop()`. See [Arduino](../arduino/ARDUINO.md).

---

## Summary

```text
return_type name(parameters) { ... return value; }
void name(parameters) { ... }              no value to return
name(arguments);                           calling a function
prototype;                                 declares a function before its definition
```

Rules to remember:

* Arguments are passed **by value** — the function gets a copy, not the
  original. Use a pointer parameter to let a function modify the caller's
  variable.
* A variable declared inside a function is local to that function.
* Every recursive function needs a base case that stops the recursion.
* `setup()` and `loop()` are just functions — the Arduino runtime calls
  them for you.

---

## Programs

This folder doesn't have an example `.c` file yet — the `add()`,
`greet()`, and `factorial()` examples above are good starting points for
one. Note also
[`pointers/functions_and_pointers.c`](../pointers/functions_and_pointers.c),
a file reserved for a class exercise on functions that modify their
caller's variables through a pointer — it's currently empty, ready to be
filled in together in class.

## Compile

```bash
clang -Wall -Wextra -Wpedantic -std=c17 functions.c -o functions
```

## Run

```bash
./functions
```
