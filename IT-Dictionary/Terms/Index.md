---
type: "term"
branch: "Data & Databases"
tags: [data, fundamental]
status: "developed"
---

# Index

> **Branch:** [[06 - Data & Databases|Data & Databases]]

An auxiliary data structure (usually a B-tree) that lets the engine find rows by a key without scanning the whole table — trading write speed and disk space for read speed.

**Context.** The single biggest lever on query performance, and the most common thing missing when a query is slow. Every index must be updated on every write, so they're not free; the art is indexing exactly the columns your queries filter and sort on.

## See also

- [[B-tree]]
- [[Query Optimizer]]
- [[Full Table Scan]]
- [[Composite Index]]
- [[Cardinality]]

## Further reading

- [Wikipedia: Database index](https://en.wikipedia.org/wiki/Database_index)
