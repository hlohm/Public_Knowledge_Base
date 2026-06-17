---
type: "term"
branch: "Programming Languages"
de: "Nebenläufigkeit"
tags: [pl, fundamental]
status: "developed"
---

# Concurrency

> **Branch:** [[07 - Programming Languages|Programming Languages]]
> **German:** Nebenläufigkeit

Structuring a program as multiple independent tasks that can make progress in overlapping time periods — about *dealing with* many things at once, even on one core.

**Context.** Rob Pike's distinction is the one to internalise: concurrency is composition of independently executing things; parallelism is doing things simultaneously. You can have concurrency on a single core (via interleaving) and you need it before parallelism helps.

## See also

- [[Parallelism]]
- [[Thread]]
- [[Async-Await|Async/Await]]
- [[Race Condition]]
- [[Coroutine]]

## Often confused with

- [[Parallelism]] — Concurrency is about structure (many tasks in flight, possibly interleaved); parallelism is about execution (many tasks literally running at once on multiple cores).

## Further reading

- [Wikipedia: Concurrency (computer science)](https://en.wikipedia.org/wiki/Concurrency_(computer_science))
