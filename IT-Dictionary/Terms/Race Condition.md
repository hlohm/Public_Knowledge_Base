---
type: "term"
branch: "Operating Systems"
tags: [os, anti-pattern]
status: "developed"
---

# Race Condition

> **Branch:** [[03 - Operating Systems|Operating Systems]]

A bug where the result depends on the unpredictable timing of concurrent operations on shared state — e.g. two threads incrementing a counter and losing an update.

**Context.** Notoriously hard to reproduce because they're timing-dependent ('Heisenbugs'). The TOCTOU (time-of-check-to-time-of-use) race is a whole security bug class where a file is swapped between the check and the use.

## See also

- [[Mutex]]
- [[Deadlock]]
- [[Critical Section]]
- [[Concurrency]]

## Further reading

- [Wikipedia: Race condition](https://en.wikipedia.org/wiki/Race_condition)
