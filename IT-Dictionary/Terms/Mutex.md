---
type: "term"
branch: "Operating Systems"
aliases: ["Lock", "Mutual Exclusion"]
tags: [os, fundamental]
status: "developed"
---

# Mutex

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** Lock, Mutual Exclusion

A synchronisation primitive ensuring only one thread enters a critical section at a time, preventing concurrent access to shared data.

**Context.** Locks are correct but composable poorly: take two in different orders in different threads and you get a deadlock. The art of concurrent code is holding locks for as short a time as possible — or avoiding shared mutable state entirely.

## See also

- [[Semaphore]]
- [[Critical Section]]
- [[Deadlock]]
- [[Race Condition]]

## Often confused with

- [[Semaphore]] — A mutex allows one holder and has ownership; a counting semaphore allows N and has none.

## Further reading

- [Wikipedia: Lock (computer science)](https://en.wikipedia.org/wiki/Lock_(computer_science))
