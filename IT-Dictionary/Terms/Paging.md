---
type: "term"
branch: "Operating Systems"
aliases: ["Page", "Page Table"]
tags: ["os", "fundamental"]
status: "developed"
---

# Paging

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** Page, Page Table

Dividing virtual and physical memory into fixed-size **pages** (typically 4 KiB) and mapping between them via **page tables**, so each process sees its own contiguous address space over scattered physical frames.

**Context.** Paging is the machinery behind [[Virtual Memory]]: per-process isolation, copy-on-write, memory-mapped files, and demand loading all fall out of the same mapping trick. The MMU walks the tables, the TLB caches the translations, and a mapping miss raises a [[Page Fault]] — which is normal operation, not an error, until it isn't (thrashing).

## See also

- [[Virtual Memory]]
- [[Page Fault]]
- [[MMU]]
- [[Swap]]
- [[Kernel]]

## Further reading

- [Wikipedia: Memory paging](https://en.wikipedia.org/wiki/Memory_paging)
