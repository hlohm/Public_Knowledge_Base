# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal public knowledge base, organized as a collection of independent Obsidian vaults. Each vault lives in its own top-level folder (`IT-Dictionary/`, `Field-Manual/`, and any future siblings). The repo root is not itself a vault — it holds only the index `README.md`, shared `.gitignore`, and the subject folders.

There are no build tools, no tests, no CI. "Working" means: correct Markdown, valid frontmatter, consistent conventions, no secrets, and internal wikilinks that resolve within their vault.

## Repository layout

```
Public_Knowledge_Base/
├── README.md                  ← repo index
├── knowledge-base-architecture.md  ← sync/privacy architecture decisions
├── IT-Dictionary/             ← ~690-term vocabulary vault
│   ├── Terms/                 ← one note per term, flat
│   ├── Maps/                  ← Maps of Content grouped by branch
│   ├── Templates/
│   ├── Conventions.md
│   ├── How to Extend.md
│   └── tools/                 ← Python generator that bootstrapped the vault (archival)
└── Field-Manual/              ← hands-on ops & dev reference
    ├── Cheatsheets/
    ├── Runbooks/
    ├── Playbooks/
    ├── Snippets/
    ├── Maps/
    ├── Templates/
    ├── Conventions.md
    └── How to Extend.md
```

## Note conventions

### IT-Dictionary

Frontmatter (in order): `branch`, `aliases`, `de` (optional), `tags`, then machine-maintained `type` (first) and `status` (last).

Body shape:
```
# Title
> **Branch:** [[NN - Branch Name|Branch Name]]
One-to-four sentence definition.
**Context.** Why it matters, where it appears in practice.
## See also
## Often confused with   (optional)
## Further reading       (optional)
```

`status` is auto-maintained: `developed` = has Context + Further reading, `note` = has Context, `stub` = neither. Do not hand-write it.

### Field-Manual

Frontmatter (in order): `type`, `area`, `aliases`, `tags`, `status`.

Note types and their folder:
- `cheatsheet` → `Cheatsheets/` — filename is the canonical invocation (`git`, `ssh`, not "Git Cheat Sheet")
- `runbook` → `Runbooks/` — named by the task
- `playbook` → `Playbooks/` — named by the symptom
- `snippet` → `Snippets/`

`status` progression: `stub` → `draft` → `working` → `stable`. A note is `stable` only when its commands have actually been run as written.

Cheatsheet body: numbered `##` sections of **annotated** command blocks (comment = *why*, not *what*), then **Daily workflows**, **Files & locations** (where relevant), **Gotchas / Golden rules**.

Runbook body: **When to use** → **Prerequisites** → numbered **Steps** each with a `*Verify:*` line → **Rollback** → **Done when**.

## Cross-vault linking

Wikilinks resolve only within the open vault. A link from Field-Manual into IT-Dictionary — or between any two subjects — dangles in a focused vault and only resolves in the unified parent vault. Prefer naming concepts in prose rather than hard-linking across vaults.

## Privacy and safety rules (non-negotiable)

- **No real hostnames, usernames, IPs, domains, tokens, keys, or passphrases.** Use placeholders: `<user>`, `<host>`, `you@example.com`, `example.com`, `10.0.0.0/8`, `/path/to/repo`.
- **English only**, including command comments.
- No work-internal or NDA material. No personal daily-notes structure.
- Every commit is a publication — public git history is permanent.

## When adding content

- Copy the matching template from `Templates/` first.
- Add every new note to its area/branch Map under *In this area* / *Terms in this branch*.
- Ghost links (to notes not yet written) in Maps are intentional — they are the backlog.
- A `stub` is a valid committed state; promote `status` as coverage grows.

## The IT-Dictionary generator (`tools/`)

`tools/build.py` can regenerate `Terms/` and `Maps/` from the structured dataset in `tools/dataset/d*.py`. The markdown notes are canonical now — the generator overwrites generated files, so it is archival rather than a live build step. Only use it for bulk operations. Prefer hand-editing individual notes.
