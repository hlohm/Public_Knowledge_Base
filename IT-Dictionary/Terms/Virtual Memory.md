---
type: "term"
branch: "Operating Systems"
tags: [os, fundamental]
status: "developed"
---

# Virtual Memory

> **Branch:** [[03 - Operating Systems|Operating Systems]]

An abstraction giving each process its own large, contiguous-looking address space, mapped behind the scenes onto physical RAM (and disk) in fixed-size pages.

**Context.** It delivers isolation, the ability to use more memory than physically exists (via swap), and simpler programming (every process thinks it starts at address 0). The MMU does the per-access translation; a missing page triggers a page fault.

## See also

- [[Paging]]
- [[Page Fault]]
- [[MMU]]
- [[Swap]]

## Further reading

- [Wikipedia: Virtual memory](https://en.wikipedia.org/wiki/Virtual_memory)
