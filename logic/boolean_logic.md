# Boolean Logic: Rules, Simplification, and Circuits

[← Logic lessons](README.md) · [Course home](../README.md)

> **Reference** See chapter 4.  **Switching Algebra** in **Boolean Algebra and its Applications** by J. Eldon Whitesitt.  

Two one-hour lectures connecting Boolean algebra to logic gates and binary adders.

## Notation

| Notation | Meaning | C equivalent |
|---|---|---|
| A · B, or AB | A AND B | `A && B` |
| A + B | A OR B | `A \|\| B` |
| ¬A | NOT A | `!A` |

**Boolean `+` means OR. It does not mean ordinary addition or XOR.**

For example:

- Boolean OR: `1 + 1 = 1`
- Binary addition: `1 + 1 = 10`
- XOR: `1 XOR 1 = 0`

Throughout these lectures, variables have only two possible values: **0 or 1**.

## Lecture 1: Boolean Rules and Simpler Circuits

**Duration:** 60 minutes

### Learning Objectives

By the end of this lecture, students should be able to:

- Explain the basic Boolean rules.
- Verify a rule using a truth table.
- Simplify a Boolean expression.
- Connect an expression to a switch or logic-gate circuit.

### 1. Switches and Boolean Expressions — 10 minutes

Consider ideal switches, where:

- `0` means open.
- `1` means closed.

Two switches in **series** must both be closed:

Y = AB

Two switches in **parallel** allow either switch to complete the circuit:

Y = A + B

#### Discussion

For each arrangement:

1. What happens if one switch is permanently open?
2. What happens if one switch is permanently closed?
3. Does the other switch still control the output?

### 2. Basic Boolean Rules — 15 minutes

#### Identity

| OR | AND |
|---|---|
| A + 0 = A | A · 1 = A |

- OR with 0 leaves the original value.
- AND with 1 leaves the original value.

#### Domination

| OR | AND |
|---|---|
| A + 1 = 1 | A · 0 = 0 |

- OR with 1 always produces 1.
- AND with 0 always produces 0.

#### Idempotence

| OR | AND |
|---|---|
| A + A = A | A · A = A |

Repeating the same condition does not change its value.

#### Complement

| OR | AND |
|---|---|
| A + ¬A = 1 | A · ¬A = 0 |

- A signal is either 1 or 0.
- A signal cannot be both 1 and 0 at the same time.

#### Double Negation

¬(¬A) = A

Inverting a signal twice returns its original value.

#### Discussion

1. Does checking the same condition twice change its result?
2. Can A and NOT A both be true?
3. Can A OR NOT A be false?

### 3. Prove the Rules — 10 minutes

A truth table verifies a Boolean rule by checking **every possible input combination**.

For example:

| A | ¬A | A + ¬A | A · ¬A |
|---|---|---|---|
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |

#### Activity

Choose two rules from the previous section.

For each rule:

1. Construct a truth table.
2. Calculate both sides.
3. Confirm that both sides match in every row.

**Question:** Why is checking one example insufficient to prove a rule?

### 4. Order, Grouping, and Distribution — 10 minutes

#### Commutative Laws

The order of the inputs does not matter.

A + B = B + A

AB = BA

#### Associative Laws

Grouping does not matter when the operations are all OR or all AND.

A + (B + C) = (A + B) + C

A(BC) = (AB)C

#### Distributive Law

A(B + C) = AB + AC

Think of A as a master switch that enables either branch B or branch C.

#### Worked Example

Simplify:

AB + A¬B

Factor out A:

AB + A¬B = A(B + ¬B)

Apply the complement rule:

A(B + ¬B) = A · 1

Apply the identity rule:

A · 1 = A

Therefore:

**AB + A¬B = A**

The output depends only on A. We do not need B or the gates used to process it.

### 5. Practice — 15 minutes

Simplify each expression. Name the rules used.

1. A + 0
2. AB + AB
3. A(B + 1)
4. (A + ¬A)B
5. AB + A¬B

#### Exit Question

Why does Boolean A + A equal A, while ordinary arithmetic x + x usually does not equal x?

### Homework

For practice questions 3–5:

1. Draw a logic-gate circuit for the original expression.
2. Draw the simplified circuit.
3. Verify one simplification using a truth table.

## Lecture 2: De Morgan’s Laws, Absorption, and NAND Circuits

**Duration:** 60 minutes

### Learning Objectives

By the end of this lecture, students should be able to:

- Negate a compound Boolean expression.
- Apply De Morgan’s laws.
- Remove redundant conditions using absorption.
- Construct NOT, AND, and OR using NAND gates.
- Identify the sum and carry expressions of a half adder.

### 1. Review — 5 minutes

Simplify without looking at your notes:

1. A + 1
2. A · 1
3. A · ¬A
4. ¬(¬A)

Explain each answer.

### 2. De Morgan’s Laws — 15 minutes

Suppose an alarm sounds if the door is open OR the window is open.

Let:

- D = door is open.
- W = window is open.

The alarm condition is:

D + W

The alarm is off when neither is open:

¬(D + W) = ¬D · ¬W

#### The Two Laws

| Original expression | Equivalent expression |
|---|---|
| ¬(A + B) | ¬A · ¬B |
| ¬(AB) | ¬A + ¬B |

To negate an entire AND or OR expression:

1. Negate each input.
2. Swap AND with OR.

**Pay attention to parentheses: the NOT must apply to the whole expression being transformed.**

#### Truth-Table Activity

Verify:

¬(A + B) = ¬A · ¬B

Complete the table:

| A | B | A + B | ¬(A + B) | ¬A | ¬B | ¬A · ¬B |
|---|---|---|---|---|---|---|
| 0 | 0 | | | | | |
| 0 | 1 | | | | | |
| 1 | 0 | | | | | |
| 1 | 1 | | | | | |

Compare the columns for ¬(A + B) and ¬A · ¬B.

#### Connection to C

The condition:

    !(doorOpen || windowOpen)

is equivalent to:

    !doorOpen && !windowOpen

### 3. Absorption — 10 minutes

Absorption removes conditions that add nothing to the result.

#### First Absorption Law

A + AB = A

Consider this statement:

> The LED turns on when the button is pressed, OR when the button is pressed and it is dark.

The darkness condition adds nothing. Pressing the button is already sufficient.

#### Algebraic Explanation

A + AB = A · 1 + AB

Factor out A:

A · 1 + AB = A(1 + B)

Since 1 + B = 1:

A(1 + B) = A · 1 = A

#### Second Absorption Law

A(A + B) = A

Using distribution:

A(A + B) = AA + AB

Using idempotence and the first absorption law:

AA + AB = A + AB = A

#### Discussion

Why can removing a redundant condition reduce the number of gates needed in a circuit?

### 4. Build Other Gates from NAND — 15 minutes

A NAND gate produces the inverse of AND:

A NAND B = ¬(AB)

#### NOT from NAND

Connect both NAND inputs to A:

A NAND A = ¬(AA) = ¬A

**Gate count: 1 NAND gate.**

#### AND from NAND

First calculate:

N = A NAND B = ¬(AB)

Then invert N using another NAND gate:

Y = N NAND N = ¬N = AB

**Gate count: 2 NAND gates.**

#### OR from NAND

Invert A and B separately:

P = A NAND A = ¬A

Q = B NAND B = ¬B

Then NAND those results:

Y = P NAND Q = ¬(¬A · ¬B)

By De Morgan’s law:

Y = A + B

**Gate count: 3 NAND gates.**

#### Circuit Activity

Build OR using three NAND gates in a simulator or on a 74HC00.

Test all four input combinations:

| A | B | Expected output: A + B |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 1 |

If using a physical breadboard, allow additional time for wiring and checking connections.

### 5. Simplification Challenge — 15 minutes

Simplify each expression, then verify your answer with a truth table.

1. ¬(A + B)
2. A + AB
3. A(A + B)
4. AB + A¬B + C
5. ¬(¬A · ¬B)

### Connection to Binary Adders

Construct a truth table for:

S = ¬A · B + A · ¬B

Which operation does this represent?

Now compare it with:

C = AB

| A | B | S: sum | C: carry |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |

These are the outputs of a **half adder**:

- Sum is XOR.
- Carry is AND.
- Written as the two-bit number CS, the result of 1 + 1 is 10.

### Homework

1. Verify the second De Morgan law with a truth table:
   ¬(AB) = ¬A + ¬B
2. Draw an OR circuit using only NAND gates.
3. Explain A + AB = A in your own words.
4. Construct a truth table for S = ¬A · B + A · ¬B.
5. Explain why the half-adder sum output alone cannot represent the result of 1 + 1.

## Teacher Answer Key

### Lecture 1 Practice

| Question | Answer | Main rules |
|---|---|---|
| A + 0 | A | Identity |
| AB + AB | AB | Idempotence |
| A(B + 1) | A | Domination, identity |
| (A + ¬A)B | B | Complement, identity |
| AB + A¬B | A | Distribution, complement, identity |

### Lecture 2 Review

| Question | Answer | Main rules |
|---|---|---|
| A + 1 | 1 | Domination |
| A · 1 | A | Identity |
| A · ¬A | 0 | Complement |
| ¬(¬A) | A | Double negation |

### Lecture 2 Simplification Challenge

| Question | Answer | Main rules |
|---|---|---|
| ¬(A + B) | ¬A · ¬B | De Morgan’s law |
| A + AB | A | Absorption |
| A(A + B) | A | Absorption |
| AB + A¬B + C | A + C | Distribution, complement, identity |
| ¬(¬A · ¬B) | A + B | De Morgan’s law, double negation |
