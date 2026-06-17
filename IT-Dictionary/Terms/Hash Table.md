---
type: "term"
branch: "Algorithms & Data Structures"
aliases: ["Hash Map", "Dictionary"]
tags: [algo, fundamental]
status: "developed"
---

# Hash Table

> **Branch:** [[09 - Algorithms & Data Structures|Algorithms & Data Structures]]
> **Also known as:** Hash Map, Dictionary

A structure mapping keys to values with average O(1) lookup, insert, and delete, by hashing the key to a bucket index.

**Context.** The workhorse associative array behind every language's dict/map. The catches: collisions (handled by chaining or open addressing), worst-case O(n) when hashing degrades, and no ordering. Hash-flooding (deliberate collision DoS) is why some runtimes randomise hash seeds.

## See also

- [[Hash Function]]
- [[Collision]]
- [[Array]]
- [[Bloom Filter]]
- [[Load Factor]]

## Further reading

- [Wikipedia: Hash table](https://en.wikipedia.org/wiki/Hash_table)
