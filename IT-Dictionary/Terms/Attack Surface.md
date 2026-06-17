---
type: "term"
branch: "Security"
domain: "Core Principles & Models"
tags: ["principle"]
status: "developed"
---

# Attack Surface

> **Domain:** [[01 - Core Principles|Core Principles & Models]]

The sum of all points where an attacker could try to enter or extract data. Reduce it, monitor it.

**Context.** Every open port, exposed API, installed agent, browser plugin, and mail-enabled mailbox is surface. Practical reduction: uninstall what you don't use, close inbound ports, disable legacy protocols (SMBv1, NTLMv1, basic auth), and put admin interfaces behind a VPN or bastion. Surface you can't remove, you inventory and watch.

## See also

- [[Hardening]]
- [[Blast Radius]]
- [[Shadow IT]]

## Further reading

- [OWASP: Attack Surface Analysis Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Attack_Surface_Analysis_Cheat_Sheet.html)
