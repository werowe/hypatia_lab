# Control Structures in C

Control structures determine which instructions a program executes and how many times it executes them.

## `if`

Use `if` to execute code only when a condition is true.

```c
int temperature = 25;

if (temperature > 20) {
    printf("It is warm.\n");
}
```

## `if` and `else`

Use `else` when you want different code to run if the condition is false.

```c
int age = 16;

if (age >= 18) {
    printf("You are an adult.\n");
} else {
    printf("You are under 18.\n");
}
```

## `else if`

Use `else if` to test several conditions.

```c
int score = 75;

if (score >= 90) {
    printf("Grade A\n");
} else if (score >= 80) {
    printf("Grade B\n");
} else if (score >= 70) {
    printf("Grade C\n");
} else {
    printf("Try again.\n");
}
```

## Comparison Operators

| Operator | Meaning |
|---|---|
| `==` | Equal to |
| `!=` | Not equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal to |
| `<=` | Less than or equal to |

Be careful:

```c
x = 5;   // Assigns 5 to x
x == 5;  // Tests whether x equals 5
```

## Logical Operators

| Operator | Meaning |
|---|---|
| `&&` | AND |
| `||` | OR |
| `!` | NOT |

```c
int age = 16;
int hasPermission = 1;

if (age >= 13 && hasPermission == 1) {
    printf("Access allowed.\n");
}
```

## `while` Loop

A `while` loop repeats while its condition is true.

```c
int number = 1;

while (number <= 5) {
    printf("%d\n", number);
    number++;
}
```

Output:

```text
1
2
3
4
5
```

The condition is checked before the loop runs. Therefore, a `while` loop might run zero times.

## `do while` Loop

A `do while` loop executes its code before checking the condition.

```c
int number = 1;

do {
    printf("%d\n", number);
    number++;
} while (number <= 5);
```

A `do while` loop always runs at least once.

Notice the semicolon after the condition:

```c
} while (number <= 5);
```

## `for` Loop

A `for` loop is useful when you know how many times the loop should run.

```c
for (int number = 1; number <= 5; number++) {
    printf("%d\n", number);
}
```

A `for` loop has three parts:

```c
for (starting_value; condition; change) {
    // Instructions
}
```

Example:

```c
for (int i = 0; i < 10; i++) {
    printf("%d\n", i);
}
```

This loop:

1. Creates `i` and gives it the value `0`.
2. Runs while `i < 10` is true.
3. Adds `1` to `i` after each repetition.

## Counting Backward

```c
for (int i = 5; i >= 1; i--) {
    printf("%d\n", i);
}
```

## Changing by More Than One

```c
for (int i = 0; i <= 10; i += 2) {
    printf("%d\n", i);
}
```

Output:

```text
0
2
4
6
8
10
```

## `switch`

Use `switch` to compare one value with several possible choices.

```c
int choice = 2;

switch (choice) {
    case 1:
        printf("You selected option 1.\n");
        break;

    case 2:
        printf("You selected option 2.\n");
        break;

    case 3:
        printf("You selected option 3.\n");
        break;

    default:
        printf("Invalid choice.\n");
}
```

Each `case` represents a possible value.

The `break` statement exits the `switch`. Without `break`, the program continues into the next case.

The `default` section runs when none of the cases match.

## `switch` with Characters

```c
char grade = 'B';

switch (grade) {
    case 'A':
        printf("Excellent\n");
        break;

    case 'B':
        printf("Good\n");
        break;

    case 'C':
        printf("Satisfactory\n");
        break;

    default:
        printf("Unknown grade\n");
}
```

## `break`

Use `break` to exit a loop immediately.

```c
for (int i = 1; i <= 10; i++) {
    if (i == 5) {
        break;
    }

    printf("%d\n", i);
}
```

Output:

```text
1
2
3
4
```

## `continue`

Use `continue` to skip the rest of the current repetition.

```c
for (int i = 1; i <= 5; i++) {
    if (i == 3) {
        continue;
    }

    printf("%d\n", i);
}
```

Output:

```text
1
2
4
5
```

## Infinite Loops

A loop continues forever if its condition never becomes false.

```c
while (1) {
    printf("This repeats forever.\n");
}
```

You can use `break` to leave an infinite loop:

```c
int number = 1;

while (1) {
    printf("%d\n", number);

    if (number == 5) {
        break;
    }

    number++;
}
```

## Nested Loops

A loop can be placed inside another loop.

```c
for (int row = 1; row <= 3; row++) {
    for (int column = 1; column <= 3; column++) {
        printf("Row %d, column %d\n", row, column);
    }
}
```

## Complete Example

```c
#include <stdio.h>

int main(void) {
    int choice;

    printf("Choose a number from 1 to 3: ");
    scanf("%d", &choice);

    switch (choice) {
        case 1:
            printf("Counting upward:\n");

            for (int i = 1; i <= 5; i++) {
                printf("%d\n", i);
            }
            break;

        case 2:
            printf("Counting downward:\n");

            for (int i = 5; i >= 1; i--) {
                printf("%d\n", i);
            }
            break;

        case 3:
            printf("Using a while loop:\n");

            int number = 1;

            while (number <= 5) {
                printf("%d\n", number);
                number++;
            }
            break;

        default:
            printf("Invalid choice.\n");
    }

    return 0;
}
```
