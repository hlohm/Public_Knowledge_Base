---
type: "term"
branch: "Data & Databases"
tags: ["data"]
status: "developed"
---

# Denormalization

> **Branch:** [[06 - Data & Databases|Data & Databases]]

Deliberately duplicating data or pre-joining tables — violating [[Normalization]] — to make reads faster by avoiding joins at query time.

**Context.** The operative word is *deliberately*: denormalization trades update complexity (every copy must be kept in sync, usually by application code that will eventually have a bug) for read speed. Standard in analytics schemas (star schema), caches, and NoSQL document design; suspicious in a transactional system's source of truth. Normalize first, denormalize where measurement says so.

## See also

- [[Normalization]]
- [[Index]]
- [[NoSQL]]
- [[OLAP]]
- [[Replication]]

## Further reading

- [Wikipedia: Denormalization](https://en.wikipedia.org/wiki/Denormalization)
