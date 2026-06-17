---
type: "term"
branch: "Hardware & Architecture"
tags: [hardware]
status: "developed"
---

# Cache Miss

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]

When data the CPU needs isn't in the cache, forcing a slower fetch from a lower level (or RAM). The opposite is a cache hit.

**Context.** A miss to main memory can cost 100–300 cycles — long enough to execute hundreds of instructions. Tuning data layout to raise the hit rate is often a bigger win than algorithmic cleverness.

## See also

- [[Cache]]
- [[Cache Line]]
- [[Locality of Reference]]

## Further reading

- [Wikipedia: CPU cache](https://en.wikipedia.org/wiki/CPU_cache)
