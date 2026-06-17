---
type: "term"
branch: "Data & Databases"
de: "Replikation"
tags: [data]
status: "developed"
---

# Replication

> **Branch:** [[06 - Data & Databases|Data & Databases]]
> **German:** Replikation

Maintaining copies of data on multiple nodes for availability, read scaling, and durability — synchronous (wait for replicas) or asynchronous (don't).

**Context.** Sync replication gives stronger consistency at the cost of latency; async is faster but replicas lag, so a read from a replica can be stale. The leader/follower (primary/replica) topology is the common shape, with failover promoting a follower when the leader dies.

## See also

- [[Sharding]]
- [[Eventual Consistency]]
- [[Failover]]
- [[Leader Election]]
- [[Replication Lag]]

## Further reading

- [Wikipedia: Replication (computing)](https://en.wikipedia.org/wiki/Replication_(computing))
