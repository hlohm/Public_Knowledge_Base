---
type: "term"
branch: "Algorithms & Data Structures"
aliases: ["Prefix Tree"]
tags: [algo]
status: "developed"
---

# Trie

> **Branch:** [[09 - Algorithms & Data Structures|Algorithms & Data Structures]]
> **Also known as:** Prefix Tree

A tree where each path from the root spells a string, sharing common prefixes — lookup is O(length of key), independent of how many keys are stored.

**Context.** The structure behind autocomplete, spell-checkers, IP routing tables (radix tries), and prefix matching. Trades memory for prefix-search speed; compressed variants (radix/Patricia tries) cut the space cost.

## See also

- [[Tree]]
- [[Hash Table]]
- [[String]]
- [[Radix Tree]]

## Further reading

- [Wikipedia: Trie](https://en.wikipedia.org/wiki/Trie)
