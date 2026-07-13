# tools/ — the generator that bootstrapped this vault

This vault was **scaffolded** by these scripts. They are included so the structure
is reproducible and auditable, not because you need them day to day.

```
python build.py            # regenerates Terms/ and Maps/ from the dataset (archival — see warning)
python gen_term_index.py   # rebuilds the Term Index A–Z + count from Terms/ (safe, run anytime)
```

`gen_term_index.py` is the one you'll actually use: it reads `Terms/`, keeps only
`type: term` notes (the same rule `Term Dashboard.base` counts by), and rewrites the
A–Z block and headline count in `Term Index.md`. It touches nothing else, so it's
safe to run against the hand-edited vault — unlike `build.py`.

## ⚠ Read before running

`build.py` **overwrites** everything in `Terms/` and `Maps/` from the dataset
modules in `tools/dataset/`. The Markdown notes are the canonical artifact now —
the moment you hand-edit a note or add a new one in Obsidian, the generator no
longer knows about that change. **Do not re-run it over a vault you've edited.**

The generator's real job is already done. From here, grow the vault by hand:
copy `Templates/Term Template.md`, fill it in, wikilink generously. See
`How to Extend.md` at the vault root.

If you ever *do* want to batch-add a tranche of terms programmatically, add them
to a new `dataset/dNN_*.py` module (each exposes `TERMS = [...]`), then run the
build into a **throwaway output dir** and diff/merge the new notes in manually.

## June 2026 — hand-extended beyond the dataset

The vault was expanded by hand well past what `tools/dataset/` contains:
the 250-odd security notes each gained a Context paragraph and links, the
below-OS/architecture notes were folded into their home branches, ~85 new
terms were written (networking fundamentals, email authentication, PKI,
OS internals, and more), and the `Post-Mortem`/`Postmortem` duplicate was
merged. `type:`/`status:` frontmatter and `Term Dashboard.base` were added.
**The dataset modules no longer reflect the vault — treat the Markdown as
the sole source of truth.**
