---
type: "term"
branch: "Programming Languages"
tags: [pl, fundamental]
status: "developed"
---

# Reference

> **Branch:** [[07 - Programming Languages|Programming Languages]]

An alias to a value — a handle that lets you access the original without copying it. Safer than a raw pointer: typically can't be null, can't do arithmetic, and is often managed by the language.

**Context.** Pass-by-reference vs pass-by-value is a defining language semantics. 'Reference' means subtly different things in C++ (an alias), Java (a managed pointer), and Rust (a borrow with a checked lifetime) — the differences matter.

## See also

- [[Pointer]]
- [[Dereference]]
- [[Pass by Reference]]
- [[Borrowing]]
- [[Aliasing]]

## Further reading

- [Wikipedia: Reference (computer science)](https://en.wikipedia.org/wiki/Reference_(computer_science))
