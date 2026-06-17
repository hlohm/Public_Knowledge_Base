---
type: "term"
branch: "Hardware & Architecture"
aliases: ["Protection Rings", "CPU Privilege Level", "Ring 0", "Ring 3"]
tags: [hardware, fundamental]
status: "developed"
---

# Protection Ring

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** CPU Privilege Level, Ring 0, Ring 3

Hardware-enforced privilege levels that bound what code may do. On x86, **Ring 0** is the most privileged ([[Kernel]] mode, full hardware access) and **Ring 3** is the least (user mode). The boundary between them is the machine's fundamental protection wall.

**Context.** Security thinking extends the model below Ring 0. The [[Hypervisor]] is informally **"Ring -1"** — it runs beneath the OS and can mediate everything the OS sees. Deeper still sit [[SMM]] ("Ring -2"), a firmware mode invisible to the OS, and platform engines like [[Intel ME]] ("Ring -3"). The deeper an attacker plants code, the less is left above it to inspect it — and, increasingly, the deeper a *defender* sits to protect the layers above (see [[VBS]]).

## See also

- [[Kernel]]
- [[User Space]]
- [[Hypervisor]]
- [[SMM]]
- [[System Call]]

## Further reading

- [Wikipedia: Protection ring](https://en.wikipedia.org/wiki/Protection_ring)
