---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["Initialization Vector"]
tags: ["crypto"]
status: "note"
---

# IV

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** Initialization Vector

**I**nitialization **V**ector. Random input that makes encryption of identical plaintexts produce different ciphertexts.

**Context.** IV misuse is a classic implementation killer: reusing an IV in AES-GCM doesn't just leak patterns, it can reveal the authentication key. Rules of thumb: never hardcode, never reuse under the same key, and use the size the mode specifies. Distinct from a nonce mainly in connotation — some modes need unpredictability, others only uniqueness.

## See also

- [[Nonce]]
- [[Symmetric Encryption]]
- [[Block Cipher]]
