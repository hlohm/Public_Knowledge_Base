---
type: "term"
branch: "Operating Systems"
tags: [os]
status: "developed"
---

# Page Fault

> **Branch:** [[03 - Operating Systems|Operating Systems]]

An exception raised when a program accesses a virtual page that isn't currently in physical RAM, prompting the OS to fetch or map it.

**Context.** A *minor* fault just needs a mapping fixed up; a *major* fault must read from disk and is slow. Not inherently an error — demand paging relies on them — but a flood of major faults means thrashing.

## See also

- [[Virtual Memory]]
- [[Paging]]
- [[Swap]]
- [[Thrashing]]

## Further reading

- [Wikipedia: Page fault](https://en.wikipedia.org/wiki/Page_fault)
