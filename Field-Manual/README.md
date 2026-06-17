# Field Manual — Obsidian Vault

A hands-on operations & development reference: cheat-sheets, runbooks, playbooks, and
reusable boilerplate for the everyday command line, systems administration, and coding.
The practical counterpart to the conceptual **IT-Dictionary** vault that sits beside it
in this repository.

## Opening this vault

1. Open **Obsidian**.
2. **Open folder as vault** → select the `Field-Manual` folder (not the repo root).
3. Open `_Home.md`.

## Layout

```
Field-Manual/
├── _Home.md                ← start here
├── README.md
├── Conventions.md          ← frontmatter, note shapes, placeholder + English policy
├── How to Extend.md        ← how to add a sheet / runbook / playbook / snippet
├── Index.md                ← full list + the backlog roadmap
├── Maps/                   ← one Map of Content per area
├── Cheatsheets/            ← command & keybind references (one tool/topic each)
├── Runbooks/               ← step-by-step procedures for recurring tasks
├── Playbooks/              ← symptom → triage → fix decision guides
├── Snippets/               ← drop-in boilerplate (scripts, unit files, configs)
└── Templates/              ← one template per note type
```

## Note types

| Type | Answers | Shape |
| --- | --- | --- |
| **cheatsheet** | "which command/flag?" | Numbered sections of annotated command blocks, daily workflows, a locations table, gotchas |
| **runbook** | "walk me through X" | Trigger → prerequisites → numbered steps (each verified) → rollback → done-criteria |
| **playbook** | "it's broken — what first?" | Symptom → quick triage → decision branches → fixes → escalation |
| **snippet** | "give me the skeleton" | What/why → the code block → customization points → usage |

## Conventions (summary — full version in `Conventions.md`)

- **Title = the tool/topic as you actually invoke it** (`git`, `ssh`, `docker`); spelled-out
  or alternate forms go in `aliases:`.
- Every note carries `type:`, a single home `area:`, `tags:`, and a `status:`.
- **English only.** **No real hostnames, usernames, IPs, or secrets** — use placeholders
  (`<user>`, `<host>`, `you@example.com`, `/path/to/...`). This repo is public.
- Annotate commands inline (`# why`, not just what) — these notes are read under pressure.

## Relationship to the IT-Dictionary

The dictionary is *explanation* (what/why); this is *how-to* + *reference* (how/which).
They are deliberately separate Obsidian vaults: each keeps a clean, single-purpose graph,
and either can be cloned and used on its own. A link from here into the dictionary will
only resolve in the unified parent ("everything") vault, so cross-reference concepts by
name rather than relying on a wikilink.
