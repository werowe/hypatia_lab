### Question about KCL — Section 2.2.1

In *Foundations of Analog and Digital Electronic Circuits*, Section 2.2.1, Kirchhoff’s Current Law says that for a node with $N = 4$ branches:

$$
i_1 + i_2 + i_3 + i_4 = 0
$$

This is written in compact form as:

$$
\sum_{n=1}^{4} i_n = 0
$$

How can this work if each current is greater than zero?

The book says that $-i_n$ is defined to be positive for current flowing out of the node. I interpreted this as meaning that all the $i_n$ values are positive. What am I misunderstanding about the sign convention?

### Second question

### Second question

Starting from KCL,

$$
\sum_{n=1}^{N} i_n = 0,
$$

show that:

$$
\sum_{n=1}^{M} i_n = -\sum_{n=M+1}^{N} i_n.
$$

Hint: Split the original sum into two groups, then move the second group to the other side.

Draw one node with four connected branches, so $N = 4$. Choose $M = 2$ and expand the sums by hand to show that:

$$
i_1 + i_2 = -(i_3 + i_4).
$$

Use signed currents, taking currents entering the node as positive and currents leaving as negative.

