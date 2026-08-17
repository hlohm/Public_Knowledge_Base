---
type: "term"
branch: "Internet & Web"
aliases: ["Mail Submission Agent", "submission", "SMTP submission"]
tags: ["web", "net", "email"]
status: "developed"
---

# MSA

> **Branch:** [[05 - Internet & Web|Internet & Web]]
> **Also known as:** Mail Submission Agent

**M**ail **S**ubmission **A**gent. The authenticated entry point where a *mail client* hands a new message to the infrastructure — conventionally port **587** with STARTTLS, or 465 with implicit TLS. Defined separately from relay in RFC 6409 precisely so the two can have different policies.

**Context.** The split exists because submission and relay have opposite trust models. Port 25 accepts mail from strangers for recipients you are responsible for, and must never relay for anyone else ([[Open Relay]]). Port 587 accepts mail from *authenticated users* for any recipient in the world, and must never accept anonymous connections. That is why hardened configurations set `smtpd_relay_restrictions = permit_sasl_authenticated, reject` on 587 while port 25 uses `reject_unauth_destination`. An MSA is also allowed to *fix* messages — adding a `Message-ID` or `Date` header, completing bare addresses — which a relay must not do. Most ISPs block outbound 25 from consumer lines to force mail through an authenticated MSA, which is why testing port 25 from a home connection so often fails for reasons that have nothing to do with the server.

## See also

- [[SMTP]]
- [[MTA]]
- [[TLS]]
- [[Authentication]]

## Often confused with

- [[MTA]] — 587 authenticated submission from your own users versus 25 anonymous relay from the internet. Same daemon, opposite rules.

## Further reading

- [RFC 6409 — Message Submission for Mail](https://datatracker.ietf.org/doc/html/rfc6409)
- [Wikipedia: Mail submission agent](https://en.wikipedia.org/wiki/Mail_submission_agent)
