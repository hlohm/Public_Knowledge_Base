---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["TLSA", "TLSA Record", "DNS-based Authentication of Named Entities"]
tags: ["network", "crypto", "pki", "email"]
status: "developed"
---

# DANE

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** TLSA, TLSA Record, DNS-based Authentication of Named Entities

Publishing a TLS certificate (or its CA, or public key) as a signed **TLSA** record in DNS, so a client can verify the server's cert against DNS instead of — or in addition to — the public CA system.

**Context.** DANE turns DNS into the trust anchor, which **requires a [[DNSSEC]]-signed zone** — without the signature a TLSA record is forgeable and worthless. Its headline use is SMTP (RFC 7672): it pins a mail server's cert so a sending MTA can't be silently downgraded to plaintext or a swapped cert, fixing the trust-on-first-use weakness of opportunistic STARTTLS. This is the concrete payoff that makes the DNS-host choice matter for an email project: managed DNSSEC makes DANE a non-event; no DNSSEC forecloses it and leaves only [[MTA-STS]].

## See also

- [[DNSSEC]]
- [[MTA-STS]]
- [[TLS]]
- [[SMTP]]
- [[Certificate Pinning]]
- [[Certificate Authority]]

## Often confused with

- [[MTA-STS]] — DANE pins via DNSSEC-signed DNS; MTA-STS achieves similar SMTP protection over HTTPS without needing DNSSEC.

## Further reading

- [RFC 6698 — The DANE TLSA Protocol](https://datatracker.ietf.org/doc/html/rfc6698)
- [RFC 7672 — SMTP Security via DANE](https://datatracker.ietf.org/doc/html/rfc7672)
