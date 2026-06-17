---
type: "reference"
tags: [reference]
---

# How to Extend

Two ways to grow the vault. **By hand is the default** — the markdown is canonical.

## 1. By hand (the normal way)

1. Copy `Templates/Term Template.md` into `Terms/` and rename it to the term.
2. Fill it in following [[Conventions]].
3. Add `[[wikilinks]]` to related terms. If a target doesn't exist yet, Obsidian
   shows it as a faded "ghost" node — that's a to-do, and a feature: your graph
   tells you what to write next.
4. Add the term to its branch Map (`Maps/NN - …`) under *Terms in this branch* so
   it's discoverable by browsing, not only by search.

When you meet a term in the wild — a SOC ticket, an RFC, a Hacker News thread —
capture it even as a one-line stub. Future you will thank you.

## 2. Regenerate from the dataset (bulk only)

The vault was bootstrapped by `tools/build.py` from the structured data in
`tools/dataset/d*.py`. Each entry is a dict:

```python
{
  "term": "Dereference",
  "branch": "Programming Languages",
  "aliases": ["Indirection"],
  "de": None,
  "tags": ["memory"],
  "flags": ["fundamental"],
  "def": "Following a pointer to read the value it points at.",
  "context": "The crash you get from dereferencing a null/dangling pointer is the "
             "single most common memory bug in C-family languages.",
  "see_also": ["Pointer", "Null Pointer", "Memory Safety"],
  "confused": [("Pointer", "A pointer holds the address; dereferencing uses it.")],
  "wikipedia": "Dereference operator",   # canonical Wikipedia title, or omit
}
```

Run `python tools/build.py`. It rewrites `Terms/` + `Maps/` and prints a link-check
report. **Warning:** it overwrites generated files, so once you've hand-edited the
vault, prefer method 1. The dataset is best thought of as the record of the initial
seed, not a long-term source of truth.

## The roadmap

[[Term Index]] lists what's written and a curated backlog of high-value terms still
to add, grouped by branch. It's a checklist, not a contract — reorder and extend it
to match what you actually run into.
