---
type: "term"
branch: "Data & Databases"
aliases: ["Brewer's Theorem"]
tags: [data, fundamental]
status: "developed"
---

# CAP Theorem

> **Branch:** [[06 - Data & Databases|Data & Databases]]
> **Also known as:** Brewer's Theorem

In a distributed data store, when a network **P**artition happens you can keep **C**onsistency or **A**vailability but not both — you can have at most two of consistency, availability, and partition tolerance.

**Context.** Often mis-stated as 'pick two of three'. Since partitions are a fact of networks, not a choice, the real decision is CP vs AP *during a partition*. Modern systems make this tunable per operation rather than as a global stance.

## See also

- [[Eventual Consistency]]
- [[BASE]]
- [[Partition Tolerance]]
- [[Distributed System]]
- [[PACELC]]

## Further reading

- [Wikipedia: CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem)
- [CAP theorem critique — Martin Kleppmann](https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html)
