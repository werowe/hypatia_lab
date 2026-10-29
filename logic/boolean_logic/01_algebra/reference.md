# Boolean algebra reference

[Course home](../../boolean_logic.md)

## Meaning and order

A variable takes one of two values: 0 or 1. In switch analysis, these mean open and closed. In positive-logic gate analysis, they mean LOW and HIGH. An open gate input is not a defined LOW: the electrical models must be kept distinct.

Read x' before products, and products before sums. Thus x'y + z means (x' y) + z. A prime after parentheses complements the entire group. Double complementation gives (x')' = x.

## Laws

See [proofs](../../proofs.md)

| Name | Identities |
|---|---|
| Commutative | x + y = y + x; xy = yx |
| Associative | (x + y) + z = x + (y + z); (xy)z = x(yz) |
| Distributive | x(y + z) = xy + xz; x + yz = (x + y)(x + z) |
| Identity | x + 0 = x; x1 = x |
| Domination | x + 1 = 1; x0 = 0 |
| Idempotent | x + x = x; xx = x |
| Complement | x + x' = 1; xx' = 0 |
| Absorption | x + xy = x; x(x + y) = x |
| De Morgan | (xy)' = x' + y'; (x + y)' = x'y' |
| Useful consequence | xy + xy' = x; x + x'y = x + y |

The dual of an identity exchanges + with product and 0 with 1 throughout. Taking a dual is not the same as complementing a function. Duality is optional vocabulary here.

## Exclusive OR

The function xy' + x'y is 1 when exactly one input is 1. Its complement is xy + x'y', which is 1 when the inputs agree. OR, x + y, also accepts the case where both are 1.

## How to prove an identity

An n-input truth table has 2^n rows. Enumerate all input assignments and compare both expressions. A single differing row disproves equality. Alternatively, transform one expression into the other using established laws, recording the reason at each step.

## Common errors

- x + x is x, not 2x.
- xx is x, not a new independent quantity x squared.
- xy = 0 does not imply x = 0: y might be 0.
- You cannot divide both sides by x. From xy = xz, y = z does not follow when x = 0.
- An equality describes the same output on every permitted input assignment. Similar-looking circuits are not necessarily equivalent.
