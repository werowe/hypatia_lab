# Mathematical Laws and Boolean Algebra

Boolean algebra uses many of the same laws as ordinary mathematics. This makes it easier to understand and simplify digital logic circuits.

The important difference is that Boolean algebra uses only two values:

- **0** means FALSE or OFF.
- **1** means TRUE or ON.

The operations are also different:

- **+** means OR.
- **·** means AND.
- **A̅** means NOT A.

For example:

In ordinary mathematics:

$$
1+1=2
$$

In Boolean algebra:

$$
1+1=1
$$

This is because TRUE OR TRUE is still TRUE.

---

## 1. Laws Shared with Ordinary Algebra

Three familiar mathematical laws also work in Boolean algebra:

1. Commutative law
2. Associative law
3. Distributive law

### Commutative Law

**Changing the order does not change the result.**

Ordinary arithmetic:

$$
A+B=B+A
$$

$$
A\times B=B\times A
$$

Boolean algebra:

$$
A+B=B+A
$$

$$
A\cdot B=B\cdot A
$$

For example, A OR B produces the same result as B OR A.

The order of the inputs does not matter.

### Associative Law

**Changing how expressions are grouped does not change the result.**

Ordinary arithmetic:

$$
(A+B)+C=A+(B+C)
$$

Boolean OR:

$$
(A+B)+C=A+(B+C)
$$

Boolean AND:

$$
(A\cdot B)\cdot C=A\cdot(B\cdot C)
$$

We can group several AND operations or several OR operations in different ways without changing the result.

### Distributive Law

**We can expand expressions using the distributive law.**

Ordinary arithmetic:

$$
A(B+C)=AB+AC
$$

Boolean algebra has this same law:

$$
A\cdot(B+C)=A\cdot B+A\cdot C
$$

But Boolean algebra has an additional distributive law:

$$
A+(B\cdot C)=(A+B)\cdot(A+C)
$$

This is an important difference.

In Boolean algebra, AND distributes over OR, and OR distributes over AND.

### Summary of the Three Laws

| Law | Boolean OR | Boolean AND |
|---|---|---|
| Commutative | $A+B=B+A$ | $AB=BA$ |
| Associative | $(A+B)+C=A+(B+C)$ | $(AB)C=A(BC)$ |
| Distributive | $A+BC=(A+B)(A+C)$ | $A(B+C)=AB+AC$ |

---

## 2. Other Important Boolean Algebra Laws

These laws are particularly useful when simplifying digital logic circuits.

### Identity Law

Adding FALSE to a Boolean value does not change it.

$$
A+0=A
$$

AND with TRUE also leaves the original value unchanged.

$$
A\cdot1=A
$$

For example:

$$
1+0=1
$$

$$
0+0=0
$$

### Domination Law

OR with TRUE always produces TRUE.

$$
A+1=1
$$

AND with FALSE always produces FALSE.

$$
A\cdot0=0
$$

### Idempotent Law

Repeating the same Boolean value does not change the result.

$$
A+A=A
$$

$$
A\cdot A=A
$$

This is different from ordinary arithmetic.

In ordinary arithmetic:

$$
A+A=2A
$$

But Boolean OR does not count how many times a condition is TRUE.

If A is already TRUE, adding another A with OR does not change the result.

This has a practical application in circuit design: repeating an identical logical condition does not add new information.

### Complement Law

A value OR its opposite is always TRUE.

$$
A+\overline A=1
$$

A value AND its opposite is always FALSE.

$$
A\cdot\overline A=0
$$

For example, a switch cannot be both ON and OFF at the same time.

### Double Negation Law

Applying NOT twice returns the original value.

$$
\overline{\overline A}=A
$$

For example:

NOT(FALSE) = TRUE.

NOT(TRUE) = FALSE.

Two NOT operations cancel each other.

### Absorption Law

Some expressions contain conditions that are unnecessary.

For example:

$$
A+A\cdot B=A
$$

We can also write:

$$
A(A+B)=A
$$

These are called absorption laws.

They are useful because they let us remove unnecessary gates from a circuit.

### De Morgan's Laws

De Morgan's laws explain what happens when NOT is applied to an AND or OR expression.

NOT of OR becomes AND of the inverted inputs:

$$
\overline{A+B}=\overline A\cdot\overline B
$$

NOT of AND becomes OR of the inverted inputs:

$$
\overline{A\cdot B}=\overline A+\overline B
$$

These laws are particularly useful when building circuits with NAND and NOR gates.

---

## 3. Summary Table of Boolean Laws

| Law | Boolean Expression |
|---|---|
| Commutative | $A+B=B+A$ |
| Commutative | $AB=BA$ |
| Associative | $(A+B)+C=A+(B+C)$ |
| Associative | $(AB)C=A(BC)$ |
| Distributive | $A(B+C)=AB+AC$ |
| Distributive | $A+BC=(A+B)(A+C)$ |
| Identity | $A+0=A$ |
| Identity | $A\cdot1=A$ |
| Domination | $A+1=1$ |
| Domination | $A\cdot0=0$ |
| Idempotent | $A+A=A$ |
| Idempotent | $A\cdot A=A$ |
| Complement | $A+\overline A=1$ |
| Complement | $A\cdot\overline A=0$ |
| Double negation | $\overline{\overline A}=A$ |
| Absorption | $A+AB=A$ |
| Absorption | $A(A+B)=A$ |
| De Morgan | $\overline{A+B}=\overline A\cdot\overline B$ |
| De Morgan | $\overline{AB}=\overline A+\overline B$ |

---

## 4. Suggested Video Narration

Before we continue, let's connect Boolean algebra to ordinary mathematics.

You already know three important laws of mathematics: the commutative, associative, and distributive laws.

The commutative law says we can change the order of two values.

The associative law says we can change how values are grouped.

And the distributive law tells us how to expand expressions.

**All three laws also work in Boolean algebra.**

But remember, here addition means OR, and multiplication means AND. We are not doing ordinary arithmetic.

For example, in ordinary arithmetic, one plus one equals two. But in Boolean algebra, one OR one equals one.

Boolean algebra also has some special rules that help us simplify circuits.

For example, X OR zero is just X. And X AND one is also X.

We can use these laws to simplify complicated arrangements of switches and logic gates without changing the result.

---

## 5. Why the Idempotent Law Is Different

Consider:

$$
X+X=X
$$

In ordinary arithmetic:

$$
x+x=2x
$$

But Boolean OR is different.

If a switch is already ON, adding another identical ON condition does not change the result.

This is the **idempotent law**.

The same principle works for AND:

$$
X\cdot X=X
$$

If a condition is TRUE, checking the same condition again does not change the logical result.

This law is especially useful when simplifying logic circuits because repeated conditions can often be eliminated.

---

## 6. Why These Laws Matter for Building Computer Circuits

Boolean algebra is useful because we can simplify a logical expression before building the circuit.

For example, consider:

$$
Y=A+(A\cdot B)
$$

At first, this expression appears to require an AND gate and an OR gate.

But the absorption law tells us:

$$
A+AB=A
$$

Therefore:

$$
Y=A
$$

The AND and OR gates are unnecessary.

This is why Boolean algebra is so important in computer design.

**We can use mathematics to reduce the number of logic gates needed to implement a function without changing what that function does.**

Fewer gates can mean simpler circuits, fewer transistors, and potentially less power consumption.

This is one of the foundations of digital circuit design.
