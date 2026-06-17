---
type: "term"
branch: "Computing Foundations"
tags: [foundations, anti-pattern]
status: "developed"
---

# Integer Overflow

> **Branch:** [[01 - Computing Foundations|Computing Foundations]]

What happens when an arithmetic result exceeds the range a fixed-width integer can hold — it wraps around (or, in some languages, is undefined behaviour).

**Context.** Source of real-world disasters (Ariane 5) and security bugs (overflow a length check, then over-read/-write). In C, signed overflow is *undefined behaviour* the compiler may exploit; in Rust it panics in debug and wraps in release.

## See also

- [[Two's Complement]]
- [[Undefined Behavior]]
- [[Buffer Overflow]]

## Further reading

- [Wikipedia: Integer overflow](https://en.wikipedia.org/wiki/Integer_overflow)
