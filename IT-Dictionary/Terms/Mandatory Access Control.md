---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam", "fundamental"]
status: "developed"
---

# Mandatory Access Control

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

Access control in which a central, system-wide policy — defined by an administrator and enforced by the operating system — decides every access. Neither resource owners nor the processes themselves can loosen it, and it binds privileged users too: being root does not override the policy.

**Context.** Mandatory access control exists because [[Discretionary Access Control]] cannot contain the programs you run — a trojan executes with your full identity, so your files are its to leak. Born in military multilevel systems ([[MLS]]), today's mainstream MAC is label- or profile-based and aimed at confining exposed services: [[SELinux]] and [[AppArmor]] on Linux, SELinux again on Android, and Windows' slimmer sibling [[Mandatory Integrity Control]]. The defining question is always *who sets the policy* — here the system mandates it; under DAC the owner grants at discretion.

## See also

- [[Discretionary Access Control]]
- [[SELinux]]
- [[AppArmor]]
- [[Type Enforcement]]
- [[MLS]]
- [[Least Privilege]]
- [[Authorization]]

## Often confused with

- [[Discretionary Access Control]] — DAC: the owner decides; MAC: the system's policy decides and the owner can't override it.
- [[MAC Address]] — unrelated; that MAC is Media Access Control, a link-layer addressing term.
- [[HMAC]] — also unrelated; in cryptography MAC means Message Authentication Code. Three meanings, one acronym — context decides.

## Further reading

- [Wikipedia: Mandatory access control](https://en.wikipedia.org/wiki/Mandatory_access_control)
