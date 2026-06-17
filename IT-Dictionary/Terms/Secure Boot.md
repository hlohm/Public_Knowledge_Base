---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
tags: [endpoint]
status: "developed"
---

# Secure Boot

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]

A [[UEFI]] feature that cryptographically verifies each component in the boot chain — firmware drivers, the [[Boot Loader]], the OS kernel — against a database of trusted keys (`db`) and revoked ones (`dbx`) before allowing it to run. It enforces a [[Chain of Trust]] from power-on to the OS.

**Context.** Secure Boot is what retired the easy disk-level [[Bootkit]]. But it verifies *signatures*, not *behaviour*: a validly-signed-but-vulnerable binary that hasn't been revoked is still trusted, which is exactly how the BlackLotus bootkit (2023) bypassed it on patched Windows 11. The practical lessons are to keep the `dbx` revocation list current and to add [[Measured Boot]], so tampering is *detected* even if verification is subverted.

## See also

- [[UEFI]]
- [[Chain of Trust]]
- [[Measured Boot]]
- [[Digital Signature]]
- [[Bootkit]]

## Often confused with

- [[Measured Boot]] — Secure Boot *blocks* untrusted code at each step; Measured Boot blocks nothing, it *records* what ran so a verifier can judge it afterwards.

## Further reading

- [Wikipedia: UEFI — Secure Boot](https://en.wikipedia.org/wiki/UEFI#Secure_Boot)
