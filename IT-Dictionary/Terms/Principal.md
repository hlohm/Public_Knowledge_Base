---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam"]
status: "note"
---

# Principal

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

The entity making a request (user, service, role).

**Context.** The umbrella term that keeps policy language precise: users, groups, service accounts, computer accounts, and cloud roles are all principals, and access rules should say which kinds they accept. In AD, every object that can authenticate is a security principal with a SID; in AWS, the `Principal` field in a policy is exactly this concept.

## See also

- [[Identity]]
- [[Service Account]]
