# Reference: Binary numbers and arithmetic circuits

[Course home](../../boolean_logic.md)

## Binary numbers

| Decimal | Four-bit binary | Decimal | Four-bit binary |
|---|---|---|---|
| 0 | 0000 | 8 | 1000 |
| 1 | 0001 | 9 | 1001 |
| 2 | 0010 | 10 | 1010 |
| 3 | 0011 | 11 | 1011 |
| 4 | 0100 | 12 | 1100 |
| 5 | 0101 | 13 | 1101 |
| 6 | 0110 | 14 | 1110 |
| 7 | 0111 | 15 | 1111 |

To decode a binary number, add the weights of its 1 positions using ordinary arithmetic. To encode a positive whole number, select powers of two from largest to smallest until their numerical total matches it.

## Gates and notation

| Function | Expression | Book's Chapter 6 label |
|---|---|---|
| Complement | x' | C |
| AND | xy | A |
| OR | x + y | O |
| NAND | (xy)' | Supplement used in this course |
| Exclusive OR | xy' + x'y | Written algebraically here |

Whitesitt uses lettered circles for logical elements. Our block diagrams use descriptive labels but retain his expression syntax. Physical logic levels occupy voltage ranges; “0” is not a promise of exactly zero volts.

## Adder formulas

| Circuit | Inputs | Sum | Carry |
|---|---|---|---|
| Half adder | x, y | s = xy' + x'y | c = xy |
| Full adder | x, y, z (carry-in) | s = x'y'z + x'yz' + xy'z' + xyz | c = xy + xz + yz |

A full adder can also use p = xy' + x'y, then s = pz' + p'z and c = xy + pz. Two half adders and one OR gate implement this form.

The arithmetic correctness condition is: the ordinary numerical total of the inputs equals twice the carry bit plus the sum bit. This sentence uses numerical addition; the expressions in the table use Boolean OR.

## Half adder using five NAND gates

This optional lab connects the course to the existing 74HC00 work. Define:

1. n = (xy)'
2. u = (xn)'
3. v = (yn)'
4. s = (uv)'
5. c = (nn)'

Gate 4 gives xy' + x'y; gate 5 gives xy. Check the four input rows before building a full adder.

A 74HC00 contains four two-input NAND gates. A five-gate half adder needs part of a second package. These equations specify logical connections, not a chip pinout. Use the class's verified pinout and power connections. Define all unused inputs and avoid loading outputs beyond the chip's permitted limits.

## Full adder using nine NAND gates

For students wanting a compact implementation, first compute n, u, v and p exactly as the first four steps above, with p as the first exclusive-OR output. Then:

5. t = (pz)'
6. a = (pt)'
7. b = (zt)'
8. s = (ab)'
9. c = (nt)'

The carry works because (nt)' = xy + pz. This implementation is a supplement, not a claim about the book's historical circuitry. Nine gates require three 74HC00 packages, with three gates unused.

## Four-bit connection rules

Use c0 = 0. In each column, inputs are xi, yi and ci; outputs are si and c(i+1). The complete answer is c4 s3 s2 s1 s0. Carry propagates toward more significant positions. A combinational adder needs no clock to compute a stable answer, but it does need time for signals to settle.

## What comes later

Registers store bits; an accumulator combines storage with addition. Subtraction and multiplication can also be derived from tables. These are extensions, not prerequisites for understanding the half or full adder.
