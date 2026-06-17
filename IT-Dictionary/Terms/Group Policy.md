---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
aliases: ["GPO", "Group Policy Object"]
de: "Gruppenrichtlinie"
tags: ["security", "endpoint", "windows"]
status: "developed"
---

# Group Policy

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]
> **Also known as:** GPO, Group Policy Object
> **German:** Gruppenrichtlinie

Active Directory's mechanism for centrally enforcing configuration on Windows machines and users. Settings are bundled into **GPOs** linked to sites, domains, or OUs, and applied at boot/logon and on refresh.

**Context.** Group Policy is how Windows hardening actually gets *deployed* — CIS Benchmarks and BSI baselines end up as GPO settings. The processing order (Local → Site → Domain → OU, last writer wins) and `gpresult /r` are daily helpdesk vocabulary. It's also an attack surface: a compromised GPO is domain-wide code execution, so GPO modification rights deserve the same scrutiny as Domain Admin membership. Intune/MDM is the cloud-era successor for devices that rarely see the domain.

## See also

- [[Active Directory]]
- [[Hardening]]
- [[CIS Benchmarks]]
- [[Permissions]]

## Further reading

- [Wikipedia: Group Policy](https://en.wikipedia.org/wiki/Group_Policy)
