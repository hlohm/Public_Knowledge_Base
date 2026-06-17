---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["X.509 Certificate"]
tags: ["crypto"]
status: "developed"
---

# X.509

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** X.509 Certificate

Standard certificate format binding a public key to an identity, signed by a CA. Used everywhere from TLS to S/MIME to code signing.

**Context.** The format's power is in its extensions: Subject Alternative Names (the field that actually matters for hostname matching — Common Name is ignored by modern clients), Key Usage, Extended Key Usage, and Basic Constraints (what makes a CA cert a CA cert). Reading certs with `openssl x509 -text` until the fields feel familiar is time well spent for anyone running a PKI.

## See also

- [[PKI]]
- [[Certificate Authority]]
- [[Chain of Trust]]

## Further reading

- [RFC 5280: X.509 PKI Certificate Profile](https://datatracker.ietf.org/doc/html/rfc5280)
