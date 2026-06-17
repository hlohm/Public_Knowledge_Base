---
type: "term"
branch: "Data & Databases"
aliases: ["Query Planner"]
tags: ["data"]
status: "developed"
---

# Query Optimizer

> **Branch:** [[06 - Data & Databases|Data & Databases]]
> **Also known as:** Query Planner

The database component that turns declarative SQL into an execution plan — choosing indexes, join order, and join algorithms by estimating costs from table statistics.

**Context.** The optimizer is why SQL can be declarative at all: you state *what*, it derives *how*. It's also why performance problems are often *statistics* problems — stale stats or skewed data mislead the cost model into a catastrophic plan (the overnight 'nothing changed but it's 100× slower' incident). `EXPLAIN` is the window in; reading plans is the core skill of database tuning.

## See also

- [[SQL]]
- [[Index]]
- [[Join]]
- [[RDBMS]]

## Further reading

- [Wikipedia: Query optimization](https://en.wikipedia.org/wiki/Query_optimization)
