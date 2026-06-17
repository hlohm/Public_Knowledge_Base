---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["Certificate Signing Request"]
tags: ["security", "crypto", "pki"]
status: "developed"
---

# CSR

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** Certificate Signing Request

**C**ertificate **S**igning **R**equest. A signed message containing a public key plus identity details (subject, SANs), sent to a CA to request a certificate. The private key never leaves the requester.

**Context.** The CSR is where PKI hygiene is won or lost: generate the key pair on the machine (or HSM) that will use it, send only the CSR, and the private key never transits anywhere. Defined by PKCS #10; the openssl one-liner (`openssl req -new -key ...`) is muscle memory for anyone running their own CA.

## See also

- [[Certificate Authority]]
- [[X.509]]
- [[PKI]]
- [[ACME]]
- [[HSM]]

## Further reading

- [RFC 2986 — PKCS #10](https://datatracker.ietf.org/doc/html/rfc2986)
- [Wikipedia: Certificate signing request](https://en.wikipedia.org/wiki/Certificate_signing_request)
