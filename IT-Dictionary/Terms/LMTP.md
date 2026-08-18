---
type: "term"
branch: "Internet & Web"
aliases: ["Local Mail Transfer Protocol"]
tags: ["web", "net", "email"]
status: "developed"
---

# LMTP

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** Local Mail Transfer Protocol

**L**ocal **M**ail **T**ransfer **P**rotocol — [[SMTP]] with the queue removed, used for the final hop from an [[MTA]] to the mailbox store.

**Context.** The difference is one promise. SMTP says: I have accepted responsibility, I will queue and retry until this is delivered or expires. A final delivery agent has nowhere to retry *to*, so it must answer immediately and per recipient — delivered, or not, with a reason. LMTP is that protocol: same syntax, `LHLO` instead of `EHLO`, and a separate reply for every recipient rather than one for the transaction. It is an internal hop, effectively never exposed to the internet, and you meet it wiring an MTA to a mailbox server such as Dovecot or Cyrus.

## See also

- [[SMTP]]
- [[MTA]]
- [[MDA]]
- [[Email Ecosystem]]

## Often confused with

- [[SMTP]] — SMTP queues and retries; LMTP must succeed or fail now, per recipient.

## Further reading

- [RFC 2033 — Local Mail Transfer Protocol](https://datatracker.ietf.org/doc/html/rfc2033)
