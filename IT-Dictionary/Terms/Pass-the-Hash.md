---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["Pass-the-Ticket"]
tags: ["threat"]
status: "note"
---

# Pass-the-Hash

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** Pass-the-Ticket

Reusing stolen credentials/hashes in Windows environments without ever knowing the password. **Pass-the-Ticket** is the Kerberos equivalent.

**Context.** Windows authenticates with the hash, so the attacker never needs to crack the password — dump it from LSASS (Mimikatz) and reuse it. The mitigations are architectural: tiered admin so high-value hashes never land on low-trust machines, Credential Guard to protect LSASS, and disabling NTLM where Kerberos can carry the load.

## See also

- [[Kerberos]]
- [[Active Directory]]
- [[Lateral Movement]]
- [[Privilege Escalation]]
