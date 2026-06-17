---
type: "term"
branch: "Networking"
aliases: ["Text Record"]
tags: [net, email]
status: "developed"
---

# TXT Record

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Text Record

A DNS record holding arbitrary text, long repurposed as the carrier for machine-readable policy and proof-of-control strings.

**Context.** It's the swiss-army record: [[SPF]], DKIM keys, [[DMARC]] policy, [[MTA-STS]] versioning, and ACME's [[DNS-01 Challenge|DNS-01]] `_acme-challenge` tokens all live in TXT records — which is why one record type quietly underpins both email authentication and certificate issuance. Practical gotchas: the 255-character per-string limit (long DKIM keys are split into multiple quoted chunks that concatenate), and putting policy on the right name (e.g. `_dmarc.example.com`, not the apex).

## See also

- [[SPF]]
- [[DMARC]]
- [[DNS-01 Challenge]]
- [[DNS]]

## Further reading

- [RFC 1035 — Domain Implementation and Specification](https://datatracker.ietf.org/doc/html/rfc1035)
