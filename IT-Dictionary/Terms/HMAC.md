---
type: "term"
branch: "Security"
domain: "Cryptography"
tags: ["crypto"]
status: "developed"
---

# HMAC

> **Domain:** [[03 - Cryptography|Cryptography]]

**H**ash-based **M**essage **A**uthentication **C**ode. Hash + secret key, proving both integrity *and* authenticity. Not just a hash.

**Context.** The answer whenever you need "prove this message is unmodified *and* from someone holding the key": API request signing, webhook verification, session tokens, TOTP internals. Use the standard construction — naive hash(key+message) is broken by length-extension attacks on SHA-2.

## See also

- [[Hash Function]]
- [[Digital Signature]]

## Further reading

- [RFC 2104: HMAC](https://datatracker.ietf.org/doc/html/rfc2104)
