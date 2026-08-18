---
type: "term"
branch: "Internet & Web"
aliases: ["Internet Message Access Protocol"]
tags: ["web", "net", "email"]
status: "developed"
---

# IMAP

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** Internet Message Access Protocol

**I**nternet **M**essage **A**ccess **P**rotocol — the protocol for reading a mailbox that lives on a server, where the server holds the authoritative state and clients are caches of it.

**Context.** Port 993 with implicit [[TLS]] is the modern default (143 with STARTTLS is the legacy arrangement). Because folders, read flags and drafts live server-side, every device sees the same mailbox — which is why IMAP displaced [[POP3]] the moment people acquired a second device. It offers server-side search, IDLE for near-push delivery, and shared or virtual folders. The cost is chattiness: a protocol designed for always-on connections behaves poorly over high-latency mobile links, and its push story was bolted on rather than designed in. Those two complaints are precisely what [[JMAP]] was created to answer.

## See also

- [[POP3]]
- [[JMAP]]
- [[MDA]]
- [[TLS]]
- [[Maildir]]
- [[Email Ecosystem]]

## Often confused with

- [[POP3]] — IMAP synchronises a server-side mailbox; POP3 downloads and typically deletes.

## Further reading

- [RFC 9051 — IMAP4rev2](https://datatracker.ietf.org/doc/html/rfc9051)
- [Wikipedia: IMAP](https://en.wikipedia.org/wiki/Internet_Message_Access_Protocol)
