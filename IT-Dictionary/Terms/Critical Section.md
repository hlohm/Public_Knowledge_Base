---
type: "term"
branch: "Operating Systems"
tags: ["os", "fundamental"]
status: "developed"
---

# Critical Section

> **Branch:** [[03 - Operating Systems|Operating Systems]]

A stretch of code that touches shared state and therefore must not be executed by more than one thread at a time — the region a [[Mutex]] or [[Semaphore]] exists to protect.

**Context.** The craft is keeping critical sections *small*: lock, do the minimal shared-state work, unlock. Hold a lock too long and you've serialized your parallel program; take two locks in inconsistent order and you've built a [[Deadlock]]. Most concurrency bugs are critical sections that someone didn't realize were critical.

## See also

- [[Mutex]]
- [[Semaphore]]
- [[Race Condition]]
- [[Deadlock]]
- [[Concurrency]]

## Further reading

- [Wikipedia: Critical section](https://en.wikipedia.org/wiki/Critical_section)
