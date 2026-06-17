---
type: "term"
branch: "Data & Databases"
tags: [data, modern]
status: "developed"
---

# Sharding

> **Branch:** [[06 - Data & Databases|Data & Databases]]

Horizontally partitioning a dataset across multiple machines by a **shard key**, so each node holds a subset — the main way to scale writes beyond one server.

**Context.** Scales out where vertical scaling (a bigger box) hits a wall, but the shard key is a near-irreversible decision: pick badly and you get hotspots or cross-shard queries that defeat the purpose. Cross-shard transactions and joins are the recurring pain.

## See also

- [[Replication]]
- [[Partition]]
- [[Horizontal Scaling]]
- [[Consistent Hashing]]

## Often confused with

- [[Replication]] — Sharding splits data across nodes for capacity; replication copies the same data to nodes for availability and read scaling.

## Further reading

- [Wikipedia: Shard (database architecture)](https://en.wikipedia.org/wiki/Shard_(database_architecture))
