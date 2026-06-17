---
type: "term"
branch: "Computing Foundations"
tags: ["foundations", "fundamental"]
status: "developed"
---

# Flynn's Taxonomy

> **Branch:** [[01 - Computing Foundations|Computing Foundations]]

The standard classification of computer architectures by how many instruction streams and data streams operate concurrently: **SISD**, **SIMD**, **MISD**, and **MIMD**.

**Context.** SISD is the classic single-core von Neumann machine; SIMD is one instruction over many data lanes (vector units, GPU lanes); MIMD is many independent instruction streams (multicore CPUs, clusters); MISD is largely theoretical. Almost every "is this one computer?" question reduces to where a system sits in this grid — and, orthogonally, whether its streams share memory or pass messages.

## See also

- [[SIMD]]
- [[SIMT]]
- [[MIMD]]
- [[Shared Memory]]
- [[Message Passing]]
- [[Parallel Computing]]

## Further reading

- [Flynn's taxonomy — Wikipedia](https://en.wikipedia.org/wiki/Flynn's_taxonomy)
