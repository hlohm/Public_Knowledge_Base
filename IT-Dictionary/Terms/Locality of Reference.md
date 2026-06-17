---
type: "term"
branch: "Hardware & Architecture"
aliases: ["Locality", "Spatial Locality", "Temporal Locality"]
tags: ["hw", "fundamental"]
status: "developed"
---

# Locality of Reference

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** Locality, Spatial Locality, Temporal Locality

The empirical law that programs reuse what they just touched (**temporal** locality) and touch what's next to it (**spatial** locality). The entire [[Memory Hierarchy]] is a bet on this law holding.

**Context.** Locality is why caches achieve 95%+ hit rates on code that never heard of them — and why code that *breaks* locality (pointer-chasing, random access over huge arrays, column-wise walks through row-major data) runs an order of magnitude slower with identical Big-O. The single most practical fact of hardware-aware programming.

## See also

- [[Cache]]
- [[Cache Line]]
- [[Memory Hierarchy]]
- [[Cache Miss]]

## Further reading

- [Wikipedia: Locality of reference](https://en.wikipedia.org/wiki/Locality_of_reference)
