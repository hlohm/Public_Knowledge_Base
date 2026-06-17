---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["NT LAN Manager", "NTLMv2", "Net-NTLM"]
tags: ["security", "iam", "windows", "deprecated"]
status: "developed"
---

# NTLM

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** NT LAN Manager, NTLMv2, Net-NTLM

**NT LAN M**anager. Microsoft's legacy challenge–response authentication family, kept alive for decades as the fallback wherever Kerberos can't be used (IP-address access, workgroups, old devices).

**Context.** NTLM is the gift that keeps on giving to attackers: the password's NT hash is a *password-equivalent* (enabling [[Pass-the-Hash]]), and the challenge–response exchange can be captured and relayed (NTLM relay) or cracked offline. Microsoft has formally put NTLM on the deprecation path, but every Windows network audit still finds it — usually pinned in place by a printer, NAS, or ancient application.

## See also

- [[Kerberos]]
- [[Pass-the-Hash]]
- [[Active Directory]]
- [[Hash Function]]
- [[MITM]]

## Often confused with

- [[Kerberos]] — Kerberos is the ticket-based default for domain auth; NTLM is the hash-based fallback — and the one attackers hope is still enabled.

## Further reading

- [Wikipedia: NTLM](https://en.wikipedia.org/wiki/NTLM)
