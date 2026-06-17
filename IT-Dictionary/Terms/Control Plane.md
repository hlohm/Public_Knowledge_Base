---
type: "term"
branch: "Security"
domain: "Cloud & Modern Architecture"
aliases: ["Data Plane"]
tags: ["cloud"]
status: "note"
---

# Control Plane

> **Domain:** [[10 - Cloud and Modern Architecture|Cloud & Modern Architecture]]
> **Also known as:** Data Plane

Management/API surface. Distinct from **data plane** (the surface that handles workload traffic).

**Context.** Where cloud security concentrates: data-plane compromise gets you one workload, control-plane compromise gets you the account — every resource creatable, every permission grantable. Practical consequences: MFA/FIDO2 on cloud consoles, scoped and short-lived API credentials, and audit logging (CloudTrail, Azure Activity Log) treated as tier-zero telemetry.
