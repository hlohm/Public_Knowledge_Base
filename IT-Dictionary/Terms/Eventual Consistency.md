---
type: "term"
branch: "Data & Databases"
tags: [data]
status: "developed"
---

# Eventual Consistency

> **Branch:** [[06 - Data & Databases|Data & Databases]]

A consistency model guaranteeing that, absent new writes, all replicas will *eventually* converge to the same value — but a read may return stale data in the meantime.

**Context.** The pragmatic consistency of large distributed systems (DNS, S3, shopping carts). Acceptable when stale-for-a-moment is fine; dangerous when it isn't (don't build a bank ledger on it). Read-your-writes and monotonic-read are stronger session guarantees layered on top.

## See also

- [[CAP Theorem]]
- [[BASE]]
- [[Strong Consistency]]
- [[Replication]]
- [[Conflict Resolution]]

## Often confused with

- [[Strong Consistency]] — Strong consistency: every read sees the latest write. Eventual: reads may lag but converge.

## Further reading

- [Wikipedia: Eventual consistency](https://en.wikipedia.org/wiki/Eventual_consistency)
