---
type: "term"
branch: "Programming Languages"
aliases: ["Null Reference"]
tags: [pl]
status: "developed"
---

# Null Pointer

> **Branch:** [[07 - Programming Languages|Programming Languages]]
> **Also known as:** Null Reference

A pointer that points to nothing — a sentinel meaning 'no value'. Dereferencing one is a classic crash or security bug.

**Context.** Tony Hoare called null his 'billion-dollar mistake'. Modern languages fight it structurally: option/maybe types (Rust's `Option`, Haskell's `Maybe`), nullable-type annotations (Kotlin, TypeScript), making 'might be absent' visible in the type rather than a runtime surprise.

## See also

- [[Null]]
- [[Pointer]]
- [[Option Type]]
- [[Memory Safety]]

## Further reading

- [Wikipedia: Null pointer](https://en.wikipedia.org/wiki/Null_pointer)
- [Null References: The Billion Dollar Mistake — Tony Hoare](https://www.infoq.com/presentations/Null-References-The-Billion-Dollar-Mistake-Tony-Hoare/)
