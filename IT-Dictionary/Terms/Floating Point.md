---
type: "term"
branch: "Computing Foundations"
de: "Gleitkommazahl"
tags: [foundations, fundamental]
status: "developed"
---

# Floating Point

> **Branch:** [[01 - Computing Foundations|Computing Foundations]]
> **German:** Gleitkommazahl

A representation of real numbers as a sign, a mantissa and an exponent — like scientific notation in binary. Trades exactness for enormous range.

**Context.** Because it's binary, many decimals (0.1) can't be represented exactly, so `0.1 + 0.2 != 0.3`. Never use floats for money — use integers of cents or a decimal type.

## See also

- [[IEEE 754]]
- [[Rounding Error]]
- [[Fixed Point]]

## Often confused with

- [[Fixed Point]] — Fixed point keeps a constant number of fractional digits; floating point lets the point move for range.

## Further reading

- [Wikipedia: Floating-point arithmetic](https://en.wikipedia.org/wiki/Floating-point_arithmetic)
