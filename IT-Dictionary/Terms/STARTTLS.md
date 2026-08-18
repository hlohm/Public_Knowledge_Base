---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: []
tags: ["security", "crypto", "network", "email"]
status: "developed"
---

# STARTTLS

> **Domain:** [[03 - Cryptography|Cryptography]]

A command that upgrades an already-open plaintext connection to [[TLS]], used by SMTP, IMAP and POP3 to add encryption without moving to a separate port.

**Context.** The session begins in the clear, the client sees the server advertise STARTTLS, asks for it, and the two negotiate TLS in place. That design let encryption be deployed across the existing mail internet without breaking anything — and it carries the flaw that follows from it: an active attacker can simply strip the advertisement, and between servers on port 25 the default response to a failed upgrade is to send in the clear rather than not at all. Certificates are frequently not validated on that hop either, so an opportunistic upgrade proves rather little. Two answers exist: for client-facing ports, implicit TLS (465, 993, 995) with no plaintext phase at all, recommended by RFC 8314; and between servers, [[MTA-STS]] or [[DANE]] to publish that TLS is not optional.

## See also

- [[TLS]]
- [[MTA-STS]]
- [[DANE]]
- [[SMTP]]
- [[IMAP]]
- [[Email Ecosystem]]

## Often confused with

- [[TLS]] — STARTTLS is a way of *starting* TLS on an existing connection, not a protocol of its own.

## Further reading

- [RFC 3207 — SMTP Service Extension for Secure SMTP over TLS](https://datatracker.ietf.org/doc/html/rfc3207)
- [RFC 8314 — Cleartext Considered Obsolete](https://datatracker.ietf.org/doc/html/rfc8314)
