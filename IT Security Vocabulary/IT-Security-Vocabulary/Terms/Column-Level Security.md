---
domain: "Identity & Access Management"
aliases: ["CLS", "Column-Level Security", "Column Level Security"]
tags: [iam, data]
---

# Column-Level Security

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** CLS

Database access control that restricts which **columns** (fields) a given user or role can read, independent of which rows they can access. Two users running the same query against the same table may get back different sets of columns.

**Context.** Implemented via column privileges (PostgreSQL `GRANT SELECT (col1, col2)`), column-level grants in SQL Server, or policy tags / masking policies in cloud warehouses (Snowflake, BigQuery). The natural complement to [[RLS]]: RLS narrows *which records* a user sees, CLS narrows *which fields*. Closely related to **dynamic data masking**, which differs by *obscuring* a column's values (e.g. `***-**-1234`) rather than hiding the column outright. Often driven by [[Data Classification]] — sensitive fields like PII or PHI get locked down or masked while the rest of the row stays visible.

## See also

- [[RLS]]
- [[Authorization]]
- [[RBAC]]
- [[ABAC]]
- [[Least Privilege]]
- [[Need to Know]]
- [[Data Classification]]
- [[Defense in Depth]]

## Often confused with

- [[RLS]] — RLS controls *which records* (rows) you can access; CLS controls *which fields* (columns). Same access-control idea applied along perpendicular axes of the table — they're frequently used together.

## Further reading

- [PostgreSQL: GRANT (column privileges)](https://www.postgresql.org/docs/current/sql-grant.html)
