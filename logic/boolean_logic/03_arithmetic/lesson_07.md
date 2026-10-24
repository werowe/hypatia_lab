# Lesson 7: Connect four adders to add four-bit numbers

[Course home](../../boolean_logic.md) | [Previous](lesson_06.md)

**Reading:** Whitesitt 6-4, extending the three-digit example to four bits. **Time:** 120 minutes.

## Goals

Build a four-bit ripple-carry adder; follow carries from the lowest column; interpret a fifth output bit; distinguish computation from storage.

## 1. Name the wires (20 minutes)

Let X = x3 x2 x1 x0 and Y = y3 y2 y1 y0. Spaces separate bit positions, not multiplication. The rightmost bits x0 and y0 have weight one.

Use c0 = 0 for ordinary addition of two numbers. For each column i, use one full adder with inputs xi, yi and ci. Its outputs are si and c(i+1).

| Column | Inputs | Outputs |
|---|---|---|
| 0, weight 1 | x0, y0, c0 = 0 | s0, c1 |
| 1, weight 2 | x1, y1, c1 | s1, c2 |
| 2, weight 4 | x2, y2, c2 | s2, c3 |
| 3, weight 8 | x3, y3, c3 | s3, c4 |

Read the complete unsigned answer as c4 s3 s2 s1 s0. Four input bits represent up to fifteen; adding two such numbers can require five result bits.

The first column can use a half adder instead because c0 is fixed at 0. Four full adders are convenient if one wants identical reusable blocks.


![Four full adders connected by carry wires](../assets/ripple_adder.svg)

The drawing places the least significant bit on the left so carry propagation is easy to trace. Numerical notation still places the most significant bit on the left.

## 2. Trace an example (25 minutes)

Add X = 0111 and Y = 0101: seven plus five.

| Column | xi | yi | Incoming carry | si | Outgoing carry |
|---|---|---|---|---|---|
| 0 | 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 0 | 1 | 0 | 1 |
| 2 | 1 | 1 | 1 | 1 | 1 |
| 3 | 0 | 0 | 1 | 1 | 0 |

The five-bit result is 01100, meaning twelve. The lower four sum bits are 1100.

## 3. Build the adder (45 minutes)

Use four copies of your tested full-adder block. Connect each carry-out only to the next column's carry-in. Give the eight operand inputs separate controls and label all five result indicators.

Test these cases and predict the answers before changing the inputs:

| X | Y | Five-bit result |
|---|---|---|
| 0000 | 0000 | 00000 |
| 0001 | 0001 | 00010 |
| 0011 | 0001 | 00100 |
| 0111 | 0101 | 01100 |
| 1111 | 0001 | 10000 |
| 1111 | 1111 | 11110 |

There are 256 operand pairs. If the simulator supports automated testing, check all pairs against ordinary numerical addition. Otherwise use the cases above and record the carry values for the two cases with long carry propagation.

## 4. Delay and storage (15 minutes)

“Ripple carry” means a carry may have to pass through successive stages. Parallel input wires do not mean all result bits settle instantly. Wait for propagation before reading the result.

This is a combinational adder. It does not remember an answer when inputs change. Storing results requires registers and timing, which are outside this unit. Carry-out c4 indicates that an unsigned result does not fit in four bits; signed overflow is a different topic.

## 5. Demonstration and assessment (15 minutes)

Show a working addition selected by another student. Explain one stage using s = pz' + p'z and c = xy + pz. Then explain how the circuit implements numerical addition even though its internal + operators mean Boolean OR.

**Homework:** [Arithmetic exercises](exercises.md), R7–R9. Optional: [half subtracter](extension_subtraction.md).
