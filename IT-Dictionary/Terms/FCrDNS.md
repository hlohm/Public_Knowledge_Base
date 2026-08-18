---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Forward-Confirmed reverse DNS", "Full-circle DNS", "iprev"]
tags: ["security", "network", "email"]
status: "developed"
---

# FCrDNS

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Forward-Confirmed reverse DNS, Full-circle DNS, iprev

**F**orward-**C**onfirmed **r**everse **DNS** — the check that an IP's [[PTR Record|reverse record]] resolves to a name whose forward lookup points back to that same IP. A round trip that must close.

**Context.** A PTR alone proves little, because the reverse zone is controlled by whoever owns the IP block and can say anything. FCrDNS closes the loop: `198.51.100.10` → PTR → `mail.example.com` → A → `198.51.100.10`. Passing requires control of *both* zones, which is exactly the bar a casual abuser cannot clear — a botnet on residential addresses has generic ISP reverse names that do not forward-confirm, if it has reverse names at all.

This is why it is a standing requirement for sending mail: receiving [[MTA|MTAs]] treat a missing or non-confirming reverse as strong negative evidence at the connection stage, often as an outright rejection (`reject_unknown_reverse_client_hostname` in Postfix). It is usually paired with a HELO check, since a well-formed sender's greeting, its PTR and its forward record should all agree. Two practical consequences: on a cloud or colo host you must ask the provider to set the PTR, because you do not own the reverse zone; and internal hosts relaying to an internal mail server will fail these checks by default, since RFC 1918 addresses have no public reverse — the fix is to make the client well-formed (a resolvable name and a matching internal PTR) rather than to exempt it from the check.

## See also

- [[PTR Record]]
- [[A Record]]
- [[SMTP]]
- [[MTA]]
- [[IP Reputation]]
- [[DNSBL]]
- [[Deliverability]]
- [[Email Ecosystem]]

## Often confused with

- [[PTR Record]] — the PTR is the record; FCrDNS is the two-way check that the record is corroborated.

## Further reading

- [Wikipedia: Forward-confirmed reverse DNS](https://en.wikipedia.org/wiki/Forward-confirmed_reverse_DNS)
- [RFC 8601 — Authentication-Results, the `iprev` method](https://datatracker.ietf.org/doc/html/rfc8601)
