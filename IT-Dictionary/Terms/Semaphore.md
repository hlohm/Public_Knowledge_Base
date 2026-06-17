---
type: "term"
branch: "Operating Systems"
tags: [os]
status: "developed"
---

# Semaphore

> **Branch:** [[03 - Operating Systems|Operating Systems]]

A counter-based synchronisation primitive (Dijkstra) that lets up to N threads proceed; threads wait when the count hits zero and signal when done.

**Context.** A binary semaphore (N=1) resembles a mutex but, unlike a mutex, has no concept of an owner — any thread can signal it, which makes it good for producer/consumer signalling but easy to misuse for mutual exclusion.

## See also

- [[Mutex]]
- [[Critical Section]]
- [[Concurrency]]

## Further reading

- [Wikipedia: Semaphore (programming)](https://en.wikipedia.org/wiki/Semaphore_(programming))
