---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
de: "Härtung"
tags: ["endpoint"]
status: "note"
---

# Hardening

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]
> **German:** Härtung

Reducing attack surface by disabling unused features, enforcing baselines (CIS Benchmarks), patching.

**Context.** The leverage move is doing it once, in the image: a hardened golden image or configuration baseline (Group Policy, Intune, Ansible) beats hardening machines retroactively forever. CIS Benchmarks and BSI SiSyPHuS profiles supply the checklist; drift monitoring keeps it true. Every disabled legacy protocol — SMBv1, NTLMv1, basic auth — is a class of attack retired.

## See also

- [[CIS Benchmarks]]
- [[Attack Surface]]
- [[Patch Management]]
- [[Group Policy]]
