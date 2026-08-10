# PROJECTS

This page tracks the hands-on builds for the course, in roughly the order
they're meant to be tackled — starting in
[TinkerCAD](https://www.tinkercad.com/) (free, in-browser, nothing to
damage) before moving to real components. See the circuit links at the top
of the main [README](../README.md).

---

## The Path

```text
1. Turn On an LED           →  electronics/ELECTRONICS.md (Ohm's Law, resistor sizing)
2. Use a Transistor as a Switch  →  electronics/transistor.c
3. Build a Logical OR Gate
4. Build a Logical AND Gate
5. Build a NAND Gate from Transistors   →  see Coming Soon below
6. Build Every Other Gate from NAND     →  the course's "NAND Rule"
7. Build a Shift Register
8. Build a 1-Bit Memory Cell from NAND Gates  →  see Coming Soon below
9. NANDINO-4 — a 4-bit CPU emulator, built from nothing but NAND gates
```

Every project after step 4 rests on one rule, stated in the main
[README](../README.md):

> Every logic gate in this course is built from NAND gates.

---

## 1. Turn On an LED

**Goal:** light an LED safely, with the correctly sized current-limiting
resistor.

**You'll need:** a breadboard, an LED, a resistor, jumper wires.

**Concepts used:** Ohm's Law and resistor sizing, from
[Electronics](../electronics/ELECTRONICS.md).

---

## 2. Use a Transistor as a Switch

**Goal:** use a small signal on a transistor's base to control a separate
circuit — the same principle behind every digital output pin.

**You'll need:** a 2N2222 transistor, an LED, two resistors, a breadboard.

**Concepts used:** the transistor walkthrough in
[Electronics](../electronics/ELECTRONICS.md), which models this exact
circuit's logic in plain C in
[`electronics/transistor.c`](../electronics/transistor.c) before you ever
touch a breadboard.

---

## 3–4. Logical OR and AND, Built from Transistors

**Goal:** wire two transistors together so the output behaves like the
`||` and `&&` operators from [Operators](../operators/OPERATORS.md) — but
in silicon instead of code.

**You'll need:** two 2N2222 transistors per gate, resistors, LEDs (to show
the output), a breadboard.

---

## 5–9. NAND Gates Through NANDINO-4

**Goal:** build a NAND gate from raw transistors, then use it (or the
74HC00 chip, four NAND gates in one IC) as the *only* building block for
every other gate, a 1-bit memory cell, and finally a working 4-bit CPU
emulator.

**You'll need:** 74HC00 NAND ICs, a breadboard, jumper wires, and — by the
final project — a shift register.

See the "Electronics and Computer Architecture Sequence" placeholders in
[Electronics](../electronics/ELECTRONICS.md) for the lessons that build up
to this.

---

## Coming Soon

*Placeholders for build-along projects still to be written.*

### Build an LED Dimmer with a Potentiometer

*Coming soon — the hands-on companion to "How Arduino Controls LED
Brightness with PWM" in [Arduino](../arduino/ARDUINO.md).*

### Beyond Blink: Build an Arduino LED Dimmer with PWM

*Coming soon.*

### How Capacitors Smooth Electrical Power

*Coming soon. This is the general electricity theory — see "Why Arduino
Circuits Need Capacitors" in [Registers](../registers/REGISTERS.md) for
the Arduino-specific, circuit-level version.*

---

## Programs

Each project above will get its own `.c` file (for logic that can be
tested on a computer first, like [`transistor.c`](../electronics/transistor.c))
and/or Arduino sketch as we build it in class. See
[Electronics](../electronics/ELECTRONICS.md) and
[Arduino](../arduino/ARDUINO.md) for the code style used throughout this
course.

## Compile

```bash
clang -Wall -Wextra -Wpedantic -std=c17 source.c -o program
```

## Run

```bash
./program
```
