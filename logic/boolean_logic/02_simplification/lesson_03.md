# Lesson 3: Simplify an existing circuit

[Course home](../../boolean_logic.md) | [Previous](../01_algebra/lesson_02.md) | [Next](lesson_04.md)

**Reading:** Whitesitt 4-3, pp. 79–83. Skip 4-4. **Time:** 120 minutes.

## Goals

Translate a series-parallel network into algebra, remove redundant contacts, redraw the circuit and verify unchanged behaviour.

## 1. The engineering task (15 minutes)

A circuit may work and still contain unnecessary contacts. Our method is:

1. Label the controls and identify linked contacts.
2. Write an expression from the actual connections.
3. Simplify the expression with Boolean laws.
4. Draw a network for the new expression.
5. Compare all input cases.

The test is equal closure conditions, not equal resistance or current. Two equivalent ideal networks can have different electrical properties.

## 2. Worked simplification (25 minutes)

Start with f = xy + xy' + x'z.

| Step | Reason |
|---|---|
| f = x(y + y') + x'z | Factor x |
| f = x + x'z | Complement and identity |
| f = (x + x')(x + z) | Distribute OR over AND |
| f = x + z | Complement and identity |

The original expression uses six contact occurrences: xy has two, xy' has two, and x'z has two. The final network uses two parallel contacts. It still has the same three named inputs in its original specification, but y is no longer needed.

| x | y | z | Original f | x + z |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 1 |
| 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 0 | 1 | 1 | 1 |
| 1 | 1 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 1 |

## 3. Factor before building (20 minutes)

Consider g = xy + xz = x(y + z). Either expression works. A direct series-parallel drawing of the expanded expression uses four contacts; the factored form uses three.

Count contacts, not only distinct letters. A circuit may need two contacts driven by the same control. A simulator with independent toggles must have those contacts linked or updated consistently.

For electronic logic gates, contact count is not automatically chip count or speed. An inverter might be shared, available gates come in packages, and extra gate levels introduce delay.

## 4. Practical comparison (40 minutes)

In pairs, simplify f = (x + y)(x + y') + x'z.

Student 1 draws and tests the original network. Student 2 derives and draws a simpler one. Compare the eight rows. Swap roles for g = x(y + z) + xy'.

Each submission must include the original expression, proof, both drawings, contact counts and complete verification table.

## 5. Debugging discussion (10 minutes)

Why does removing a contact sometimes preserve behaviour? Why can a visually shorter drawing fail? What would happen if two contacts labelled x were operated independently?

## 6. Exit check (10 minutes)

Simplify xy + xy'z. Do not assume the answer is x. Explain which condition still limits the output.

**Homework:** [Simplification exercises](exercises.md), S1–S4.
