---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
tags: [endpoint]
status: "developed"
---

# Measured Boot

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]

A boot-integrity scheme where each component hashes the next *before* handing off, recording the measurements into the [[TPM]]'s PCRs. It doesn't stop anything from running — it produces a tamper-evident log of exactly what ran, which [[Remote Attestation]] can later verify against a known-good baseline.

**Context.** This is the one mechanism that catches a *successful* pre-boot implant. [[Secure Boot]] can be bypassed by a signed-but-vulnerable component; Measured Boot still records the deviation, so an attestation server sees that the boot no longer matches policy and can quarantine the device. Verify *and* measure — they cover each other's gaps.

## See also

- [[TPM]]
- [[Secure Boot]]
- [[Remote Attestation]]
- [[Chain of Trust]]
- [[Bootkit]]

## Often confused with

- [[Secure Boot]] — verification that *prevents* untrusted code from running, versus measurement that *detects* what ran after the fact.

## Further reading

- [Wikipedia: Trusted Platform Module](https://en.wikipedia.org/wiki/Trusted_Platform_Module)
