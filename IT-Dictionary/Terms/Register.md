---
type: "term"
branch: "Hardware & Architecture"
tags: [hardware, fundamental]
status: "developed"
---

# Register

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]

A tiny, extremely fast storage location inside the CPU holding a value the processor is working on right now. There are only a few dozen.

**Context.** Registers sit at the top of the memory hierarchy — a register access is effectively free, while a cache miss to RAM costs hundreds of cycles. Compilers spend real effort on 'register allocation' to keep hot values here.

## See also

- [[CPU]]
- [[Cache]]
- [[Memory Hierarchy]]
- [[ALU]]

## Further reading

- [Wikipedia: Processor register](https://en.wikipedia.org/wiki/Processor_register)
