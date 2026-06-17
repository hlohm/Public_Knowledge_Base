---
type: "term"
branch: "Networking"
aliases: ["Reverse DNS", "Pointer Record", "rDNS"]
tags: [net]
status: "developed"
---

# PTR Record

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Reverse DNS, Pointer Record, rDNS

The reverse mapping: from an IP address back to a name, served out of the special `in-addr.arpa` (IPv4) / `ip6.arpa` (IPv6) zones.

**Context.** Forward and reverse are independent — a PTR isn't created automatically when you add an [[A Record]], and the reverse zone is usually controlled by whoever owns the IP block (your ISP/host), not you. It matters most for **mail**: receiving servers reject or distrust senders whose IP has no PTR or whose PTR doesn't forward-confirm (FCrDNS), so a sending mail server needs a matching reverse record. Tools that 'add PTR' for a local host just publish the reverse alongside the forward in your own resolver.

## See also

- [[A Record]]
- [[DNS Zone]]
- [[SMTP]]
- [[MX Record]]

## Further reading

- [Wikipedia: Reverse DNS lookup](https://en.wikipedia.org/wiki/Reverse_DNS_lookup)
