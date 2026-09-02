# Class 2: Characters and Text

In the previous class, we used `int` to store whole numbers.

```cpp
int age = 15;
```

Programs also need to store letters, symbols, words, and sentences.

In this class, we will learn how C stores characters and text.

---

## One character

A character is one letter, number, punctuation mark, or symbol.

Examples of characters include:

```text
A
b
7
?
!
```

In C, we use the `char` data type to store one character.

```cpp
char grade = 'A';
```

This creates a variable with:

- Data type: `char`
- Name: `grade`
- Value: `'A'`

A single character uses **single quotation marks**:

```cpp
'A'
```

---

## Printing a character

```cpp
void setup()
{
    Serial.begin(9600);

    char grade = 'A';

    Serial.println(grade);
}

void loop()
{
}
```

The output is:

```text
A
```

---

## More character examples

```cpp
char firstLetter = 'H';
char answer = 'Y';
char symbol = '?';
char digit = '7';
```

Each variable stores exactly one character.

Notice that this:

```cpp
char digit = '7';
```

stores the character `'7'`.

It does not store the integer `7`.

Compare these two variables:

```cpp
int number = 7;
char digit = '7';
```

They may look similar when printed, but they contain different types of information.

---

## Changing a character

A character variable can change.

```cpp
void setup()
{
    Serial.begin(9600);

    char answer = 'N';

    Serial.println(answer);

    answer = 'Y';

    Serial.println(answer);
}

void loop()
{
}
```

The output is:

```text
N
Y
```

---

## Words and sentences

A `char` stores only one character.

This is correct:

```cpp
char letter = 'A';
```

This is not correct:

```cpp
char name = 'Anna';
```

`Anna` contains four characters, not one.

To store several characters, we write:

```cpp
char name[] = "Anna";
```

For text, we use **double quotation marks**:

```cpp
"Anna"
```

---

## Single and double quotation marks

This is an important rule:

```cpp
char letter = 'A';
char name[] = "Anna";
```

Use:

- Single quotation marks for one character: `'A'`
- Double quotation marks for text: `"Anna"`

Another example:

```cpp
char answer = 'Y';
char message[] = "Yes";
```

---

## Printing text

```cpp
void setup()
{
    Serial.begin(9600);

    char name[] = "Anna";

    Serial.println(name);
}

void loop()
{
}
```

The output is:

```text
Anna
```

---

## Combining integers and text

A program can use different data types.

```cpp
void setup()
{
    Serial.begin(9600);

    char studentName[] = "Anna";
    int studentAge = 14;
    char studentGrade = 'A';

    Serial.print("Name: ");
    Serial.println(studentName);

    Serial.print("Age: ");
    Serial.println(studentAge);

    Serial.print("Grade: ");
    Serial.println(studentGrade);
}

void loop()
{
}
```

The output is:

```text
Name: Anna
Age: 14
Grade: A
```

The program uses three kinds of information:

| Information | Code |
|---|---|
| Whole number | `int studentAge = 14;` |
| One character | `char studentGrade = 'A';` |
| Text | `char studentName[] = "Anna";` |

---

## Text does not perform arithmetic

This stores a number:

```cpp
int value = 10;
```

We can use it in a calculation:

```cpp
value = value + 5;
```

This stores text:

```cpp
char word[] = "10";
```

The characters `"10"` are text. They are not being used as a number.

---

## Example: Student information

```cpp
void setup()
{
    Serial.begin(9600);

    char name[] = "Danylo";
    int age = 15;
    char group = 'B';

    Serial.println("Student information");
    Serial.println("-------------------");

    Serial.print("Name: ");
    Serial.println(name);

    Serial.print("Age: ");
    Serial.println(age);

    Serial.print("Group: ");
    Serial.println(group);
}

void loop()
{
}
```

Change the values so the program prints your information.

---

## Exercise 1

Create a character variable named `firstLetter`.

Store the first letter of your name in it and print it.

Example:

```cpp
char firstLetter = 'A';
```

---

## Exercise 2

Create a variable named `name` that stores your name.

Print it in the Serial Monitor.

Example:

```cpp
char name[] = "Anna";
```

---

## Exercise 3

Create these three variables:

```text
name
age
group
```

Use:

- Text for the name
- An integer for the age
- One character for the group

Print all three values.

---

## Exercise 4

Which lines are correct?

```cpp
char letter = 'B';
char letter = "B";
char name[] = "Bohdan";
int age = 15;
int age = "15";
```

Explain why each incorrect line is wrong.

---

## Exercise 5

Correct the mistakes in this code:

```cpp
char grade = "A";
char studentName = 'Olena';
int age = "14";
```

---

## Summary

In this class, we learned:

- `int` stores a whole number.
- `char` stores one character.
- One character uses single quotation marks.
- Text uses double quotation marks.
- Several characters can be stored together using `char name[]`.

Examples:

```cpp
int age = 15;
char grade = 'A';
char name[] = "Anna";
```

In the next class, we will look more closely at how C stores text.