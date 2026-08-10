# MEMORY

Every variable in a C program lives somewhere in the computer's memory.
Understanding roughly *where* and *how long* a variable lives explains some
of C's most important rules — and its most common bugs.

For the mechanics of addresses and pointers themselves, see
[Pointers](../pointers/POINTERS.md). This page is about the bigger picture:
where variables actually live, and how long they last.

---

## 1. A Variable Is a Labeled Box in Memory

```c
int age = 16;
```

Conceptually, the computer reserves a small piece of memory, gives it an
address, and stores `16` there:

```text
Address       Value
0x1000        16
```

`age` is just a name your program uses to refer to that box. The `&`
operator reveals the actual address:

```c
printf("%p\n", (void *)&age);
```

---

## 2. Four Regions of Memory

A running C program's memory is roughly divided into these regions:

```text
+----------------------+  high addresses
|        Stack          |  local variables, function calls — grows downward
|          ↓            |
|                        |
|          ↑            |
|         Heap           |  malloc()/free() memory — grows upward
+------------------------+
|   Static / Global      |  global variables, static variables
+------------------------+
|         Code            |  the compiled instructions of your program
+----------------------+  low addresses
```

You don't manage most of this by hand, but knowing it exists explains a
lot of C's behavior.

### The Stack

Every time a function is called, C sets aside space on the **stack** for
its local variables and parameters. When the function returns, that space
is automatically reclaimed — instantly and for free.

```c
void greet(void)
{
    int count = 0;   // lives on the stack, only while greet() is running
}
```

This is why returning the address of a local variable is dangerous — see
"Error 6: Returning the address of a local variable" in
[Pointers](../pointers/POINTERS.md).

### The Heap

Memory you request yourself with `malloc()`, `calloc()`, or `realloc()`
comes from the **heap**. Unlike the stack, heap memory does *not* get
cleaned up automatically — you must call `free()` yourself, or the memory
stays reserved for the rest of the program's life (a **memory leak**). The
full `malloc()`/`free()` story is in
[Pointers](../pointers/POINTERS.md).

### Static / Global Storage

Global variables, and local variables declared `static`, live here for the
**entire run** of the program — not just while one function call is active.

```c
void counter(void)
{
    static int calls = 0;   // keeps its value between calls

    calls++;
    printf("%d\n", calls);
}
```

Called three times, this prints `1`, `2`, `3` — a normal (non-`static`)
local variable would reset to `0` every time, because it's created fresh
on the stack for each call.

---

## 3. Scope vs. Lifetime

These are two different, easily confused ideas:

```text
Scope     — where in the code a name is visible
Lifetime  — how long the variable's memory actually exists
```

```c
#include <stdio.h>

int global_count = 0;              // scope: whole file. lifetime: whole program

void increment(void)
{
    int local_value = 1;           // scope: this function. lifetime: one call
    global_count += local_value;
}

int main(void)
{
    increment();
    increment();

    printf("%d\n", global_count);  // 2

    return 0;
}
```

`local_value` is created and destroyed every time `increment()` runs.
`global_count` is created once, when the program starts, and lives until it
ends.

---

## 4. `sizeof` — How Much Memory a Variable Uses

`sizeof` tells you, in bytes, how much memory a type or variable occupies.

```c
#include <stdio.h>

int main(void)
{
    int number = 42;

    printf("%zu\n", sizeof number);   // typically 4
    printf("%zu\n", sizeof(double));  // typically 8

    return 0;
}
```

`sizeof` returns a `size_t` — always print it with `%zu`. See the `size_t`
note in [Strings](../strings/STRINGS.md) and the type-size table in
[Data Types](../misc/DATATYPES.md).

---

## 5. Two Ways to Run Out of Memory

### A Stack Overflow

Because the stack is limited in size, calling functions too deeply — most
often from a recursive function with no working base case — can exhaust it.

```c
void forever(void)
{
    forever();   // no base case — crashes with a stack overflow
}
```

See the base-case rule in [Functions](../functions/FUNCTIONS.md).

### A Memory Leak

Because the heap is *not* cleaned up automatically, forgetting to `free()`
memory you `malloc()`'d leaves it reserved for no reason, for as long as
the program keeps running.

```c
int *numbers = malloc(100 * sizeof *numbers);

// ... used, but free(numbers); was never called
```

A short-lived command-line program might get away with this — the
operating system reclaims everything when it exits — but on a long-running
program, or a memory-constrained microcontroller, a leak will eventually
cause it to run out of memory entirely.

---

## 6. Memory on a Microcontroller

An Arduino Uno has far less memory than a laptop — its ATmega328P chip has
about 2 KB of RAM in total, shared between the stack, the heap, and every
global variable in your sketch. That's roughly 30,000 times less RAM than a
typical modern computer. This is why embedded C code:

* avoids `malloc()`/`free()` when it can, preferring fixed-size arrays and
  global variables instead — a leak that a desktop OS would shrug off can
  crash a microcontroller in seconds;
* uses the smallest integer type that fits the job — `uint8_t` instead of
  `int` when the value only needs to hold `0`–`255` (see
  [Data Types](../misc/DATATYPES.md));
* keeps recursion shallow, since the stack is small too.

See [Registers](../registers/REGISTERS.md) and
[Arduino](../arduino/ARDUINO.md).

---

## Summary

```text
Stack     local variables, function calls — automatic, fast, limited size
Heap      malloc()/free() memory — manual, flexible, must be freed
Static    globals and static locals — exist for the whole program
Code      your compiled instructions
```

Rules to remember:

* A variable's *scope* is where its name is visible; its *lifetime* is how
  long its memory actually exists — they are not the same thing.
* Stack memory is reclaimed automatically when a function returns; heap
  memory is not — you must `free()` it yourself.
* `static` makes a local variable keep its value between calls.
* Memory is especially precious on a microcontroller — favor fixed-size,
  right-sized types over dynamic allocation.

---

## Coming Soon

### Where Does Arduino Store Your Variables?

*Coming soon — part of the "Electronics and Computer Architecture Sequence"
placeholders in [Electronics](../electronics/ELECTRONICS.md).*

---

## Programs

This folder doesn't have an example `.c` file yet. Create `memory.c` and
try the `static` counter example above — call the function three times
from `main()` and watch the count persist between calls.

## Compile

```bash
clang -Wall -Wextra -Wpedantic -std=c17 memory.c -o memory
```

## Run

```bash
./memory
```
