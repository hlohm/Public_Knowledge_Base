---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["Object Capabilities", "Capability Model"]
tags: ["iam"]
status: "developed"
---

# Capability-Based Security

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** Object Capabilities, Capability Model

An access-control paradigm in which access is granted by *possessing an unforgeable token* (a capability) that both names an object and carries the authority to use it. No token, no access — and no [[Ambient Authority]] lying around to abuse.

**Context.** This is the row-wise reading of the [[Access Control Matrix]]: each subject carries its rights instead of objects carrying lists. Because authority travels explicitly together with designation, capability systems structurally resist the [[Confused Deputy Problem]] — a privileged program tricked into misusing its own authority on an attacker's behalf. Pure capability systems are rare but real: seL4, Google's Fuchsia (handles), FreeBSD's [[Capsicum]]; the everyday Unix file descriptor behaves like a capability once passed over a socket — the receiver can use it regardless of what its own permissions would allow. Despite the name, Linux [[Capabilities]] are something else entirely.

## See also

- [[Access Control Matrix]]
- [[ACL]]
- [[Mandatory Access Control]]
- [[Least Privilege]]

## Often confused with

- [[Capabilities]] — Linux capabilities slice up root's *privileges*; object capabilities are tokens conferring access to *objects*. A name collision, not a family relation.

## Further reading

- [Wikipedia: Capability-based security](https://en.wikipedia.org/wiki/Capability-based_security)
