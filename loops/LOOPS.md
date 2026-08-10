# LOOPS

A **loop** repeats a block of code, either a fixed number of times or until
some condition changes. Loops are what let a program blink an LED forever,
read every character of a file, or scan every element of an array.

---

## 1. `while`

A `while` loop checks its condition **before** each pass. If the condition
is false the first time, the body never runs at all.

```c
#include <stdio.h>

int main(void)
{
    int count = 0;

    while (count < 5) {
        printf("%d\n", count);
        count++;
    }

    return 0;
}
```

Output:

```text
0
1
2
3
4
```

A `while` loop needs three things, or it never ends:

```text
1. A starting value      (count = 0)
2. A condition to check  (count < 5)
3. Something that moves toward ending it   (count++)
```

Forget step 3, and you get an **infinite loop**:

```c
int count = 0;

while (count < 5) {
    printf("%d\n", count);
    // forgot count++ — this never stops!
}
```

---

## 2. `do while`

A `do while` loop checks its condition **after** each pass, so the body
always runs at least once — useful for things like "ask the user for input,
and keep asking until they give a valid answer."

```c
#include <stdio.h>

int main(void)
{
    int number;

    do {
        printf("Enter a number from 1-10: ");
        scanf("%d", &number);
    } while (number < 1 || number > 10);

    printf("You entered %d\n", number);

    return 0;
}
```

Notice the semicolon after `while (...)` in a `do while` — it's easy to
forget.

---

## 3. `for`

A `for` loop packs the starting value, the condition, and the update into
one line. It is the most common loop for "repeat exactly N times."

```c
for (initialization; condition; update) {
    // body
}
```

```c
#include <stdio.h>

int main(void)
{
    for (int i = 0; i < 5; i++) {
        printf("%d\n", i);
    }

    return 0;
}
```

Output:

```text
0
1
2
3
4
```

This is exactly equivalent to the `while` loop in section 1 — `for` is just
a more compact way to write the same three steps.

### Counting Down

```c
for (int i = 10; i > 0; i--) {
    printf("%d\n", i);
}

printf("Liftoff!\n");
```

### Counting by More Than One

```c
for (int i = 0; i <= 20; i += 2) {
    printf("%d\n", i);   // 0, 2, 4, ... 20
}
```

---

## 4. Looping Over an Array

This is one of the most common uses of a `for` loop in C.

```c
#include <stdio.h>

int main(void)
{
    int scores[5] = {88, 92, 79, 65, 100};
    size_t length = sizeof scores / sizeof scores[0];

    for (size_t i = 0; i < length; i++) {
        printf("%d\n", scores[i]);
    }

    return 0;
}
```

`sizeof scores / sizeof scores[0]` calculates how many elements are in the
array, so the loop keeps working even if the array's size changes later.
This trick is explained fully in [Arrays](../arrays/ARRAYS.md).

---

## 5. `break` — Exit a Loop Early

```c
#include <stdio.h>

int main(void)
{
    for (int i = 0; i < 100; i++) {
        if (i == 5) {
            break;   // stop the loop immediately
        }

        printf("%d\n", i);
    }

    return 0;
}
```

Output:

```text
0
1
2
3
4
```

`break` exits the **innermost** loop it's inside — it does not stop a loop
further out.

---

## 6. `continue` — Skip to the Next Pass

```c
#include <stdio.h>

int main(void)
{
    for (int i = 0; i < 10; i++) {
        if (i % 2 != 0) {
            continue;   // skip odd numbers
        }

        printf("%d\n", i);
    }

    return 0;
}
```

Output:

```text
0
2
4
6
8
```

`continue` jumps straight to the loop's update step (`i++`), skipping
whatever code comes after it in the body.

---

## 7. Nested Loops

A loop can contain another loop. This is how you work through a grid,
a multiplication table, or a pattern of stars.

```c
#include <stdio.h>

int main(void)
{
    for (int row = 1; row <= 3; row++) {
        for (int col = 1; col <= 3; col++) {
            printf("%d ", row * col);
        }
        printf("\n");
    }

    return 0;
}
```

Output:

```text
1 2 3
2 4 6
3 6 9
```

The **outer** loop runs once per row; the **inner** loop runs completely
(all three columns) for every single pass of the outer loop.

---

## 8. An Intentional Infinite Loop: `for (;;)`

Sometimes you want a loop that never stops on its own — you rely on
`break`, `return`, or an external event (like power being cut) to end it.

```c
for (;;) {
    // runs forever
}
```

This should look familiar — it's exactly what an Arduino sketch's `loop()`
function is. The Arduino runtime calls `loop()` over and over, forever,
after `setup()` runs once:

```c
void setup()
{
    pinMode(13, OUTPUT);
}

void loop()
{
    digitalWrite(13, HIGH);
    delay(500);
    digitalWrite(13, LOW);
    delay(500);
}
```

This blinks the built-in LED on and off every half second, forever — an
infinite loop is not a bug here, it's the entire point. See
[Arduino](../arduino/ARDUINO.md).

---

## 9. Reading Input Until It Runs Out

A very common C pattern reads one item at a time in the loop's condition
itself:

```c
#include <stdio.h>

int main(void)
{
    int c;

    while ((c = getchar()) != EOF) {
        putchar(c);
    }

    return 0;
}
```

`getchar()` reads one character and returns it. When there is no more
input, it returns the special value `EOF` ("end of file"), which stops the
loop. This exact program lives in this course as
[`snippets/copy.c`](../snippets/copy.c) — see
[Snippets](../snippets/SNIPPETS.md) for a full walkthrough.

---

## Summary

```text
while (condition) { ... }         checks first, may run zero times
do { ... } while (condition);     checks last, always runs once
for (init; condition; update)     compact counted loop
break;                            exit the loop immediately
continue;                         skip to the next pass
for (;;) { ... }                  intentional infinite loop
```

Rules to remember:

* Every loop needs a condition that can eventually become false — or a
  `break` — or it never ends.
* `for` is best when you know how many times to repeat.
* `while` is best when you're repeating "until something happens."
* `do while` guarantees at least one pass.
* `break` exits only the loop it's directly inside; nested loops need their
  own `break` for each level.

---

## Programs

This folder doesn't have an example `.c` file yet. Create `loops.c` and
try the multiplication table and countdown examples above. For a real,
already-written loop example, see
[`snippets/copy.c`](../snippets/copy.c), described in
[Snippets](../snippets/SNIPPETS.md).

## Compile

```bash
clang -Wall -Wextra -Wpedantic -std=c17 loops.c -o loops
```

## Run

```bash
./loops
```
