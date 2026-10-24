# Lesson 5: Binary arithmetic and the half adder

[Course home](../../boolean_logic.md) | [Previous](../02_simplification/lesson_04.md) | [Next](lesson_06.md)

**Reading:** Whitesitt 6-2, whole numbers only, and the half-adder portion of 6-4, pp. 142–143. **Time:** 120 minutes.

## Goals

Read binary place values; distinguish arithmetic addition from Boolean OR; derive the two output functions of a half adder; build and test it.

## 1. Binary place value (20 minutes)

The four positions of a four-bit unsigned number have weights 8, 4, 2 and 1. Thus 1011 in binary represents eleven in decimal: eight plus two plus one. Leading zeros do not change the value.

Practise converting 3, 6, 9 and 12 to four-bit binary. Then decode 0101, 1010 and 1111.

## 2. Adding two one-bit numbers (15 minutes)

In ordinary arithmetic, zero plus zero is zero; zero plus one and one plus zero are one; one plus one is two. Binary writes two as 10.

A one-bit addition therefore needs two output wires: a sum digit s and a carry digit c. The result is read as the two-bit number cs, with c having weight two and s weight one.

| x | y | c | s | Arithmetic result cs |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 00 |
| 0 | 1 | 0 | 1 | 01 |
| 1 | 0 | 0 | 1 | 01 |
| 1 | 1 | 1 | 0 | 10 |

The Boolean expression x + y is OR. It gives 1 at 11, so it is not the sum digit.

## 3. Derive the circuit (25 minutes)

s is 1 at 01 and 10, giving s = x'y + xy'. The carry is 1 only at 11, giving c = xy.

The first expression is exclusive OR. A **half adder** adds two input bits and produces these outputs. “Half” refers to the missing carry-in input; it does not mean half a binary digit.

Gate recipe:

1. Complement x and y.
2. Form xy' and x'y with AND gates.
3. OR those terms to obtain s.
4. AND the original inputs to obtain c.

Another useful expression is s = (x + y)(xy)'. Expand to verify that it gives the same function. This shares the xy result with the carry circuit.


![Half-adder gate schematic](../assets/half_adder.svg)

![Five NAND gates implementing a half adder](../assets/nand_half.svg)

These are IEC rectangular gate symbols: & means AND, ≥1 means OR, and an output circle means NOT. Matching wire labels are connected electrically. These are logical schematics, not breadboard pinouts.

## 4. Practical work (45 minutes)

Build the half adder in a simulator with two input controls and two labelled indicators, **s** and **c**. Test all four rows. Label the outputs so the two-bit answer reads cs.

If using the classroom 74HC00 devices, follow the NAND implementation in the [arithmetic reference](reference.md). Use the existing lab procedure for power, defined inputs and suitable LED loading. Do not connect an LED to an output without a resistor.

## 5. Exit check (15 minutes)

Why are there two outputs? What does cs = 10 mean? Why is OR unsuitable for s? What extra input will be needed to add a column that receives a carry from its neighbour?

**Homework:** [Arithmetic exercises](exercises.md), R1–R3.
