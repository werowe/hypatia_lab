# Lesson 2: Boolean laws and short proofs

[Course home](../../boolean_logic.md) | [Previous](lesson_01.md) | [Next](../02_simplification/lesson_03.md)

**Reading:** Use 4-2 and the start of 4-3 as circuit context. The laws below supply the background assumed by the book. **Time:** 120 minutes.

## Goals

Apply identity, domination, idempotence and complement laws; factor and expand expressions; prove absorption; use De Morgan's laws without confusing OR with numerical addition.

## 1. Give constants a circuit meaning (20 minutes)

In the ideal switch network, 1 is a permanent conducting connection and 0 is a permanent break.

| Law | OR | AND |
|---|---|---|
| Identity | x + 0 = x | x1 = x |
| Domination | x + 1 = 1 | x0 = 0 |
| Idempotence | x + x = x | xx = x |
| Complement | x + x' = 1 | xx' = 0 |

Explain each using paths. A permanent connection in parallel bypasses x. A permanent break in series prevents conduction.

The identity xx = x assumes both contacts follow the same control x. Two independent contacts cannot be renamed x just to apply this law.

## 2. Expand and factor (20 minutes)

The distributive laws are:

- x(y + z) = xy + xz
- x + yz = (x + y)(x + z)

The second is easy to miss because ordinary numerical algebra does not have the same rule. Verify it with a truth table before using it.

Work through:

xy + xy' = x(y + y') = x1 = x.

At each equals sign ask which law permits the step.

## 3. Prove absorption (20 minutes)

x + xy = x1 + xy = x(1 + y) = x1 = x.

The branch xy cannot add any conducting state: if xy conducts, x already conducts.

The companion law is x(x + y) = x. One proof is:

x(x + y) = xx + xy = x + xy = x.


![Absorption before and after simplification](../assets/absorption.svg)

The branch containing xy cannot conduct unless the separate x branch already conducts.

## 4. Complement a whole condition (20 minutes)

De Morgan's laws:

- (xy)' = x' + y'
- (x + y)' = x'y'

In words: failing to have both inputs is the same as having at least one missing. Having neither input is the same as having both complements.

Example: if an indicator is on when f = x(y + z), the opposite indicator condition is:

f' = [x(y + z)]' = x' + (y + z)' = x' + y'z'.

Complement every part and exchange AND with OR at the level being complemented. Merely adding primes to letters gives the wrong result.

## 5. Student work (30 minutes)

Prove and verify:

1. x + x'y = x + y.
2. (x + y)(x + y') = x.
3. (xy + z)' = (x' + y')z'.

Use a line-by-line algebraic proof for the first two. Use a complete truth table for one result. Then explain one proof as a statement about conducting paths.

## 6. Exit check (10 minutes)

A student writes x + xy = xy. Give one input combination showing the error. A student writes (x + y)' = x' + y'. Give one counterexample.

**Homework:** [Algebra exercises](exercises.md), A5–A8.
