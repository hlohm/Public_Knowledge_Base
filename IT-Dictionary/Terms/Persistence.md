---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
tags: ["threat"]
status: "developed"
---

# Persistence

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]

Maintaining access across reboots and credential changes.

**Context.** The attacker's insurance against reboots and password resets: scheduled tasks, run keys, services, WMI subscriptions, and — nastier — golden tickets, rogue OAuth grants, and added credentials on service accounts. Eviction means hunting all of it, which is why "we reset the password" rarely ends an intrusion. ASEP enumeration (Autoruns) is the bread-and-butter check.

## See also

- [[Rootkit]]
- [[Beacon]]
- [[MITRE ATT&CK]]

## Further reading

- [MITRE ATT&CK: Persistence](https://attack.mitre.org/tactics/TA0003/)
