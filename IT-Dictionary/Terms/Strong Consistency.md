---
type: "term"
branch: "Data & Databases"
aliases: ["Linearizability"]
tags: ["data"]
status: "developed"
---

# Strong Consistency

> **Branch:** [[06 - Data & Databases|Data & Databases]]
> **Also known as:** Linearizability

The guarantee that every read sees the most recent committed write, system-wide — the distributed system behaves as if there were a single copy of the data. **Linearizability** is the formal version.

**Context.** Strong consistency is what single-node intuition silently assumes and what distribution makes expensive: per [[CAP Theorem]], under partition you pay with availability, and even without partitions you pay coordination latency (consensus rounds). The design question is rarely 'strong or eventual?' globally — it's *which operations* (payments: yes; view counters: no).

## See also

- [[Eventual Consistency]]
- [[CAP Theorem]]
- [[ACID]]
- [[Replication]]

## Further reading

- [Wikipedia: Consistency model](https://en.wikipedia.org/wiki/Consistency_model)
