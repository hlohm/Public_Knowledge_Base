#!/usr/bin/env python3
"""
Build the IT Dictionary Obsidian vault.

Pipeline:
  1. Migrate the legacy IT-Security-Vocabulary terms + domain MOCs into the new
     vault (Security becomes one branch among many).
  2. Generate new term notes from the structured dataset (dataset/d*.py).
  3. Auto-generate the branch Maps (MOCs), Home, README, Conventions,
     How-to-Extend, Concept Map, Often-Confused-Pairs and the Term Index roadmap.
  4. Validate every [[wikilink]] and report unresolved targets.

The markdown vault is the canonical, hand-editable artifact. This generator only
bootstraps it; after this you add terms by copying Templates/Term Template.md.
"""

import importlib.util
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEGACY = ROOT / "legacy"
OUT = ROOT / "out" / "IT-Dictionary"
DATASET_DIR = ROOT / "dataset"

WIKI = "https://en.wikipedia.org/wiki/"

# ---------------------------------------------------------------------------
# Branch definitions (non-security). Order = number in the Maps/ filenames.
# Each: key -> (display name, short branch tag, one-line scope blurb for the MOC)
# ---------------------------------------------------------------------------
BRANCHES = [
    ("Computing Foundations", "foundations",
     "The bedrock concepts every other branch leans on: bits, encodings, abstraction, the von Neumann model."),
    ("Hardware & Architecture", "hardware",
     "What the machine is physically made of and how the CPU actually executes — registers, caches, buses, ISAs."),
    ("Operating Systems", "os",
     "The layer that turns hardware into something programs can share safely: processes, memory, files, the kernel."),
    ("Networking", "net",
     "Moving bytes between machines reliably and in order — the stack from cables to sockets. (You live here; entries stay terse.)"),
    ("Internet & Web", "web",
     "The application-layer world built on the network: HTTP, DNS, browsers, the request/response lifecycle."),
    ("Data & Databases", "data",
     "Persisting, querying and modelling information — relational, NoSQL, transactions, consistency."),
    ("Programming Languages", "pl",
     "How we tell machines what to do, and the ideas that distinguish languages: types, paradigms, memory models."),
    ("Software Engineering", "se",
     "Building software with other humans over time: version control, testing, architecture, process."),
    ("Algorithms & Data Structures", "algo",
     "The reusable shapes of computation and the structures that make them fast."),
    ("Theory of Computation", "theory",
     "What is computable, how hard problems are, and the formal machines behind it all."),
    ("Cloud & Infrastructure", "cloud",
     "Renting and orchestrating other people's computers — virtualization, containers, IaC, the service models."),
    ("DevOps & SRE", "devops",
     "Shipping and operating software continuously and reliably — pipelines, observability, error budgets."),
    ("AI & Machine Learning", "ai",
     "Systems that learn from data: models, training, the vocabulary of the current wave."),
    ("Graphics, Media & HCI", "media",
     "Pixels, codecs, colour, and how humans interact with all of it."),
    ("Standards, Formats & Bodies", "standards",
     "The organisations and specifications that keep the field interoperable — IETF, IEEE, ISO, Unicode, W3C."),
]
BRANCH_NAMES = [b[0] for b in BRANCHES]
BRANCH_TAG = {b[0]: b[1] for b in BRANCHES}
BRANCH_BLURB = {b[0]: b[2] for b in BRANCHES}
SECURITY = "Security"

# Map a branch name -> its Map MOC note basename (for the > Branch: link)
def branch_map_basename(branch):
    if branch == SECURITY:
        return "Security"
    idx = BRANCH_NAMES.index(branch) + 1
    return f"{idx:02d} - {branch}"

# ---------------------------------------------------------------------------
# Load dataset modules
# ---------------------------------------------------------------------------
def load_dataset():
    terms = []
    seen = {}
    for path in sorted(DATASET_DIR.glob("d*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for t in getattr(mod, "TERMS", []):
            name = t["term"]
            if name in seen:
                print(f"  ! duplicate term '{name}' in {path.name} "
                      f"(also in {seen[name]}) — skipping dup")
                continue
            seen[name] = path.name
            terms.append(t)
    return terms

# ---------------------------------------------------------------------------
# Rendering a new term note
# ---------------------------------------------------------------------------
def yaml_list(items):
    return "[" + ", ".join(f'"{i}"' for i in items) + "]"

# Characters illegal in note filenames on common filesystems (esp. Windows).
# A term like "CI/CD" or "TCP/IP" keeps its slash in the displayed title but
# gets a safe basename for the file, so the flat Terms/ folder never sprouts
# accidental subfolders and links still resolve.
_ILLEGAL = '\\/:*?"<>|'

def safe_base(name):
    out = name
    for ch in _ILLEGAL:
        out = out.replace(ch, "-")
    return out

def wl(target):
    """Emit a wikilink whose file target is filesystem-safe, preserving the
    human-readable form as the display label when they differ."""
    base = safe_base(target)
    return f"[[{base}]]" if base == target else f"[[{base}|{target}]]"

def render_term(t):
    branch = t["branch"]
    aliases = t.get("aliases", [])
    de = t.get("de")
    tags = []
    if branch in BRANCH_TAG:
        tags.append(BRANCH_TAG[branch])
    tags += t.get("tags", [])
    tags += t.get("flags", [])
    # dedupe, keep order
    seen = set(); tags = [x for x in tags if not (x in seen or seen.add(x))]

    fm = ["---", f'branch: "{branch}"']
    if aliases:
        fm.append(f"aliases: {yaml_list(aliases)}")
    if de:
        fm.append(f'de: "{de}"')
    fm.append(f"tags: [{', '.join(tags)}]")
    fm.append("---")

    map_base = branch_map_basename(branch)
    header = [f"\n# {t['term']}\n",
              f"> **Branch:** [[{map_base}|{branch}]]"]
    if aliases:
        header.append(f"> **Also known as:** {', '.join(aliases)}")
    if de:
        header.append(f"> **German:** {de}")

    body = ["", t["def"]]
    if t.get("context"):
        body += ["", f"**Context.** {t['context']}"]

    sa = t.get("see_also", [])
    if sa:
        body += ["", "## See also", ""]
        body += [f"- {wl(x)}" for x in sa]

    conf = t.get("confused", [])
    if conf:
        body += ["", "## Often confused with", ""]
        for pair in conf:
            target, note = pair
            body.append(f"- {wl(target)} — {note}")

    fr = []
    if t.get("wikipedia"):
        slug = t["wikipedia"].replace(" ", "_")
        label = t["wikipedia"]
        fr.append(f"- [Wikipedia: {label}]({WIKI}{slug})")
    for extra in t.get("links", []):
        fr.append(f"- {extra}")
    if fr:
        body += ["", "## Further reading", ""] + fr

    return "\n".join(fm + header + body) + "\n"

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def migrate_legacy():
    """Copy legacy security terms (add branch frontmatter) and domain MOCs."""
    count = 0
    for f in sorted((LEGACY / "Terms").glob("*.md")):
        text = f.read_text(encoding="utf-8")
        # inject branch into frontmatter (after opening ---)
        if text.startswith("---"):
            text = text.replace("---\n", '---\nbranch: "Security"\n', 1)
        write(OUT / "Terms" / f.name, text)
        count += 1
    # domain MOCs -> Maps/Security/
    for f in sorted((LEGACY / "Domains").glob("*.md")):
        text = f.read_text(encoding="utf-8")
        write(OUT / "Maps" / "Security" / f.name, text)
    # carry over the security-specific learning + reference helpers
    for name, dest in [("Study Path.md", OUT / "Maps" / "Security" / "Study Path.md")]:
        src = LEGACY / name
        if src.exists():
            write(dest, src.read_text(encoding="utf-8"))
    return count

def build_term_notes(terms):
    for t in terms:
        write(OUT / "Terms" / f"{safe_base(t['term'])}.md", render_term(t))

def build_branch_maps(terms):
    by_branch = defaultdict(list)
    for t in terms:
        by_branch[t["branch"]].append(t)
    for i, branch in enumerate(BRANCH_NAMES, start=1):
        items = sorted(by_branch.get(branch, []), key=lambda x: x["term"].lower())
        lines = ["---", 'type: "map"', f"tags: [map, {BRANCH_TAG[branch]}]", "---", "",
                 f"# {branch}", "", f"> {BRANCH_BLURB[branch]}", ""]
        if items:
            lines += [f"## Terms in this branch ({len(items)})", ""]
            for t in items:
                short = t.get("short") or first_sentence(t["def"])
                lines.append(f"- {wl(t['term'])} — {short}")
        else:
            lines += ["*No terms yet — copy `Templates/Term Template.md` to add the first.*"]
        lines += ["", "---", "← Back to [[_Home]]"]
        write(OUT / "Maps" / f"{i:02d} - {branch}.md", "\n".join(lines) + "\n")

def first_sentence(text):
    # strip bold markers used for acronym expansion, take first sentence
    plain = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    m = re.split(r"(?<=[.!?])\s", plain.strip())
    s = m[0] if m else plain
    return s.strip()

def build_security_overview():
    domains = sorted((OUT / "Maps" / "Security").glob("*.md"))
    rows = []
    for d in domains:
        base = d.stem
        if base == "Study Path":
            continue
        rows.append(f"- [[{base}]]")
    lines = ["---", 'type: "map"', "tags: [map, security]", "---", "",
             "# Security", "",
             "> The original IT-Security-Vocabulary, preserved intact as one branch of the "
             "dictionary. It keeps its own 13-domain substructure because the security field "
             "really is that internally organised. Entries here stay deliberately terse — this "
             "is the branch you already live and breathe.", "",
             "## Security domains", ""] + rows + [
             "", "## Security helpers", "",
             "- [[Study Path]] — suggested order if learning security from scratch",
             "", "---", "← Back to [[_Home]]"]
    write(OUT / "Maps" / "16 - Security.md", "\n".join(lines) + "\n")

def build_home():
    branch_links = []
    for i, branch in enumerate(BRANCH_NAMES, start=1):
        branch_links.append(f"  - [[{i:02d} - {branch}|{branch}]]")
    branch_links.append("  - [[16 - Security|Security]] — the original vocabulary, intact")
    lines = ["---", 'type: "home"', "---", "",
             "# IT Dictionary — Home", "",
             "A densely-interlinked, learning-oriented dictionary for the whole language of "
             "information technology. Security is one branch among many. Built to be an "
             "everyday companion you grow for the rest of your career.", "",
             "## Branches", "",
             "Read a branch Map top-to-bottom, or just follow your nose through the links.",
             ""] + branch_links + [
             "", "## Cross-cutting maps", "",
             "- 🗺️ [[Concept Map]] — how the branches relate",
             "- ⚠️ [[Often Confused Pairs]] — the false friends, across all of IT",
             "- 📇 [[Term Index]] — full A–Z + the roadmap toward fuller coverage",
             "", "## How this vault works", "",
             "Every term lives in its own note under `Terms/`. Notes link to related concepts "
             "with `[[wikilinks]]`; open any note and check the **Backlinks** pane to see what "
             "points back. **Graph View** (Ctrl/Cmd-G) is the truest picture of the field.", "",
             "Acronyms are the note titles (`TLS`, `RAII`); the spelled-out form lives in "
             "`aliases:` so a link to either resolves. A `de:` field carries the German term "
             "**only where Germans actually use a German word** — most IT jargon stays English "
             "even in German shops, so the field is often absent by design.", "",
             "## Adding to it", "",
             "See [[How to Extend]]. Short version: copy `Templates/Term Template.md` into "
             "`Terms/`, fill it in, wikilink generously. Backlinks happen automatically.", "",
             "See also [[README]] and [[Conventions]].", ""]
    write(OUT / "_Home.md", "\n".join(lines) + "\n")

def build_static(terms):
    # README
    nbranch = len(BRANCH_NAMES) + 1
    readme = f"""# IT Dictionary — Obsidian Vault

A working, densely-interlinked knowledge base for the language of information
technology — {nbranch} branches, security being one of them. Grown from the
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
"""
    write(OUT / "README.md", readme)

    # Conventions
    conventions = """---
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

## Sources

Prefer **Wikipedia** for durable concepts (stable URLs, good for a lifelong reference)
and **primary sources** for specs: RFCs (`datatracker.ietf.org`), NIST, ISO, the
language/standard's own site. Cite the long-lived terms (the top slice) at minimum;
cite more whenever the link adds something the note can't.
"""
    write(OUT / "Conventions.md", conventions)

    # How to Extend
    extend = """---
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
"""
    write(OUT / "How to Extend.md", extend)

    # Template
    template = """---
branch: ""
aliases: []
de: ""
tags: []
---

# Term Name

> **Branch:** [[NN - Branch Name|Branch Name]]
> **Also known as:**
> **German:**

One- to four-sentence definition.

**Context.** Why it matters / the gotcha / where you meet it.

## See also

- [[Related Term]]

## Often confused with

- [[Other Term]] — short note on the distinction.

## Further reading

- [Wikipedia: Title](https://en.wikipedia.org/wiki/Title)
"""
    write(OUT / "Templates" / "Term Template.md", template)

    # Concept Map
    cmap = """---
type: "reference"
tags: [reference]
---

# Concept Map

A rough mental model of how the branches stack and feed each other. Read bottom-up.

```
                ┌───────────────────────────────────────────────┐
   people  →    │  Software Engineering · DevOps & SRE · HCI     │
                ├───────────────────────────────────────────────┤
   build   →    │  Programming Languages · Algorithms · AI/ML    │
                ├───────────────────────────────────────────────┤
   run     →    │  Operating Systems · Cloud & Infrastructure    │
                ├───────────────────────────────────────────────┤
   talk    →    │  Internet & Web · Networking · Data & DBs      │
                ├───────────────────────────────────────────────┤
   compute →    │  Hardware & Architecture · Theory of Comp.     │
                ├───────────────────────────────────────────────┤
   ground  →    │  Computing Foundations (bits, encodings…)      │
                └───────────────────────────────────────────────┘

   woven through every layer:  Security · Cryptography · Standards & Bodies
```

- **[[01 - Computing Foundations|Foundations]]** underlies everything — bits, bytes,
  encodings, abstraction.
- **[[02 - Hardware & Architecture|Hardware]]** and **[[10 - Theory of Computation|Theory]]**
  bound what's physically and mathematically possible.
- **[[03 - Operating Systems|OS]]** and **[[11 - Cloud & Infrastructure|Cloud]]** turn raw
  machines into something programs can share.
- **[[04 - Networking|Networking]]**, **[[05 - Internet & Web|Web]]**, and
  **[[06 - Data & Databases|Data]]** are how systems talk and remember.
- **[[07 - Programming Languages|Languages]]**, **[[09 - Algorithms & Data Structures|Algorithms]]**
  and **[[13 - AI & Machine Learning|AI/ML]]** are how we express computation.
- **[[08 - Software Engineering|Engineering]]**, **[[12 - DevOps & SRE|DevOps]]** and
  **[[14 - Graphics, Media & HCI|HCI]]** are how humans build and meet it.
- **[[16 - Security|Security]]**, cryptography and **[[15 - Standards, Formats & Bodies|Standards]]**
  cut across all of it.

Open **Graph View** and colour by the branch tags to watch these clusters form.

---
← Back to [[_Home]]
"""
    write(OUT / "Concept Map.md", cmap)

    # Often Confused Pairs — seed with cross-IT pairs, then append legacy security pairs.
    confused_general = """---
type: "reference"
tags: [reference]
---

# Often Confused Pairs

False friends across all of IT — close enough to swap, distinct enough to matter.
(The security-specific pairs from the original vault are at the bottom.)

| Pair | The distinction |
|---|---|
| [[Compiler]] vs [[Interpreter]] | Compiler translates the whole program ahead of time to another form; interpreter executes it statement-by-statement. Many runtimes (JVM, V8) do both via [[JIT Compilation\\|JIT]]. |
| [[Process]] vs [[Thread]] | A process owns an address space; threads share one process's address space. Crash isolation vs cheap sharing. |
| [[Concurrency]] vs [[Parallelism]] | Concurrency = dealing with many things at once (structure); parallelism = doing many things at once (execution). You can have one without the other. |
| [[Stack]] vs [[Heap]] | Stack = automatic, LIFO, function-scoped, fast; heap = manually/GC-managed, long-lived, flexible. Two different *memory regions* and two different *data structures* — don't conflate the senses. |
| [[Latency]] vs [[Bandwidth]] vs [[Throughput]] | Latency = time for one trip; bandwidth = capacity of the pipe; throughput = what you actually achieve. A fat pipe with high latency still feels slow. |
| [[TCP]] vs [[UDP]] | TCP = ordered, reliable, connection-oriented, slower to start; UDP = fire-and-forget, no guarantees, lower overhead. |
| [[Authentication]] vs [[Authorization]] | AuthN = "who are you?"; AuthZ = "what may you do?". AuthN first. |
| [[Encryption]] vs [[Encoding]] vs [[Hashing]] | Encryption is reversible *with a key*; encoding (Base64) is reversible *without* one (not security); hashing is one-way. |
| [[Mutable]] vs [[Immutable]] | Can the value change in place after creation, or not? Immutability buys safety in concurrency and reasoning, at a copying cost. |
| [[Statically Typed]] vs [[Dynamically Typed]] | When are type errors caught — compile time or run time? Orthogonal to *strong* vs *weak*. |
| [[Strongly Typed]] vs [[Weakly Typed]] | How much implicit coercion the language allows. A language can be dynamically *and* strongly typed (Python). |
| [[GET]] vs [[POST]] | GET = safe, idempotent, cacheable retrieval; POST = state-changing submission. Mixing them up breaks caches and audits. |
| [[Idempotent]] vs [[Safe (HTTP)\\|Safe]] | Safe = no side effects at all; idempotent = same effect whether called once or many times. PUT/DELETE are idempotent but not safe. |
| [[Null]] vs [[Undefined]] vs [[NaN]] | "Intentionally empty" vs "never assigned" vs "not a number". JavaScript exposes all three and they bite. |
| [[Library]] vs [[Framework]] | You call a library; a framework calls you (inversion of control). |
| [[API]] vs [[ABI]] | API = source-level contract (function names, types); ABI = binary-level contract (calling convention, layout). Recompile fixes API breaks; ABI breaks need relinking. |
| [[Bit]] vs [[Byte]] | 1 byte = 8 bits. Network speeds quote bits (Mb/s), file sizes quote bytes (MB) — a factor-of-8 trap. |
| [[Cache]] vs [[Buffer]] | Cache = keep likely-reused data close (speed); buffer = smooth a rate/size mismatch between producer and consumer. |
| [[Race Condition]] vs [[Deadlock]] | Race = outcome depends on timing of unsynchronised access; deadlock = two parties each waiting on the other forever. |
| [[Big-O Notation\\|Big-O]] vs actual speed | Big-O is asymptotic growth, not wall-clock time. An O(n²) routine can beat an O(n) one for small n with smaller constants. |
| [[SQL]] vs [[NoSQL]] | Relational + schema + joins + ACID vs a family of non-relational stores trading some of those for scale/flexibility. "NoSQL" is a non-category. |
| [[Container]] vs [[Virtual Machine]] | VM virtualizes hardware (own kernel); container virtualizes the OS (shared kernel) — lighter, faster, less isolated. |
| [[Git]] vs [[GitHub]] | Git is the distributed version-control tool; GitHub is one hosting service for git repos. |
"""
    legacy_confused = (LEGACY / "Often Confused Pairs.md").read_text(encoding="utf-8")
    # strip the legacy frontmatter + title, keep its table rows under a sub-heading
    legacy_body = re.sub(r"^---.*?---\s*# Often Confused Pairs.*?\n", "", legacy_confused,
                         flags=re.DOTALL)
    confused = confused_general + "\n## Security-specific pairs (from the original vault)\n" + \
        legacy_body.strip() + "\n\n---\n← Back to [[_Home]]\n"
    write(OUT / "Often Confused Pairs.md", confused)

def build_term_index(terms, all_titles):
    """A–Z of everything that exists + a curated backlog per branch."""
    by_branch = defaultdict(list)
    for title in sorted(all_titles, key=str.lower):
        by_branch_key = title  # placeholder
    # group authored (new + legacy) by first letter for the A–Z
    az = defaultdict(list)
    for title in sorted(all_titles, key=str.lower):
        az[title[0].upper() if title[0].isalpha() else "#"].append(title)

    lines = ["---", 'type: "reference"', "tags: [reference, index]", "---", "",
             "# Term Index", "",
             f"**{len(all_titles)} terms** currently in the vault. Below: an A–Z of what "
             "exists, then a per-branch backlog of high-value terms still worth adding. The "
             "backlog is a checklist toward fuller coverage, not a contract — extend it freely.",
             "", "## A–Z (existing terms)", ""]
    for letter in sorted(az):
        links = " · ".join(f"[[{t}]]" for t in az[letter])
        lines.append(f"**{letter}** — {links}")
        lines.append("")

    lines += ["## Coverage roadmap (backlog)", "",
              "Curated terms still worth writing, by branch. `code` = not yet written; "
              "write it by copying the template. This is where the path toward broad, "
              "~2,500-term coverage lives — fill in as you go.", ""]
    for branch, items in BACKLOG.items():
        existing = {t.lower() for t in all_titles}
        todo = [x for x in items if x.lower() not in existing]
        done = len(items) - len(todo)
        lines.append(f"### {branch}  ({done}/{len(items)} written)")
        if todo:
            lines.append("")
            lines.append(" · ".join(f"`{x}`" for x in todo))
        lines.append("")
    lines += ["---", "← Back to [[_Home]]"]
    write(OUT / "Term Index.md", "\n".join(lines) + "\n")

# A curated backlog of high-value, long-lived terms per branch (names only).
# These scope the path toward broad coverage; write them by copying the template.
from backlog import BACKLOG  # noqa: E402

# ---------------------------------------------------------------------------
def validate_links():
    titles = set()
    aliases = set()
    for f in OUT.rglob("*.md"):
        titles.add(f.stem)
        text = f.read_text(encoding="utf-8")
        m = re.search(r"^aliases:\s*\[(.*?)\]", text, flags=re.MULTILINE)
        if m:
            for a in re.findall(r'"([^"]+)"', m.group(1)):
                aliases.add(a)
    resolvable = {t.lower() for t in titles} | {a.lower() for a in aliases}
    unresolved = defaultdict(set)
    link_re = re.compile(r"\[\[([^\]]+?)\]\]")
    for f in OUT.rglob("*.md"):
        for raw in link_re.findall(f.read_text(encoding="utf-8")):
            target = raw.split("|")[0].split("#")[0].strip()
            target = target.replace("\\", "")
            base = target.split("/")[-1]
            if base.lower() not in resolvable:
                unresolved[base].add(f.name)
    return titles, unresolved

def main():
    print("Building IT-Dictionary vault…")
    terms = load_dataset()
    print(f"  dataset: {len(terms)} new terms")
    legacy_count = migrate_legacy()
    print(f"  legacy : {legacy_count} security terms migrated")
    build_term_notes(terms)
    build_branch_maps(terms)
    build_security_overview()
    build_home()
    build_static(terms)

    all_titles = sorted(p.stem for p in (OUT / "Terms").glob("*.md"))
    build_term_index(terms, all_titles)

    titles, unresolved = validate_links()
    total_notes = sum(1 for _ in OUT.rglob("*.md"))
    print(f"  total notes: {total_notes}  (terms: {len(all_titles)})")
    if unresolved:
        print(f"\n  ⚠ {len(unresolved)} unresolved link target(s) "
              f"(these show as ghost nodes — expansion hooks):")
        for base in sorted(unresolved)[:60]:
            print(f"     - {base}  ←  {', '.join(sorted(unresolved[base]))[:80]}")
        if len(unresolved) > 60:
            print(f"     … and {len(unresolved) - 60} more")
    else:
        print("  ✓ all wikilinks resolve")

if __name__ == "__main__":
    sys.exit(main())
