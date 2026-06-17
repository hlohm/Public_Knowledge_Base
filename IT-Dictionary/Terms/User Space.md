---
type: "term"
branch: "Operating Systems"
aliases: ["Userland", "User Mode"]
tags: ["os", "fundamental"]
status: "developed"
---

# User Space

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** Userland, User Mode

Where ordinary programs run: unprivileged CPU mode, own virtual address space, every privileged action requested from the kernel via [[System Call]].

**Context.** The user/kernel split is *the* protection boundary: a userland crash kills one process; a kernel crash kills the machine. It's also why security tooling keeps migrating downward (EDR drivers, eBPF) — userland can be lied to by a compromised kernel, never the reverse.

## See also

- [[Kernel Space]]
- [[Kernel]]
- [[System Call]]
- [[Protection Ring]]
- [[Process]]

## Further reading

- [Wikipedia: User space and kernel space](https://en.wikipedia.org/wiki/User_space_and_kernel_space)
