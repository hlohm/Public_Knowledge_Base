---
type: "term"
branch: "Security"
domain: "Cryptography"
de: "Digitale Signatur"
tags: ["crypto"]
status: "developed"
---

# Digital Signature

> **Domain:** [[03 - Cryptography|Cryptography]]
> **German:** Digitale Signatur

Hash of a message encrypted with the signer's private key; anyone with the public key can verify. Provides authenticity, integrity, and non-repudiation.

**Context.** The mechanism behind code signing, signed email, document signatures, JWTs, and certificate issuance itself — same primitive, different wrappers. Legally, eIDAS gives qualified electronic signatures the weight of handwritten ones in the EU. Note the modern detail: you sign the *hash*, and signature schemes (Ed25519, ECDSA, RSA-PSS) differ in their failure modes.

## See also

- [[Asymmetric Encryption]]
- [[PKI]]
- [[Non-repudiation]]
- [[HMAC]]

## Further reading

- [Wikipedia: Digital signature](https://en.wikipedia.org/wiki/Digital_signature)
