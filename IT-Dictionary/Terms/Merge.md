---
type: "term"
branch: "Software Engineering"
tags: [se]
status: "developed"
---

# Merge

> **Branch:** [[08 - Software Engineering|Software Engineering]]

Combining divergent branches, reconciling their changes — automatically where they don't overlap, with a **merge conflict** to resolve where they do.

**Context.** A merge commit preserves the true branching history (two parents); the alternative, rebasing, rewrites for a linear history. Conflicts are inevitable on shared code; merging often and keeping branches short is how you keep them small.

## See also

- [[Branch]]
- [[Rebase]]
- [[Merge Conflict]]
- [[Three-way Merge]]

## Often confused with

- [[Rebase]] — Merge preserves history with a merge commit (true but messy); rebase replays your commits onto a new base for a clean linear history (tidy but rewrites).

## Further reading

- [Wikipedia: Merge (version control)](https://en.wikipedia.org/wiki/Merge_(version_control))
