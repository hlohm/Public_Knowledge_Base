---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Certification Authority Authorization"]
tags: ["network", "crypto", "pki"]
status: "developed"
---

# CAA Record

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Certification Authority Authorization

A DNS record listing which [[Certificate Authority|CAs]] are permitted to issue certificates for a domain. Compliant CAs must check it and refuse if they're not authorised.

**Context.** It's a cheap, declarative guardrail against mis-issuance: publish `0 issue "letsencrypt.org"` and a different CA is supposed to decline even if someone tricks it into a request. You can scope to specific validation methods or account URIs, and `iodef` names a contact for violation reports. It binds CAs at issuance time, not browsers at connection time — so it complements, not replaces, [[Certificate Pinning]]/[[DANE]].

## See also

- [[Certificate Authority]]
- [[ACME]]
- [[TXT Record]]
- [[DANE]]

## Further reading

- [RFC 8659 — DNS Certification Authority Authorization](https://datatracker.ietf.org/doc/html/rfc8659)
