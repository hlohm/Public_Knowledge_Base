---
type: reference
tags: [reference]
status: stable
---

# How to Extend

## Add a note

1. Pick the **type** and copy the matching template from `Templates/` into the right folder:
   - reference for a tool/topic → `Cheatsheets/` ([[Cheatsheet Template]])
   - a procedure you run repeatedly → `Runbooks/` ([[Runbook Template]])
   - a "what do I do when X breaks" guide → `Playbooks/` ([[Playbook Template]])
   - reusable boilerplate → `Snippets/` ([[Snippet Template]])
2. Rename it to the canonical invocation (`zsh`, not "Zsh Cheat Sheet") and fill in the
   frontmatter — set `area:` to its home Map and `status:` honestly (`stub` is fine to start).
3. Write it following [[Conventions]]. Annotate every command with *why*. Keep it English,
   generic, secret-free.
4. **Add it to its area Map** under *In this area*, and remove the ghost link if it had one.
5. Add `[[wikilinks]]` to related notes — a faded target is a future note, and a feature:
   your graph shows you what to write next.

## Capture-first

When you solve something fiddly — a flag you always forget, a recovery you just performed,
a script header you keep re-typing — capture it **now**, even as a `stub`. The backlog in
[[Index]] is a place to park the name so it isn't lost; promote it to a real note later.

## Grow a big topic instead of bloating one note

"Linux administration" or "Python" is not one cheatsheet — it's an **area**. Model it as a
Map that lists several focused notes (e.g. *users & permissions*, *packages*, *networking*,
*storage* under Linux Administration), not a single 2,000-line page. Split when a section
outgrows its sheet; the Map holds the cluster together.

## Promote status as it matures

`stub` → `draft` → `working` → `stable`. A note is `stable` once it covers the everyday
cases and its commands have actually been run as written. Don't claim `stable` on commands
you haven't executed.
