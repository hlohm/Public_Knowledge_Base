---
type: "term"
branch: "Data & Databases"
aliases: ["Object-Relational Mapping"]
tags: [data]
status: "developed"
---

# ORM

> **Branch:** [[06 - Data & Databases|Data & Databases]]
> **Also known as:** Object-Relational Mapping

A library that maps database rows to objects in your programming language, letting you query and persist data without writing raw SQL.

**Context.** Productive for CRUD, but the abstraction leaks: the classic **N+1 query** problem and opaque generated SQL bite at scale. The 'object-relational impedance mismatch' it papers over is real. Know the SQL underneath, even when the ORM writes it.

## See also

- [[SQL]]
- [[RDBMS]]
- [[N+1 Problem]]
- [[Active Record Pattern]]

## Further reading

- [Wikipedia: Object–relational mapping](https://en.wikipedia.org/wiki/Object–relational_mapping)
