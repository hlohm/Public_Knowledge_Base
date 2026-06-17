---
type: "term"
branch: "Security"
domain: "Cryptography"
tags: ["crypto"]
status: "note"
---

# Pepper

> **Domain:** [[03 - Cryptography|Cryptography]]

A site-wide secret added alongside the salt when hashing passwords, stored separately from the database (e.g. in an HSM, KMS, or application config). Defense-in-depth for password storage.

**Context.** The scenario it defends: SQL injection dumps the user table, but the attacker has hashes peppered with a secret that lives outside the database — offline cracking goes nowhere. Costs almost nothing to add; the operational catch is that losing the pepper invalidates every stored hash, so treat it like a real key.

## See also

- [[Salt]]
- [[HSM]]
- [[KDF]]
