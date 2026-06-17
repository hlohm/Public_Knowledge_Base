---
type: "term"
branch: "Hardware & Architecture"
aliases: ["Memory Management Unit"]
tags: [hardware]
status: "developed"
---

# MMU

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** Memory Management Unit

Hardware that translates the virtual addresses programs use into physical RAM addresses, and enforces access permissions, page by page.

**Context.** The MMU is what makes virtual memory and process isolation possible — one process literally cannot name another's memory. The TLB caches recent translations so this lookup doesn't dominate every access.

## See also

- [[Virtual Memory]]
- [[TLB]]
- [[Paging]]
- [[Memory Protection]]

## Further reading

- [Wikipedia: Memory management unit](https://en.wikipedia.org/wiki/Memory_management_unit)
