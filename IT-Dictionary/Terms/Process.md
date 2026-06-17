---
type: "term"
branch: "Operating Systems"
de: "Prozess"
tags: [os, fundamental]
status: "developed"
---

# Process

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **German:** Prozess

A running program together with its own isolated address space, file handles, and execution state. The OS's unit of resource ownership.

**Context.** Isolation is the point: a crash or corruption in one process can't directly touch another's memory. The cost of that isolation is why creating a process is heavier than creating a thread.

## See also

- [[Thread]]
- [[Context Switch]]
- [[Fork]]
- [[Virtual Memory]]

## Often confused with

- [[Thread]] — A process owns an address space; threads share one process's address space.

## Further reading

- [Wikipedia: Process (computing)](https://en.wikipedia.org/wiki/Process_(computing))
