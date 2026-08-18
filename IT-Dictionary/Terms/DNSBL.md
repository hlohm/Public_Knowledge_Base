---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["RBL", "DNS Blocklist", "Realtime Blackhole List"]
tags: ["security", "network", "email"]
status: "developed"
---

# DNSBL

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** RBL, DNS Blocklist, Realtime Blackhole List

**DNS**-based **B**lock**L**ist — a blocklist distributed as a DNS zone, where the existence of a record for a reversed IP address means that address has been observed sending abuse.

**Context.** The query is an ordinary A lookup: reverse the octets, append the list's domain, and a `127.0.0.x` answer means listed, with the final octet encoding the reason. That makes it fast and cacheable, which is why it runs at the connection stage before any message body is transferred. Lists come in several shapes — IP blocklists, domain and URL lists, and allow-lists — and good practice is to weight several as scoring inputs rather than hard-blocking on any single one, since false positives are inevitable and delisting takes time. Being listed yourself is usually self-service to fix once the cause is dealt with; the cause is often an outbound compromise or a [[Backscatter]] problem.

## See also

- [[IP Reputation]]
- [[Greylisting]]
- [[Backscatter]]
- [[DNS]]
- [[Deliverability]]
- [[Email Ecosystem]]

## Further reading

- [Wikipedia: DNSBL](https://en.wikipedia.org/wiki/Domain_Name_System_blocklist)
