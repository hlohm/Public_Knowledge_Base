---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
tags: ["threat"]
status: "developed"
---

# Lateral Movement

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]

Moving from initial foothold to other systems inside the network.

**Context.** The phase where one workstation becomes a domain compromise — via stolen credentials (Pass-the-Hash), remote services (RDP, WMI, PsExec), or trust relationships. It generates internal east-west traffic the perimeter never sees, so detection lives in EDR, AD logs, and network segmentation that simply denies the hops.

## See also

- [[Privilege Escalation]]
- [[Persistence]]
- [[Pass-the-Hash]]
- [[Pivoting]]
- [[East-West vs North-South Traffic]]

## Further reading

- [MITRE ATT&CK: Lateral Movement](https://attack.mitre.org/tactics/TA0008/)
