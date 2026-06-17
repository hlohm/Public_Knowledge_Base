---
type: "term"
branch: "Hardware & Architecture"
tags: ["hardware", "modern"]
status: "developed"
---

# Systolic Array

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]

A hardware architecture: a regular grid of simple processing elements that rhythmically pass data to their neighbours, computing operations like matrix multiplication with minimal control logic and memory traffic.

**Context.** The design at the core of TPUs and many NPUs — even less general than a GPU, trading flexibility for extreme efficiency on a single operation (the matmul). Data flows through the array like a pulse (hence "systolic"), each value reused across many PEs before leaving. The far end of the spectrum from a general-purpose CPU.

## See also

- [[Tensor Core]]
- [[TPU]]
- [[Matrix Multiplication]]
- [[Dataflow Architecture]]

## Further reading

- [Systolic array — Wikipedia](https://en.wikipedia.org/wiki/Systolic_array)
