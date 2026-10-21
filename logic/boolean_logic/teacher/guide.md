# Teacher guide

[Course home](../../boolean_logic.md) | [Answers](answers.md)

## Intended class and sequence

Designed for Hypatia Academy students progressing from switches, transistors and NAND gates toward a CPU. Seven approximately two-hour lessons give space for practical work. The three topics are independent folders with reference and exercise pages so they can also be assigned separately.

| Topic | Main outcome | Suggested sessions |
|---|---|---|
| Boolean algebra | Read expressions and justify transformations | 1–2 |
| Circuit simplification | Preserve behaviour while reducing contacts | 3–4 |
| Arithmetic | Derive, build and combine adders | 5–7 |

If students already know series/parallel logic, use Lesson 1 as a short review. Do not require a preliminary set-theory chapter. Introduce each law when a circuit demonstrates why it matters.

## Scope relative to Whitesitt

Use 4-1, 4-2 and 4-3, and selected accessible examples from 4-5. Omit 4-4 entirely. Do not assign general n-terminal design or the switching-network construction of symmetric functions. Majority and odd-parity conditions arise naturally in the full-adder table and do not require those constructions.

Use the binary whole-number material of 6-2; complement, AND and OR elements from 6-3; and addition from 6-4. The full adder is explicitly posed in the book's exercises. Use it as a central lesson rather than leaving it as an unsupported homework question. Omit relay memory construction, sequential accumulation and multiplication. Keep half subtraction optional.

The notes are original adaptations. Refer to the supplied book for its diagrams and historical presentation. Do not upload the PDF as part of these course notes without considering its distribution permissions separately.

## Three distinctions to teach explicitly

1. **Boolean OR and arithmetic addition:** the same printed + sign has different meanings in their respective contexts. Have students say “OR” aloud when reading circuit equations.
2. **Switch contact and electronic gate:** a contact represents continuity; a gate computes an output voltage level. Open switch inputs and floating electronic inputs are not the same concept.
3. **Control variable and contact occurrence:** two contacts labelled x operate together. Counting letters alone undercounts physical contacts.

## Practical preparation

Use a simulator capable of expressing linked complementary contacts for switch exercises. Supply a low-voltage LED circuit with an appropriate current-limiting resistor for physical demonstrations. For repeated or complementary controls, check that the chosen switches really have the necessary contacts; otherwise use the simulator.

For arithmetic lessons, abstract gate blocks are sufficient. Physical NAND work is optional and should use the established classroom 74HC00 wiring procedure, including decoupling, defined inputs, proper output loading and a common ground. The course provides connection equations rather than unverified pin-by-pin wiring instructions.

## Supporting mixed levels

Before symbolic manipulation, ask students to predict an LED's state for one concrete switch assignment. Have them narrate “both”, “either” and “opposite” before naming AND, OR and complement. Use two-variable examples first, then eight-row tables. Pair a student deriving expressions with one testing circuits; swap roles.

Students who finish early can verify consensus, implement NAND adders or automate the four-bit test. These extensions should not block students who can derive and explain a half adder.

## Assessment

For each major circuit submission, award up to two points each for: clear input/output meanings; correct table; correct expression; justified simplification; correctly labelled circuit and verification. Total: ten points.

Minimum outcomes: explain constants and complements; simplify xy + xy'; design a small series-parallel network from a table; derive both half-adder outputs; explain carry-in; demonstrate one multi-bit addition.

A simulator result without an explanation is incomplete. A correct algebraic simplification without checking the intended input constraints can also be incomplete.

## Deployment

Extract the ZIP into the desired GitHub directory. Keep boolean_logic.md beside the boolean_logic folder. Links are relative and work when the whole package is placed under a directory such as lectures. The teacher answer page is a normal Markdown file and will be public if committed to a public repository; omit the teacher folder if answers should be withheld, and remove its links from the landing and exercise pages.
