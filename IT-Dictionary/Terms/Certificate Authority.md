---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["CA"]
de: "Zertifizierungsstelle"
tags: ["crypto", "trust"]
status: "developed"
---

# Certificate Authority

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** CA
> **German:** Zertifizierungsstelle

Trusted issuer of digital certificates. Root CAs anchor the trust chain.

**Context.** Trust in a CA is binary and systemic: a single mis-issuance can undermine every relying party, which is why public CAs live under the CA/Browser Forum rules and Certificate Transparency logs. For an internal PKI, the root CA should be offline/air-gapped, with issuance done by intermediates — the root signs rarely and is otherwise powered off.

## See also

- [[PKI]]
- [[Chain of Trust]]
- [[X.509]]
- [[CRL and OCSP]]

## Further reading

- [Wikipedia: Certificate authority](https://en.wikipedia.org/wiki/Certificate_authority)
