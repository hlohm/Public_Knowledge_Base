---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam", "protocol"]
status: "developed"
---

# Kerberos

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

Ticket-based authentication protocol; backbone of Windows domain logon. Key terms: **KDC** (Key Distribution Center), **TGT** (Ticket Granting Ticket), **service ticket**.

**Context.** Worth learning properly because AD attack and defense both speak it: Kerberoasting abuses service tickets, Golden/Silver Tickets forge them, and "why does my service get a 401" is usually an SPN or delegation problem. Time sync matters — more than 5 minutes of clock skew and authentication fails domain-wide, a classic after-VM-restore incident.

## See also

- [[Active Directory]]
- [[Pass-the-Hash]]

## Further reading

- [RFC 4120: Kerberos V5](https://datatracker.ietf.org/doc/html/rfc4120)
