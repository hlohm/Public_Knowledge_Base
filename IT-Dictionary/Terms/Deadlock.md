---
type: "term"
branch: "Operating Systems"
tags: [os, anti-pattern]
status: "developed"
---

# Deadlock

> **Branch:** [[03 - Operating Systems|Operating Systems]]

A standstill where two or more threads each hold a resource the other needs and none will release, so all wait forever.

**Context.** Needs four conditions simultaneously (mutual exclusion, hold-and-wait, no preemption, circular wait); break any one to prevent it. The usual practical fix is a global lock-ordering rule so a cycle can't form.

## See also

- [[Mutex]]
- [[Livelock]]
- [[Race Condition]]

## Often confused with

- [[Race Condition]] — A deadlock freezes; a race produces a wrong-but-running result from unsynchronised timing.

## Further reading

- [Wikipedia: Deadlock (computer science)](https://en.wikipedia.org/wiki/Deadlock_(computer_science))
