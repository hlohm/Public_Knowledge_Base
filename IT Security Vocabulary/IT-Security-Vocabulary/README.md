# IT Security Vocabulary — Obsidian Vault

A working knowledge base for the language of information security: ~270 notes covering the core vocabulary of the field, wired together with Obsidian wikilinks and grouped by domain.

## Opening this vault

1. Open **Obsidian**.
2. Click **Open folder as vault**.
3. Select the `IT-Security-Vocabulary` folder you extracted.
4. Open `_Home.md` — that's the entry point.

## Structure

```
IT-Security-Vocabulary/
├── _Home.md                  ← start here
├── README.md
├── Concept Map.md            ← visual overview
├── Study Path.md             ← suggested learning order
├── Often Confused Pairs.md   ← false-friends table
├── Domains/                  ← one MOC (Map of Content) per domain
│   ├── 01 - Core Principles.md
│   ├── 02 - Risk and Governance.md
│   └── ... (13 domains)
├── Terms/                    ← one note per term
│   └── ... (~180 terms)
└── Templates/
    └── Term Template.md      ← copy this when adding a new term
```

## Conventions

- **Acronyms** are the note titles (e.g. `MFA`, not the spelled-out form). The expansion lives in the `aliases` frontmatter so a wikilink to either form resolves correctly.
- Each term note has the shape: definition → context → see-also → confused-with → further reading.
- Tags are sparingly used: `#fundamental` for foundational terms, `#modern` for post-2015 concepts, `#anti-pattern` for things-not-to-do, etc.
