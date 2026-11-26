## Full Adder: Showing the Circuit Matches the Equations

Let `a` and `b` be the input digits, and let `c` be the input carry digit.

The standard full-adder equations are:

```text
Sum   = a XOR b XOR c

C_out = (a AND b) OR (b AND c) OR (a AND c)
```

Define the intermediate values in the circuit:

```text
d = a XOR b
e = a AND b
f = d XOR c       // column sum
g = d AND c
h = e OR g        // carry out
```

### Sum

```text
f = d XOR c
  = (a XOR b) XOR c
  = a XOR b XOR c
```

So `f` equals the standard sum equation.

### Carry out

```text
h = e OR g
  = (a AND b) OR (c AND (a XOR b))
```

Expand the XOR:

```text
h = (a AND b)
    OR (a AND c AND NOT b)
    OR (NOT a AND b AND c)
```

Now simplify:

```text
h = a AND (b OR (c AND NOT b))
    OR (NOT a AND b AND c)

  = (a AND b)
    OR (a AND c)
    OR (NOT a AND b AND c)

  = (a AND b)
    OR (a AND c)
    OR (b AND c)
```

Thus, the circuit’s outputs are equivalent to the standard full-adder equations.
