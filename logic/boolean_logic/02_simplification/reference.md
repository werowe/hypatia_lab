# Reference: Circuit simplification and design

[Course home](../../boolean_logic.md)

## Switching model

| Arrangement | Expression |
|---|---|
| x and y in series | xy |
| x and y in parallel | x + y |
| x in series with a parallel pair | x(y + z) |
| Two series branches in parallel | xy + zw |
| Permanently conducting link | 1 |
| Permanent break | 0 |

These describe ideal continuity between two terminals. Repeated labels are linked controls. Complements have opposite states. Do not interpret parallel gate outputs as an OR gate: electronic gates are directional components and need their own wiring rules.

## Simplification patterns

| Before | After | Why useful |
|---|---|---|
| xy + xz | x(y + z) | Share a contact |
| xy + xy' | x | Remove a variable |
| x + xy | x | Remove a redundant branch |
| x + x'y | x + y | Remove an unnecessary complementary contact |
| (x + y)(x + y') | x | Eliminate a redundant condition |
| xy + x'z + yz | xy + x'z | Remove the consensus term |

The last is optional. A shorter expression need not be the cheapest electronic implementation. State what you count: contact occurrences, gate count, chip count or gate levels.

## Design method

Write the full truth table. For each output-1 row write a product of all inputs, complementing the inputs whose row values are 0. OR these products together. Simplify and verify against the original table.

For example, the accepted rows 01 and 10 give x'y + xy'. A product of literals is a term; an OR of product terms is called a sum of products. A term containing every input once is a minterm.

## Equivalent versus acceptable

Equivalent functions agree on every input assignment. Two different functions can both satisfy a partial specification if they disagree only on explicitly unspecified rows. Record those assumptions alongside the design.

## Deliberately outside this course

Chapter 4-4 bridge networks and transformations, general n-terminal synthesis, and the general symmetric switching networks of 4-7. We will still meet the simple idea of “at least two inputs are 1” when deriving an adder's carry.
