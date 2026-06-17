---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
aliases: ["Hypervisor-Protected Code Integrity", "Memory Integrity", "Hypervisor-Enforced Code Integrity"]
tags: [endpoint, modern]
status: "developed"
---

# HVCI

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]
> **Also known as:** Memory Integrity, Hypervisor-Protected Code Integrity

A [[VBS]] feature that moves kernel code-integrity decisions into the hypervisor-protected secure world, so only validated, signed code can ever execute in [[Kernel]] mode — and kernel pages are never both writable and executable at once.

**Context.** HVCI is the direct counter to [[BYOVD]] and [[DKOM]]: even with a vulnerable signed driver loaded, injected kernel code can't be made executable without passing checks the ordinary kernel no longer controls. It's surfaced in the Windows Security app as "Memory Integrity." The cost is driver compatibility — incompatible drivers are blocked, which is the usual reason it gets left off.

## See also

- [[VBS]]
- [[Kernel]]
- [[BYOVD]]
- [[DKOM]]
- [[Code Signing]]

## Further reading

- [Microsoft Learn: Enable memory integrity (HVCI)](https://learn.microsoft.com/en-us/windows/security/hardware-security/enable-virtualization-based-protection-of-code-integrity)
