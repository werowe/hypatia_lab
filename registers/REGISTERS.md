# REGISTERS

Every function you've used so far to control an Arduino pin —
`pinMode()`, `digitalWrite()`, `digitalRead()` — is really just a friendly
wrapper around something much more direct: writing individual bits into the
microcontroller's own **registers**. This page pulls back that curtain.

This builds directly on [Bits and Bitwise Operations](../bits/BITS.md) —
read that first if `|=`, `&=`, and `<<` aren't yet familiar.

---

## 1. What Is a Register?

A **register** is a tiny, extremely fast storage location built directly
into the CPU or microcontroller chip itself — not out in main RAM. Some
registers hold data the processor is actively working with; others, called
**special function registers**, aren't really "data" at all — each *bit*
directly controls or reports the state of a piece of hardware, like a
physical pin.

Writing a `1` to the right bit of the right register can turn a physical
pin's voltage from 0V to 5V, instantly, with no function call overhead at
all.

---

## 2. The Arduino Uno's Registers

The Arduino Uno is built around the ATmega328P microcontroller. Its pins
are grouped into "ports," each controlled by three 8-bit registers:

```text
DDRx    Data Direction Register  — 1 = pin is OUTPUT, 0 = pin is INPUT
PORTx   Port Register            — for an OUTPUT pin: 1 = HIGH, 0 = LOW
PINx    Pin Input Register       — reading it tells you a pin's current state
```

`x` is the port letter — `B`, `C`, or `D`. Arduino digital pins 8–13, for
example, all belong to **Port B**:

```text
Arduino pin   Port B bit
8             PB0
9             PB1
10            PB2
11            PB3
12            PB4
13            PB5     ← the built-in LED
```

---

## 3. Blinking the Built-In LED — Without `digitalWrite()`

Here is the classic Blink sketch (see [Arduino](../arduino/ARDUINO.md)),
rewritten to talk to the registers directly instead of using the Arduino
core functions:

```c
void setup()
{
    DDRB |= (1 << 5);    // set bit 5 of DDRB: pin 13 becomes OUTPUT
}

void loop()
{
    PORTB |= (1 << 5);   // set bit 5 of PORTB: pin 13 goes HIGH
    delay(500);

    PORTB &= ~(1 << 5);  // clear bit 5 of PORTB: pin 13 goes LOW
    delay(500);
}
```

Compare this to the friendlier version:

```c
void setup()
{
    pinMode(13, OUTPUT);
}

void loop()
{
    digitalWrite(13, HIGH);
    delay(500);
    digitalWrite(13, LOW);
    delay(500);
}
```

Both do exactly the same thing. `pinMode(13, OUTPUT)` is, internally,
doing roughly `DDRB |= (1 << 5);` on your behalf — it looks up which port
and bit pin 13 belongs to, and sets that one bit, using the same bitwise
patterns covered in [Bits](../bits/BITS.md):

```text
value |=  (1u << n);   set bit n     — used by pinMode(OUTPUT) / digitalWrite(HIGH)
value &= ~(1u << n);   clear bit n   — used by digitalWrite(LOW)
```

---

## 4. Reading a Pin Through `PINx`

```c
bool pin2_is_high = (PIND & (1 << 2)) != 0;   // reads pin 2 (Port D, bit 2)
```

Compare to:

```c
bool pin2_is_high = digitalRead(2) == HIGH;
```

---

## 5. Why Bother, If `digitalWrite()` Already Works?

For most sketches in this course, `digitalWrite()` and `pinMode()` are the
right choice — they're clear, safe, and portable across different Arduino
boards. Direct register access matters once you care about:

* **Speed** — `digitalWrite()` does extra work each call (looking up which
  port and bit a pin number maps to) that a direct register write skips
  entirely. This matters when you need to toggle a pin thousands of times
  per second.
* **Setting several pins at once** — a single register write can change
  every pin on a port simultaneously; eight calls to `digitalWrite()`
  cannot happen at exactly the same instant.
* **Understanding what's actually happening** — once you've written
  `DDRB |= (1 << 5);` yourself, `pinMode()` stops being magic.

---

## Summary

```text
DDRx    which pins on port x are OUTPUT (1) vs INPUT (0)
PORTx   for OUTPUT pins: the HIGH (1) / LOW (0) state to drive
PINx    for INPUT pins: the current HIGH (1) / LOW (0) state

DDRB  |= (1 << 5);    pin 13 → OUTPUT
PORTB |= (1 << 5);    pin 13 → HIGH
PORTB &= ~(1 << 5);   pin 13 → LOW
```

`pinMode()`, `digitalWrite()`, and `digitalRead()` are convenient,
board-independent wrappers around exactly this kind of direct register
manipulation. See [Bits](../bits/BITS.md) for the bitwise operators behind
it, and [Arduino](../arduino/ARDUINO.md) for the friendlier version.

---

## Intermediate Embedded-Systems Topics

*Coming soon — the sections below are placeholders for lessons still to
be written.*

### Arduino Interrupts Explained: Respond Without Constantly Checking

*Coming soon.*

### Build a Hardware Interrupt Button Without `delay()`

*Coming soon.*

### Why Arduino Circuits Need Capacitors

*Coming soon. This is the Arduino-specific, circuit-level version of this
topic — see "How Capacitors Smooth Electrical Power" in
[Projects](../projects/PROJECTS.md) for the general electricity theory
behind it.*

---

## Programs

This folder doesn't have an example `.c` file yet. Direct register access
(`DDRB`, `PORTB`, `PIND`, ...) only compiles for the actual AVR chip, so
these examples are written and tested as Arduino sketches rather than with
`clang` on a computer — see [Arduino](../arduino/ARDUINO.md) for the
upload workflow.
