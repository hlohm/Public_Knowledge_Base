---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["AD", "\"Entra ID\"", "\"Azure AD\""]
de: "Active Directory"
tags: ["iam"]
status: "developed"
---

# Active Directory

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** AD, "Entra ID", "Azure AD"
> **German:** Active Directory

Microsoft's directory and identity service for enterprise networks. Cloud cousin: Entra ID (formerly Azure AD).

**Context.** Still the identity backbone of most enterprises, and therefore the prime target: compromise AD and you own everything joined to it. The attack canon (Kerberoasting, Pass-the-Hash, DCSync, Golden Ticket) is mature, which makes tiered administration, LAPS for local admin passwords, and monitoring of privileged groups baseline hygiene rather than advanced practice.

## See also

- [[LDAP]]
- [[Kerberos]]
- [[SSO]]
- [[Group Policy]]

## Further reading

- [Microsoft: Best practices for securing Active Directory](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/best-practices-for-securing-active-directory)
