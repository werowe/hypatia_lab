# Class 1: Numbers and Variables in C

C programs can store information and use it later.

In this class, we will learn how to:

- write a simple C program;
- store a whole number;
- print a number;
- change a number; and
- do simple calculations.

---

## Your first C program

Create a file named:

```text
numbers.c
```

Enter this program:

```c
#include <stdio.h>

int main(void)
{
    printf("Hello!\n");

    return 0;
}
```

Run the program.

The output is:

```text
Hello!
```

---

## Understanding the program

This line gives the program access to `printf()`:

```c
#include <stdio.h>
```

This line begins the main part of the program:

```c
int main(void)
```

The program starts running here.

The opening and closing braces contain the instructions:

```c
{
    // Instructions go here.
}
```

This instruction prints text:

```c
printf("Hello!\n");
```

The `\n` moves the cursor to a new line.

This instruction ends the program:

```c
return 0;
```

---

## Instructions end with a semicolon

Most C instructions end with a semicolon:

```c
;
```

For example:

```c
printf("Hello!\n");
return 0;
```

If you forget a semicolon, the compiler will report an error.

---

## Storing a whole number

A program can store a whole number in a variable.

```c
int age = 15;
```

This creates a variable with:

- Data type: `int`
- Name: `age`
- Value: `15`

The word `int` means integer.

An integer is a whole number.

Examples include:

```text
0
7
15
100
-3
```

---

## What is a variable?

A variable is a named place where a program stores a value.

Look at this instruction:

```c
int age = 15;
```

We can imagine it like this:

| Variable name | Stored value |
|---|---:|
| `age` | 15 |

The name `age` helps us remember what the number means.

---

## Printing a whole number

Enter this program:

```c
#include <stdio.h>

int main(void)
{
    int age = 15;

    printf("%d\n", age);

    return 0;
}
```

The output is:

```text
15
```

The `%d` tells `printf()` to print an integer.

The value of `age` replaces `%d`.

---

## Printing text and a number

```c
#include <stdio.h>

int main(void)
{
    int age = 15;

    printf("Age: %d\n", age);

    return 0;
}
```

The output is:

```text
Age: 15
```

The text `Age:` is printed normally.

The `%d` is replaced by the value of `age`.

---

## More integer variables

A program can contain several variables.

```c
int age = 15;
int students = 12;
int score = 90;
```

Each variable has its own name and value.

| Variable name | Stored value |
|---|---:|
| `age` | 15 |
| `students` | 12 |
| `score` | 90 |

---

## Printing several variables

```c
#include <stdio.h>

int main(void)
{
    int age = 15;
    int score = 90;

    printf("Age: %d\n", age);
    printf("Score: %d\n", score);

    return 0;
}
```

The output is:

```text
Age: 15
Score: 90
```

---

## Changing a variable

The value stored in a variable can change.

```c
#include <stdio.h>

int main(void)
{
    int score = 10;

    printf("First score: %d\n", score);

    score = 20;

    printf("Second score: %d\n", score);

    return 0;
}
```

The output is:

```text
First score: 10
Second score: 20
```

This instruction creates the variable:

```c
int score = 10;
```

This instruction gives it a new value:

```c
score = 20;
```

We write `int` when we create the variable.

We do not write `int` again when we change its value.

---

## The equals sign

In this instruction:

```c
int age = 15;
```

The equals sign places the value `15` into the variable `age`.

We can read the instruction like this:

> Store 15 in age.

---

## Adding numbers

C can perform calculations.

```c
#include <stdio.h>

int main(void)
{
    int firstNumber = 5;
    int secondNumber = 3;
    int answer = firstNumber + secondNumber;

    printf("Answer: %d\n", answer);

    return 0;
}
```

The output is:

```text
Answer: 8
```

This instruction adds the two numbers:

```c
int answer = firstNumber + secondNumber;
```

The result is stored in `answer`.

---

## Other calculations

C uses these symbols:

| Calculation | Symbol | Example | Result |
|---|:---:|---|---:|
| Addition | `+` | `5 + 3` | 8 |
| Subtraction | `-` | `5 - 3` | 2 |
| Multiplication | `*` | `5 * 3` | 15 |

Examples:

```c
int answer1 = 5 + 3;
int answer2 = 5 - 3;
int answer3 = 5 * 3;
```

---

## Printing a calculation

```c
#include <stdio.h>

int main(void)
{
    int apples = 4;
    int oranges = 3;
    int totalFruit = apples + oranges;

    printf("Apples: %d\n", apples);
    printf("Oranges: %d\n", oranges);
    printf("Total fruit: %d\n", totalFruit);

    return 0;
}
```

The output is:

```text
Apples: 4
Oranges: 3
Total fruit: 7
```

---

## Variable names

Use names that explain what the values mean.

These names are clear:

```c
int age = 15;
int score = 90;
int numberOfStudents = 12;
```

These names are not clear:

```c
int x = 15;
int a = 90;
int n = 12;
```

A variable name cannot contain a space.

We can write several words like this:

```c
numberOfStudents
```

---

## Complete example

```c
#include <stdio.h>

int main(void)
{
    int studentAge = 15;
    int firstScore = 8;
    int secondScore = 7;
    int totalScore = firstScore + secondScore;

    printf("Student age: %d\n", studentAge);
    printf("First score: %d\n", firstScore);
    printf("Second score: %d\n", secondScore);
    printf("Total score: %d\n", totalScore);

    return 0;
}
```

The output is:

```text
Student age: 15
First score: 8
Second score: 7
Total score: 15
```

---

## Exercise 1

Create this variable:

```c
int age = 14;
```

Print:

```text
Age: 14
```

Use `%d` to print the value.

---

## Exercise 2

Create a variable named `score` and store the value `25` in it.

Print the score.

---

## Exercise 3

Start with:

```c
int number = 10;
```

Print the number.

Then change it to `20` and print it again.

The output should be:

```text
10
20
```

---

## Exercise 4

Create two variables:

```c
int firstNumber = 6;
int secondNumber = 4;
```

Add them and store the result in a variable named `answer`.

Print the answer.

---

## Exercise 5

Create these variables:

```c
int cats = 3;
int dogs = 2;
```

Create a variable named `animals` that stores the total.

Print:

```text
Total animals: 5
```

---

## Exercise 6

Write a program that stores:

- your age;
- your favourite number; and
- the number of students in the class.

Print each value on a separate line.

---

## Summary

In this class, we learned:

- A C program starts running in `main()`.
- `printf()` prints information.
- Most C instructions end with a semicolon.
- A variable is a named place that stores a value.
- `int` stores a whole number.
- `%d` prints an integer.
- A variable's value can change.
- C can perform calculations with numbers.

Example:

```c
int age = 15;
printf("Age: %d\n", age);
```

The variable is named `age`.

It stores the whole number `15`.

