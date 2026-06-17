---
type: "term"
branch: "Operating Systems"
aliases: ["Preemptive Multitasking"]
tags: ["os", "fundamental"]
status: "developed"
---

# Preemption

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** Preemptive Multitasking

The scheduler's right to interrupt a running task at any time (via timer interrupt) and give the CPU to another — as opposed to cooperative multitasking, where tasks must yield voluntarily.

**Context.** Preemption is why one spinning process no longer freezes the machine (it did, in Windows 3.x/classic Mac OS) — and why all shared state needs locks: your code can be paused *between any two instructions*. The same idea at different scales: thread preemption, VM scheduling, even Kubernetes pod preemption.

## See also

- [[Scheduler]]
- [[Context Switch]]
- [[Interrupt]]
- [[Race Condition]]
- [[Thread]]

## Further reading

- [Wikipedia: Preemption (computing)](https://en.wikipedia.org/wiki/Preemption_(computing))
