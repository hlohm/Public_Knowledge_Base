---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["DNS Security Extensions"]
tags: ["network", "crypto"]
status: "developed"
---

# DNSSEC

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** DNS Security Extensions

Extensions that add origin authentication and integrity to DNS by signing records, so a resolver can verify an answer genuinely came from the zone's owner and wasn't forged in transit.

**Context.** It doesn't encrypt (that's DoT/DoH) — it *signs*. Each zone signs its records ([[RRSIG]]) with a key ([[DNSKEY]]); the parent zone vouches for the child's key by publishing a hash of it ([[DS Record|DS]]); and the root's key is trusted out-of-band — a [[Chain of Trust]] from root to leaf. Deploying it is mostly a delegation dance: your DNS host signs the zone, you publish the DS at the registrar, and validating resolvers do the rest. It's also the hard prerequisite for [[DANE]] — no signed zone, no DANE.

## See also

- [[DS Record]]
- [[DNSKEY]]
- [[RRSIG]]
- [[NSEC]]
- [[CDS and CDNSKEY]]
- [[Chain of Trust]]
- [[DANE]]
- [[DNS Security]]

## Often confused with

- [[DNS Security]] — DNSSEC is signing/integrity specifically; 'DNS Security' broadly also covers encrypting queries (DoT/DoH) and blocking malicious domains.

## Further reading

- [RFC 4033 — DNS Security Introduction and Requirements](https://datatracker.ietf.org/doc/html/rfc4033)
- [Wikipedia: Domain Name System Security Extensions](https://en.wikipedia.org/wiki/Domain_Name_System_Security_Extensions)
