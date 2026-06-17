---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["Access Control List"]
tags: ["iam"]
status: "developed"
---

# ACL

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** Access Control List

**A**ccess **C**ontrol **L**ist. A per-object list of entries stating who may do what — each entry a (principal, permissions) pair, attached to the thing being protected.

**Context.** Two habitats share the name. *Filesystem and object ACLs* (POSIX ACLs, the NTFS DACL) refine the coarse owner/group/other model with per-user and per-group entries — finer-grained [[Discretionary Access Control]], same paradigm. *Network ACLs* on routers and firewalls filter traffic by address, port, and protocol — packet filtering that borrowed the name, not file permissions. Conceptually, an ACL is one *column* of the [[Access Control Matrix]] stored with its object; the row-wise dual, stored with the subject, is the capability list ([[Capability-Based Security]]).

## See also

- [[Permissions]]
- [[Discretionary Access Control]]
- [[Access Control Matrix]]
- [[Firewall]]

## Often confused with

- [[Capability-Based Security]] — an ACL asks "who may touch this object?"; a capability asks "what may this subject touch?". Columns vs rows of the same matrix.

## Further reading

- [Wikipedia: Access-control list](https://en.wikipedia.org/wiki/Access_control_list)
