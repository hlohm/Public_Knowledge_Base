---
type: "term"
branch: "Security"
domain: "Network Security"
aliases:
  - '"DoH"'
  - '"DoT"'
tags:
  - network
status: note
---

# DNS Security

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** DNSSEC, "DoH", "DoT"

Protecting name resolution. **DNSSEC** adds signatures; **DoH/DoT** encrypt queries; **DNS firewalling** blocks malicious domains.

**Context.** DNS is both attack vector and detection goldmine: malware needs to resolve its C2 somewhere, so protective DNS (Quad9, internal RPZ, M365's equivalent) blocks cheaply and DNS logs answer "who talked to this domain?" in seconds. The flip side: DNS tunneling exfiltrates data through the one protocol everyone allows outbound.

## See also

- [[C2]]
- [[Exfiltration]]
- [[DNSSEC]]
