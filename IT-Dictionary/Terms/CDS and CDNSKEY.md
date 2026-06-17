---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["CDS", "CDNSKEY"]
tags: ["network", "crypto"]
status: "note"
---

# CDS and CDNSKEY

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** CDS, CDNSKEY

Child-published records that signal the desired [[DS Record|DS]] (CDS) or key (CDNSKEY) to the parent, so DS updates can be automated instead of hand-carried to the registrar.

**Context.** They close the one manual gap in DNSSEC: normally the child can't touch the parent's DS, so a key roll means logging into the registrar to paste a new DS. With CDS/CDNSKEY the child signs its intent and a registry/registrar that supports RFC 8078 polls and applies it — turning key rollover and even initial trust into a hands-off process. Support is uneven across registries, so it's a 'nice if available' rather than guaranteed.

## See also

- [[DS Record]]
- [[DNSKEY]]
- [[DNSSEC]]

## Further reading

- [RFC 7344 — Automating DNSSEC Delegation Trust Maintenance](https://datatracker.ietf.org/doc/html/rfc7344)
