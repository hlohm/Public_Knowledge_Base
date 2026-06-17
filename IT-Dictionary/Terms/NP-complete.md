---
type: "term"
branch: "Theory of Computation"
tags: [theory]
status: "developed"
---

# NP-complete

> **Branch:** [[10 - Theory of Computation|Theory of Computation]]

The hardest problems in NP: in NP themselves, and every NP problem reduces to them — so a fast solution to one would solve them all (and prove P = NP).

**Context.** The practical takeaway is recognition, not theory: if your problem is NP-complete (SAT, travelling salesman decision, graph colouring, knapsack), stop looking for an efficient exact algorithm and reach for approximation, heuristics, or constraint solvers. Recognising a disguised NP-complete problem saves weeks.

## See also

- [[P vs NP]]
- [[NP-hard]]
- [[Reduction]]
- [[SAT]]
- [[Approximation Algorithm]]

## Often confused with

- [[NP-hard]] — NP-complete = NP-hard *and* in NP (verifiable quickly). NP-hard problems are at least as hard but needn't be in NP — the halting problem is NP-hard but not NP-complete.

## Further reading

- [Wikipedia: NP-completeness](https://en.wikipedia.org/wiki/NP-completeness)
