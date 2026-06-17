---
type: "term"
branch: "Algorithms & Data Structures"
tags: [algo]
status: "developed"
---

# Bloom Filter

> **Branch:** [[09 - Algorithms & Data Structures|Algorithms & Data Structures]]

A space-efficient probabilistic structure that tests set membership with possible false positives but no false negatives — 'definitely not present' or 'probably present'.

**Context.** When 'might be there' is good enough and memory is tight: databases skip disk lookups for definitely-absent keys, caches and CDNs avoid useless fetches. You can tune the false-positive rate against size, but you can't delete elements (counting variants can).

## See also

- [[Hash Function]]
- [[Hash Table]]
- [[Probabilistic Data Structure]]
- [[Cache]]

## Further reading

- [Wikipedia: Bloom filter](https://en.wikipedia.org/wiki/Bloom_filter)
