---
type: "term"
branch: "Hardware & Architecture"
aliases: ["Non-Uniform Memory Access"]
tags: ["hardware"]
status: "developed"
---

# NUMA

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** Non-Uniform Memory Access

A shared-memory architecture in which memory is physically split among processors (sockets), so a core reaches its local memory faster than another socket's memory.

**Context.** How large multi-socket servers keep one coherent address space without a single memory bottleneck — at the price that data placement now matters. Schedulers and allocators become NUMA-aware to keep threads near their data. It's still one computer (one coherence domain), just with a non-flat cost map laid over the address space.

## See also

- [[Cache Coherence]]
- [[Shared Memory]]
- [[Multiprocessor]]

## Further reading

- [Non-uniform memory access — Wikipedia](https://en.wikipedia.org/wiki/Non-uniform_memory_access)
