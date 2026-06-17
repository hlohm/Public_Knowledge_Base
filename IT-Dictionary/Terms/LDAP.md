---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam", "protocol"]
status: "note"
---

# LDAP

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

**L**ightweight **D**irectory **A**ccess **P**rotocol. Used to query directory services. Active Directory speaks LDAP.

**Context.** The protocol you script against AD with: filters like `(&(objectClass=user)(memberOf=...))`, ports 389 (LDAP, +StartTLS) and 636 (LDAPS). Two hygiene items: require signing/channel binding to blunt relay attacks, and remember anything that does an LDAP *bind* with a service account stores that password somewhere — printer address books are infamous for leaking them.

## See also

- [[Active Directory]]
- [[IAM]]
