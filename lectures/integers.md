# Class 1: Integers

## What is a data type?

A variable stores information.

Every variable has:

1. A name
2. A value
3. A data type

The **data type** tells the computer what kind of information the variable stores.

In this class, we will use the `int` data type.

---

## Integers

An integer is a whole number.

These are integers:

```text
0
4
17
-3
100
```

These are not integers:

```text
3.5
7.25
```

In C, we use `int` to create an integer variable.

```cpp
int age = 15;
```

This creates a variable with:

- Data type: `int`
- Name: `age`
- Value: `15`

---

## Printing an integer

Upload this program to the Arduino:

```cpp
void setup()
{
    Serial.begin(9600);

    int age = 15;

    Serial.println(age);
}

void loop()
{
}
```

Open the Serial Monitor.

You should see:

```text
15
```

Notice that we write:

```cpp
Serial.println(age);
```

We do not write quotation marks around `age`.

If we wrote:

```cpp
Serial.println("age");
```

the Arduino would print the word:

```text
age
```

---

## Creating several integer variables

A program can contain many variables.

```cpp
void setup()
{
    Serial.begin(9600);

    int students = 16;
    int computers = 10;
    int LEDs = 8;

    Serial.println(students);
    Serial.println(computers);
    Serial.println(LEDs);
}

void loop()
{
}
```

Each variable has its own name and value.

---

## Changing an integer

The value stored in a variable can change.

```cpp
void setup()
{
    Serial.begin(9600);

    int score = 10;

    Serial.println(score);

    score = 15;

    Serial.println(score);
}

void loop()
{
}
```

The output is:

```text
10
15
```

The line:

```cpp
score = 15;
```

replaces the old value with a new value.

We do not write `int` again because the variable already exists.

---

## Calculations with integers

The Arduino can calculate using integer variables.

```cpp
void setup()
{
    Serial.begin(9600);

    int redLEDs = 3;
    int greenLEDs = 4;
    int totalLEDs = redLEDs + greenLEDs;

    Serial.println(totalLEDs);
}

void loop()
{
}
```

The output is:

```text
7
```

We can use the normal arithmetic operators:

| Operator | Meaning |
|---|---|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |

Example:

```cpp
int answer = 6 * 4;
```

The value of `answer` is `24`.

---

## Adding to a variable

We can use the old value to calculate a new value.

```cpp
int score = 10;

score = score + 5;
```

The new value of `score` is `15`.

For adding one, we can write:

```cpp
score = score + 1;
```

We can also write:

```cpp
score++;
```

Both instructions add one.

---

## Example: Counting

```cpp
void setup()
{
    Serial.begin(9600);

    int count = 1;
    Serial.println(count);

    count++;
    Serial.println(count);

    count++;
    Serial.println(count);
}

void loop()
{
}
```

The output is:

```text
1
2
3
```

---

## Exercise 1

Create an integer variable named `temperature`.

Give it the value `25` and print it.

Complete this program:

```cpp
void setup()
{
    Serial.begin(9600);

    // Create the variable here

    // Print the variable here
}

void loop()
{
}
```

---

## Exercise 2

Create these variables:

```text
boys = 7
girls = 9
```

Create another variable named `totalStudents`.

Calculate and print the total number of students.

The output should be:

```text
16
```

---

## Exercise 3

Start with:

```cpp
int points = 5;
```

Add 10 to `points` and print the result.

The output should be:

```text
15
```

---

## Exercise 4

What will this program print?

```cpp
int boxes = 4;
boxes = boxes + 3;
Serial.println(boxes);
```

Write your answer before running the program.

---

## Summary

In this class, we learned:

- A variable stores information.
- A data type tells the computer what kind of information is stored.
- `int` stores a whole number.
- An integer variable has a name and a value.
- The value of a variable can change.
- We can use integers in calculations.

Example:

```cpp
int students = 16;
```

Here:

- `int` is the data type.
- `students` is the variable name.
- `16` is the value.