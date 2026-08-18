---
type: "term"
branch: "Security"
domain: "Identity and Access Management"
aliases: ["Simple Authentication and Security Layer"]
tags: ["security", "iam", "network", "email"]
status: "developed"
---

# SASL

> **Domain:** [[04 - Identity and Access Management|Identity and Access Management]]
> **Also known as:** Simple Authentication and Security Layer

**S**imple **A**uthentication and **S**ecurity **L**ayer — a framework that lets a protocol negotiate an authentication mechanism instead of hard-coding one.

**Context.** A protocol adds one command (`AUTH` in SMTP, `AUTHENTICATE` in IMAP), advertises the mechanisms it supports, and the client picks: `PLAIN` and `LOGIN` send credentials directly and are therefore only acceptable inside [[TLS]]; `CRAM-MD5` and `SCRAM` are challenge-response schemes that avoid transmitting the password; `XOAUTH2` carries an OAuth bearer token, which is how large providers moved away from passwords entirely. The design point is separation of concerns — SMTP, IMAP, LDAP and XMPP all reuse the same mechanisms rather than each inventing authentication. In mail specifically, SASL is what makes the [[MSA]] on port 587 a different trust domain from the anonymous [[MTA]] on port 25.

## See also

- [[MSA]]
- [[SMTP]]
- [[IMAP]]
- [[TLS]]
- [[Authentication]]
- [[MFA]]

## Further reading

- [RFC 4422 — Simple Authentication and Security Layer](https://datatracker.ietf.org/doc/html/rfc4422)
