## Exclusive OR: xy' + x'y

**Exclusive OR means exactly one input is 1.**

In `xy' + x'y`:

- **`xy'`** means x is 1 **and y is 0**.  (**Explanation**:  xy' is 1 only when x is 1 and y is 0. In that case y' is 1.)
- **`x'y`** means x is 0 **and y is 1**.
- **`+`** means OR: either case makes the output 1.

| x | y | xy' | x'y | xy' + x'y |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | **0** |
| 0 | 1 | 0 | 1 | **1** |
| 1 | 0 | 1 | 0 | **1** |
| 1 | 1 | 0 | 0 | **0** |

When **both inputs are 1**, both terms become 0 because each requires
one input to be 0. That excludes the “both” case—hence **exclusive** OR.

Ordinary OR, `x + y`, produces 1 when both inputs are 1.
Exclusive OR, `xy' + x'y`, produces 0 in that case.
