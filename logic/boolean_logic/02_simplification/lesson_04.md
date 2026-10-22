# Lesson 4: Design a circuit from requirements

[Course home](../../boolean_logic.md) | [Previous](lesson_03.md) | [Next](../03_arithmetic/lesson_05.md)

**Reading:** Whitesitt 4-5, pp. 90–94. Focus on tables, the two-switch light and simple unspecified cases. **Time:** 120 minutes.

## Goals

Translate a verbal requirement into a truth table, obtain a sum of products, simplify it and build the circuit. Distinguish equivalent functions from functions that merely agree on the cases required by a specification.

## 1. From words to a table (15 minutes)

An indicator must light when an enable switch x is on and at least one of request switches y and z is on.

Ask students to fill the eight-row table before writing an equation. Output 1 occurs at 101, 110 and 111, in the order xyz.

## 2. Build one product for each accepted row (25 minutes)

For a row whose output is 1, use the variable for an input 1 and its complement for an input 0. Thus row 101 becomes xy'z. This product accepts exactly that row.

OR together the accepted rows:

f = xy'z + xyz' + xyz.

Now simplify:

f = x[y'z + y(z' + z)] = x(y'z + y) = x(y + z).

The table gives a correct starting expression even when the simpler form is not obvious.


![Accepted minterms and simplified enable-request network](../assets/design.svg)

Each original branch corresponds to one accepted truth-table row.

## 3. Two places control one light (25 minutes)

Either control must change the light's state, whatever the other control's position. Choose the light to be off at 00.

| x | y | f |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

Then f = xy' + x'y. Use linked complementary contacts or changeover switches.

Whitesitt chooses the alternative initial state in his example, giving xy + x'y'. Both meet the requirement that changing either control changes the light. The wording alone does not select the initial state.

This is an indicator experiment at low voltage, not a household mains wiring exercise.


![XOR and its complemented output as switch networks](../assets/xor_contacts.svg)

The left circuit is off at 00; the right is on at 00. Either control toggles the output in both circuits.

## 4. Practical design (35 minutes)

An enable x and two requests y and z control an indicator. The indicator must light only when x = 1 and exactly one request is on.

Make the full table. Derive a sum of products, factor it, draw the switch network, and test all eight inputs. Explain why x(y + z) would fail this specification.

## 5. Optional: unspecified cases (10 minutes)

Suppose a specification requires f = 0 at xy = 00 and f = 1 at 11, while 01 and 10 cannot occur in normal operation. Mark the latter outputs ?. Both f = x and f = y satisfy the stated cases. They are not equal Boolean functions: their outputs differ on the unspecified cases.

Use ? only where the requirement really permits either result. A case that seems unlikely is not automatically unspecified.

## 6. Exit check (10 minutes)

Given the accepted rows 01 and 10, write the expression and identify the operation in words.

**Homework:** [Simplification exercises](exercises.md), S5–S8.
