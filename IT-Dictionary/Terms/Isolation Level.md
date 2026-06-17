---
type: "term"
branch: "Data & Databases"
aliases: ["Transaction Isolation"]
tags: ["data"]
status: "developed"
---

# Isolation Level

> **Branch:** [[06 - Data & Databases|Data & Databases]]
> **Also known as:** Transaction Isolation

How much a running [[Transaction]] is allowed to see of others' concurrent work. The SQL ladder: Read Uncommitted → Read Committed → Repeatable Read → Serializable — each rung forbidding more anomalies (dirty/non-repeatable/phantom reads) at more cost.

**Context.** The trap is that nobody runs Serializable by default: Postgres defaults to Read Committed, MySQL/InnoDB to Repeatable Read, and each implements the levels differently (snapshot isolation wearing various names). Subtle bugs — double-spends, lost updates — are often isolation-level bugs: code that assumed serializable behavior on a weaker level.

## See also

- [[Transaction]]
- [[ACID]]
- [[MVCC]]
- [[Race Condition]]

## Further reading

- [Wikipedia: Isolation (database systems)](https://en.wikipedia.org/wiki/Isolation_(database_systems))
