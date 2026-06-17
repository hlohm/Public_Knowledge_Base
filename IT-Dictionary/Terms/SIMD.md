---
type: "term"
branch: "Hardware & Architecture"
aliases: ["Single Instruction", "\"Multiple Data\""]
tags: ["hardware"]
status: "developed"
---

# SIMD

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** Single Instruction, "Multiple Data"

An execution model in which one instruction operates on several data elements at once, through wide vector registers and parallel lanes.

**Context.** The CPU's bulk-throughput tool — AVX, SVE, NEON — and the "MD" cell of Flynn's taxonomy. Fetch and decode are amortised across the lanes, the same trick a GPU scales to the extreme. Strong on regular array work, useless on branchy code. **Often confused with:** [[SIMT]] — SIMD exposes fixed-width vectors to the programmer; SIMT presents many independent "threads" that the hardware happens to run in lockstep groups.

## See also

- [[Flynn's Taxonomy]]
- [[SIMT]]
- [[Vector Processor]]
- [[Tensor Core]]

## Further reading

- [Single instruction, multiple data — Wikipedia](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data)
