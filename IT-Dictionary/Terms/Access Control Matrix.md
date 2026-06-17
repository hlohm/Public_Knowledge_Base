---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["Access Matrix", "Lampson Matrix"]
tags: ["iam"]
status: "developed"
---

# Access Control Matrix

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** Access Matrix, Lampson Matrix

The formal model beneath most access control (Butler Lampson, 1971): a grid with one row per subject, one column per object, and each cell holding that subject's rights over that object.

**Context.** Nobody stores the matrix literally — it is enormous and almost entirely empty. Real systems store *slices*: [[ACL]]s keep it column by column (with each object), capability lists keep it row by row (with each subject — [[Capability-Based Security]]), and policy-driven systems like [[SELinux]] store no cells at all, deriving them from rules over equivalence classes (types, roles). A useful lens for the whole field: most access-control designs are answers to the question "how do we compress this matrix without losing the ability to query it?"

## See also

- [[ACL]]
- [[Capability-Based Security]]
- [[Discretionary Access Control]]
- [[RBAC]]
- [[Type Enforcement]]

## Further reading

- [Wikipedia: Access control matrix](https://en.wikipedia.org/wiki/Access_control_matrix)
