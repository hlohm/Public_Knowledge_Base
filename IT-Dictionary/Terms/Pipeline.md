---
type: "term"
branch: "Hardware & Architecture"
aliases: ["Instruction Pipelining"]
tags: [hardware]
status: "developed"
---

# Pipeline

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** Instruction Pipelining

Overlapping the stages of consecutive instructions (fetch, decode, execute…) like an assembly line, so a new instruction can start before the previous finishes.

**Context.** Pipelining is why a 'branch misprediction' is expensive — the speculatively-loaded pipeline must be flushed. This same speculation underlies the Spectre/Meltdown class of side-channel attacks.

## See also

- [[Branch Prediction]]
- [[Speculative Execution]]
- [[Superscalar]]
- [[CPU]]

## Further reading

- [Wikipedia: Instruction pipelining](https://en.wikipedia.org/wiki/Instruction_pipelining)
