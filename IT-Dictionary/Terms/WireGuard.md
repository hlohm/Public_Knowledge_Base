---
type: "term"
branch: "Security"
domain: "Network Security"
tags: ["network", "cryptography", "modern"]
status: "developed"
---

# WireGuard

> **Domain:** [[05 - Network Security|Network Security]]

A modern [[VPN]] tunnel protocol built on fixed, opinionated cryptography (Curve25519, ChaCha20-Poly1305, BLAKE2) with a deliberately tiny codebase — a few thousand lines against the hundreds of thousands in IPsec/OpenVPN — small enough to audit. It runs over UDP, identifies peers by public key, and has shipped in the Linux kernel since 5.6.

**Context.** The small attack surface and kernel integration made it the default for self-hosted tunnels and the engine inside many commercial VPNs and mesh tools (e.g. Tailscale). Two operational sharp edges worth knowing: it is silent by design — a peer emits packets only when there's traffic (or a `PersistentKeepalive`), so "no recent handshake" isn't necessarily "down"; and a peer's endpoint hostname is resolved *once, at tunnel bring-up*, so pointing it at a name that only resolves *inside* the tunnel is a bootstrap deadlock. Roaming clients need no static address — the server learns a peer's current source address from its latest authenticated packet.

## See also

- [[VPN]]
- [[ZTNA]]
- [[Key Exchange]]

## Further reading

- [Wikipedia: WireGuard](https://en.wikipedia.org/wiki/WireGuard)
