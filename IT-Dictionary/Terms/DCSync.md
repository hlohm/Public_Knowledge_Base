---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
tags: [threat]
status: "developed"
---

# DCSync

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]

An attack that abuses the Directory Replication Service protocol to *ask* a domain controller to hand over password hashes — impersonating a DC requesting replication, rather than touching disk or LSASS. With the right replication rights, any account's hash (including `krbtgt`) can be pulled remotely.

**Context.** DCSync is the usual way attackers obtain the `krbtgt` hash needed for a [[Golden Ticket]], or a target user's hash for [[Pass-the-Hash]]. It needs replication privileges (Replicating Directory Changes), which is why those rights are tightly audited. Note that it queries the [[Active Directory]] database directly, so endpoint protections like [[Credential Guard]] don't stop it. ATT&CK **T1003.006**.

## See also

- [[Active Directory]]
- [[Golden Ticket]]
- [[Pass-the-Hash]]
- [[Kerberos]]
- [[Credential Guard]]

## Further reading

- [MITRE ATT&CK: DCSync (T1003.006)](https://attack.mitre.org/techniques/T1003/006/)
