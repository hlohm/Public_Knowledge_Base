---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["Post-Quantum Cryptography"]
tags: ["crypto", "modern"]
status: "developed"
---

# PQC

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** Post-Quantum Cryptography

**P**ost-**Q**uantum **C**ryptography. Algorithms believed resistant to quantum attacks. NIST has standardized an initial set (ML-KEM, ML-DSA). Migration is a multi-year project.

**Context.** The driver is "harvest now, decrypt later": traffic recorded today is at risk the day a cryptographically relevant quantum computer exists. NIST finalized ML-KEM (key exchange) and ML-DSA/SLH-DSA (signatures) in 2024; hybrid key exchange is already live in major browsers and SSH. Signatures and PKI migrate slower — inventorying where you use which algorithm is the actionable first step.

## See also

- [[Asymmetric Encryption]]

## Further reading

- [NIST: Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
