---
type: "reference"
tags: [reference]
---

# Conventions

The rules that keep this vault consistent and link-resolvable. Follow them when
you add notes and the graph stays clean.

## File naming

- One note per term, in `Terms/`, flat (no sub-folders). Flat + Maps + tags scales
  better than nested folders and lets a term belong to several branches at once.
- **The title is the canonical short form.** For acronyms that means the acronym
  (`TCP`, `ACID`, `RAII`), not the expansion. For everything else, the common name.

## Frontmatter

```yaml
---
branch: "Operating Systems"        # exactly one home branch (the MOC it lists under)
aliases: ["Spelled Out Form", "Synonym"]   # so links to any name resolve
de: "Betriebssystem"               # OPTIONAL — see German policy below
tags: [os, fundamental]            # branch tag first, then a few descriptive tags
---
```

## Note body shape

```
# Title

> **Branch:** [[NN - Branch Name|Branch Name]]
> **Also known as:** ...        (only if aliases exist)
> **German:** ...               (only if a de: term exists)

One- to four-sentence definition. Bold can expand an acronym inline: **T**ransmission…

**Context.** Why it matters, the gotcha, the nuance, where you meet it.

## See also
- [[Related Term]]

## Often confused with        (optional)
- [[Sibling]] — the one-line distinction.

## Further reading             (optional but expected for important terms)
- [Wikipedia: Title](https://en.wikipedia.org/wiki/Title)
```

## German policy

Add `de:` **only where a German word is actually used in German workplaces.**
Most IT jargon is borrowed wholesale — *Server, Firewall, Cache, Commit, Branch,
Deployment* are said in English even in an all-German team, so those get **no**
`de:` field. Genuine German terms that *are* used (and so are worth recording):
*Betriebssystem, Festplatte, Arbeitsspeicher, Verzeichnis, Datei, Datenbank,
Verschlüsselung, Schwachstelle/Sicherheitslücke, Treiber, Zwischenspeicher,
Datensicherung, Netzwerk, Rechteverwaltung.* When in doubt, leave it out.

## Tags

Keep them few and meaningful:

- **Branch tag** (always): `#foundations #hardware #os #net #web #data #pl #se
  #algo #theory #cloud #devops #ai #media #standards` (and the security branch's own).
- **Cross-cutting** (sparingly): `#fundamental` (load-bearing), `#modern` (post-~2015),
  `#anti-pattern` (a thing not to do), `#deprecated` (historical / on the way out).

## Generated metadata

Two fields are maintained mechanically (you don't hand-write them):

- `type: "term"` — marks the note as a term, so [[Term Dashboard]] and
  other Bases views can select it apart from maps and reference pages.
- `status:` — `developed` (has a Context paragraph **and** Further reading),
  `note` (has Context), or `stub` (neither). It's a coverage signal, not a
  quality judgement; grow `note`s into `developed` as links and sources accrue.

`type` sits first in the frontmatter and `status` last, wrapping the
hand-written fields. The base file `Term Dashboard.base` at the vault root
drives the dashboard views off these two fields.

## Sources

Prefer **Wikipedia** for durable concepts (stable URLs, good for a lifelong reference)
and **primary sources** for specs: RFCs (`datatracker.ietf.org`), NIST, ISO, the
language/standard's own site. Cite the long-lived terms (the top slice) at minimum;
cite more whenever the link adds something the note can't.
