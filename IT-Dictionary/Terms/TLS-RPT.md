---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["SMTP TLS Reporting"]
tags: ["security", "network", "email", "crypto"]
status: "developed"
---

# TLS-RPT

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** SMTP TLS Reporting

A reporting channel by which sending servers mail a domain owner daily summaries of their TLS negotiation successes and failures — the observability layer for [[MTA-STS]] and [[DANE]].

**Context.** Both MTA-STS and DANE fail in the direction that is hardest to notice: a sender that cannot satisfy the policy simply does not deliver, and the domain owner sees nothing at all. TLS-RPT closes that blind spot. Publish a `_smtp._tls.<domain>` TXT record with a reporting address, and participating senders return JSON reports counting successful sessions and, more usefully, failures by type — certificate mismatch, expired policy, STARTTLS stripped, DANE validation failure. It is what turns a policy you *hope* is working into one you can confirm, which is why deploying MTA-STS in `testing` mode without TLS-RPT wastes the point of having a testing mode at all.

## See also

- [[MTA-STS]]
- [[DANE]]
- [[STARTTLS]]
- [[TLS]]
- [[TXT Record]]
- [[Email Ecosystem]]

## Further reading

- [RFC 8460 — SMTP TLS Reporting](https://datatracker.ietf.org/doc/html/rfc8460)
