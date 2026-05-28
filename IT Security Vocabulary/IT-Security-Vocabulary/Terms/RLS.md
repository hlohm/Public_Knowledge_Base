---
domain: "Identity & Access Management"
aliases: ["Row-Level Security", "Row Level Security"]
tags: [iam, data]
---

# RLS

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** Row-Level Security

Database access control that restricts which **rows** a given user or role can read or modify, based on a policy the database evaluates per query. The same `SELECT` returns different rows to different users — enforcement is transparent to the application.

**Context.** Implemented natively in most modern databases (PostgreSQL `CREATE POLICY`, SQL Server security policies). It's the backbone of **multi-tenant SaaS**, where one table holds many tenants' data and an RLS policy keyed on `tenant_id` keeps them isolated. Distinct from **column-level security** / **data masking**, which restrict *which fields* are visible rather than *which rows*. Because enforcement lives in the database, RLS still holds if the application layer has a bug — making it a defense-in-depth control for data.

## See also

- [[Authorization]]
- [[RBAC]]
- [[ABAC]]
- [[Least Privilege]]
- [[Need to Know]]
- [[Tenant]]
- [[Defense in Depth]]

## Often confused with

- [[ABAC]] — RBAC and ABAC are access-control *models* (how a decision is made); RLS is an enforcement *mechanism* (where it's applied — the data layer). You typically drive RLS policies *using* roles or attributes.
- [[Column-Level Security]]  — Database access control that restricts which **columns** (fields) a given user or role can read, independent of which rows they can access. Two users running the same query against the same table may get back different sets of columns.

## Further reading

- [PostgreSQL: Row Security Policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
