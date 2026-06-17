---
type: "term"
branch: "Cloud & Infrastructure"
aliases: ["Virtual Machine Monitor", "VMM"]
tags: [cloud]
status: "developed"
---

# Hypervisor

> **Branch:** [[11 - Cloud & Infrastructure|Cloud & Infrastructure]]
> **Also known as:** Virtual Machine Monitor, VMM

The software layer that creates and runs virtual machines, mediating their access to physical hardware. **Type 1** runs on bare metal; **Type 2** runs atop a host OS.

**Context.** Type 1 (ESXi, Xen, KVM, Hyper-V) is what powers data centres and clouds — minimal overhead, strong isolation. Type 2 (VirtualBox, VMware Workstation) is for desktops. The isolation boundary is a security boundary, so hypervisor escapes are among the most severe vulnerabilities.

## See also

- [[Virtualization]]
- [[Virtual Machine]]
- [[Container]]
- [[Bare Metal]]

## Further reading

- [Wikipedia: Hypervisor](https://en.wikipedia.org/wiki/Hypervisor)
