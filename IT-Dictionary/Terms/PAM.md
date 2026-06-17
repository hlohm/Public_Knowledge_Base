---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["Privileged Access Management"]
tags: ["iam"]
status: "note"
---

# PAM

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** Privileged Access Management

**P**rivileged **A**ccess **M**anagement. Tooling and process for managing admin/root accounts: vaults, session recording, JIT elevation.

**Context.** The pattern: admins check out privileged credentials from a vault (or get JIT elevation), sessions to critical systems run through a recorded gateway, and passwords rotate after use. Even without commercial tooling, the budget version — separate admin accounts, LAPS, a hardened jump host — captures much of the value.

## See also

- [[JIT Access]]
- [[Separation of Duties]]
- [[Bastion Host]]
