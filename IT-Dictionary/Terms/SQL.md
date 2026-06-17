---
type: "term"
branch: "Data & Databases"
aliases: ["Structured Query Language"]
tags: [data, fundamental]
status: "developed"
---

# SQL

> **Branch:** [[06 - Data & Databases|Data & Databases]]
> **Also known as:** Structured Query Language

The declarative language for querying and manipulating relational data — you state *what* you want and the engine's query planner decides *how* to fetch it.

**Context.** Declarative is the whole point: the optimiser is free to use indexes, reorder joins, and parallelise without you rewriting the query. Standardised (SQL-92 onward) but every vendor adds dialect, so portability is partial.

## See also

- [[RDBMS]]
- [[Query Optimizer]]
- [[Join]]
- [[Index]]
- [[NoSQL]]

## Often confused with

- [[NoSQL]] — SQL names a query language; NoSQL names a category of stores, many of which now offer SQL-like languages anyway.

## Further reading

- [Wikipedia: SQL](https://en.wikipedia.org/wiki/SQL)
