---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["Role-Based Access Control"]
tags: ["iam"]
status: "note"
---

# RBAC

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** Role-Based Access Control

**R**ole-**B**ased **A**ccess **C**ontrol. Permissions granted to roles, roles assigned to users. Simple and common.

**Context.** RBAC succeeds or fails on role design: model roles after job functions, keep the count manageable, and review membership — otherwise you get role explosion and people accumulating roles as they change jobs (privilege creep). Group-based licensing and access in AD/Entra is everyday RBAC.

## See also

- [[ABAC]]
- [[Authorization]]
- [[Least Privilege]]

## Often confused with

- [[ABAC]] — RBAC = static role-permission mapping; ABAC = dynamic attribute-driven decisions.
