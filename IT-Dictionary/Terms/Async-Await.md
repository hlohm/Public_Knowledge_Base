---
type: "term"
branch: "Programming Languages"
tags: [pl, modern]
status: "developed"
---

# Async/Await

> **Branch:** [[07 - Programming Languages|Programming Languages]]

Language syntax for writing asynchronous, non-blocking code that *reads* like sequential code — `await` suspends until a result is ready without blocking the thread.

**Context.** The mainstream answer to callback hell, now in JS, Python, Rust, C#. Underneath sits an event loop or executor and (often) coroutines. The classic trap: 'function colouring' — async infects callers, so a sync function can't easily call an async one.

## See also

- [[Coroutine]]
- [[Concurrency]]
- [[Event Loop]]
- [[Future]]
- [[Non-blocking I-O|Non-blocking I/O]]

## Further reading

- [Wikipedia: Async/await](https://en.wikipedia.org/wiki/Async/await)
