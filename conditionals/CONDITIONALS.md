# CONDITIONALS

A **conditional** lets a program make a decision: run one block of code if
something is true, and skip it (or run something else) if it isn't.

```c
if (temperature > 30) {
    printf("It's hot!\n");
}
```

Conditionals depend on the comparison and logical operators covered in
[Operators](../operators/OPERATORS.md) — `==`, `!=`, `<`, `>`, `&&`, `||`,
and `!`.

---

## 1. `if`

```c
#include <stdio.h>

int main(void)
{
    int age = 16;

    if (age >= 13) {
        printf("Teenager or older\n");
    }

    return 0;
}
```

The code inside `{ }` only runs when the condition in `( )` is true (any
non-zero value). If the condition is false (`0`), the block is skipped
entirely.

---

## 2. `if` / `else`

`else` runs when the `if` condition is false.

```c
#include <stdio.h>

int main(void)
{
    int battery_percent = 15;

    if (battery_percent > 20) {
        printf("Battery OK\n");
    } else {
        printf("Battery low!\n");
    }

    return 0;
}
```

Output:

```text
Battery low!
```

---

## 3. `else if` — Checking Several Conditions

```c
#include <stdio.h>

int main(void)
{
    int score = 72;

    if (score >= 90) {
        printf("Grade: A\n");
    } else if (score >= 80) {
        printf("Grade: B\n");
    } else if (score >= 70) {
        printf("Grade: C\n");
    } else {
        printf("Grade: F\n");
    }

    return 0;
}
```

Output:

```text
Grade: C
```

C checks each condition **in order** and stops at the first one that is
true. Once `score >= 70` matches, the remaining `else if` and `else`
branches are skipped, even if they would also have been true.

---

## 4. Nested Conditionals

An `if` can contain another `if`.

```c
#include <stdio.h>

int main(void)
{
    int age = 16;
    int has_permission_slip = 1;

    if (age >= 13) {
        if (has_permission_slip) {
            printf("Allowed in the lab\n");
        } else {
            printf("Need a permission slip\n");
        }
    } else {
        printf("Too young for this class\n");
    }

    return 0;
}
```

The same logic is often clearer written with `&&`:

```c
if (age >= 13 && has_permission_slip) {
    printf("Allowed in the lab\n");
}
```

Prefer combining conditions with `&&` / `||` when it doesn't hurt
readability — fewer nested `{ }` levels is easier to follow.

---

## 5. The Dangling `else`

Indentation is for humans; the compiler only cares about `{ }`. This is a
classic trap:

```c
if (a > 0)
    if (b > 0)
        printf("Both positive\n");
else
    printf("a is not positive\n");   // Actually attaches to the inner if!
```

An `else` always belongs to the **nearest** unmatched `if`, no matter how
it's indented. Always use braces, even for one-line bodies, to avoid this:

```c
if (a > 0) {
    if (b > 0) {
        printf("Both positive\n");
    }
} else {
    printf("a is not positive\n");
}
```

---

## 6. The Ternary Operator: `? :`

A compact way to choose between two values.

```c
condition ? value_if_true : value_if_false
```

```c
#include <stdio.h>

int main(void)
{
    int age = 16;

    const char *category = (age >= 18) ? "adult" : "minor";

    printf("%s\n", category);

    return 0;
}
```

Output:

```text
minor
```

This is equivalent to:

```c
const char *category;

if (age >= 18) {
    category = "adult";
} else {
    category = "minor";
}
```

The ternary operator is best for short, simple choices. For anything more
than one condition, a normal `if` / `else` is easier to read.

---

## 7. `switch` — Choosing Among Several Exact Values

`switch` compares one value against a list of exact matches. It reads more
cleanly than a long `else if` chain when you're checking one variable
against many specific values.

```c
#include <stdio.h>

int main(void)
{
    int day = 3;

    switch (day) {
        case 1:
            printf("Monday\n");
            break;
        case 2:
            printf("Tuesday\n");
            break;
        case 3:
            printf("Wednesday\n");
            break;
        default:
            printf("Some other day\n");
            break;
    }

    return 0;
}
```

Output:

```text
Wednesday
```

### Don't Forget `break`

Without `break`, execution **falls through** into the next `case`, running
every case below it until it hits a `break` or the end of the `switch`.

```c
switch (day) {
    case 1:
        printf("Monday\n");
        // no break — falls through!
    case 2:
        printf("Tuesday\n");
        break;
}
```

If `day` is `1`, this prints **both** `Monday` and `Tuesday`. Sometimes
fall-through is intentional (grouping several cases together), but for
beginners it is almost always a bug. Always add `break` unless you have a
specific reason not to.

```c
switch (day) {
    case 6:
    case 7:
        printf("Weekend\n");
        break;
    default:
        printf("Weekday\n");
        break;
}
```

Here, `case 6` falls through into `case 7` on purpose — both print
`Weekend`.

`switch` only works with integer types (`int`, `char`, `enum`) and constant
`case` values. It cannot switch on a `double` or a string.

---

## 8. A Practical Example: Reading a Button

```c
const int BUTTON_PIN = 2;
const int LED_PIN = 13;

void setup()
{
    pinMode(BUTTON_PIN, INPUT);
    pinMode(LED_PIN, OUTPUT);
}

void loop()
{
    int button_state = digitalRead(BUTTON_PIN);

    if (button_state == HIGH) {
        digitalWrite(LED_PIN, HIGH);
    } else {
        digitalWrite(LED_PIN, LOW);
    }
}
```

Every Arduino sketch that reacts to a sensor, a button, or a timer is built
from exactly this pattern: read a value, then use a conditional to decide
what to do about it. See [Arduino](../arduino/ARDUINO.md).

---

## Summary

```text
if (condition) { ... }
if (condition) { ... } else { ... }
if (condition) { ... } else if (condition) { ... } else { ... }
condition ? value_if_true : value_if_false
switch (value) { case X: ...; break; default: ...; }
```

Rules to remember:

* `else` attaches to the nearest `if` — use `{ }` to make this unambiguous.
* `switch` needs `break` in each case, or execution falls through.
* Prefer `&&` / `||` over deeply nested `if` statements when it stays readable.
* `switch` only works on integer-like types, not `double` or strings.

---

## Programs

This folder doesn't have an example `.c` file yet. Create `conditionals.c`
with a few of the examples above — the grading example and the `switch`
weekday example are good ones to start with.

## Compile

```bash
clang -Wall -Wextra -Wpedantic -std=c17 conditionals.c -o conditionals
```

## Run

```bash
./conditionals
```
