---
type: "term"
branch: "Operating Systems"
tags: [os]
status: "developed"
---

# Scheduler

> **Branch:** [[03 - Operating Systems|Operating Systems]]

The kernel component that decides which ready process/thread runs next and for how long, balancing fairness, responsiveness, and throughput.

**Context.** Different goals need different policies: interactive desktops favour low latency, batch servers favour throughput, real-time systems favour deadline guarantees. The timer interrupt is what lets a *preemptive* scheduler take the CPU back.

## See also

- [[Preemption]]
- [[Context Switch]]
- [[Round Robin Scheduling]]
- [[Interrupt]]

## Further reading

- [Wikipedia: Scheduling (computing)](https://en.wikipedia.org/wiki/Scheduling_(computing))
