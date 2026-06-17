---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["Multilevel Security"]
tags: ["iam"]
status: "developed"
---

# MLS

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** Multilevel Security

**M**ulti**l**evel **S**ecurity. Access control over *sensitivity levels*: data carries classifications (public → top secret), subjects carry clearances, and a mandatory policy governs how information may flow between levels.

**Context.** The canonical confidentiality policy is the [[Bell–LaPadula Model]]: *no read up* (you cannot read above your clearance) and *no write down* (you cannot leak downward). Its integrity mirror is the [[Biba Model]] — read up, write down, trust flows the other way. Born in military computing and the origin story of [[Mandatory Access Control]], MLS survives in [[SELinux]] as the optional fourth field of a security context (`s0`, `s0-s15:c0.c1023`). Its pragmatic descendant is [[MCS]] (Multi-Category Security), which reuses the same machinery without the hierarchy: container runtimes give every container a unique category pair, so two workloads that escape to the host still cannot touch each other's files.

## See also

- [[Mandatory Access Control]]
- [[SELinux]]
- [[Data Classification]]

## Further reading

- [Wikipedia: Multilevel security](https://en.wikipedia.org/wiki/Multilevel_security)
