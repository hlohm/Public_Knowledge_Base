---
type: "term"
branch: "Algorithms & Data Structures"
aliases: ["Topological Ordering", "Toposort"]
tags: ["algo"]
status: "developed"
---

# Topological Sort

> **Branch:** [[09 - Algorithms & Data Structures|Algorithms & Data Structures]]
> **Also known as:** Topological Ordering, Toposort

An ordering of a directed acyclic graph's nodes such that every edge points forward — dependencies before dependents. Computed by Kahn's algorithm or DFS finish times in O(V+E).

**Context.** This is the algorithm hiding inside every build system, package manager, task scheduler, and spreadsheet recalculation: 'what order satisfies the dependencies?' A cycle means no valid order exists — which is exactly how tools *detect* circular dependencies and why the error message names topological sort's failure.

## See also

- [[Graph]]
- [[Depth-First Search]]
- [[Dependency]]
- [[Build System]]

## Further reading

- [Wikipedia: Topological sorting](https://en.wikipedia.org/wiki/Topological_sorting)
