---
type: "term"
branch: "Data & Databases"
aliases: ["Basically Available Soft-state Eventual consistency"]
tags: [data]
status: "developed"
---

# BASE

> **Branch:** [[06 - Data & Databases|Data & Databases]]
> **Also known as:** Basically Available Soft-state Eventual consistency

The consistency philosophy of many distributed NoSQL systems: **B**asically **A**vailable, **S**oft state, **E**ventual consistency — accept temporary inconsistency in exchange for availability and partition tolerance.

**Context.** A deliberate, half-joking counterpoint to ACID (acid vs. base). It's the CAP theorem made into a design stance: when the network partitions, stay available and reconcile later.

## See also

- [[ACID]]
- [[Eventual Consistency]]
- [[CAP Theorem]]
- [[NoSQL]]

## Further reading

- [Wikipedia: Eventual consistency](https://en.wikipedia.org/wiki/Eventual_consistency)
