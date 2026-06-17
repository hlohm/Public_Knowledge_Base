---
type: "term"
branch: "Hardware & Architecture"
aliases: ["Single Instruction", "\"Multiple Threads\""]
tags: ["hardware", "modern"]
status: "developed"
---

# SIMT

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** Single Instruction, "Multiple Threads"

The GPU execution model in which many threads are programmed as if independent, but the hardware runs them in fixed-size lockstep groups that share one instruction stream.

**Context.** The heart of how a GPU trades single-thread cleverness for raw throughput. You write ordinary per-thread code; the hardware bundles threads into **warps** and broadcasts one instruction across all lanes, amortising fetch/decode over dozens of datapaths. The cost shows up as **branch divergence** when threads in a group disagree on control flow. **Often confused with:** [[SIMD]] — see the SIMD note for the contrast.

## See also

- [[Warp]]
- [[Streaming Multiprocessor]]
- [[SIMD]]
- [[Branch Divergence]]
- [[Latency Hiding]]

## Further reading

- [Single instruction, multiple threads — Wikipedia](https://en.wikipedia.org/wiki/Single_instruction,_multiple_threads)
