---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam"]
status: "note"
---

# Claim

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

A piece of information about a principal inside a token (e.g. `email`, `role`, `exp`).

**Context.** Claims are where identity meets application logic: the app reads `groups` or `roles` from the token instead of querying a directory. The classic integration headaches are claim mapping (IdP sends `upn`, app expects `email`) and group bloat overflowing token size limits in AD-heavy environments.

## See also

- [[JWT]]
- [[Assertion]]
- [[Token]]
