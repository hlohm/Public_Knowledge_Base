---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Sender Reputation"]
tags: ["network"]
status: "developed"
---

# IP Reputation

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Sender Reputation

The score mail providers and security services attach to an IP address based on its history — spam complaints, malware, open relays, or simply sitting in a range full of bad neighbours. A poor score gets traffic rejected or silently junked regardless of how correct the sender's [[SPF]]/[[DKIM]]/[[DMARC]] setup is.

**Context.** The reason self-hosted mail is hard even when every DNS record is perfect: authentication proves *who* you are, reputation decides whether anyone *cares*. Cloud and hosting ranges start pre-tarnished from years of abuse, so the first step before building outbound mail on any IP is checking it against DNSBLs and reputation portals — inheriting a burned address can sink a project before the first message. Reputation attaches to the IP and the domain separately, is warmed up slowly (low volume, consistent sending), and is squandered instantly. It's also why providers block outbound port 25 by default ([[Egress Filtering]] as a platform default): one spamming customer damages the whole range's standing.

## See also

- [[SPF]]
- [[DKIM]]
- [[DMARC]]
- [[SMTP]]
- [[Egress Filtering]]
- [[Envelope Sender]]

## Further reading

- [Wikipedia: DNSBL](https://en.wikipedia.org/wiki/Domain_Name_System_blocklist)
