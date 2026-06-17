---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["NSEC3", "Authenticated Denial of Existence"]
tags: ["network", "crypto"]
status: "developed"
---

# NSEC

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** NSEC3, Authenticated Denial of Existence

The DNSSEC mechanism for *signing a negative answer* — proving that a name (or record type) genuinely does not exist, since you can't sign a record that isn't there.

**Context.** A plain [[NXDOMAIN]] is unsigned and could be forged, so DNSSEC needs signed proof of non-existence: NSEC records point to the next existing name, letting a resolver prove nothing lives in the gap. The catch is that NSEC lets anyone *walk the zone* by following the chain (zone enumeration); **NSEC3** hashes the names to frustrate that, at extra cost. This is also why a split-horizon internal zone is served as local data that short-circuits before validation — the resolver never has to reconcile a private name against the parent's signed denial.

## See also

- [[DNSSEC]]
- [[RRSIG]]
- [[NXDOMAIN]]
- [[Split-horizon DNS]]

## Further reading

- [RFC 5155 — DNSSEC Hashed Authenticated Denial of Existence](https://datatracker.ietf.org/doc/html/rfc5155)
