---
type: "term"
branch: "Hardware & Architecture"
de: "Zwischenspeicher"
tags: [hardware, fundamental]
status: "developed"
---

# Cache

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **German:** Zwischenspeicher

Small, fast memory near the CPU that holds recently- or likely-used data so the processor avoids slow trips to main RAM. Organised in levels (L1/L2/L3).

**Context.** The single biggest performance lever in modern code is cache-friendliness: an array (contiguous) often beats a linked list (scattered) by 10× purely on cache behaviour, regardless of Big-O. 'Cache' as a general idea (keep likely-reused data close) recurs at every layer of computing.

## See also

- [[Cache Line]]
- [[Cache Miss]]
- [[Memory Hierarchy]]
- [[Locality of Reference]]

## Often confused with

- [[Buffer]] — A cache keeps reusable data for speed; a buffer smooths a rate/size mismatch between producer and consumer.

## Further reading

- [Wikipedia: CPU cache](https://en.wikipedia.org/wiki/CPU_cache)
