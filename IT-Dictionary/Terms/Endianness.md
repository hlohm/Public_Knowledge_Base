---
type: "term"
branch: "Computing Foundations"
tags: [foundations, fundamental]
status: "developed"
---

# Endianness

> **Branch:** [[01 - Computing Foundations|Computing Foundations]]

The order in which a multi-byte value's bytes are stored in memory. **Big-endian** stores the most significant byte first; **little-endian** stores the least significant first.

**Context.** x86 is little-endian; network protocols are big-endian ('network byte order'), which is why you call `htons()`/`ntohl()` at the boundary. Mismatches produce values that look byte-swapped — a classic cross-platform bug.

## See also

- [[Byte]]
- [[Word]]
- [[Most Significant Bit]]

## Further reading

- [Wikipedia: Endianness](https://en.wikipedia.org/wiki/Endianness)
