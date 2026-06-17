---
type: "term"
branch: "Operating Systems"
tags: [os, fundamental]
status: "developed"
---

# Kernel

> **Branch:** [[03 - Operating Systems|Operating Systems]]

The core of an OS, running in privileged mode with full hardware access. It mediates everything programs do via system calls.

**Context.** The privileged/unprivileged split (kernel space vs user space) is the fundamental protection boundary of the machine. Monolithic kernels (Linux) put drivers inside the kernel for speed; microkernels push them out for isolation.

## See also

- [[User Space]]
- [[System Call]]
- [[Monolithic Kernel]]
- [[Microkernel]]

## Further reading

- [Wikipedia: Kernel (operating system)](https://en.wikipedia.org/wiki/Kernel_(operating_system))
