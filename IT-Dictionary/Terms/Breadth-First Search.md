---
type: "term"
branch: "Algorithms & Data Structures"
aliases: ["BFS"]
tags: [algo, fundamental]
status: "developed"
---

# Breadth-First Search

> **Branch:** [[09 - Algorithms & Data Structures|Algorithms & Data Structures]]
> **Also known as:** BFS

A graph traversal exploring all neighbours at the current depth before going deeper, using a queue.

**Context.** Finds the shortest path in an *unweighted* graph (fewest edges), level by level. The queue-based counterpart to DFS's stack/recursion. Reach for it whenever 'fewest steps' is the question — maze solving, social-graph degrees of separation.

## See also

- [[Depth-First Search]]
- [[Graph]]
- [[Queue]]
- [[Shortest Path]]
- [[Dijkstra's Algorithm]]

## Often confused with

- [[Depth-First Search]] — BFS explores level by level (queue, finds shortest unweighted path); DFS plunges down one branch fully before backtracking (stack/recursion).

## Further reading

- [Wikipedia: Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)
