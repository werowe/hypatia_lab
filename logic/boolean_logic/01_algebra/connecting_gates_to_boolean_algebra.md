# Connecting Gates to Boolean Algebra

[Course home](../../boolean_logic.md) | [Previous: Switches and expressions](lesson_01.md) | [Next: Laws and proofs](lesson_02.md)

**Hypatia Academy supplement. Suggested time: 60–90 minutes.**

Students have already met logic gates and their truth tables. This lesson connects that knowledge to algebra before we use algebra to simplify circuits. It supplements the switching-algebra material referenced to J. Eldon Whitesitt; the modern gate diagrams and the gate-to-expression teaching sequence are Hypatia Academy material, not a quotation or a lesson attributed to his book.

## Goals

- Translate a gate into a Boolean expression.
- Follow gate connections to construct a complete expression.
- Draw a gate network from an expression.
- Explain why Boolean `1 + 1 = 1`.
- Distinguish circuit translation from circuit simplification.
- Use a complete truth table to establish equivalence.

## 1. Start from the gates students already know

A Boolean variable is either 0 or 1. In positive-logic gate diagrams these correspond to LOW and HIGH. We are describing a logical state, not calculating voltage, current or brightness.

| Gate | Expression | Read it as |
|---|---|---|
| NOT | `x'` | The opposite of x |
| AND | `xy` | x and y must both be 1 |
| OR | `x + y` | At least one of x and y is 1 |
| NAND | `(xy)'` | NOT of the complete AND result |
| NOR | `(x + y)'` | NOT of the complete OR result |
| XOR | `xy' + x'y` | Exactly one input is 1 |

A prime after parentheses complements the entire group. Read NOT before AND, and AND before OR. Thus `x'y + z` means `(x' AND y) OR z`.

An open electrical input is not automatically a defined Boolean zero. Fixed LOW and HIGH inputs must be provided correctly in a physical circuit. Do not join gate outputs together to imitate the parallel paths of a switch network.

### Why is 1 + 1 = 1?

Here `+` is the OR operation, not numerical addition. The output records whether the condition is true; it does not count how many inputs are true.

| x | y | x + y | xy | xy' + x'y |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 | 0 |

At `11`, OR is 1 because at least one input is 1. XOR is 0 because the inputs are not different. These are different operations. This lesson is about Boolean logic, not arithmetic addition.

## 2. Follow a circuit from inputs to output

![NOT x, AND with y, then OR with z](../assets/gates_to_boolean.svg)

Take a circuit with these connections:

1. Feed x into a NOT gate. Call its output `a`.
2. Feed a and y into an AND gate. Call its output `b`.
3. Feed b and z into an OR gate. Call the final output `f`.

Write one equation per gate:

```text
a = x'
b = ay
f = b + z
```

Substitute the earlier expressions into the later ones:

```text
b = x'y
f = x'y + z
```

We have written the circuit as an expression. **Nothing has been simplified yet.** The expression records the original connections.

| x | y | z | a = x' | b = x'y | f = x'y + z |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 1 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 | 1 |
| 0 | 1 | 0 | 1 | 1 | 1 |
| 0 | 1 | 1 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 0 | 0 | 1 |
| 1 | 1 | 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 0 | 0 | 1 |

Ask students to identify the intermediate signal at each wire before showing the final formula.

## 3. Reverse the process: expression to gates

Given `f = x(y + z)`:

1. The parentheses require an OR gate combining y and z.
2. Feed that result and x into an AND gate.
3. The AND output is f.

Given `g = xy + z`:

1. Use an AND gate for x and y.
2. Feed that result and z into an OR gate.

These are different circuits and different functions. At `x = 0, y = 0, z = 1`, f is 0 but g is 1. The parentheses record an important difference in the connections.

## 4. Now algebra can change the circuit

Start with `h = xy + xz`.

A direct implementation has two AND gates feeding one OR gate: three gates.

Factor x:

```text
xy + xz = x(y + z)
```

The factored form needs one OR gate feeding one AND gate: two gates.

### A short proof

- If `x = 0`, both expressions are 0 for every y and z.
- If `x = 1`, both expressions are `y + z`.

These cases exhaust the possible values of x. Therefore the two expressions are equivalent for every assignment. A complete eight-row truth table gives another proof.

The number of distinct input variables has not changed. The number of illustrated gate instances has.

## 5. A second application: a branch that adds nothing

Translate a circuit with an AND gate for xy and an OR gate for x and xy:

```text
f = x + xy
```

Whenever the AND output is 1, x is already 1. The extra branch cannot add a new true case.

The algebraic proof is:

| Step | Reason |
|---|---|
| `x + xy = x1 + xy` | Identity: x = x1 |
| `= x(1 + y)` | Distributive law |
| `= x1` | Domination: 1 + y = 1 |
| `= x` | Identity |

The final network can connect x directly to the output: zero logic gates in this ideal representation. Revisit each underlying rule in the laws lesson and prove it by its possible input values.

## 6. Why this belongs on the path to a CPU

CPU designers describe digital behaviour using Boolean logic. Logic synthesis tools transform design descriptions into gate networks and optimize them while preserving the required function.

Our small examples expose that reasoning step by step. Real designs also account for area, timing, power, available cells and fan-out. Fewer drawn gates does not by itself establish lower cost, lower power or higher speed.

Truth-table equivalence describes settled logic outputs. Real gate delays can also create temporary glitches when inputs change; this lesson does not analyse those transients.

## 7. Student work

**G1. Translate into expressions.** Label intermediate wires first.

1. OR x and y, then NOT the result.
2. NOT x and NOT y, then AND those results.
3. AND x and y, then OR with z.
4. OR y and z, then AND with x.

**G2. Draw gate circuits** for `(xy)'`, `x' + y`, and `x(y + z')`.

**G3. Prove identity laws** `x + 0 = x` and `x1 = x` by checking both possible values of x. Draw the gates and the direct-wire equivalents.

**G4. Prove complement laws** `x + x' = 1` and `xx' = 0`. Explain why x and x' must not be independently controlled.

**G5. Translate, simplify and redraw** `xy + xy'`. Include the original expression, the short algebraic proof, the two circuits and a four-row truth table.

**G6. Find a counterexample** to the claim `xy + z = x(y + z)`.

**G7. Explain in words:** Why does Boolean `1 + 1 = 1`? How is XOR different from OR when both inputs are 1?

## Teacher answers

- G1: `(x + y)'`; `x'y'`; `xy + z`; `x(y + z)`.
- G2: AND then NOT; NOT x then OR with y; NOT z then OR with y, followed by AND with x.
- G3: For x = 0 both results are 0; for x = 1 both are 1.
- G4: The pairs `(x, x')` are only `(0,1)` and `(1,0)`; OR is always 1 and AND always 0.
- G5: `xy + xy' = x(y + y') = x1 = x`. Four illustrated gates become a wire when NOT is counted separately. Outputs in xy order 00, 01, 10, 11: 0, 0, 1, 1.
- G6: x = 0, y = 0, z = 1 gives 1 on the left and 0 on the right.
- G7: OR records whether at least one input is 1. It does not count inputs. OR(1,1) = 1; XOR(1,1) = 0.

## Teaching sequence

Use this bridge after students know individual gates and before asking them to simplify whole circuits. Continue with [Laws and short proofs](lesson_02.md), then [Simplify an existing circuit](../02_simplification/lesson_03.md). The video narration and Manim source in the accompanying pack cover the same examples.
