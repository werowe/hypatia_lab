# Practice: Arithmetic circuits

[Course home](../../boolean_logic.md)

**R1.** Convert decimal 3, 6, 9 and 12 into four-bit binary. Convert binary 0101, 1010 and 1111 into decimal.

**R2.** Complete a half-adder table and derive s and c from its output-1 rows. Explain why x + y cannot replace s.

**R3.** Prove xy' + x'y = (x + y)(xy)'. Draw gate networks for both expressions. Count the basic gates used if NOT, two-input AND and two-input OR are available, sharing intermediate results with c where possible.

**R4.** Make a full-adder table. For each row, read cs as a binary number and check it against the numerical input total.

**R5.** Starting from the full-adder table, derive the four-term sum function and simplify the carry to xy + xz + yz.

**R6.** Connect two half adders and one OR gate. Trace the intermediate values p, q and r for inputs 101 and 111. Prove q and r cannot both be 1.

**R7.** Draw a four-bit ripple-carry adder. Label all operand, sum and carry wires. Show why a half adder is sufficient for the first column when c0 = 0.

**R8.** Trace every column for 1111 plus 0001. Explain what is lost if only four sum indicators are fitted.

**R9.** Final project: demonstrate a four-bit adder. Submit a block diagram, one full-adder truth table, the equations used, and results for the six test pairs in Lesson 7. Explain what extra hardware would be required to store the answer. Automated verification of all 256 pairs is an optional extension.

**Optional R10.** Verify the five-NAND half adder or nine-NAND full adder in the reference. Submit all four or eight input rows, including intermediate signals.
