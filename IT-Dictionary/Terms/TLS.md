---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["SSL", "\"Transport Layer Security\""]
tags: ["crypto", "network"]
status: "developed"
---

# TLS

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** SSL, "Transport Layer Security"

**T**ransport **L**ayer **S**ecurity. Successor to SSL. Puts the 'S' in HTTPS. Uses asymmetric crypto for handshake, symmetric for bulk data.

**Context.** Operationally, TLS work is certificate work: issuance, chain deployment, renewal automation (ACME), and retiring old protocol versions. TLS 1.3 cut the handshake to one round trip and removed the foot-guns (static RSA, CBC suites, renegotiation); 1.0/1.1 are formally deprecated. Test servers with SSL Labs or `openssl s_client` — assumptions about what's actually negotiated are usually wrong.

## See also

- [[mTLS]]
- [[Forward Secrecy]]
- [[PKI]]
- [[Key Exchange]]

## Further reading

- [RFC 8446: TLS 1.3](https://datatracker.ietf.org/doc/html/rfc8446)
- [SSL Labs Server Test](https://www.ssllabs.com/ssltest/)
