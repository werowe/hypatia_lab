# Teacher answers

[Course home](../../boolean_logic.md) | [Teacher guide](guide.md)

These answers correspond to the original exercises supplied with this course.

## Boolean algebra

**A1.** In x + 1, a permanent parallel connection provides a path whatever x does. In x0, a permanent series break blocks every path.

**A2.** At xyz = 001, xy + z = 1 while x(y + z) = 0. First network: series x,y branch in parallel with z. Second: x in series with parallel y,z.

**A3.** For xyz ordered 000,001,010,011,100,101,110,111, f = x'y + z has outputs 0,1,1,1,0,1,0,1. The x' column is 1,1,1,1,0,0,0,0.

**A4.** Independent switches admit states 00 and 11; a complementary pair must admit only 01 and 10.

**A5.** (1) x. (2) x by absorption twice. (3) x + yy' = x. (4) (x + x')(x + y) = x + y.

**A6.** (1) (x' + y')z'. (2) x' + y'z. (3) x(y' + z').

**A7.** False. At xyz = 100, the left side is 1 and the right side is 0.

**A8.** yz = xyz + x'yz. Then xy + x'z + yz = xy + xyz + x'z + x'yz = xy(1 + z) + x'z(1 + y) = xy + x'z.

## Simplification and design

**S1.** xy + xy' + x'z = x + x'z = x + z. Six contact occurrences become two in these direct series-parallel realizations.

**S2.** (1) x(y + z), four contacts to three. (2) x[y + z + y'] = x. (3) x + x'z = x + z. (4) x(y + y'z) = x(y + z), four contacts to three.

**S3.** At xyz = 001, the original output is 1 and the replacement is 0. The independent z branch was incorrectly made dependent on x.

**S4.** Factored x(y + z) has three contacts versus four for a direct xy + xz drawing. The truth tables agree, but Boolean analysis says nothing about contact resistance or LED current.

**S5.** f = x(yz' + y'z). In xyz order 000 through 111, outputs are 0,0,0,0,0,1,1,0. Put x in series with parallel branches yz' and y'z.

**S6.** f = x'y'z + x'yz' + xy'z' + xyz. Outputs in ascending xyz order: 0,1,1,0,1,0,0,1. Odd parity flips whenever one input flips.

**S7.** f = x'yz + xy'z + xyz' + xyz. Repeat xyz three times by idempotence and group to obtain yz + xz + xy. Outputs: 0,0,0,1,0,1,1,1.

**S8.** f = x and f = y both satisfy 00 and 11. They disagree at 01 and 10, so they are not equal functions.

## Arithmetic

**R1.** 3 = 0011, 6 = 0110, 9 = 1001, 12 = 1100. The decoded values are 5, 10 and 15.

**R2.** s = xy' + x'y; c = xy. For xy = 00,01,10,11 the pairs cs are 00,01,01,10. OR fails at 11, where s must be 0.

**R3.** (x + y)(xy)' = (x + y)(x' + y') = xx' + xy' + yx' + yy' = xy' + x'y. Direct sum-of-products implementation including carry: two NOTs, three ANDs and one OR, six basic gates. Shared alternative including carry: compute xy with one AND, complement it with one NOT, form x + y with one OR, then AND these for s: four gates. These counts use the stated basic gates, not a packaged exclusive-OR gate.

**R4.** In xyz order 000 through 111, cs is 00,01,01,10,01,10,10,11. The numerical totals are 0,1,1,2,1,2,2,3.

**R5.** The sum is x'y'z + x'yz' + xy'z' + xyz. The carry is the same majority function derived in S7.

**R6.** At 101, p = 1, q = 0, r = 1, s = 0, c = 1. At 111, p = 0, q = 1, r = 0, s = 1, c = 1. Since q = xy, q = 1 implies p = xy' + x'y = 0, hence r = pz = 0.

**R7.** Four full-adder stages with c0 = 0 and c(i+1) passed to the next stage. In column zero the third input is fixed 0, reducing its sum and carry to the half-adder functions.

**R8.** Column zero: 1,1,0 gives s0 = 0,c1 = 1. Each remaining column receives 1,0,1 and gives sum 0 and carry 1. Complete result 10000. Four sum bits alone show 0000 and lose the sixteen's bit.

**R9.** Use the six expected results in Lesson 7. Require labelled carry wiring and a correct explanation of propagation. To store the answer, add suitable register hardware and a controlled capture signal after the adder settles.

**R10.** For half-adder inputs xy = 00,01,10,11: n = 1,1,1,0; u = 1,1,0,1; v = 1,0,1,1; s = 0,1,1,0; c = 0,0,0,1. For the full adder, its eight final output pairs must match R4; inspect intermediate values using the reference equations.

## Lesson exit checks

Lesson 2: x + xy = xy is disproved by x = 1,y = 0. Incorrect De Morgan (x + y)' = x' + y' is disproved by x = 0,y = 1.

Lesson 3: xy + xy'z = x(y + z), not x. At xyz = 100, the function is 0 even though x = 1.

Lesson 6: Input 101 gives cs = 10, meaning two.

## Optional subtraction

d = xy' + x'y, b = x'y. Swapping inputs swaps the roles of 01 and 10, which changes the borrow. The difference is 1 in both cases. A difference bit alone does not distinguish 0 minus 1 from 1 minus 0.
