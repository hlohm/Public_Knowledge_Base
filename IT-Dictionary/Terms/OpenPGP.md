---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["PGP", "GnuPG", "GPG"]
tags: ["security", "crypto", "email"]
status: "developed"
---

# OpenPGP

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** PGP, GnuPG, GPG

A standard for content-level encryption and signing where users manage their own keys and decide directly whom to trust, without a central certificate authority.

**Context.** Trust is established by verifying keys yourself — in person, via fingerprints, or historically through the web of trust in which signatures on other people's keys transitively vouch for them. That removes the CA as a single point of failure and replaces it with a usability problem that has defeated general adoption for three decades: key discovery, key rotation, safe backup, and the fact that a single participant without a key drops the conversation back to plaintext. It remains entrenched among technical users and for signing software releases, where the key-management burden falls on people equipped to carry it. As with [[S-MIME|S/MIME]], envelope metadata is never hidden.

## See also

- [[S-MIME]]
- [[MIME]]
- [[Digital Signature]]
- [[Asymmetric Encryption]]
- [[Email Ecosystem]]

## Often confused with

- [[S-MIME|S/MIME]] — OpenPGP is decentralised key management; S/MIME relies on X.509 certificate authorities.

## Further reading

- [RFC 9580 — OpenPGP](https://datatracker.ietf.org/doc/html/rfc9580)
