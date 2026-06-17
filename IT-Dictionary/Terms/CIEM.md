---
type: "term"
branch: "Security"
domain: "Cloud & Modern Architecture"
aliases: ["Cloud Infrastructure Entitlement Management"]
tags: ["cloud", "iam"]
status: "note"
---

# CIEM

> **Domain:** [[10 - Cloud and Modern Architecture|Cloud & Modern Architecture]]
> **Also known as:** Cloud Infrastructure Entitlement Management

**C**loud **I**nfrastructure **E**ntitlement **M**anagement. IAM-for-cloud, focused on detecting over-permissioned identities.

**Context.** Exists because cloud IAM sprawls beyond human review: thousands of roles, policies, and trust relationships, where one `iam:PassRole` wildcard quietly equals admin. CIEM tooling computes *effective* permissions, flags unused and excessive ones, and proposes right-sizing — least privilege as a continuous process rather than a design-time hope.

## See also

- [[CSPM]]
- [[CNAPP]]
- [[Service Account]]
- [[Least Privilege]]
