# Optional extension: A half subtracter

[Course home](../../boolean_logic.md)

**Reading:** Whitesitt 6-5, pp. 145–147. Attempt after the full adder.

A half subtracter computes one bit of x minus y with no incoming borrow. Unlike addition, the order of the inputs matters. Let d be the difference bit and b the borrow output.

| x | y | d | b |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 0 |

At x = 0 and y = 1, borrowing one unit from the next column contributes two units in this column. Two minus one leaves one, so d = 1 and b = 1.

The table gives d = xy' + x'y and b = x'y. The difference uses the same exclusive-OR function as the half-adder sum, but the borrow is not the half-adder carry.

## Tasks

1. Build and test the half subtracter.
2. Explain why exchanging x and y can change b but not d.
3. Explain why d alone cannot tell us whether subtraction required borrowing.

Stop here for this course. Full subtracters and signed arithmetic can be studied later.
