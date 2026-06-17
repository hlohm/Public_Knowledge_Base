---
type: "term"
branch: "Operating Systems"
tags: [os, fundamental]
status: "developed"
---

# Thread

> **Branch:** [[03 - Operating Systems|Operating Systems]]

An independent flow of execution within a process. Multiple threads in one process share its memory but have their own stack and registers.

**Context.** Threads are cheap to create and share data instantly — which is exactly why they're dangerous: shared mutable state invites race conditions. The shared address space is the whole feature and the whole hazard.

## See also

- [[Process]]
- [[Race Condition]]
- [[Mutex]]
- [[Concurrency]]

## Often confused with

- [[Process]] — Threads share memory (fast, risky); processes are isolated (safe, heavier).

## Further reading

- [Wikipedia: Thread (computing)](https://en.wikipedia.org/wiki/Thread_(computing))
