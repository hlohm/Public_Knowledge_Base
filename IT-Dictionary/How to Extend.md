---
type: "reference"
tags: [reference]
---

# How to Extend

Three ways to grow the vault. **By hand is the default** — the Markdown is canonical.

## 1. By hand (the normal way)

1. Copy `Templates/Term Template.md` into `Terms/` and rename it to the term. The
   **filename is the canonical short form** — the acronym for acronyms (`TCP`, `RAII`),
   the common name for everything else.
2. Fill it in following [[Conventions]]. Frontmatter order wraps the hand-written
   fields between the two generated ones: `type` (first) → `branch` → `domain`
   (Security only) → `aliases` → `de` (only genuine German) → `tags` → `status` (last).
3. Point the branch line at the right Map. Most branches use
   `> **Branch:** [[NN - Branch Name|Branch Name]]`. The **Security** branch is
   subdivided, so its terms instead carry a `domain:` field and use
   `> **Domain:** [[NN - Domain Name|Domain Name]]` (Network Security, IAM,
   SecOps, …). When unsure, open a sibling term and copy its shape.
4. Add `[[wikilinks]]` to related terms. If a target doesn't exist yet, Obsidian
   shows it as a faded "ghost" node — that's a to-do, and a feature: your graph
   tells you what to write next.
5. Add the term to its branch/domain Map (`Maps/…`) under *Terms in this
   domain/branch*, in alphabetical order, with a one-line gloss — so it's
   discoverable by browsing, not only by search.
6. Refresh the index. Run `python tools/gen_term_index.py` to rebuild the A–Z and
   the headline count in [[Term Index]] from the notes, or add the link to the A–Z
   by hand. The **live** count always lives in `Term Dashboard.base` (it counts
   every `type: term` note); the Term Index A–Z is a browsable snapshot of it.

`status` is a coverage signal you keep in step with the note: `stub` (no Context),
`note` (has a Context paragraph), `developed` (Context **and** Further reading).
Promote as links and sources accrue.

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
vault it no longer knows about those changes — the dataset is now the record of the
initial seed, **not** a source of truth. Prefer method 1; the Markdown is canonical.

## 3. For an AI agent (Claude Code & friends)

This vault is often extended by an AI coding agent. If that's you, the rules that
keep the graph clean and the repo publishable:

- **Dedupe before you write.** This is a ~700-term vault; near-duplicates hide
  behind spelling (the merged `Post-Mortem` / `Postmortem` pair is the cautionary
  tale). Search `Terms/` and the target Map first, and prefer adding an **alias**
  to an existing note over creating a new one.
- **Match an existing sibling exactly.** One note per term, flat in `Terms/`,
  filename = canonical title. Copy the frontmatter order and body shape from a
  neighbouring term in the same branch/domain rather than from memory.
- **File it, don't orphan it.** Add the term to its branch/domain Map alphabetically
  with a one-line gloss, and add a reciprocal `See also` link from the obvious
  neighbours.
- **Public-repo hygiene — non-negotiable.** Every commit here is published. No real
  hostnames, IPs, usernames, tokens, or org-internal specifics — write generic,
  public-safe definitions even when the term came from a private runbook. English
  only, including examples and command comments. Cite Wikipedia for durable
  concepts and primary sources (RFC / NIST / the spec's own site) for standards.
- **Refresh, never clobber.** After a batch, run `python tools/gen_term_index.py` to
  sync [[Term Index]]. **Do not run `build.py`** over the live vault — it regenerates
  from the stale dataset and overwrites hand-written notes.
- **Small, honest commits.** A `stub` is a valid committed state; ghost links record
  the backlog. Don't fabricate a Further-reading link to bump `status` — leave it a
  `note`.

## The roadmap

[[Term Index]] carries a generated A–Z (see step 6) plus a curated, per-branch
backlog of high-value terms still worth writing. It's a checklist, not a contract —
reorder and extend it to match what you actually run into.
