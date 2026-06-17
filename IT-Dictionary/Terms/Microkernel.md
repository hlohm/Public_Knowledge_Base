---
type: "term"
branch: "Operating Systems"
tags: ["os"]
status: "developed"
---

# Microkernel

> **Branch:** [[03 - Operating Systems|Operating Systems]]

Kernel design that keeps only the irreducible minimum in kernel space (scheduling, IPC, basic memory) and runs drivers, file systems, and services as isolated user-space processes talking via messages.

**Context.** The promise is fault isolation — a crashed driver restarts instead of panicking the machine — which is why microkernels rule where failure is unacceptable: QNX in cars, seL4 (formally verified) in high-assurance systems, Minix quietly inside Intel's ME. The historical Linux-vs-Tanenbaum flame war is the field's favorite origin story; modern designs hybridize.

## See also

- [[Monolithic Kernel]]
- [[Kernel]]
- [[Message Passing]]
- [[User Space]]

## Further reading

- [Wikipedia: Microkernel](https://en.wikipedia.org/wiki/Microkernel)
