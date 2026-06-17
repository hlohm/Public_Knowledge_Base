---
type: "term"
branch: "Security"
domain: "Core Principles & Models"
tags: ["principle"]
status: "note"
---

# Blast Radius

> **Domain:** [[01 - Core Principles|Core Principles & Models]]

How much damage one compromise can cause. Limiting blast radius (segmentation, least privilege, short-lived credentials) is a key design goal.

**Context.** The question to ask of any credential, service account, or flat network: "if this one thing is compromised, what falls with it?" A domain admin account that browses the web has the blast radius of the whole forest. Tiered admin models, network segmentation, and per-service credentials exist to shrink the answer.

## See also

- [[Microsegmentation]]
- [[Least Privilege]]
- [[JIT Access]]
- [[Network Segmentation]]
