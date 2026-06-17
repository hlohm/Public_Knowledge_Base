---
type: "term"
branch: "Data & Databases"
aliases: ["Atomicity Consistency Isolation Durability"]
tags: [data, fundamental]
status: "developed"
---

# ACID

> **Branch:** [[06 - Data & Databases|Data & Databases]]
> **Also known as:** Atomicity Consistency Isolation Durability

The four guarantees of a reliable transaction: **A**tomicity (all-or-nothing), **C**onsistency (valid state to valid state), **I**solation (concurrent transactions don't corrupt each other), **D**urability (committed data survives crashes).

**Context.** What lets you reason about a database as if you were the only user even when thousands aren't. Isolation is the subtle one — full serialisability is expensive, so engines offer weaker levels (read committed, repeatable read) with documented anomalies.

## See also

- [[Transaction]]
- [[Isolation Level]]
- [[BASE]]
- [[MVCC]]
- [[Durability]]

## Often confused with

- [[BASE]] — ACID prioritises correctness and consistency; BASE deliberately relaxes them for availability and scale.

## Further reading

- [Wikipedia: ACID](https://en.wikipedia.org/wiki/ACID)
