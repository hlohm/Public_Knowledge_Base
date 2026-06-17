---
type: "term"
branch: "Cloud & Infrastructure"
aliases: ["VM"]
tags: [cloud, fundamental]
status: "developed"
---

# Virtual Machine

> **Branch:** [[11 - Cloud & Infrastructure|Cloud & Infrastructure]]
> **Also known as:** VM

A software emulation of a complete computer, running its own full OS atop a hypervisor, isolated from the host and other VMs.

**Context.** Strong isolation (each has its own kernel) at the cost of weight — minutes to boot, gigabytes of RAM. The tradeoff against containers is the central infra decision: VMs for hard isolation boundaries, containers for density and speed.

## See also

- [[Hypervisor]]
- [[Container]]
- [[Virtualization]]
- [[Guest OS]]

## Often confused with

- [[Container]] — A VM virtualises hardware and runs its own kernel (heavy, strong isolation); a container shares the host kernel and isolates only the process (light, weaker isolation).

## Further reading

- [Wikipedia: Virtual machine](https://en.wikipedia.org/wiki/Virtual_machine)
