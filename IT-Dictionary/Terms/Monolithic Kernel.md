---
type: "term"
branch: "Operating Systems"
tags: ["os"]
status: "developed"
---

# Monolithic Kernel

> **Branch:** [[03 - Operating Systems|Operating Systems]]

Kernel design where the whole OS core — scheduling, memory, file systems, drivers, network stack — runs as one program in kernel space. Linux and the BSDs are the canonical examples.

**Context.** The trade is raw speed (everything is a function call) against blast radius (any driver bug is a kernel bug). Linux softens it with loadable modules and pushes risky logic out via eBPF and userspace drivers — monolithic in architecture, pragmatic in practice.

## See also

- [[Microkernel]]
- [[Kernel]]
- [[Kernel Space]]
- [[eBPF]]

## Often confused with

- [[Microkernel]] — Monolithic: everything in kernel space, fast, shared fate. Microkernel: minimal kernel, services in user space, isolation at the cost of message-passing overhead.

## Further reading

- [Wikipedia: Monolithic kernel](https://en.wikipedia.org/wiki/Monolithic_kernel)
