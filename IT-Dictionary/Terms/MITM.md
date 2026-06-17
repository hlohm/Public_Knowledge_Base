---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["AitM", "\"Man-in-the-Middle\"", "\"Adversary-in-the-Middle\""]
tags: ["threat"]
status: "note"
---

# MITM

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** AitM, "Man-in-the-Middle", "Adversary-in-the-Middle"

**M**an-**I**n-**T**he-**M**iddle (also **AitM** = Adversary-in-the-Middle). Attacker sits between two parties, observing or altering traffic.

**Context.** The MITM-vs-AitM framing tracks where the action moved: classic network MITM is largely closed by ubiquitous TLS and HSTS, so attackers shifted to adversary-in-the-middle phishing proxies (Evilginx) that relay the real login and steal the *session cookie* after MFA. That pivot is exactly why FIDO2's origin binding matters — it's the one factor an AitM proxy can't forward.

## See also

- [[Replay Attack]]
- [[TLS]]
- [[FIDO2 and WebAuthn]]
