---
type: "term"
branch: "Hardware & Architecture"
tags: ["hardware"]
status: "developed"
---

# Speculative Execution

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]

Executing instructions before it is certain they are needed — typically past a predicted branch — and discarding the work if the guess was wrong.

**Context.** Buys speed by not waiting on branch resolution, but it leaves microarchitectural traces (cache state) even when the squashed results are thrown away — the root of the **Spectre/Meltdown** class of side-channel attacks. A vivid case of a pure performance optimisation becoming a security problem, and a reason this concept sits at the seam between architecture and security.

## See also

- [[Branch Prediction]]
- [[Out-of-Order Execution]]
- [[Side-Channel Attack]]
- [[Cache]]

## Further reading

- [Speculative execution — Wikipedia](https://en.wikipedia.org/wiki/Speculative_execution)
