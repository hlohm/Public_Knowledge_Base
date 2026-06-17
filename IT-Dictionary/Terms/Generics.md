---
type: "term"
branch: "Programming Languages"
tags: [pl, fundamental]
status: "developed"
---

# Generics

> **Branch:** [[07 - Programming Languages|Programming Languages]]

Writing code parameterised over types — a `List<T>` or `Vec<T>` that works for any element type while staying type-safe.

**Context.** Lets you write an algorithm once for all types without sacrificing type checking or (with monomorphisation) performance. Implementation strategies differ sharply: monomorphisation (C++ templates, Rust — fast, code bloat) vs type erasure (Java — small, runtime cost).

## See also

- [[Type System]]
- [[Polymorphism]]
- [[Template]]
- [[Monomorphization]]
- [[Type Erasure]]

## Further reading

- [Wikipedia: Generic programming](https://en.wikipedia.org/wiki/Generic_programming)
