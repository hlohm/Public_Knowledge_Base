---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
tags: ["threat"]
status: "note"
---

# Replay Attack

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]

Capturing valid data and resending it to gain unauthorized effect.

**Context.** Capture something valid, send it again: an auth token, a signed API call, a contactless payment frame. Defenses are nonces, timestamps, and sequence numbers that make each message single-use — the reason Kerberos cares about clock skew and TLS injects freshness into its handshake. Pass-the-Hash is a replay attack wearing a Windows hat.

## See also

- [[MITM]]
- [[Nonce]]
- [[Pass-the-Hash]]
