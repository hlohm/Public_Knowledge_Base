---
type: "term"
branch: "Security"
domain: "Cryptography"
tags: ["crypto"]
status: "note"
---

# Salt

> **Domain:** [[03 - Cryptography|Cryptography]]

Random data added to a password before hashing to defeat rainbow tables. Must be unique per password.

**Context.** Salts kill the economics of precomputation: identical passwords hash differently, so each hash must be attacked individually and rainbow tables are useless. Salts are stored next to the hash and are *not* secret — that's the pepper's job. Any modern KDF handles salting for you; finding manual salt handling in code is a smell.

## See also

- [[Pepper]]
- [[KDF]]
- [[Hash Function]]
