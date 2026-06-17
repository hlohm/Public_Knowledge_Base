---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Resource Record Signature"]
tags: ["network", "crypto"]
status: "note"
---

# RRSIG

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Resource Record Signature

The signature record covering a set of DNS records of one type/name — the actual cryptographic proof a validating resolver checks against the zone's [[DNSKEY]].

**Context.** Every signed record set has an accompanying RRSIG, and crucially RRSIGs **expire** (they carry inception/expiration timestamps), so a zone must be *re-signed* on a schedule — a forgotten re-signing is a way to take a zone down even with valid keys. The validator checks the RRSIG with the DNSKEY, the DNSKEY against the parent's [[DS Record|DS]], and so up the [[Chain of Trust]].

## See also

- [[DNSKEY]]
- [[DS Record]]
- [[DNSSEC]]
- [[NSEC]]
