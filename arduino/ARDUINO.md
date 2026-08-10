# ARDUINO

An Arduino is a small circuit board built around a microcontroller — a
tiny, self-contained computer with its own CPU, memory, and pins that can
be turned into inputs (to read a sensor or button) or outputs (to drive an
LED, motor, or speaker). You program it in a language that is, for
everything in this course, ordinary C.

Before touching real hardware, build these circuits in
[TinkerCAD](https://www.tinkercad.com/) — free, in your browser, and
impossible to damage. See the links at the top of the main
[README](../README.md).

---

## 1. The Shape of an Arduino Sketch

An Arduino program is called a **sketch**. Every sketch needs exactly two
functions — the Arduino runtime calls them for you, you never call them
yourself. See the special-functions note in
[Functions](../functions/FUNCTIONS.md).

```c
void setup()
{
    // runs once, when the board powers on or is reset
}

void loop()
{
    // runs over and over, forever, right after setup() finishes
}
```

`loop()` is, quite literally, an infinite loop the Arduino runtime keeps
calling for you — see the `for (;;)` section of [Loops](../loops/LOOPS.md).

---

## 2. Digital Pins: `pinMode()`, `digitalWrite()`, `digitalRead()`

A digital pin is either **HIGH** (5V, or 3.3V on some boards) or **LOW**
(0V) — nothing in between.

```c
pinMode(pin, OUTPUT);          // this pin will drive a voltage out
pinMode(pin, INPUT);           // this pin will read a voltage in
pinMode(pin, INPUT_PULLUP);    // read a voltage in, defaulting to HIGH

digitalWrite(pin, HIGH);       // drive the pin to 5V
digitalWrite(pin, LOW);        // drive the pin to 0V

int state = digitalRead(pin);  // HIGH or LOW
```

### Blink — The "Hello, World" of Arduino

```c
const int LED_PIN = 13;

void setup()
{
    pinMode(LED_PIN, OUTPUT);
}

void loop()
{
    digitalWrite(LED_PIN, HIGH);
    delay(500);   // milliseconds

    digitalWrite(LED_PIN, LOW);
    delay(500);
}
```

`delay(500)` pauses the whole program for 500 milliseconds. It's simple,
but nothing else can happen while it's paused — see the interrupts topic in
[Registers](../registers/REGISTERS.md) for the alternative.

### Reading a Button

```c
const int BUTTON_PIN = 2;
const int LED_PIN = 13;

void setup()
{
    pinMode(BUTTON_PIN, INPUT);
    pinMode(LED_PIN, OUTPUT);
}

void loop()
{
    if (digitalRead(BUTTON_PIN) == HIGH) {
        digitalWrite(LED_PIN, HIGH);
    } else {
        digitalWrite(LED_PIN, LOW);
    }
}
```

See [Conditionals](../conditionals/CONDITIONALS.md) for the `if` behind
this pattern — read a value, then decide what to do about it.

---

## 3. Analog Input: `analogRead()`

Digital pins only know HIGH or LOW. The analog input pins (labeled `A0`
through `A5` on an Uno) can measure a whole *range* of voltage, returning a
number from `0` to `1023`.

```c
int reading = analogRead(A0);   // 0 (0V) to 1023 (5V)
```

```c
const int SENSOR_PIN = A0;

void setup()
{
    Serial.begin(9600);
}

void loop()
{
    int reading = analogRead(SENSOR_PIN);

    Serial.println(reading);

    delay(100);
}
```

`Serial.begin(9600)` opens a connection to your computer; `Serial.println()`
sends a line of text back over it, viewable in the Arduino IDE's Serial
Monitor — the most useful debugging tool you have when there's no screen
attached to the board.

---

## 4. Analog-ish Output: `analogWrite()` and PWM

None of the Arduino Uno's pins can output a true, continuously variable
voltage — only HIGH or LOW. Instead, certain pins (marked with a `~` on the
board) can flicker between HIGH and LOW so fast that an LED or motor
*behaves* as if it's receiving a middle voltage. This trick is called
**PWM**, and it's covered in its own placeholder section below.

```c
analogWrite(pin, value);   // value: 0 (always off) to 255 (always on)
```

---

## 5. Compiling and Uploading

Arduino sketches aren't compiled with `clang` from the command line the
way the rest of this course's `.c` files are — the Arduino IDE compiles
your sketch with `avr-gcc` for the exact chip on your board, then uploads
it over USB.

```text
1. Write your sketch (a .ino file) in the Arduino IDE.
2. Click Verify (✓)  — compiles the code and reports any errors.
3. Click Upload (→)  — compiles again and sends it to the board.
```

Plain C logic that doesn't call any Arduino-specific functions —
`pinMode()`, `digitalWrite()`, `analogRead()`, and so on — can still be
written and tested with `clang` on your own computer first, the same way
as every other file in this course. That's a good way to work out tricky
logic (like a state machine for Morse code timing) before wiring it into a
sketch. See [`electronics/transistor.c`](../electronics/transistor.c) for
an example of ordinary C logic modeling a circuit without any Arduino
functions at all.

---

## Summary

```text
setup()                  runs once
loop()                   runs forever, after setup()

pinMode(pin, OUTPUT)      configure a pin to drive voltage out
pinMode(pin, INPUT)       configure a pin to read voltage in
digitalWrite(pin, HIGH)   drive a pin to 5V
digitalWrite(pin, LOW)    drive a pin to 0V
digitalRead(pin)          HIGH or LOW

analogRead(pin)           0-1023, a range of input voltage
analogWrite(pin, value)   0-255, a PWM "fake" output voltage

delay(ms)                 pause everything for ms milliseconds

Serial.begin(9600)        open a connection to your computer
Serial.println(value)     print a line to the Serial Monitor
```

---

## Coming Soon

*Placeholders for lessons still to be written.*

### How Arduino Converts Voltage into a Number

*Coming soon.*

### Build an Arduino Voltmeter with an Analog Input

*Coming soon.*

### How Arduino Controls LED Brightness with PWM

*Coming soon. This is the explanation video — see "Beyond Blink: Build an
Arduino LED Dimmer with PWM" in [Projects](../projects/PROJECTS.md) for
the hands-on companion project.*

### Why Your Arduino Code Fails: 7 Common Mistakes

*Coming soon.*

### Build an Arduino Morse Code Transmitter in C

*Coming soon.*

---

## Programs

This folder doesn't have an example sketch file yet. The Blink sketch
above is the traditional first program to type in, upload, and run.
