# OPERATORS

An **operator** is a symbol that tells C to do something with one or more
values, called **operands**.

```c
int total = 5 + 3;
//              ^ operator
//          ^   ^ operands
```

---

## 1. Arithmetic Operators

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` | Addition | `5 + 3` | `8` |
| `-` | Subtraction | `5 - 3` | `2` |
| `*` | Multiplication | `5 * 3` | `15` |
| `/` | Division | `5 / 3` | `1` |
| `%` | Modulo (remainder) | `5 % 3` | `2` |

```c
#include <stdio.h>

int main(void)
{
    int a = 7;
    int b = 2;

    printf("%d\n", a + b);
    printf("%d\n", a - b);
    printf("%d\n", a * b);
    printf("%d\n", a / b);
    printf("%d\n", a % b);

    return 0;
}
```

Output:

```text
9
5
14
3
1
```

### Integer Division Truncates

When both operands of `/` are integers, C throws away the fractional part.
It does not round.

```c
int result = 7 / 2;

printf("%d\n", result);
```

Output:

```text
3
```

To get a fractional answer, at least one operand must be a floating-point
type:

```c
double result = 7.0 / 2;

printf("%f\n", result);
```

Output:

```text
3.500000
```

### `%` Only Works on Integers

`%` gives you the remainder after division. It is extremely useful for:

* deciding whether a number is even or odd;
* wrapping a counter back to `0` (for example, blinking every 4th time
  through a loop);
* extracting individual digits of a number.

```c
int number = 17;

if (number % 2 == 0) {
    printf("Even\n");
} else {
    printf("Odd\n");
}
```

---

## 2. Assignment Operators

| Operator | Meaning | Same as |
|---|---|---|
| `=` | Assign | — |
| `+=` | Add and assign | `x = x + value` |
| `-=` | Subtract and assign | `x = x - value` |
| `*=` | Multiply and assign | `x = x * value` |
| `/=` | Divide and assign | `x = x / value` |
| `%=` | Modulo and assign | `x = x % value` |

```c
int score = 10;

score += 5;   // score = 15
score -= 3;   // score = 12
score *= 2;   // score = 24
score /= 4;   // score = 6
```

---

## 3. Increment and Decrement

`++` adds one; `--` subtracts one.

```c
int count = 0;

count++;   // count = 1
count--;   // count = 0
```

### Prefix vs. Postfix

The position of `++` matters when the result is used immediately.

```c
int a = 5;
int b = ++a;   // a becomes 6 first, then b = 6

int c = 5;
int d = c++;   // d = 5 first, then c becomes 6
```

```c
#include <stdio.h>

int main(void)
{
    int a = 5;
    int b = ++a;   // pre-increment: increment, then use

    printf("a = %d, b = %d\n", a, b);

    int c = 5;
    int d = c++;   // post-increment: use, then increment

    printf("c = %d, d = %d\n", c, d);

    return 0;
}
```

Output:

```text
a = 6, b = 6
c = 6, d = 5
```

When `++` or `--` is used on its own line, as in a loop counter, prefix and
postfix behave the same:

```c
for (int i = 0; i < 5; i++) {
    // i++ and ++i work identically here
}
```

---

## 4. Comparison Operators

Comparison operators compare two values and produce `1` (true) or `0`
(false).

| Operator | Meaning |
|---|---|
| `==` | Equal to |
| `!=` | Not equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal to |
| `<=` | Less than or equal to |

```c
#include <stdio.h>

int main(void)
{
    int age = 16;

    printf("%d\n", age == 16);   // 1 (true)
    printf("%d\n", age != 16);   // 0 (false)
    printf("%d\n", age > 18);    // 0 (false)
    printf("%d\n", age < 18);    // 1 (true)

    return 0;
}
```

### The Classic Mistake: `=` vs. `==`

`=` assigns a value. `==` compares two values. Mixing them up is one of the
most common beginner bugs in C.

```c
int x = 5;

if (x = 10) {    // BUG: this assigns 10 to x, and 10 is "true"
    printf("This always runs!\n");
}
```

Correct:

```c
if (x == 10) {   // compares x to 10
    printf("x is 10\n");
}
```

Turning on compiler warnings helps catch this:

```bash
clang -Wall -Wextra -Wpedantic -std=c17 source.c -o program
```

---

## 5. Logical Operators

Logical operators combine `true`/`false` conditions.

| Operator | Meaning | Example |
|---|---|---|
| `&&` | AND — both must be true | `a > 0 && a < 10` |
| `\|\|` | OR — at least one must be true | `a == 0 \|\| a == 1` |
| `!` | NOT — flips true/false | `!(a == 0)` |

```c
#include <stdio.h>

int main(void)
{
    int age = 16;
    int has_permission = 1;

    if (age >= 13 && age <= 18) {
        printf("Teenager\n");
    }

    if (age < 13 || age > 18) {
        printf("Not a teenager\n");
    } else {
        printf("Teenager\n");
    }

    if (!has_permission) {
        printf("Access denied\n");
    } else {
        printf("Access granted\n");
    }

    return 0;
}
```

Output:

```text
Teenager
Teenager
Access granted
```

### Short-Circuit Evaluation

`&&` and `||` stop as soon as the answer is already known.

```c
int divisor = 0;

if (divisor != 0 && 10 / divisor > 1) {
    printf("Big enough\n");
}
```

Because `divisor != 0` is false, C never evaluates `10 / divisor`, which
would have crashed the program by dividing by zero.

---

## 6. Bitwise Operators (Preview)

C also has operators that work directly on the individual bits of a number.
They look similar to the logical operators but behave very differently and
are essential once you start controlling hardware registers directly.

```text
&    bitwise AND
|    bitwise OR
^    bitwise XOR
~    bitwise NOT
<<   shift left
>>   shift right
```

These are covered fully in [Bits and Bitwise Operations](../bits/BITS.md)
and put to work in [Registers](../registers/REGISTERS.md). Do not confuse
`&&` (logical AND) with `&` (bitwise AND) — they do very different things.

---

## 7. Operator Precedence

Just like in math class, some operators are evaluated before others.

```c
int result = 2 + 3 * 4;

printf("%d\n", result);
```

Output:

```text
14
```

Multiplication happens before addition, exactly like `2 + (3 * 4)`. A
simplified order, from highest to lowest priority:

```text
1. ()                  parentheses
2. ++  --  !           unary operators
3. *  /  %             multiplication, division, modulo
4. +  -                addition, subtraction
5. <  <=  >  >=        comparisons
6. ==  !=               equality
7. &&                  logical AND
8. ||                  logical OR
9. =  +=  -=  ...      assignment
```

When in doubt, use parentheses. They cost nothing and make your intention
obvious to the next person reading the code — including you, next week.

```c
int result = (2 + 3) * 4;   // 20, not 14

printf("%d\n", result);
```

---

## 8. A Practical Example: Reading an Analog Sensor

Operators show up constantly in Arduino code. Here is a sketch that reads a
potentiometer and decides whether it is turned past the halfway point.

```c
const int SENSOR_PIN = A0;
const int LED_PIN = 13;

void setup()
{
    pinMode(LED_PIN, OUTPUT);
    Serial.begin(9600);
}

void loop()
{
    int reading = analogRead(SENSOR_PIN);   // 0 to 1023

    Serial.println(reading);

    if (reading > 511) {
        digitalWrite(LED_PIN, HIGH);
    } else {
        digitalWrite(LED_PIN, LOW);
    }

    delay(100);
}
```

`reading > 511` is a comparison operator, `analogRead()` returns a value
that is compared, and the whole `if` decides `digitalWrite()`'s argument.
This pattern — read, compare, act — is behind almost every Arduino sketch
you will write in this course. See [Arduino](../arduino/ARDUINO.md).

---

## Summary

```text
+  -  *  /  %          arithmetic
=  +=  -=  *=  /=  %=  assignment
++  --                 increment, decrement
==  !=  >  <  >=  <=   comparison
&&  ||  !               logical
&  |  ^  ~  <<  >>     bitwise (see Bits)
```

Rules to remember:

* `=` assigns; `==` compares. Never confuse them.
* Integer division truncates; use a `double` for fractional results.
* `&&` and `||` short-circuit — they stop as soon as the answer is known.
* When precedence is unclear, add parentheses.

---

## Programs

This folder doesn't have an example `.c` file yet. Create `operators.c`,
type in a few of the examples above, and compile it yourself — that's the
best way to see the precedence and truncation rules actually happen.

## Compile

```bash
clang -Wall -Wextra -Wpedantic -std=c17 operators.c -o operators
```

## Run

```bash
./operators
```
