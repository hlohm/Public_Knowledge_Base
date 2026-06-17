---
type: "term"
branch: "Security"
domain: "Cryptography"
de: "Symmetrische Verschlüsselung"
tags: ["crypto"]
status: "note"
---

# Symmetric Encryption

> **Domain:** [[03 - Cryptography|Cryptography]]
> **German:** Symmetrische Verschlüsselung

Same key encrypts and decrypts. Fast. Examples: **AES**, **ChaCha20**. Core challenge: key distribution.

**Context.** Everything bulk is symmetric: disk encryption (BitLocker, LUKS), database TDE, VPN tunnels, the data phase of TLS. AES persists partly because CPUs accelerate it in hardware (AES-NI); ChaCha20 wins where they don't. The hard part was never the cipher — it's getting the same key to both ends safely, which is what key exchange and PKI exist for.

## See also

- [[Asymmetric Encryption]]
- [[Key Exchange]]
- [[Block Cipher]]

## Often confused with

- [[Asymmetric Encryption]] — Symmetric = one shared key; asymmetric = key pair.
