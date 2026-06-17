---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam", "modern"]
status: "note"
---

# JIT Access

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

**J**ust-**I**n-**T**ime access. Grant privileges only when needed, only for as long as needed. Removes standing privilege.

**Context.** Standing admin rights are a 24/7 attack surface; JIT shrinks the window to the task at hand. In practice: Entra PIM role activation with approval and time limit, or vault-issued ephemeral credentials. Side benefit — every elevation leaves an auditable request trail with a stated reason.

## See also

- [[PAM]]
- [[Least Privilege]]
