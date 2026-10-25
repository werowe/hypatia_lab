## Prove x + x = xx

These are the idempotent laws:
$$
x+x=x \qquad xx=x
$$
You can prove them algebraically using the identity, complement, and distributive laws.

**Series contacts**: $xx=x$

Start with \(x\) and rewrite it:
```math
\begin{aligned}
x &= x\cdot 1 && \text{Identity}\\
  &= x(x+x') && \text{Complement: }x+x'=1\\
  &= xx+xx' && \text{Distribute}\\
  &= xx+0 && \text{Complement: }xx'=0\\
  &= xx && \text{Identity}
\end{aligned}
```
Therefore, $xx=x$.

**Parallel contacts**: $x+x=x$

```msth
\begin{aligned}
x
&=x+0 &&\text{Identity}\\
&=x+xx' &&\text{Complement: }xx'=0\\
&=(x+x)(x+x') &&\text{Distribute OR over AND}\\
&=(x+x)\cdot1 &&\text{Complement: }x+x'=1\\
&=x+x &&\text{Identity}
\end{aligned}
```
Therefore, $x+x=x$.

Here $x'$ means NOT x.
