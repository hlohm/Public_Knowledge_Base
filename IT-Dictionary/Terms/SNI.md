---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["Server Name Indication"]
tags: ["crypto", "network"]
status: "developed"
---

# SNI

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** Server Name Indication

The TLS extension where the client states the hostname it wants **at the start of the handshake**, so a server hosting many sites on one IP can present the right certificate.

**Context.** Before SNI, one IP could serve one cert; SNI is what makes name-based virtual hosting over HTTPS possible. The operational gotcha: SNI is the key a reverse proxy uses to pick the certificate, so anything that disturbs how the hostname is presented — a misconfigured proxy directive, an unexpected upgrade path — can cause the server to fall back to the wrong (or a default) cert and throw an `internal_error`/handshake failure that *looks* like a cert problem but is really a routing problem. Classic SNI is sent in cleartext; ECH (Encrypted Client Hello) is the evolving fix.

## See also

- [[TLS]]
- [[Reverse Proxy]]
- [[HTTPS]]
- [[Certificate Authority]]

## Further reading

- [RFC 6066 — TLS Extensions](https://datatracker.ietf.org/doc/html/rfc6066)
