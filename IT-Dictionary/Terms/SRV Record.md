---
type: "term"
branch: "Networking"
aliases: ["Service Record"]
tags: [net]
status: "note"
---

# SRV Record

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Service Record

A record advertising the host and port for a named service under a domain, as `_service._proto.name`, with priority and weight for selection.

**Context.** It decouples a service from a fixed hostname/port: `_minecraft._tcp.example.com` or `_sip._udp` lets clients discover where the service actually runs, so users type only the bare domain. Priority works like [[MX Record|MX]] preference; weight load-balances within a priority tier. SIP, XMPP, Minecraft, and AD all lean on SRV; HTTP largely doesn't (browsers ignore it, though the newer HTTPS/SVCB records fill that gap).

## See also

- [[MX Record]]
- [[A Record]]
- [[DNS]]
