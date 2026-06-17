---
type: "term"
branch: "Programming Languages"
aliases: ["GC", "Automatic Memory Management"]
tags: [pl, fundamental]
status: "developed"
---

# Garbage Collection

> **Branch:** [[07 - Programming Languages|Programming Languages]]
> **Also known as:** GC, Automatic Memory Management

Automatic reclamation of memory no longer reachable by the program, freeing the developer from manual `free()`/`delete` and the bugs that come with it.

**Context.** Trades a class of memory bugs (leaks, use-after-free) for unpredictable **GC pauses** and higher memory use — a real problem for latency-sensitive systems. Tracing (mark-sweep, generational) vs reference counting are the two families; Rust's borrow checker is the notable 'neither' answer.

## See also

- [[Memory Safety]]
- [[Reference Counting]]
- [[Memory Leak]]
- [[RAII]]
- [[Stop-the-world]]

## Often confused with

- [[RAII]] — GC reclaims memory automatically at some later point; RAII ties resource release deterministically to scope exit, no collector needed.

## Further reading

- [Wikipedia: Garbage collection (computer science)](https://en.wikipedia.org/wiki/Garbage_collection_(computer_science))
