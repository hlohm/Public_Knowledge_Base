---
type: "term"
branch: "Operating Systems"
tags: [os]
status: "developed"
---

# Context Switch

> **Branch:** [[03 - Operating Systems|Operating Systems]]

Saving the state of one process/thread and restoring another's so a single CPU can interleave many of them, creating the illusion of simultaneity.

**Context.** Switches aren't free — they cost cycles plus cache/TLB pollution. Excessive switching ('context-switch thrashing') from too many threads can make a system slower than fewer would.

## See also

- [[Scheduler]]
- [[Process]]
- [[Thread]]
- [[Preemption]]

## Further reading

- [Wikipedia: Context switch](https://en.wikipedia.org/wiki/Context_switch)
