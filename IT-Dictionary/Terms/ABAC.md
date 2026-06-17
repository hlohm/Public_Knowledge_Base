---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["Attribute-Based Access Control"]
tags: ["iam"]
status: "note"
---

# ABAC

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** Attribute-Based Access Control

**A**ttribute-**B**ased **A**ccess **C**ontrol. Decisions based on attributes (user, resource, environment). More expressive than RBAC.

**Context.** What ABAC buys you: "managers may approve expenses of their own department during business hours from managed devices" as one policy instead of a role explosion. The cost is debuggability — answering "why was this denied?" requires evaluating the whole rule set. Azure AD Conditional Access and AWS IAM conditions are ABAC in production clothing.

## See also

- [[RBAC]]
- [[Authorization]]
