---
type: "term"
branch: "Computing Foundations"
tags: [foundations, fundamental]
status: "developed"
---

# Two's Complement

> **Branch:** [[01 - Computing Foundations|Computing Foundations]]

The standard way to represent signed integers in binary: negate by inverting all bits and adding one. The top bit becomes the sign.

**Context.** It wins because addition and subtraction work identically on signed and unsigned values — the hardware needs no special case. Its asymmetry (one more negative value than positive) is the source of the classic `abs(INT_MIN)` overflow.

## See also

- [[Binary]]
- [[Integer Overflow]]
- [[Sign Extension]]

## Further reading

- [Wikipedia: Two's complement](https://en.wikipedia.org/wiki/Two's_complement)
