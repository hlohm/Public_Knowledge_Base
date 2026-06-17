---
type: "term"
branch: "Hardware & Architecture"
tags: ["hw", "fundamental"]
status: "developed"
---

# Memory Hierarchy

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]

The pyramid of storage from registers (sub-ns, bytes) through L1/L2/L3 cache (ns, MBs) and RAM (~100 ns, GBs) to SSD (~100 µs) and beyond — each level bigger, slower, and cheaper per byte than the one above.

**Context.** The hierarchy exists because fast and large are physically incompatible; it *works* because programs exhibit [[Locality of Reference]], letting small fast levels serve most accesses. Internalizing the rough latency ratios (RAM ≈ 100× cache, disk ≈ 1000× RAM) explains most performance behavior — from why caches exist to why [[Swap|swapping]] feels like the machine died.

## See also

- [[Cache]]
- [[RAM]]
- [[SSD]]
- [[Register]]
- [[Locality of Reference]]

## Further reading

- [Wikipedia: Memory hierarchy](https://en.wikipedia.org/wiki/Memory_hierarchy)
