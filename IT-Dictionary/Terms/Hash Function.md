---
type: "term"
branch: "Security"
domain: "Cryptography"
tags: [crypto]
status: "note"
---

# Hash Function

> **Domain:** [[03 - Cryptography|Cryptography]]

One-way function producing a fixed-length digest. Used for integrity, fingerprinting, password storage. Examples: SHA-256, SHA-3, BLAKE2/3.

**Context.** MD5 and SHA-1 are broken for security use — fine only as fast non-security checksums.

## See also

- [[HMAC]]
- [[Digital Signature]]
- [[Salt]]

## Often confused with

- [[HMAC]] — Hash gives integrity; HMAC adds authenticity via a shared secret.
- [[Symmetric Encryption]] — Hashing is one-way; encryption is reversible with a key.
