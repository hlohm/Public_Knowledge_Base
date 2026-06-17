---
type: "term"
branch: "Computing Foundations"
tags: [foundations, fundamental, standards]
status: "developed"
---

# UTF-8

> **Branch:** [[01 - Computing Foundations|Computing Foundations]]

A variable-width encoding of Unicode using 1–4 bytes per code point. ASCII characters stay one byte, so ASCII text is already valid UTF-8.

**Context.** It dominates the web (>98% of pages) because it is ASCII-compatible, self-synchronising, and endian-free. Prefer it as your default everywhere; the alternatives (UTF-16, legacy code pages) mostly cause pain.

## See also

- [[Unicode]]
- [[Code Point]]
- [[ASCII]]

## Further reading

- [Wikipedia: UTF-8](https://en.wikipedia.org/wiki/UTF-8)
