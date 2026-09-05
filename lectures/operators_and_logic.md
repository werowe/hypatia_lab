# Class 4: Math, Comparisons, and Logic

Operators calculate values, compare values, and combine conditions.

---

## Arithmetic operators

```c
int a = 17;
int b = 5;
```

| Operator | Meaning | Example | Result |
|:---:|---|---|---:|
| `+` | add | `a + b` | 22 |
| `-` | subtract | `a - b` | 12 |
| `*` | multiply | `a * b` | 85 |
| `/` | divide | `a / b` | 3 |
| `%` | remainder | `a % b` | 2 |

Create `operators.c`:

```c
#include <stdio.h>

int main(void)
{
    int a = 17;
    int b = 5;

    printf("%d + %d = %d\n", a, b, a + b);
    printf("%d - %d = %d\n", a, b, a - b);
    printf("%d * %d = %d\n", a, b, a * b);
    printf("%d / %d = %d\n", a, b, a / b);
    printf("%d %% %d = %d\n", a, b, a % b);

    return 0;
}
```

Inside a `printf()` format string, `%%` prints one percent sign.

---

## Integer division

Both operands in `17 / 5` are integers, so C discards the fractional part. It
does not round.

```c
printf("%d\n", 17 / 5);        // 3
printf("%.2f\n", 17.0 / 5.0); // 3.40
```

Cast an integer to `double` when a calculation needs a fractional result:

```c
int correct = 17;
int questions = 20;

double percentage = (double) correct / questions * 100;
printf("%.1f%%\n", percentage); // 85.0%
```

Never divide by zero.

---

## Modulo

`%` returns the remainder after integer division.

```c
if (number % 2 == 0)
{
    printf("even\n");
}
```

Modulo can also wrap a position back to zero:

```c
int nextPosition = (position + 1) % 4;
```

When `position` is `3`, `nextPosition` is `0`. This is useful when cycling
through four LEDs or four array positions.

---

## Updating variables

These pairs mean the same thing:

```c
score = score + 5;
score += 5;

score = score - 2;
score -= 2;

score = score * 3;
score *= 3;
```

Adding and subtracting one have shorter forms:

```c
count++;
count--;
```

Multiplication, division, and modulo happen before addition and subtraction.
Use parentheses to make the intended order clear.

```c
double average = (first + second + third) / 3.0;
```

---

## Comparison operators

A comparison asks a question. It produces `1` when true and `0` when false.

| Operator | Meaning |
|:---:|---|
| `==` | equal to |
| `!=` | not equal to |
| `>` | greater than |
| `<` | less than |
| `>=` | greater than or equal to |
| `<=` | less than or equal to |

One equals sign assigns. Two equals signs compare.

```c
score = 10; // store 10
score == 10 // compare score with 10
```

---

## `if`, `else if`, and `else`

```c
if (temperature > 30)
{
    printf("hot\n");
}
else if (temperature >= 20)
{
    printf("warm\n");
}
else
{
    printf("cool\n");
}
```

C checks from top to bottom and runs the first matching branch.

---

## Logical operators

Logical operators combine or reverse conditions.

| Operator | Name | True when... |
|:---:|---|---|
| `&&` | AND | both conditions are true |
| `||` | OR | at least one condition is true |
| `!` | NOT | the condition is false |

```c
if (age >= 13 && hasPermission)
{
    printf("student may join\n");
}

if (day == 6 || day == 7)
{
    printf("weekend\n");
}

if (!isRaining)
{
    printf("no umbrella needed\n");
}
```

In C, zero is false and every nonzero value is true.

---

## Ranges and grouped conditions

This mathematical notation does not work as intended in C:

```c
13 <= age <= 19 // wrong
```

Write both comparisons:

```c
age >= 13 && age <= 19
```

Use parentheses to show how a larger condition is grouped:

```c
if ((age >= 13 && hasPermission) || isTeacher)
{
    printf("access allowed\n");
}
```

---

## Short-circuit evaluation

C stops evaluating `&&` as soon as one part is false. It stops evaluating `||`
as soon as one part is true.

```c
if (divisor != 0 && number / divisor > 10)
{
    printf("large quotient\n");
}
```

If `divisor != 0` is false, C does not perform the division. Order matters.

---

## Complete example: Arduino-style alarm logic

```c
#include <stdio.h>

int main(void)
{
    int temperature = 42;
    int smokeDetected = 0;
    int systemEnabled = 1;

    int danger = temperature >= 40 || smokeDetected;

    if (systemEnabled && danger)
    {
        printf("alarm on\n");
    }
    else if (!systemEnabled)
    {
        printf("system disabled\n");
    }
    else
    {
        printf("conditions normal\n");
    }

    return 0;
}
```

---

## Common mistakes

```c
if (score = 10)                  // wrong: assignment
if (score == 10)                 // correct: comparison

if (ready & enabled)             // bitwise AND
if (ready && enabled)            // logical AND

if (choice == 1 || 2)            // wrong
if (choice == 1 || choice == 2)  // correct
```

---

## Exercises

1. Print the quotient and remainder when `47` is divided by `6`.
2. Calculate the average of four integers without losing the fractional part.
3. Print `teenager` when an age is from 13 through 19.
4. Test whether a number is divisible by both `3` and `5`.
5. Modify the alarm so a pressed emergency button also creates danger.

---

## Summary

- `+`, `-`, `*`, `/`, and `%` perform arithmetic.
- Integer division discards the fractional part.
- `=`, `==`, and `!=` have different jobs.
- Comparisons produce true or false.
- `&&`, `||`, and `!` mean AND, OR, and NOT.
- Parentheses make calculations and conditions clearer.
- `&&` and `||` stop as soon as the result is known.

Next: pointers and dynamic memory.
