---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["AuthZ"]
de: "Autorisierung"
tags: ["iam", "fundamental"]
status: "note"
---

# Authorization

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** AuthZ
> **German:** Autorisierung

Determining what an authenticated principal is allowed to do. Often abbreviated **AuthZ**.

**Context.** Almost always the harder half. Authentication is a solved handshake; authorization is business logic — who may see which customer, approve what amount, delete whose data — and that's where the bugs live. Broken access control tops the OWASP Top 10, mostly as missing object-level checks rather than exotic flaws.

## See also

- [[Authentication]]
- [[RBAC]]
- [[ABAC]]
- [[Scope]]

## Often confused with

- [[Authentication]] — AuthZ comes *after* AuthN — most confused pair in the field.
