---
type: reference
tags: [reference]
status: stable
---

# Conventions

The rules that keep this vault consistent, scannable, and safe to publish.

## File naming & placement

- One note per tool or topic, in the folder for its **type**: `Cheatsheets/`, `Runbooks/`,
  `Playbooks/`, `Snippets/`.
- **The title is the canonical invocation** — what you actually type or call: `git`, `ssh`,
  `docker`, `systemd`, `nvim`. Not "Git Cheat Sheet". Alternate names, expansions, and
  closely-bound tools go in `aliases:` (e.g. `docker` aliases `docker-compose`, `compose`).
- Runbooks/playbooks are named by the task or symptom: `Backup Restore Drill`,
  `Service Down — Triage & Recovery`.

## Frontmatter

```yaml
---
type: cheatsheet          # cheatsheet | runbook | playbook | snippet | map | reference | home
area: "CLI Tools"         # exactly one home area (the Map it lists under)
aliases: ["docker-compose", "compose"]
tags: [containers]        # a few; the area is implied by `area:`, so tags are extra signal
status: stable            # stub | draft | working | stable
---
```

`type:` sits first and `status:` last, wrapping the hand-written fields — same discipline as
the IT-Dictionary, so a Bases view can select notes by type and status later.

**`status:` meaning** — a coverage signal, not a quality grade:

- `stub` — skeleton + scope line only; a placeholder you can already link to.
- `draft` — partial; usable but visibly incomplete.
- `working` — covers the everyday 80%; gaps are known and fine.
- `stable` — complete for daily use and its commands have been run/verified.

## Note body shapes

Every note opens the same way:

```
# <title>

> **Area:** [[Area Map]]

One-line scope: what this covers and what it deliberately doesn't.
(Optional) > version/platform note as a blockquote.
```

Then, by type:

- **Cheatsheet** — numbered `##` sections of **annotated** fenced command blocks (the comment
  says *why*, not just *what*), then a **Daily workflows** section (scenario → the exact
  commands), a **Files & locations** table where relevant, and a **Gotchas / Golden rules**
  closer. The annotated, sectioned style of the seeded sheets *is* the house format — copy it.
- **Runbook** — **When to use** (trigger) → **Prerequisites** → numbered **Steps**, each with a
  verification → **Rollback** → **Done when**.
- **Playbook** — **Symptom** → **Quick triage** (the first 3 commands) → **Decision branches**
  (if X then Y) → **Fixes** → **Escalation / after-action**.
- **Snippet** — **What & why** → the code block → **Customize** (the knobs) → **Use**.

## English & safety policy

- **English only**, including command comments. (Some sheets were translated in from German.)
- **This repository is public.** No real hostnames, usernames, internal IPs, domains, tokens,
  keys, or passphrases — ever. Use placeholders:
  `<user>`, `<host>`, `you@example.com`, `example.com`, `/path/to/repo`, `<REPO>`, `10.0.0.0/8`.
- No work-internal or NDA material, no personal daily-notes plumbing (no `## Trail`,
  "Touched today", PARA `Purpose:` blocks). Those belong in private notes, not here.
- Treat every commit as a publication — public git history is permanent.

## Sources & verification

- Prefer the tool's **own man page / official docs** as the canonical reference; cite a stable
  URL under *Further reading* for the load-bearing notes.
- A command in a `stable` note should have been **run at least once** as written. If you're
  unsure, mark the note `working` and flag the uncertain command.

## Linking

- Link freely **within** this vault; every internal `[[link]]` resolves and keeps the graph alive.
- A link **into the IT-Dictionary** dangles in this focused vault (separate vault) and only
  resolves in the unified parent vault. So name dictionary concepts in prose rather than
  hard-linking them, unless you're deliberately working in the parent "everything" vault.
- Ghost links (to notes not yet written) are the **backlog** — leave them in Maps as
  invitations. [[Index]] tracks them.
