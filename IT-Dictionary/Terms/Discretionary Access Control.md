---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam", "fundamental"]
status: "developed"
---

# Discretionary Access Control

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

Access control in which the *owner* of an object decides who may access it — the model of classic Unix mode bits, POSIX ACLs, and Windows DACLs. "Discretionary" because protection is at the owner's discretion: whoever holds access can typically also grant it onward.

**Context.** DAC does the everyday work on every operating system, and its weak point is *ambient authority*: every program you run wields your entire identity, so the policy cannot tell you apart from a trojan acting as you — the classic trojan-horse problem. The superuser bypasses it outright. That is the gap [[Mandatory Access Control]] closes, layered *on top*: on Linux the DAC check runs first, and only if it passes does the [[LSM]] hook fire — MAC can further restrict, never grant. Finer-grained [[ACL]]s refine the granularity but not the paradigm.

## See also

- [[Mandatory Access Control]]
- [[ACL]]
- [[Permissions]]
- [[Authorization]]
- [[Access Control Matrix]]

## Often confused with

- [[Mandatory Access Control]] — who sets the policy: the owner (DAC) vs a central authority the owner cannot override (MAC).

## Further reading

- [Wikipedia: Discretionary access control](https://en.wikipedia.org/wiki/Discretionary_access_control)
