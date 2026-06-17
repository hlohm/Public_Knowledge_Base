---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["Plaintext", "\"Ciphertext\""]
tags: ["crypto-basics"]
status: "note"
---

# Plaintext and Ciphertext

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** Plaintext, "Ciphertext"

Pre- and post-encryption data.

**Context.** Worth keeping precise in incident write-ups and configs: "plaintext" also describes any data stored or sent unencrypted (plaintext passwords, plaintext HTTP). "Cleartext" specifically means never-encrypted. Ciphertext should be indistinguishable from random noise — visible structure means something is broken.
