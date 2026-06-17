---
type: "term"
branch: "Networking"
aliases: ["Port Number"]
tags: ["net", "fundamental"]
status: "developed"
---

# Port

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Port Number

A 16-bit number (0–65535) that identifies a specific service endpoint on a host, so one IP address can host many conversations. IP gets you to the machine; the port gets you to the program.

**Context.** Well-known ports (0–1023: 22 SSH, 25 SMTP, 80 HTTP, 443 HTTPS, 445 SMB, 3389 RDP) are the alphabet of firewall rules and port scans. Registered (1024–49151) and ephemeral (~49152+) ranges cover services and client-side connection ends. A port being open means a process is listening — the basic fact that all network reconnaissance and all firewalling is built on.

## See also

- [[Socket]]
- [[TCP]]
- [[UDP]]
- [[Firewall]]
- [[NAT]]

## Further reading

- [Wikipedia: Port (computer networking)](https://en.wikipedia.org/wiki/Port_(computer_networking))
