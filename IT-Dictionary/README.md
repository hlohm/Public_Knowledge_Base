# IT Dictionary — Obsidian Vault

A working, densely-interlinked knowledge base for the language of information
technology — 16 branches, security being one of them. Grown from the
original IT-Security-Vocabulary vault.

## Opening this vault

1. Open **Obsidian**.
2. **Open folder as vault** → select the `IT-Dictionary` folder.
3. Open `_Home.md`.

## Layout

```
IT-Dictionary/
├── _Home.md                ← start here
├── README.md
├── Conventions.md          ← file format, frontmatter, tag + German policy
├── How to Extend.md        ← add terms by hand, or re-run the generator
├── Concept Map.md          ← visual overview
├── Often Confused Pairs.md ← false-friends across all of IT
├── Term Index.md           ← full A–Z + coverage roadmap
├── Maps/                   ← one MOC per branch
│   ├── 01 - Computing Foundations.md ... 16 - Security.md
│   └── Security/           ← the 13 security sub-domain MOCs (preserved)
├── Terms/                  ← one note per term (flat)
└── Templates/
    └── Term Template.md
```

## Conventions (summary — full version in `Conventions.md`)

- **Acronyms are titles**; the expansion lives in `aliases:`.
- Note shape: definition → **Context** → *See also* → *Often confused with* → *Further reading*.
- `de:` frontmatter = German term, present only where a German word is genuinely used in practice.
- `Further reading` cites **Wikipedia** (canonical-title URLs) for the load-bearing,
  long-lived terms, plus primary sources (RFCs, NIST, standards bodies) where they exist.
- Tags are light: a branch tag (`#os`, `#net`, …) plus the odd `#fundamental` / `#modern` / `#anti-pattern`.

## Regenerating

This vault was bootstrapped by `tools/build.py` from `tools/dataset/`. The
**markdown is now canonical** — edit it directly. The generator is included only
for transparency and bulk operations; re-running it overwrites `Terms/` and `Maps/`,
so don't run it after you've started hand-editing unless you know what you're doing.
