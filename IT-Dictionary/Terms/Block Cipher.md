---
type: "term"
branch: "Security"
domain: "Cryptography"
tags: ["crypto"]
status: "developed"
---

# Block Cipher

> **Domain:** [[03 - Cryptography|Cryptography]]

Encrypts fixed-size chunks (AES). Contrast with stream ciphers (ChaCha20) that produce a keystream XORed with plaintext.

**Context.** The cipher alone is half the story — the *mode* makes or breaks it. ECB leaks patterns (the famous penguin), CBC needs careful padding, and modern practice is AEAD modes like AES-GCM or ChaCha20-Poly1305 that encrypt and authenticate in one pass. "We use AES" is meaningless without the mode.

## See also

- [[Symmetric Encryption]]
- [[IV]]

## Further reading

- [Wikipedia: Block cipher mode of operation](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)
