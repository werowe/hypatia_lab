# Boolean Algebra Laws and Proofs

Here, `+` means **OR**, multiplication means **AND**, and a prime means **NOT**. Variables can only be `0` or `1`.

The definitions are:

- `x + y = 1` if at least one input is `1`.
- `xy = 1` only if both inputs are `1`.
- `x' = 1` when `x = 0`, and `x' = 0` when `x = 1`.

Because each variable has only two possible values, checking every case proves an identity for all inputs.

## 1. Identity Laws

\[
x+0=x,\qquad x\cdot1=x
\]

| \(x\) | \(x+0\) | \(x\cdot1\) |
|---:|---:|---:|
| 0 | 0 | 0 |
| 1 | 1 | 1 |

Each result equals `x`.

## 2. Domination Laws

\[
x+1=1,\qquad x\cdot0=0
\]

| \(x\) | \(x+1\) | \(x\cdot0\) |
|---:|---:|---:|
| 0 | 1 | 0 |
| 1 | 1 | 0 |

OR with `1` is always `1`; AND with `0` is always `0`.

## 3. Idempotent Laws

\[
x+x=x,\qquad xx=x
\]

| \(x\) | \(x+x\) | \(xx\) |
|---:|---:|---:|
| 0 | 0 | 0 |
| 1 | 1 | 1 |

Repeating the same Boolean condition does not change it.

## 4. Complement Laws

\[
x+x'=1,\qquad xx'=0
\]

| \(x\) | \(x'\) | \(x+x'\) | \(xx'\) |
|---:|---:|---:|---:|
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |

Exactly one of `x` and `x'` is `1`.

## 5. Double Negation

\[
(x')'=x
\]

If `x = 0`, then `x' = 1`, and `(x')' = 0`. If `x = 1`, then `x' = 0`, and `(x')' = 1`. In both cases, `(x')' = x`.

## 6. Commutative Laws

\[
x+y=y+x,\qquad xy=yx
\]

| \(x\) | \(y\) | \(x+y\) | \(y+x\) | \(xy\) | \(yx\) |
|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 | 0 | 0 |
| 1 | 0 | 1 | 1 | 0 | 0 |
| 1 | 1 | 1 | 1 | 1 | 1 |

The order of the inputs does not change OR or AND.

## 7. Associative Laws

\[
(x+y)+z=x+(y+z)
\]

Both sides are `1` exactly when **at least one** of `x`, `y`, or `z` is `1`. Otherwise, both sides are `0`.

\[
(xy)z=x(yz)
\]

Both sides are `1` exactly when **all three** of `x`, `y`, and `z` are `1`. Otherwise, both sides are `0`.

So regrouping ORs or ANDs does not change the result.

## 8. Distributive Laws

### AND Distributes over OR

\[
x(y+z)=xy+xz
\]

Check the two possible values of `x`:

- If `x = 0`, the left side is `0(y + z) = 0`. The right side is `0y + 0z = 0 + 0 = 0`.
- If `x = 1`, the left side is `1(y + z) = y + z`. The right side is `1y + 1z = y + z`.

Both sides agree for either value of `x`.

### OR Distributes over AND

\[
x+yz=(x+y)(x+z)
\]

Again, check `x`:

- If `x = 0`, the left side is `0 + yz = yz`. The right side is `(0 + y)(0 + z) = yz`.
- If `x = 1`, the left side is `1 + yz = 1`. The right side is `(1 + y)(1 + z) = 1\cdot1 = 1`.

Both sides agree for either value of `x`.

## 9. Absorption Laws

\[
x+xy=x
\]

- If `x = 0`, the left side is `0 + 0y = 0`, which equals `x`.
- If `x = 1`, the left side is `1 + 1y = 1`, which equals `x`.

Therefore:

\[
x+xy=x
\]

The dual law is:

\[
x(x+y)=x
\]

- If `x = 0`, the left side is `0(0 + y) = 0`, which equals `x`.
- If `x = 1`, the left side is `1(1 + y) = 1`, which equals `x`.

## 10. De Morgan’s Laws

### NOT of AND

\[
(xy)'=x'+y'
\]

| \(x\) | \(y\) | \(xy\) | \((xy)'\) | \(x'\) | \(y'\) | \(x'+y'\) |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 1 | 1 | 1 | 1 |
| 0 | 1 | 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 | 1 | 1 |
| 1 | 1 | 1 | 0 | 0 | 0 | 0 |

The `(xy)'` and `x' + y'` columns match in every case.

### NOT of OR

\[
(x+y)'=x'y'
\]

| \(x\) | \(y\) | \(x+y\) | \((x+y)'\) | \(x'\) | \(y'\) | \(x'y'\) |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 1 | 1 | 1 | 1 |
| 0 | 1 | 1 | 0 | 1 | 0 | 0 |
| 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| 1 | 1 | 1 | 0 | 0 | 0 | 0 |

The `(x + y)'` and `x'y'` columns match in every case.

In circuit terms, when you complement a series-parallel switch condition, **swap series and parallel and complement each switch**.

## 11. Useful Simplification: \(xy+xy'=x\)

Factor out `x`, then use the complement and identity laws:

\[
\begin{aligned}
xy+xy' &= x(y+y') &&\text{Distributive law}\\
       &= x\cdot1 &&\text{Complement law: } y+y'=1\\
       &= x &&\text{Identity law}
\end{aligned}
\]

## 12. Useful Simplification: \(x+x'y=x+y\)

Check the two values of `x`:

- If `x = 0`, then `x'y = 1\cdot y = y`, and `x + y = 0 + y = y`.
- If `x = 1`, then `x'y = 0\cdot y = 0`, so `x + x'y = 1 + 0 = 1`, and `x + y = 1 + y = 1`.

Thus both sides agree for every `x`, `y`:

\[
x+x'y=x+y
\]

## Quick Reference for Simplification

| Law | Rule |
|---|---|
| Identity | \(x+0=x;\quad x1=x\) |
| Domination | \(x+1=1;\quad x0=0\) |
| Idempotent | \(x+x=x;\quad xx=x\) |
| Complement | \(x+x'=1;\quad xx'=0\) |
| Double negation | \((x')'=x\) |
| Commutative | \(x+y=y+x;\quad xy=yx\) |
| Associative | \((x+y)+z=x+(y+z);\quad (xy)z=x(yz)\) |
| Distributive | \(x(y+z)=xy+xz;\quad x+yz=(x+y)(x+z)\) |
| Absorption | \(x+xy=x;\quad x(x+y)=x\) |
| De Morgan | \((xy)'=x'+y';\quad(x+y)'=x'y'\) |
| Useful consequence | \(xy+xy'=x;\quad x+x'y=x+y\) |

These are Boolean identities: `+` is OR, so `1 + 1 = 1`, not 2.
