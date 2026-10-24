# Lesson 1: Switches and Boolean expressions

[Course home](../../boolean_logic.md) | [Next: Gates to Boolean algebra](connecting_gates_to_boolean_algebra.md)

**Reading:** Whitesitt 4-1 and 4-2, pp. 75–79. **Time:** 120 minutes.

## Goals

Explain 0 and 1 in a switching circuit; translate series and parallel connections into expressions; use a complement; construct a complete truth table.

## 1. Begin with a physical question (15 minutes)

Connect a low-voltage supply, resistor, LED and switch in one loop. Ask: what must be true for the LED to light?

Let x describe the switch: x = 1 when closed, x = 0 when open. Let f describe whether the switch network provides a conducting path. Then f = x.

We are studying the conditions for conduction. The expression does not calculate resistance, voltage, current or brightness. A closed switch only lights the LED if the rest of the powered circuit is correctly connected.

## 2. Two switches (20 minutes)

Put x and y in series. Both must close, so f = xy. Now connect them in parallel. Either branch can conduct, so f = x + y.

| x | y | xy | x + y |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 |

Ask why the final OR entry is 1 rather than 2. There is a path; Boolean algebra does not count paths.


![Series AND and parallel OR switch networks](../assets/series_parallel.svg)

A and B are the terminals of the switch network. Connect the supply, resistor and LED outside these terminals.

## 3. Complementary contacts (15 minutes)

The expression x' means the opposite state of x. A pair of contacts labelled x and x' must operate together: whenever x closes, x' opens, and conversely.

| x | x' |
|---|---|
| 0 | 1 |
| 1 | 0 |

Two unrelated pushbuttons are not automatically complements. Use a changeover switch, linked simulator contacts or a NOT gate in the appropriate model. Multiple contacts with the same label also represent one linked control, not independent inputs.


![Complement contacts in parallel and series](../assets/complements.svg)

Contacts with the same control must move together; a primed contact has the opposite state.

## 4. Read a compound expression (20 minutes)

Consider f = x(y + z).

1. Make a parallel pair y + z.
2. Put x in series with that pair.
3. Connect the whole switch network in the LED circuit.

The LED lights when x is closed and at least one of y and z is closed.

| x | y | z | y + z | f |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 1 | 0 |
| 1 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 | 1 |
| 1 | 1 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 1 |


![Compare x(y + z) with xy + z](../assets/compound.svg)

Trace each complete conducting path between A and B.

## 5. Practical work (35 minutes)

Build or simulate each network and test every combination:

1. f = xy + z: a series pair in parallel with z.
2. g = (x + y)z: a parallel pair in series with z.
3. h = x'y: a complementary x contact in series with y.

For f and g, find an input combination on which they differ. Explain why parentheses matter. Give your partner a circuit drawing and ask them to write its expression without seeing yours.

## 6. Exit check (15 minutes)

Explain: what is 1? What does x' mean? Why are xy + z and x(y + z) different?

**Homework:** [Algebra exercises](exercises.md), A1–A4. Read the notation and truth tables in the [reference](reference.md).
