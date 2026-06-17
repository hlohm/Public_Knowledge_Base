---
type: "term"
branch: "Programming Languages"
tags: [pl]
status: "developed"
---

# Coroutine

> **Branch:** [[07 - Programming Languages|Programming Languages]]

A function that can suspend and resume its execution, preserving local state across suspensions — cooperative, lightweight, and not tied to an OS thread.

**Context.** The building block under async/await and Go's goroutines. Cheap compared to OS threads (you can have millions), they multiplex onto a few threads via an event loop or scheduler. Cooperative scheduling means one coroutine that never yields can starve the rest.

## See also

- [[Async-Await|Async/Await]]
- [[Thread]]
- [[Green Threads]]
- [[Generator]]
- [[Concurrency]]

## Further reading

- [Wikipedia: Coroutine](https://en.wikipedia.org/wiki/Coroutine)
