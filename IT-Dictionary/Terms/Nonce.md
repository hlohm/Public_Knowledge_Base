---
type: "term"
branch: "Security"
domain: "Cryptography"
tags: ["crypto"]
status: "note"
---

# Nonce

> **Domain:** [[03 - Cryptography|Cryptography]]

**N**umber used **once**. Prevents replay attacks; required by many crypto modes.

**Context.** Appears at every layer: TLS handshakes, OIDC flows, AEAD ciphers, anti-replay in APIs. The contract is strict uniqueness per key/context — counters and random values of sufficient size both work, but "random 32-bit value" will collide in practice (birthday math) and has caused real CVEs.

## See also

- [[IV]]
- [[Replay Attack]]
