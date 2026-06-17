---
type: "term"
branch: "Hardware & Architecture"
aliases: ["Trusted Platform Module"]
tags: [hardware]
status: "developed"
---

# TPM

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** Trusted Platform Module

A dedicated secure crypto-processor (a discrete chip, or a firmware equivalent) that stores keys, performs cryptographic operations, and holds integrity measurements in tamper-resistant **Platform Configuration Registers (PCRs)**. It is the hardware root of trust most platform-security features build on.

**Context.** The TPM is what makes [[Measured Boot]] and [[Remote Attestation]] possible: each boot stage is hashed into a PCR, and because PCRs can only be *extended* (never overwritten), a verifier can later prove whether the early boot was tampered with. It also anchors disk encryption (BitLocker seals keys to PCR state) and hardware-bound credentials ([[Credential Guard]] can bind to it). Windows 11 requires TPM 2.0.

## See also

- [[Measured Boot]]
- [[Secure Boot]]
- [[Chain of Trust]]
- [[HSM]]
- [[Firmware]]

## Often confused with

- [[HSM]] — both are secure crypto hardware, but a TPM is a low-cost chip bound to one machine's integrity; an HSM is a high-assurance appliance built for bulk key operations.

## Further reading

- [Wikipedia: Trusted Platform Module](https://en.wikipedia.org/wiki/Trusted_Platform_Module)
