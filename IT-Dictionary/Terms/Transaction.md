---
type: "term"
branch: "Data & Databases"
de: "Transaktion"
tags: [data, fundamental]
status: "developed"
---

# Transaction

> **Branch:** [[06 - Data & Databases|Data & Databases]]
> **German:** Transaktion

A unit of work executed as a single atomic, isolated operation — it either fully commits or fully rolls back, leaving the database consistent either way.

**Context.** The abstraction that lets you bundle 'debit A, credit B' so a crash between them can't lose money. The ACID guarantees are exactly the transaction's promises. In distributed systems, multi-node transactions are the hard, expensive case.

## See also

- [[ACID]]
- [[Commit]]
- [[Rollback]]
- [[Isolation Level]]
- [[Two-phase Commit]]

## Further reading

- [Wikipedia: Database transaction](https://en.wikipedia.org/wiki/Database_transaction)
