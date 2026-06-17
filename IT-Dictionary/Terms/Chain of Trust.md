---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["Trust Chain", "Certificate Chain"]
tags: ["crypto", "pki"]
status: "developed"
---

# Chain of Trust

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** Trust Chain, Certificate Chain

A sequence of cryptographic vouchers from a trusted root down to a leaf, where each link signs the next — so trusting one anchor transitively validates the whole path. Sequence of certs from end-entity → intermediate CA(s) → root CA.

**Context.** The same shape appears twice in this stack. In **PKI/TLS**: a root CA signs intermediates, which sign your server cert; clients ship the root and verify down ([[Certificate Authority]], [[TLS]]). In **[[DNSSEC]]**: the root zone's key is the anchor, each parent's [[DS Record|DS]] vouches for the child's [[DNSKEY]], and [[RRSIG]] signatures cover the leaf data. Either way the security reduces to one out-of-band trusted anchor plus an unbroken signature path — and a single broken link (expired signature, missing DS, untrusted intermediate) collapses everything below it.

Most real-world TLS failures are chain failures: a server sending its leaf without the intermediate works in browsers (which cache intermediates) and breaks in curl, Java, and printers. Always deploy the full chain (fullchain.pem), and remember validation also checks expiry, name match, and key usage at every link.

## See also

- [[Certificate Authority]]
- [[DNSSEC]]
- [[DS Record]]
- [[DNSKEY]]
- [[Digital Signature]]
- [[TLS]]
- [[PKI]]

## Further reading

- [Wikipedia: Chain of trust](https://en.wikipedia.org/wiki/Chain_of_trust)
