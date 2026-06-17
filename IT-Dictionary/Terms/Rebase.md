---
type: "term"
branch: "Software Engineering"
tags: [se]
status: "developed"
---

# Rebase

> **Branch:** [[08 - Software Engineering|Software Engineering]]

Reapplying a branch's commits onto a new base commit, producing a linear history as if you'd branched from the new point.

**Context.** Cleaner history than merge, but it *rewrites* commits (new hashes) — hence the golden rule: never rebase commits you've already pushed and shared. Interactive rebase is also the tool for tidying local history (squash, reorder, reword) before review.

## See also

- [[Merge]]
- [[Commit]]
- [[Git]]
- [[Interactive Rebase]]
- [[Force Push]]

## Further reading

- [Wikipedia: Rebasing (version control)](https://en.wikipedia.org/wiki/Rebasing_(version_control))
