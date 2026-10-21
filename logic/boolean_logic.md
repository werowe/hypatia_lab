# Boolean Algebra and Arithmetic Circuits

Hypatia Academy | From switches to an adder

How can an equation describe a circuit? How can changing that equation remove unnecessary switches? How can a circuit add two numbers?

This course answers those questions in three parts. We begin with switches and Boolean algebra, use algebra to simplify circuits, and finish by building half adders, full adders and a four-bit adder.

## Course map

| Topic | Lessons | Reference and practice |
|---|---|---|
| 1. Boolean algebra | [Lesson 1: Switches and expressions](boolean_logic/01_algebra/lesson_01.md); [Lesson 2: Laws and proofs](boolean_logic/01_algebra/lesson_02.md) | [Reference](boolean_logic/01_algebra/reference.md); [Exercises](boolean_logic/01_algebra/exercises.md) |
| 2. Simplifying circuits | [Lesson 3: Simplify an existing circuit](boolean_logic/02_simplification/lesson_03.md); [Lesson 4: Design from requirements](boolean_logic/02_simplification/lesson_04.md) | [Reference](boolean_logic/02_simplification/reference.md); [Exercises](boolean_logic/02_simplification/exercises.md) |
| 3. Circuits for arithmetic | [Lesson 5: Binary and the half adder](boolean_logic/03_arithmetic/lesson_05.md); [Lesson 6: The full adder](boolean_logic/03_arithmetic/lesson_06.md); [Lesson 7: A four-bit adder](boolean_logic/03_arithmetic/lesson_07.md) | [Reference](boolean_logic/03_arithmetic/reference.md); [Exercises](boolean_logic/03_arithmetic/exercises.md); [Optional subtraction](boolean_logic/03_arithmetic/extension_subtraction.md) |

Each lesson is planned for about two hours, including discussion and practical work. Take longer where needed. Lessons 1–2 can be shortened for students already comfortable with switching expressions.

## Notation used everywhere

| Symbol | Meaning | Example |
|---|---|---|
| `0` | False; an open switch; LOW in the gate model | No conducting path |
| `1` | True; a closed switch; HIGH in the gate model | Conducting path exists |
| `x'` | Complement, or NOT x | If x = 1, x' = 0 |
| `xy` | x AND y | Series switches |
| `x + y` | x OR y | Parallel switches |
| `(x + y)'` | Complement the entire expression | NOT of x OR y |

In Boolean expressions, **+ means OR**, not numerical addition. **1 + 1 = 1** in Boolean algebra. In ordinary binary arithmetic, one plus one is the two-digit number **10**. Arithmetic lessons label the context explicitly.

We write exclusive OR as `xy' + x'y`, following the book's algebraic notation, rather than introducing another operator.  (See [here](boolean_logic/xor.md for an explanation).

## How to work

For a circuit task, submit a labelled circuit, its Boolean expression, a complete truth table and any simplification with a reason for each step. Test every input combination. Simulator screenshots are useful evidence, but do not replace an expression or table.

Use a circuit simulator for linked contacts and larger circuits. A physical LED demonstration needs a low-voltage supply and a current-limiting resistor. Keep the LED and resistor outside the switch network being analysed. Never connect logic-gate outputs together to imitate parallel switches.

## Reading and scope

Based on J. Eldon Whitesitt, *Boolean Algebra and Its Applications*, Chapter 4, **Switching Algebra**, and selected parts of Chapter 6, **Circuits for Arithmetic Computation**. Page numbers below mean printed book pages, not PDF viewer page numbers.

- Core Chapter 4 reading: Sections 4-1 and 4-2 (pp. 75–79), 4-3 (pp. 79–83), and the accessible parts of 4-5 (pp. 90–94).
- Section **4-4 is omitted**. Sections 4-6 and 4-7 are not required.
- Core Chapter 6 reading: whole-number binary in 6-2 (pp. 135–138), complement/AND/OR elements in 6-3 (pp. 138–140), and addition in 6-4 (pp. 142–145).
- Omit the relay flip-flop construction in 6-3, accumulation in 6-6 and multiplication in 6-7. Subtraction in 6-5 is optional.

These are original teaching notes and exercises, not a reproduction of the book. Modern gate diagrams and a NAND implementation supplement the book's notation. The supplied PDF is not included in this package.

[Teacher guide](boolean_logic/teacher/guide.md) | [Answers](boolean_logic/teacher/answers.md)
