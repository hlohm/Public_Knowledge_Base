---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["PFS", "\"Perfect Forward Secrecy\""]
tags: ["crypto"]
status: "note"
---

# Forward Secrecy

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** PFS, "Perfect Forward Secrecy"

Compromise of long-term keys doesn't reveal past session data. Achieved via ephemeral key exchange (DHE, ECDHE).

**Context.** The threat model: an adversary records your encrypted traffic for years, then obtains the server's private key (court order, breach, factoring). Without forward secrecy, everything decrypts retroactively. TLS 1.3 made ephemeral key exchange mandatory — one reason it's a meaningful upgrade, and a property worth checking on VPNs.

## See also

- [[TLS]]
- [[Key Exchange]]
