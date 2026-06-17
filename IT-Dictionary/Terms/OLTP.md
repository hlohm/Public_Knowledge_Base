---
type: "term"
branch: "Data & Databases"
aliases: ["Online Transaction Processing"]
tags: [data]
status: "developed"
---

# OLTP

> **Branch:** [[06 - Data & Databases|Data & Databases]]
> **Also known as:** Online Transaction Processing

Workloads dominated by many small, fast read/write transactions — order entry, banking, the operational database behind an app.

**Context.** Optimised for low-latency point operations and high concurrency; row-oriented storage suits it. The counterpart to OLAP, and the reason analytics is usually run on a separate system rather than your production database.

## See also

- [[OLAP]]
- [[Transaction]]
- [[RDBMS]]
- [[Row-oriented Storage]]

## Often confused with

- [[OLAP]] — OLTP is many small transactions (running the business); OLAP is few large analytical scans (understanding the business).

## Further reading

- [Wikipedia: Online transaction processing](https://en.wikipedia.org/wiki/Online_transaction_processing)
