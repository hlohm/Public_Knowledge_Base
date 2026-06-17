---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["KSK", "ZSK", "Key Signing Key", "Zone Signing Key"]
tags: ["network", "crypto"]
status: "developed"
---

# DNSKEY

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** KSK, ZSK, Key Signing Key, Zone Signing Key

The record publishing a zone's public signing key(s). Conventionally split into a **KSK** (key-signing key, which signs the keyset and is what the [[DS Record|DS]] hashes) and a **ZSK** (zone-signing key, which signs the actual data).

**Context.** The KSK/ZSK split is an operational convenience: rotate the ZSK freely without touching the parent, and rotate the rarely-changed KSK only when you're ready to update the DS upstream. Managed providers (deSEC and the like) hide all of this — they pick algorithms, sign, and roll keys for you, leaving you only the DS to publish once. Self-hosting signing means owning rollover, which is where most DNSSEC self-inflicted outages come from.

## See also

- [[DS Record]]
- [[RRSIG]]
- [[DNSSEC]]
- [[Chain of Trust]]

## Further reading

- [RFC 4034 — Resource Records for DNSSEC](https://datatracker.ietf.org/doc/html/rfc4034)
