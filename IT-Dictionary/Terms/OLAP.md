---
type: "term"
branch: "Data & Databases"
aliases: ["Online Analytical Processing"]
tags: [data]
status: "developed"
---

# OLAP

> **Branch:** [[06 - Data & Databases|Data & Databases]]
> **Also known as:** Online Analytical Processing

Workloads dominated by large aggregating queries over historical data — reporting, dashboards, analytics — typically on a data warehouse.

**Context.** Optimised for scanning and aggregating columns across millions of rows; columnar storage (Parquet, ClickHouse, BigQuery) is the natural fit. Kept separate from OLTP so heavy analytics don't starve the operational system.

## See also

- [[OLTP]]
- [[Data Warehouse]]
- [[Column-oriented Storage]]
- [[Star Schema]]

## Further reading

- [Wikipedia: Online analytical processing](https://en.wikipedia.org/wiki/Online_analytical_processing)
