---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["DNS-01", "ACME DNS Challenge"]
tags: ["crypto", "pki", "modern"]
status: "developed"
---

# DNS-01 Challenge

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** DNS-01, ACME DNS Challenge

The [[ACME]] challenge type that proves control of a domain by publishing a given token as a `_acme-challenge` [[TXT Record|TXT]] record, rather than serving a file over HTTP.

**Context.** Two things make it the challenge of choice for infrastructure: it needs **no inbound port** (the CA reads DNS, doesn't connect to you), and it's the **only** way to get a [[Wildcard Certificate|wildcard]] — and it works for purely internal names whose hosts the CA can never reach. The cost is automation against your DNS provider's API to write and clean up the TXT record, which is exactly why a DNS host with a good API matters. Contrast HTTP-01 (serve a file on :80) and TLS-ALPN-01 (:443), which both require the CA to reach the host.

## See also

- [[ACME]]
- [[Wildcard Certificate]]
- [[TXT Record]]
- [[TLS]]
- [[CAA Record]]

## Often confused with

- [[ACME]] — ACME is the protocol; DNS-01 is one of its challenge methods (alongside HTTP-01, TLS-ALPN-01).

## Further reading

- [RFC 8555 — Automatic Certificate Management Environment](https://datatracker.ietf.org/doc/html/rfc8555)
