---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["Public-Key Cryptography"]
de: "Asymmetrische Verschlüsselung"
tags: ["crypto"]
status: "developed"
---

# Asymmetric Encryption

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** Public-Key Cryptography
> **German:** Asymmetrische Verschlüsselung

Key pair: public encrypts / verifies, private decrypts / signs. Solves the key-distribution problem. Examples: **RSA**, **ECC**, **Ed25519**.

**Context.** In real protocols asymmetric crypto is the bootstrap, not the workhorse: it authenticates parties and establishes a symmetric session key, then gets out of the way (it's orders of magnitude slower). RSA is legacy-everywhere; new designs default to elliptic curves. Key sizes are not comparable across families — RSA-3072 ≈ ECC-256.

## See also

- [[Symmetric Encryption]]
- [[Digital Signature]]
- [[PKI]]
- [[Key Exchange]]

## Further reading

- [Wikipedia: Public-key cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography)
