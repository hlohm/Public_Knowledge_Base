---
type: "term"
branch: "Internet & Web"
aliases: ["Mail Delivery Agent", "Local Delivery Agent", "LDA"]
tags: ["web", "net", "email"]
status: "developed"
---

# MDA

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** Mail Delivery Agent, Local Delivery Agent

**M**ail **D**elivery **A**gent. The component at the *end* of the mail path: it takes a message the [[MTA]] has finished transporting and writes it into the recipient's mailbox, applying per-user filing rules on the way.

**Context.** This is where mail stops being a network problem and becomes a storage problem — mbox or Maildir on disk, quotas, folder rules, sieve filtering. Dovecot's LDA/LMTP, `procmail` and Postfix's own `local(8)` and `virtual(8)` agents are MDAs. The practical reason to care: a **forwarder deliberately has no MDA**. If a relay is configured so that its own domain appears in `mydestination`, Postfix hands the message to the local MDA and it lands in a mailbox on the relay instead of being forwarded — a message that has not bounced and has not arrived, which is the most confusing failure mode in mail.

## See also

- [[MTA]]
- [[MSA]]
- [[SMTP]]

## Often confused with

- [[MTA]] — transport between hosts versus final delivery into storage.
- IMAP / POP3 — the MDA *writes* the mailbox; those protocols are how a client later *reads* it.

## Further reading

- [Wikipedia: Mail delivery agent](https://en.wikipedia.org/wiki/Mail_delivery_agent)
