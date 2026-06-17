---
type: "term"
branch: "Data & Databases"
tags: [data, fundamental]
status: "developed"
---

# Primary Key

> **Branch:** [[06 - Data & Databases|Data & Databases]]

The column(s) uniquely identifying each row in a table — non-null, unique, and the row's stable identity.

**Context.** Choosing natural (a real attribute) vs surrogate (an auto-generated id like a UUID or sequence) keys is a perennial debate; surrogate usually wins for stability. The primary key typically backs a clustered index, shaping physical row order.

## See also

- [[Foreign Key]]
- [[Index]]
- [[UUID]]
- [[Composite Key]]

## Further reading

- [Wikipedia: Primary key](https://en.wikipedia.org/wiki/Primary_key)
