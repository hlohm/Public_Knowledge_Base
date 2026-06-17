---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
tags: [threat]
status: "developed"
---

# Golden Ticket

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]

A forged [[Kerberos]] ticket-granting ticket (TGT) created using the stolen password hash of the domain's `krbtgt` account. Because every TGT in the domain is signed by that one key, possessing it lets an attacker mint tickets for *any* user — including domain admins — that the domain accepts as genuine.

**Context.** This is the apex of [[Active Directory]] [[Persistence]]: it survives password resets of the impersonated users (only rotating `krbtgt` *twice* invalidates it) and needs no further contact with a domain controller to forge tickets. Getting the `krbtgt` hash usually comes via [[DCSync]] or outright domain-controller compromise. ATT&CK **T1558.001**. The cloud-federation analogue is [[Golden SAML]].

## See also

- [[Kerberos]]
- [[Active Directory]]
- [[DCSync]]
- [[Pass-the-Hash]]
- [[Persistence]]
- [[Golden SAML]]

## Often confused with

- [[Silver Ticket]] — a Golden Ticket forges a TGT (domain-wide) from the `krbtgt` key; a Silver Ticket forges a single service ticket from one service account's key (one service, stealthier, no DC contact).

## Further reading

- [MITRE ATT&CK: Golden Ticket (T1558.001)](https://attack.mitre.org/techniques/T1558/001/)
