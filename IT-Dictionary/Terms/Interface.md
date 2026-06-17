---
type: "term"
branch: "Programming Languages"
tags: ["pl", "fundamental"]
status: "developed"
---

# Interface

> **Branch:** [[07 - Programming Languages|Programming Languages]]

A named contract of operations without implementation: anything providing these methods can be used here. Java/C# `interface`, Go interfaces (satisfied implicitly), Rust traits, Python protocols — same idea, different binding rules.

**Context.** Interfaces are how you get [[Polymorphism]] without inheritance and the mechanism behind 'program to an interface, not an implementation' — callers depend on the contract, so implementations can be swapped, mocked, or added freely. The word also means any boundary contract (API, ABI, UI); in code it's the dependency-breaking tool.

## See also

- [[Polymorphism]]
- [[API]]
- [[Dependency Injection]]
- [[Type System]]
- [[Coupling]]

## Further reading

- [Wikipedia: Interface (object-oriented programming)](https://en.wikipedia.org/wiki/Interface_(object-oriented_programming))
