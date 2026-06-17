---
type: "term"
branch: "Computing Foundations"
aliases: ["Machine Word", "Word Size"]
tags: ["foundations", "hw", "fundamental"]
status: "developed"
---

# Word

> **Branch:** [[01 - Computing Foundations|Computing Foundations]]
> **Also known as:** Machine Word, Word Size

The natural unit of data for a CPU — the register width and the size it moves and computes in one step. '64-bit architecture' means a 64-bit word.

**Context.** Word size silently sets the limits people then rediscover: 32-bit words → 4 GiB address ceilings and the 2038 Unix-time problem; pointer width = word width is why binaries come in 32/64-bit flavors. Beware the unit soup: a 'word' is 16 bits in Win32 API jargon and x86 assembly tradition, but the architectural word of the machine running it is 64 — context decides.

## See also

- [[Register]]
- [[Bit]]
- [[Byte]]
- [[CPU]]
- [[Two's Complement]]

## Further reading

- [Wikipedia: Word (computer architecture)](https://en.wikipedia.org/wiki/Word_(computer_architecture))
