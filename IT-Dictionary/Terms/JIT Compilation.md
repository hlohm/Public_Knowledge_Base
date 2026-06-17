---
type: "term"
branch: "Programming Languages"
aliases: ["Just-in-Time Compilation"]
tags: [pl, modern]
status: "developed"
---

# JIT Compilation

> **Branch:** [[07 - Programming Languages|Programming Languages]]
> **Also known as:** Just-in-Time Compilation

Compiling bytecode to native machine code at runtime, often guided by profiling of which paths are actually hot — blending interpretation's flexibility with compilation's speed.

**Context.** Why modern JavaScript (V8) and Java (HotSpot) are fast despite being 'interpreted'. The runtime can optimise using information a static compiler never has — actual hot paths and observed types — at the cost of warm-up time and memory.

## See also

- [[Bytecode]]
- [[Compiler]]
- [[Interpreter]]
- [[AOT Compilation]]
- [[Profile-guided Optimization]]

## Further reading

- [Wikipedia: Just-in-time compilation](https://en.wikipedia.org/wiki/Just-in-time_compilation)
