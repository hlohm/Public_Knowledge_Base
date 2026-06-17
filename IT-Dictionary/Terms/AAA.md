---
type: "term"
branch: "Security"
domain: "Core Principles & Models"
aliases: ["Authentication Authorization Accounting"]
tags: ["fundamental"]
status: "developed"
---

# AAA

> **Domain:** [[01 - Core Principles|Core Principles & Models]]
> **Also known as:** Authentication Authorization Accounting

**A**uthentication, **A**uthorization, **A**ccounting. The three pillars of access control: prove who you are, determine what you can do, record what you did.

**Context.** You meet AAA wherever access is brokered centrally: RADIUS/TACACS+ for network gear, NPS in Windows shops, and conceptually in every cloud IAM. When troubleshooting access, identify *which* A is failing — wrong identity, missing permission, or no log trail are three different problems.

## See also

- [[Authentication]]
- [[Authorization]]
- [[IAM]]

## Often confused with

- [[CIA Triad]] — AAA is access; CIA is goals.

## Further reading

- [Wikipedia: AAA (computer security)](https://en.wikipedia.org/wiki/AAA_(computer_security))
