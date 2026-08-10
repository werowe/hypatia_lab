# ELECTRONICS

Before code can turn on an LED, blink a light, or control a motor, it has
to work through real electricity. This page covers the basic electronics
this course relies on — just enough to safely build and understand the
circuits in [the Arduino Circuits section of the README](../README.md).

---

## 1. Voltage, Current, and Resistance

```text
Voltage (V)     "electrical pressure" — measured in volts
Current (I)     the flow of electricity — measured in amps
Resistance (R)  how much a component resists that flow — measured in ohms (Ω)
```

A useful analogy: voltage is like water pressure in a pipe, current is how
much water actually flows, and resistance is how narrow the pipe is.

### Ohm's Law

These three quantities are related by one of the most important equations
in electronics:

```text
V = I × R
```

```text
I = V / R      (current = voltage ÷ resistance)
R = V / I      (resistance = voltage ÷ current)
```

---

## 2. Why an LED Needs a Resistor

An LED (light-emitting diode) has almost no resistance of its own. Connect
one directly to a 5V pin with no resistor, and it will draw far more
current than it — or the Arduino pin driving it — can safely handle,
destroying one or both.

A resistor placed in series with the LED limits the current to a safe
amount. A typical calculation, for a red LED with a roughly 2V forward
voltage drop, on a 5V Arduino pin:

```text
Voltage across the resistor  = 5V - 2V = 3V
Safe current for a small LED = about 0.02A (20 mA)

R = V / I = 3V / 0.02A = 150Ω
```

A 220Ω or 330Ω resistor is commonly used instead — slightly higher
resistance than the bare minimum, which means slightly less current and a
dimmer, but safer, LED.

---

## 3. The Breadboard

A breadboard lets you build a circuit by pushing component legs and wires
into holes, with no soldering. The holes are connected in strips underneath
the board:

```text
Each short row (5 holes) in the middle section is electrically connected.
The long rows along the top and bottom edges are the power rails
(usually marked + and -), connected along the entire length of the board.
```

Components placed in the same short row are automatically wired together.

---

## 4. The Transistor as a Switch

A transistor is a small component with three legs — **base**, **collector**,
and **emitter** — that acts as an electrically controlled switch. This
course uses the 2N2222 transistor.

```text
base        the "control" pin — a small signal here decides whether
            the transistor conducts
collector   connects toward the higher-voltage side of the circuit
emitter     connects toward ground
```

When the base receives enough voltage, current is allowed to flow from the
collector to the emitter — the switch is "closed." When the base has no
voltage, no current flows — the switch is "open." This is exactly how a
digital pin, which can only output HIGH or LOW, can still control something
that needs more current than the pin itself can safely supply.

### Walkthrough: `transistor.c`

This course models that behavior in plain C, with no hardware attached, in
[`electronics/transistor.c`](transistor.c):

```c
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

#define ON  1
#define OFF 0

struct Transistor {
    bool base_on;
    bool conducting;
};

void update_transistor(struct Transistor *transistor)
{
    // when the base turns on, the collector-to-emitter path conducts
    transistor->conducting = transistor->base_on;
}

int main(int argc, char *argv[])
{
    if (argc != 2) {
        printf("Usage: %s 1\n", argv[0]);
        printf("       %s 0\n", argv[0]);
        return 1;
    }

    int input = atoi(argv[1]);

    if (input != ON && input != OFF) {
        printf("Enter 1 for ON or 0 for OFF.\n");
        return 1;
    }

    struct Transistor transistor = {
        .base_on = false,
        .conducting = false
    };

    transistor.base_on = input == ON;

    update_transistor(&transistor);

    if (transistor.conducting) {
        printf("Base: ON\n");
        printf("Collector-to-emitter path: conducting\n");
    } else {
        printf("Base: OFF\n");
        printf("Collector-to-emitter path: blocked\n");
    }

    return 0;
}
```

Run with the base on:

```bash
./transistor 1
```

```text
Base: ON
Collector-to-emitter path: conducting
```

Run with the base off:

```bash
./transistor 0
```

```text
Base: OFF
Collector-to-emitter path: blocked
```

A few things worth pointing out in this program, all covered elsewhere in
this course:

* `struct Transistor` groups the transistor's state together — see
  [Structs](../structs/STRUCTS.md).
* `update_transistor()` takes a **pointer** to the struct so it can modify
  the caller's actual transistor — see [Pointers](../pointers/POINTERS.md).
* `argc` / `argv` are how a C program receives command-line arguments —
  `argv[0]` is always the program's own name, `argv[1]` is the first
  argument typed after it.
* `atoi()` converts a string like `"1"` to the integer `1`.
* `input != ON && input != OFF` uses the logical AND from
  [Operators](../operators/OPERATORS.md) to validate the input.

---

## 5. From One Transistor to a NAND Gate

This course follows one rule, stated in the main [README](../README.md):

> Every logic gate is built from NAND gates.

A NAND gate can itself be built from nothing but transistors — two of them,
wired so that the output is HIGH unless *both* inputs are HIGH. The
74HC00 chip used in this course packages four such NAND gates, already
wired up, into one small IC. Building one from raw transistors first, and
only then using the 74HC00, is what makes the chip stop being a mystery.
See the placeholder section below.

---

## 6. Safety Notes

* Never connect an LED directly to power without a current-limiting
  resistor.
* Double-check polarity — LEDs and electrolytic capacitors only work one
  way around.
* Disconnect power before rewiring a breadboard.
* A 2N2222 transistor and a 5V Arduino circuit are safe to touch — but
  always treat "which way does current flow" as a question worth answering
  *before* connecting power, not after something gets hot.

---

## Summary

```text
V = I × R                          Ohm's Law
LED + resistor                     resistor limits current so the LED survives
breadboard row                     5 holes, all electrically connected
transistor base                    the control pin
transistor collector → emitter     the switched path
```

---

## Electronics and Computer Architecture Sequence

*Placeholders for lessons still to be written — these trace a path from
a single transistor up to how a computer actually runs your code.*

### Build a NAND Gate with Transistors

*Coming soon.*

### Build a 1-Bit Memory Cell with NAND Gates

*Coming soon.*

### Where Does Arduino Store Your Variables?

*Coming soon. See also [Memory](../memory/MEMORY.md).*

### How Arduino Turns C Code into Machine Instructions

*Coming soon.*

---

## Programs

* [`transistor.c`](transistor.c) — models a transistor switch in plain C,
  no hardware required. Walked through in section 4 above.

## Compile

```bash
clang -Wall -Wextra -Wpedantic -std=c17 transistor.c -o transistor
```

## Run

```bash
./transistor 1
./transistor 0
```
