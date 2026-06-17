---
type: "term"
branch: "Operating Systems"
aliases: ["Swap Space", "Pagefile", "Swapping"]
tags: ["os"]
status: "developed"
---

# Swap

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** Swap Space, Pagefile, Swapping

Disk space (swap partition/file, Windows pagefile) used as overflow for RAM: when memory pressure rises, the kernel evicts cold pages to disk and reloads them on access.

**Context.** A little swap activity is healthy housekeeping; sustained swapping is **thrashing**, and the machine feels frozen because disk is orders of magnitude slower than RAM — the classic 'PC slow' culprit on under-RAM'd clients. Security footnote: secrets in memory can end up on disk via swap, which is why encrypted swap and `mlock` exist.

## See also

- [[Paging]]
- [[Virtual Memory]]
- [[RAM]]
- [[Page Fault]]

## Further reading

- [Wikipedia: Memory paging](https://en.wikipedia.org/wiki/Memory_paging)
