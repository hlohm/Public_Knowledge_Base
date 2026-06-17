---
type: "term"
branch: "Data & Databases"
tags: [data, fundamental]
status: "developed"
---

# Foreign Key

> **Branch:** [[06 - Data & Databases|Data & Databases]]

A column referencing the primary key of another table, enforcing **referential integrity** — you can't reference a row that doesn't exist.

**Context.** The database-level guarantee that relationships stay valid (no orphaned orders pointing at a deleted customer). Some high-scale systems drop them for write performance and enforce integrity in the application — a real tradeoff, not free.

## See also

- [[Primary Key]]
- [[Join]]
- [[Referential Integrity]]
- [[Normalization]]

## Further reading

- [Wikipedia: Foreign key](https://en.wikipedia.org/wiki/Foreign_key)
