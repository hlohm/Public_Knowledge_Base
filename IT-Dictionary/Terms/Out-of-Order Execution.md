---
type: "term"
branch: "Hardware & Architecture"
aliases: ["OoO Execution"]
tags: ["hardware"]
status: "developed"
---

# Out-of-Order Execution

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** OoO Execution

A CPU technique that executes instructions as their inputs become ready rather than in strict program order, while retiring results in order, to keep execution units busy through stalls.

**Context.** A pillar of single-thread performance and a large slice of a CPU core's transistor budget — register renaming, reorder buffers, reservation stations. It is precisely the machinery a GPU largely *omits*: a GPU hides latency with thousands of resident threads instead of with per-thread reordering. CPU = clever about one stream; GPU = many streams, each kept simple.

## See also

- [[Speculative Execution]]
- [[Branch Prediction]]
- [[Latency Hiding]]
- [[Pipeline]]

## Further reading

- [Out-of-order execution — Wikipedia](https://en.wikipedia.org/wiki/Out-of-order_execution)
