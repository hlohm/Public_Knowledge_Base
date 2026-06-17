---
type: "term"
branch: "Security"
domain: "Cryptography"
tags: ["crypto"]
status: "note"
---

# HSM

> **Domain:** [[03 - Cryptography|Cryptography]]

**H**ardware **S**ecurity **M**odule. Tamper-resistant hardware for key storage and crypto operations.

**Context.** The point is that keys are generated inside and can never leave — operations go in, signatures come out, and physical tampering zeroizes the device. Where you meet them: CA root keys, payment infrastructure, cloud KMS backends, and their small cousins: smartcards, YubiKeys, and TPMs are HSM-thinking at personal scale.

## See also

- [[Pepper]]
- [[PKI]]
- [[Secrets Manager]]
- [[TPM]]
