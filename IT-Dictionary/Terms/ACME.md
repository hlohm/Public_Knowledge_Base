---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["Automatic Certificate Management Environment"]
tags: ["security", "crypto", "pki", "modern"]
status: "developed"
---

# ACME

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** Automatic Certificate Management Environment

**A**utomatic **C**ertificate **M**anagement **E**nvironment. The protocol behind Let's Encrypt: an agent proves control of a domain via a challenge (HTTP-01, DNS-01), then obtains and renews certificates automatically.

**Context.** ACME turned certificates from an annual manual chore into infrastructure that renews itself — which is what made 90-day (and now shorter) lifetimes viable and pushed the web to near-universal HTTPS. It also works against private CAs (smallstep, Vault), so the same automation applies to an internal PKI.

## See also

- [[Certificate Authority]]
- [[CSR]]
- [[TLS]]
- [[PKI]]
- [[X.509]]

## Further reading

- [RFC 8555 — ACME](https://datatracker.ietf.org/doc/html/rfc8555)
- [Wikipedia: Automatic Certificate Management Environment](https://en.wikipedia.org/wiki/Automatic_Certificate_Management_Environment)
