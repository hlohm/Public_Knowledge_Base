---
type: "term"
branch: "Computing Foundations"
tags: ["foundations"]
status: "developed"
---

# Shared Memory

> **Branch:** [[01 - Computing Foundations|Computing Foundations]]

A parallelism model in which multiple processors cooperate by reading and writing a single common address space; coordination happens through memory itself — loads, stores, locks, atomics.

**Context.** Defines the tightest hardware boundary of "one computer": the set of processors that can transparently touch each other's data via ordinary loads and stores. Programming uses threads, mutexes and atomics, and leans on cache coherence to stay sane. It scales beautifully inside a node and poorly across a network — which is exactly where message passing takes over. **Often confused with:** [[Message Passing]] — shared memory cooperates through one common address space; message passing cooperates by explicitly sending data between separate memories.

## See also

- [[Message Passing]]
- [[Cache Coherence]]
- [[NUMA]]
- [[Multiprocessor]]
- [[Thread]]

## Further reading

- [Shared memory — Wikipedia](https://en.wikipedia.org/wiki/Shared_memory)
