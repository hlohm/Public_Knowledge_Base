---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
aliases: ["Virtualization-Based Security", "Core Isolation"]
tags: [endpoint, modern]
status: "developed"
---

# VBS

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]
> **Also known as:** Virtualization-Based Security, Core Isolation

A Windows defence that uses the [[Hypervisor]] to carve a small, isolated "secure world" out of the running system — assuming the normal [[Kernel]] *can* be compromised, and protecting critical secrets and policy from it. It is the foundation for [[HVCI]] and [[Credential Guard]].

**Context.** This is the defensive inversion of hypervisor-based malware: instead of an attacker slipping beneath the OS at "Ring -1", Microsoft gets there first and runs a higher-trust secure kernel the ordinary kernel can't touch. VBS needs hardware virtualization plus [[Secure Boot]]; on Windows 11 it's on by default on most hardware. It's surfaced in the UI as "Core Isolation."

## See also

- [[Hypervisor]]
- [[HVCI]]
- [[Credential Guard]]
- [[Kernel]]
- [[Secure Boot]]

## Further reading

- [Microsoft Learn: Virtualization-based Security (VBS)](https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/oem-vbs)
