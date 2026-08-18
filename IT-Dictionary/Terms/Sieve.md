---
type: "term"
branch: "Internet & Web"
aliases: ["Sieve filtering language"]
tags: ["web", "net", "email"]
status: "developed"
---

# Sieve

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** Sieve filtering language

A small, deliberately non-Turing-complete language for filtering mail at delivery time — sorting into folders, forwarding, discarding, or sending a vacation reply.

**Context.** Sieve runs on the server as part of the [[MDA]], so rules apply whether or not any client is connected — the decisive advantage over client-side rules, which only fire when that particular application happens to be open. The language has no loops and no way to run external programs, which is a security property rather than a limitation: a filter language that executes in someone else's mailbox must not be able to do arbitrary work. Clients edit scripts remotely over ManageSieve (port 4190). Extensions cover regular expressions, notifications and duplicate detection, each negotiated explicitly so a server can refuse what it does not implement.

## See also

- [[MDA]]
- [[IMAP]]
- [[Mailing List]]
- [[Email Ecosystem]]

## Further reading

- [RFC 5228 — Sieve: An Email Filtering Language](https://datatracker.ietf.org/doc/html/rfc5228)
