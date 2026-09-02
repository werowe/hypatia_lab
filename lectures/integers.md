# Class 3: Character Arrays

In the previous class, we stored text like this:

```cpp
char name[] = "Anna";
```

In this class, we will look inside the text and see how the computer stores each character.

---

## An array stores several values

An array is a group of values stored together.

This is a character array:

```cpp
char name[] = "Anna";
```

The variable `name` contains several characters.

We can imagine it like this:

| Position | Character |
|---:|:---:|
| 0 | A |
| 1 | n |
| 2 | n |
| 3 | a |

Each character has a position.

The first position is `0`, not `1`.

---

## Reading one character

We can use square brackets to select one character.

```cpp
char name[] = "Anna";

Serial.println(name[0]);
```

The output is:

```text
A
```

This prints the character at position `0`.

---

## Reading every character

```cpp
void setup()
{
    Serial.begin(9600);

    char name[] = "Anna";

    Serial.println(name[0]);
    Serial.println(name[1]);
    Serial.println(name[2]);
    Serial.println(name[3]);
}

void loop()
{
}
```

The output is:

```text
A
n
n
a
```

---

## Array positions

For the word `"Arduino"`:

```cpp
char word[] = "Arduino";
```

the positions are:

| Position | Character |
|---:|:---:|
| 0 | A |
| 1 | r |
| 2 | d |
| 3 | u |
| 4 | i |
| 5 | n |
| 6 | o |

Examples:

```cpp
Serial.println(word[0]);  // A
Serial.println(word[3]);  // u
Serial.println(word[6]);  // o
```

---

## Changing one character

We can change a character stored at a particular position.

```cpp
void setup()
{
    Serial.begin(9600);

    char word[] = "cat";

    Serial.println(word);

    word[0] = 'h';

    Serial.println(word);
}

void loop()
{
}
```

The output is:

```text
cat
hat
```

This line:

```cpp
word[0] = 'h';
```

changes the character in position `0`.

It does not replace the entire array. It changes only one character.

---

## Another example

```cpp
char word[] = "car";

word[2] = 't';

Serial.println(word);
```

The output is:

```text
cat
```

The original characters were:

| Position | Character |
|---:|:---:|
| 0 | c |
| 1 | a |
| 2 | r |

We replaced the character at position `2`.

---

## Why text is called a character array

Look at this code:

```cpp
char name[] = "Anna";
```

It is called a **character array** because it contains an array of `char` values.

The computer stores:

```text
A
n
n
a
```

Together, these characters form the text `"Anna"`.

In C, text like this is also called a **string**.

Therefore:

> A string in C is text stored in a character array.

---

## The invisible ending character

The computer needs to know where the text ends.

C places a special invisible character after the final visible character.

It is written:

```cpp
'\0'
```

This character tells the computer:

> The text ends here.

The word `"cat"` is stored like this:

| Position | Character |
|---:|:---:|
| 0 | c |
| 1 | a |
| 2 | t |
| 3 | `'\0'` |

The final character is not the number zero.

It is a special character that marks the end of the text.

---

## Two ways to create the same string

This is the easiest way:

```cpp
char word[] = "cat";
```

The computer automatically adds the invisible ending character.

We could also write every character ourselves:

```cpp
char word[] = {'c', 'a', 't', '\0'};
```

Both lines create the same text.

Normally, we use the easier version:

```cpp
char word[] = "cat";
```

---

## Printing characters with a loop

A loop can print one character at a time.

```cpp
void setup()
{
    Serial.begin(9600);

    char word[] = "Arduino";
    int position = 0;

    while (word[position] != '\0')
    {
        Serial.println(word[position]);
        position++;
    }
}

void loop()
{
}
```

The program starts at position `0`.

It continues until it finds:

```cpp
'\0'
```

The output is:

```text
A
r
d
u
i
n
o
```

---

## Understanding the loop

This is the condition:

```cpp
word[position] != '\0'
```

It means:

> Continue while the current character is not the end of the text.

This line moves to the next position:

```cpp
position++;
```

The positions are:

```text
0, 1, 2, 3, 4, 5, 6
```

When the program reaches `'\0'`, the loop stops.

---

## Complete example

```cpp
void setup()
{
    Serial.begin(9600);

    char studentName[] = "Olena";
    int studentAge = 15;

    Serial.print("Student: ");
    Serial.println(studentName);

    Serial.print("First character: ");
    Serial.println(studentName[0]);

    Serial.print("Age: ");
    Serial.println(studentAge);
}

void loop()
{
}
```

---

## Exercise 1

Create this character array:

```cpp
char city[] = "Kyiv";
```

Print the entire word.

Then print each character separately using:

```cpp
city[0]
city[1]
city[2]
city[3]
```

---

## Exercise 2

Create this word:

```cpp
char word[] = "dog";
```

Change one character so that the program prints:

```text
dig
```

Which position must you change?

---

## Exercise 3

Start with:

```cpp
char word[] = "hat";
```

Change it to:

```text
hot
```

Change only one character in the array.

---

## Exercise 4

Consider this array:

```cpp
char board[] = "Arduino";
```

Answer these questions before running the program:

1. What is stored at `board[0]`?
2. What is stored at `board[2]`?
3. What is stored at `board[6]`?
4. At which position is the invisible `'\0'`?

---

## Exercise 5

Write a loop that prints every character in your name on a separate line.

Start with:

```cpp
char name[] = "YourName";
int position = 0;
```

Stop the loop when it reaches:

```cpp
'\0'
```

---

## Summary

In this class, we learned:

- An array stores several values together.
- A character array stores several characters.
- Array positions begin at `0`.
- We use square brackets to access one character.
- We can change an individual character.
- A string in C is text stored in a character array.
- C adds `'\0'` to mark the end of the text.

Example:

```cpp
char name[] = "Anna";
```

The computer stores:

```text
Position 0: A
Position 1: n
Position 2: n
Position 3: a
Position 4: '\0'
```

The invisible `'\0'` tells the computer where the text ends.
