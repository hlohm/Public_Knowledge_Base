---
type: "term"
branch: "Data & Databases"
aliases: ["Multiversion Concurrency Control"]
tags: [data]
status: "developed"
---

# MVCC

> **Branch:** [[06 - Data & Databases|Data & Databases]]
> **Also known as:** Multiversion Concurrency Control

A concurrency technique where writes create new versions of rows rather than overwriting, so readers see a consistent snapshot without blocking writers (and vice versa).

**Context.** Why Postgres readers don't block writers. The cost is bloat — old versions must be garbage-collected (Postgres's VACUUM), and long-running transactions hold old versions alive. The mechanism behind snapshot isolation.

## See also

- [[Transaction]]
- [[Isolation Level]]
- [[ACID]]
- [[Snapshot Isolation]]

## Further reading

- [Wikipedia: Multiversion concurrency control](https://en.wikipedia.org/wiki/Multiversion_concurrency_control)
