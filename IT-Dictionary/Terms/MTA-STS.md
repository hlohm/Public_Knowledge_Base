---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["SMTP MTA Strict Transport Security"]
tags: ["network", "email"]
status: "developed"
---

# MTA-STS

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** SMTP MTA Strict Transport Security

A policy that lets a domain require inbound SMTP be delivered over authenticated TLS, published over HTTPS and discovered via a DNS TXT record — the non-DNSSEC alternative to [[DANE]].

**Context.** It exists for the large population that wants downgrade protection for mail but hasn't deployed DNSSEC: a sender fetches `https://mta-sts.<domain>/.well-known/mta-sts.txt`, caches the policy, and then refuses to deliver to a server that fails TLS or presents a mismatched cert. The trade vs DANE is the trust model — MTA-STS leans on the web PKI and trust-on-first-use of the policy, where DANE leans on DNSSEC. Pair it with TLS-RPT to get reports of delivery failures.

## See also

- [[DANE]]
- [[SMTP]]
- [[TLS]]
- [[TXT Record]]

## Often confused with

- [[DANE]] — MTA-STS is HTTPS/web-PKI based and needs no DNSSEC; DANE is DNSSEC-based pinning.

## Further reading

- [RFC 8461 — SMTP MTA Strict Transport Security](https://datatracker.ietf.org/doc/html/rfc8461)
