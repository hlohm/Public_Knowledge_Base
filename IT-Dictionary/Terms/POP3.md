---
type: "term"
branch: "Internet & Web"
aliases: ["Post Office Protocol"]
tags: ["web", "net", "email"]
status: "developed"
---

# POP3

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** Post Office Protocol

**P**ost **O**ffice **P**rotocol version 3 — a minimal protocol for downloading mail from a server to one machine, usually deleting the server copy as it goes.

**Context.** Port 995 with implicit TLS (110 in the clear historically). POP3 embodies a single-device world: the mailbox is a spool to be drained, and once drained the client owns the only copy. That was correct when storage was expensive and connections metered, and it is still useful for pulling mail into a local archive or feeding a one-way gateway. The trap is the leave-messages-on-server option, which people enable when they get a second device: it reproduces exactly the multi-device state problems [[IMAP]] was designed to solve, without solving them.

## See also

- [[IMAP]]
- [[JMAP]]
- [[MDA]]
- [[Email Ecosystem]]

## Often confused with

- [[IMAP]] — POP3 is download-and-forget; IMAP keeps the server authoritative.

## Further reading

- [RFC 1939 — POP3](https://datatracker.ietf.org/doc/html/rfc1939)
