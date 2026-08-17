---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["open mail relay", "third-party relay"]
tags: ["security", "net", "email", "anti-pattern"]
status: "developed"
---

# Open Relay

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** open mail relay

An [[SMTP]] server that accepts mail from any sender for any recipient — that is, it will carry mail *from* strangers *to* strangers. Once the internet's default, now a serious misconfiguration.

**Context.** An open relay is free, anonymous, attributable-to-you infrastructure for whoever finds it, and they will: the internet is scanned continuously and an open relay is typically discovered within hours. The consequences are not subtle — your IP lands on blocklists within a day, and IP reputation is slow and painful to repair, so a few hours of misconfiguration can cost weeks of deliverability. The guard is one directive: in Postfix, `smtpd_relay_restrictions` (or the older `reject_unauth_destination` in `smtpd_recipient_restrictions`) says "accept mail for domains I am responsible for, refuse everything else". The rule that matters operationally is that **you verify this from off-network, never by reading your own config** — the common way to build one accidentally is a `mynetworks` entry that is broader than intended, or a hand-written restriction list that quietly dropped the guard. Note the distinction from an *open resolver* or an *open proxy*: same shape of mistake, different service.

## See also

- [[SMTP]]
- [[MTA]]
- [[Backscatter]]
- [[IP Reputation]]
- [[Attack Surface]]

## Often confused with

- [[Null Client]] — a null client sends only its own mail to one fixed smarthost; an open relay carries anyone's mail anywhere.
- Open resolver — the same class of "will serve strangers" misconfiguration, but in [[DNS]] and typically abused for amplification rather than spam.

## Further reading

- [Wikipedia: Open mail relay](https://en.wikipedia.org/wiki/Open_mail_relay)
