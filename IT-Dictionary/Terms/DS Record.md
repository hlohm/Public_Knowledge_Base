---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Delegation Signer"]
tags: ["network", "crypto"]
status: "developed"
---

# DS Record

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Delegation Signer

A record in the *parent* zone holding a hash of the child zone's signing key — the link that lets the parent vouch for the child in the [[DNSSEC]] chain.

**Context.** This is the one record that must cross the registrar boundary: your DNS host signs the zone and publishes the [[DNSKEY]], but only the *parent* (the registry, via your registrar) can publish the DS that authenticates it. A mismatched or missing DS is the most common DNSSEC outage — and the most common cause of a botched migration, since changing DNS host means re-publishing a new DS. [[CDS and CDNSKEY]] automate this so the parent can pull updates instead of you hand-pasting.

## See also

- [[DNSKEY]]
- [[DNSSEC]]
- [[Chain of Trust]]
- [[CDS and CDNSKEY]]
- [[NS Record]]

## Often confused with

- [[DNSKEY]] — DNSKEY is the signing key, in the child zone; DS is a hash of it, in the parent zone.

## Further reading

- [RFC 4034 — Resource Records for DNSSEC](https://datatracker.ietf.org/doc/html/rfc4034)
