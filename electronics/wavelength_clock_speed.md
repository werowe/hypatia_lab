## Wavelength, Circuit Size, and Clock Speed

A clock period is the time between two identical points in successive clock cycles—for example, from one rising edge to the next. A clock signal repeats, typically switching between low and high voltage. The period is a measure of time; wavelength is a measure of distance.

For a signal travelling through a circuit, its wavelength is:

```text
wavelength = propagation speed / frequency
```

Equivalently:

```text
λ = v / f
```

Here, `λ` is the wavelength, `v` is the signal’s propagation speed in the material, and `f` is its frequency.

The wavelength does **not** have to be longer than the chip for the chip to complete a clock cycle. A signal can complete many cycles while travelling through a circuit, and different parts of a circuit can be at different phases of the signal.

Wavelength matters when deciding how to model a circuit. If the circuit’s physical dimensions are much smaller than the signal’s wavelength, voltage and current changes can often be treated as happening throughout the circuit without significant travel-time differences. This is the **lumped-element approximation** used in basic circuit analysis.

A common rule of thumb is that this approximation works well when the circuit’s largest dimension is less than about one-tenth of the wavelength. As the circuit becomes a substantial fraction of a wavelength, propagation delays and phase differences matter. The circuit may need to be treated as a distributed system, using transmission-line methods or, in more complex cases, Maxwell’s equations.

For digital circuits, the important frequency is not always just the clock frequency. Very fast voltage edges contain higher-frequency components. So signal travel time and circuit size can become important even when the clock frequency itself seems modest.

This is not a rule that sets the minimum possible clock period. A processor’s speed is limited by factors such as transistor switching time, delays in the interconnects between transistors, power use, heat, and the time needed for signals to arrive reliably. Wavelength and circuit size affect signal behaviour and the design methods required; they do not require the clock cycle to be longer than the time a signal takes to cross the chip.
