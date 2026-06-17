---
type: "term"
branch: "Programming Languages"
aliases: ["UB"]
tags: [pl]
status: "developed"
---

# Undefined Behavior

> **Branch:** [[07 - Programming Languages|Programming Languages]]
> **Also known as:** UB

Code whose result the language spec leaves entirely unconstrained — the compiler may do anything, including silently miscompile, crash, or appear to work.

**Context.** The C/C++ minefield: signed overflow, out-of-bounds access, data races, null dereference. Crucially, optimisers *assume UB never happens* and rewrite code on that assumption, so UB can corrupt code far from the bug. A core motivator for memory-safe languages.

## See also

- [[Memory Safety]]
- [[Pointer]]
- [[Optimization]]
- [[Sanitizer]]

## Further reading

- [Wikipedia: Undefined behavior](https://en.wikipedia.org/wiki/Undefined_behavior)
