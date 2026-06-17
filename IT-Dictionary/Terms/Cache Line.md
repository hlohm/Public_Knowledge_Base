---
type: "term"
branch: "Hardware & Architecture"
tags: ["hw"]
status: "developed"
---

# Cache Line

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]

The unit of transfer between memory and CPU caches — typically 64 bytes. Touch one byte and the whole line is fetched; caches track, evict, and keep coherent whole lines, never single bytes.

**Context.** The cache line is why memory layout is a performance topic: arrays iterate fast because each fetched line prepays the next several elements ([[Locality of Reference]] made physical), and linked lists crawl because every node is a fresh miss. It's also the granularity of **false sharing** — two threads writing different variables that share a line will ping-pong it between cores and mysteriously serialize.

## See also

- [[Cache]]
- [[Cache Miss]]
- [[Cache Coherence]]
- [[Locality of Reference]]

## Further reading

- [Wikipedia: CPU cache](https://en.wikipedia.org/wiki/CPU_cache)
