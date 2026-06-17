---
type: "term"
branch: "Operating Systems"
aliases: ["Kernel Mode", "Supervisor Mode"]
tags: ["os", "fundamental"]
status: "developed"
---

# Kernel Space

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** Kernel Mode, Supervisor Mode

The privileged execution environment of the kernel and (in monolithic designs) its drivers: full hardware access, shared address space, no safety net.

**Context.** Everything in kernel space trusts everything else there — which is why a single buggy third-party driver can blue-screen a fleet, why kernel rootkits are game over, and why [[BYOVD]] attacks bother loading a vulnerable signed driver at all: it's a ticket across the boundary.

## See also

- [[User Space]]
- [[Kernel]]
- [[Protection Ring]]
- [[Rootkit]]
- [[BYOVD]]

## Further reading

- [Wikipedia: User space and kernel space](https://en.wikipedia.org/wiki/User_space_and_kernel_space)
