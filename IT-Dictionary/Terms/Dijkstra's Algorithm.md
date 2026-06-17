---
type: "term"
branch: "Algorithms & Data Structures"
tags: [algo]
status: "developed"
---

# Dijkstra's Algorithm

> **Branch:** [[09 - Algorithms & Data Structures|Algorithms & Data Structures]]

Finds the shortest path from a source to all vertices in a graph with non-negative edge weights, using a priority queue to always expand the nearest unvisited vertex.

**Context.** The canonical weighted shortest-path algorithm (routing, maps). Fails with negative weights (use Bellman-Ford), and A* extends it with a heuristic to search faster toward a goal. A clean example of the greedy strategy done right.

## See also

- [[Graph]]
- [[Priority Queue]]
- [[Greedy Algorithm]]
- [[A- Search|A* Search]]
- [[Shortest Path]]
- [[Heap]]

## Further reading

- [Wikipedia: Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra's_algorithm)
