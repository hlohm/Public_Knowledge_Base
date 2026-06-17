---
type: "term"
branch: "Operating Systems"
aliases: ["Syscall"]
tags: [os, fundamental]
status: "developed"
---

# System Call

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** Syscall

The controlled gateway a user-space program uses to ask the kernel for a privileged service — open a file, send on a socket, allocate memory.

**Context.** It's the one legitimate door from user space into kernel space, and so a key place to enforce and audit security ([[seccomp]] filters syscalls). Each crossing has overhead, which is why high-performance I/O tries to batch or avoid them (io_uring).

## See also

- [[Kernel]]
- [[User Space]]
- [[Kernel Space]]
- [[File Descriptor]]

## Further reading

- [Wikipedia: System call](https://en.wikipedia.org/wiki/System_call)
