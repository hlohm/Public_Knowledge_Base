---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
aliases: ["HIDS", "\"HIPS\""]
tags: ["endpoint"]
status: "note"
---

# HIDS and HIPS

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]
> **Also known as:** HIDS, "HIPS"

**H**ost-based **I**ntrusion **D**etection / **P**revention. IDS/IPS that runs on the host itself.

**Context.** The genre survives in specific niches: file-integrity monitoring (a PCI DSS requirement — who changed this binary/config?), log-based detection on servers (OSSEC/Wazuh), and auditd rules. On the modern endpoint, EDR has absorbed the role; on appliances and pets-not-cattle servers, classic HIDS still earns a slot.

## See also

- [[IDS and IPS]]
- [[EDR]]
