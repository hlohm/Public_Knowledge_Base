---
type: "term"
branch: "Data & Databases"
tags: [data, fundamental]
status: "developed"
---

# B-tree

> **Branch:** [[06 - Data & Databases|Data & Databases]]

A self-balancing, multi-way search tree that keeps data sorted and supports search, insert, and delete in logarithmic time — designed so each node is one disk page.

**Context.** The reason it dominates database and filesystem indexes: it's *disk-aware*. A high branching factor means a few page reads reach any record, minimising the expensive operation (I/O). The B+tree variant, with all values in the leaves linked for range scans, is what most engines actually use.

## See also

- [[Index]]
- [[LSM Tree]]
- [[Binary Search Tree]]
- [[Disk I-O|Disk I/O]]

## Often confused with

- [[Binary Search Tree]] — A BST is binary and memory-oriented; a B-tree is wide and disk-oriented, with many keys per node to minimise page reads.

## Further reading

- [Wikipedia: B-tree](https://en.wikipedia.org/wiki/B-tree)
