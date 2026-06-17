---
type: "term"
branch: "Security"
domain: "Cryptography"
de: "Schlüsselaustausch"
tags: ["crypto"]
status: "developed"
---

# Key Exchange

> **Domain:** [[03 - Cryptography|Cryptography]]
> **German:** Schlüsselaustausch

Protocol to establish a shared secret over an insecure channel. **Diffie-Hellman**, **ECDH**.

**Context.** The quiet miracle underneath every TLS handshake: two parties who have never met derive a shared secret while an eavesdropper watching every byte learns nothing. Modern stacks use ephemeral ECDH (X25519); the post-quantum migration (ML-KEM hybrids, already shipping in browsers) targets key exchange first because recorded traffic is decryptable later.

## See also

- [[Symmetric Encryption]]
- [[Forward Secrecy]]
- [[TLS]]

## Further reading

- [Wikipedia: Diffie–Hellman key exchange](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange)
