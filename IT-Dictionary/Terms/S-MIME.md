---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["S/MIME", "Secure/Multipurpose Internet Mail Extensions"]
tags: ["security", "crypto", "pki", "email"]
status: "developed"
---

# S/MIME

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** S/MIME, Secure/Multipurpose Internet Mail Extensions

A standard for signing and encrypting mail *content* using X.509 certificates, so that intermediaries carrying the message cannot read or alter it.

**Context.** It operates on a different axis from [[TLS]], [[MTA-STS]] and [[DANE]], which protect the hop between two servers while leaving each server able to read the message. S/MIME protects the message itself, end to end. Trust comes from the certificate hierarchy rather than from personal key exchange, which is why it is common in enterprise and government where a CA and a directory already exist, and rare elsewhere. The costs are real: server-side search and filtering cannot see encrypted content, key loss means permanent loss of the archive, and metadata — sender, recipients, timing, usually the subject line — stays visible regardless.

## See also

- [[OpenPGP]]
- [[MIME]]
- [[TLS]]
- [[Certificate Authority]]
- [[Digital Signature]]
- [[Email Ecosystem]]

## Often confused with

- [[OpenPGP]] — same goal, different trust model — S/MIME uses X.509 and a CA; OpenPGP uses self-managed keys.

## Further reading

- [RFC 8551 — S/MIME 4.0 Message Specification](https://datatracker.ietf.org/doc/html/rfc8551)
