---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Domain-based Message Authentication, Reporting and Conformance"]
tags: ["security", "network", "email"]
status: "developed"
---

# DMARC

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Domain-based Message Authentication, Reporting and Conformance

**D**omain-based **M**essage **A**uthentication, **R**eporting and **C**onformance. A DNS policy that ties SPF and DKIM to the visible From: header (*alignment*) and tells receivers what to do on failure: `none`, `quarantine`, or `reject`.

**Context.** DMARC is the piece that actually stops direct domain spoofing — SPF and DKIM alone authenticate things the user never sees. The standard rollout path is `p=none` with aggregate (RUA) reports to discover all legitimate senders, then tightening to `quarantine` and finally `reject`. Major mailbox providers now require DMARC for bulk senders, so it has shifted from best practice to table stakes.

## See also

- [[SPF]]
- [[DKIM]]
- [[Phishing]]
- [[BEC]]
- [[DNS]]

## Further reading

- [RFC 7489 — DMARC](https://datatracker.ietf.org/doc/html/rfc7489)
- [Wikipedia: DMARC](https://en.wikipedia.org/wiki/DMARC)
