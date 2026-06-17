---
type: "term"
branch: "Computing Foundations"
aliases: ["Epoch Time"]
tags: ["foundations"]
status: "developed"
---

# Epoch

> **Branch:** [[01 - Computing Foundations|Computing Foundations]]
> **Also known as:** Epoch Time

The fixed zero-point a timekeeping scheme counts from. [[Unix Time]]'s epoch is 1970-01-01 00:00:00 UTC; Windows FILETIME counts from 1601; GPS from 1980.

**Context.** Epoch mismatches and counter widths are where time bugs live: 32-bit seconds-since-1970 overflows in **2038**, GPS week counters roll over every ~19.6 years, and converting between epochs (NTFS↔Unix timestamps in forensics) is a classic off-by-eleven-thousand-days hazard. Unrelated but colliding term: an ML training *epoch* is one pass over the dataset — same word, different universe.

## See also

- [[Unix Time]]
- [[ISO 8601]]
- [[Integer Overflow]]

## Further reading

- [Wikipedia: Epoch (computing)](https://en.wikipedia.org/wiki/Epoch_(computing))
