---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Brand Indicators for Message Identification"]
tags: ["security", "network", "email"]
status: "developed"
---

# BIMI

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Brand Indicators for Message Identification

A specification for publishing a brand logo in DNS so participating mail clients display it beside authenticated messages — available only to domains already enforcing [[DMARC]].

**Context.** The technical content is slight: a TXT record at `default._bimi.<domain>` pointing at an SVG Tiny PS logo, plus in most implementations a Verified Mark Certificate — a paid attestation that the trademark is yours. Its real function is incentive design. DMARC enforcement is unglamorous work with no visible payoff, so BIMI attaches a visible payoff that marketing departments will fund, and the security improvement arrives as a side effect. Read it that way rather than as a security control: a logo is a trust cue for humans, and a domain an attacker legitimately owns can display one too.

## See also

- [[DMARC]]
- [[DKIM]]
- [[SPF]]
- [[Phishing]]
- [[Email Ecosystem]]

## Further reading

- [BIMI Group](https://bimigroup.org/)
