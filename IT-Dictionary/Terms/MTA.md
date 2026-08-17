---
type: "term"
branch: "Internet & Web"
aliases: ["Mail Transfer Agent", "Message Transfer Agent", "mail server"]
tags: ["web", "net", "email", "fundamental"]
status: "developed"
---

# MTA

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** Mail Transfer Agent

**M**ail **T**ransfer **A**gent. The server program that accepts email over [[SMTP]] and moves it onward — to another MTA, or to a local delivery agent. Postfix, Exim, Sendmail and Mox are MTAs.

**Context.** The defining property is that an MTA **spools**: it takes custody of a message, writes it to a queue, and keeps retrying until it is delivered or expires (five days is a common ceiling). That is why a brief mail outage is usually survivable — every sending MTA on the internet is patiently retrying on your behalf — and why a "backup MX" buys less than intuition suggests. An MTA is also where all of email authentication is enforced or produced: it checks [[SPF]], applies [[DKIM]] signatures, honours [[DMARC]] policy and negotiates [[TLS]]. Confusingly, one Postfix install can act as MTA, [[MSA]] and [[MDA]] at once depending on which port and which service you are talking to.

## See also

- [[SMTP]]
- [[MSA]]
- [[MDA]]
- [[Envelope Sender]]
- [[Queue]]
- [[Open Relay]]

## Often confused with

- [[MDA]] — the MTA moves mail *between hosts*; the MDA puts it in a *mailbox*. The last MTA in the chain hands off to an MDA.
- [[MSA]] — the MSA is the authenticated front door for *your own users*; the MTA is the unauthenticated door for *the internet*.

## Further reading

- [Wikipedia: Message transfer agent](https://en.wikipedia.org/wiki/Message_transfer_agent)
- [RFC 5321 — SMTP](https://datatracker.ietf.org/doc/html/rfc5321)
