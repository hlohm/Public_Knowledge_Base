---
type: "term"
branch: "Hardware & Architecture"
tags: ["hardware", "modern"]
status: "note"
---

# Tensor Core

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]

A specialised GPU execution unit that performs a small matrix multiply-accumulate as a single operation, sharply accelerating the dense linear algebra at the heart of deep learning.

**Context.** A direct counter-example to the idea that throughput hardware means *simpler* instructions: once instruction fetch is amortised across many lanes, the winning move is to make each instruction do **more** work, not less. Tensor cores push toward high-semantic, fused operations — the same logic taken even further by systolic-array accelerators like TPUs.

## See also

- [[Systolic Array]]
- [[SIMT]]
- [[Tensor]]
- [[GPU]]
- [[Matrix Multiplication]]
