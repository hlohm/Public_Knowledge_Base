---
title: Knowledge Base & Notes — Sync Architecture
status: Decided
last_updated: 2026-05-28
owner: <you>
---

# Knowledge Base & Notes — Sync Architecture

## Summary

A single Obsidian-based knowledge system split into two strictly separated data domains. The publishable knowledge base lives in a public git repository — both for publishing and to give a separate security domain authentication-free read access — and is *also* continuously mirrored across personal devices via Syncthing, so the latest state is everywhere immediately regardless of whether it's been published. Private personal notes live local-only and sync between personal machines via Syncthing alone. Content belonging to other security domains never enters this system at all. The boundary between public and private runs along the git repository's folder edge, and the architecture is designed so that the structure itself enforces most of the privacy discipline rather than relying on vigilance.

## Context & problem

The knowledge base is a growing, interconnected Obsidian vault — currently a security-vocabulary dictionary, intended to keep expanding into general, shareable reference material. It needs to be reachable from personal machines and from one additional security domain that should have read-only access without authentication.

A naive single-repository approach — one public repo holding everything, retrievable from anywhere without authentication — is ruled out as soon as personal notes enter the picture: a public repository cannot hold private content. The system must therefore separate the publishable portion from the private one while keeping the public portion accessible without credentials. That separation is the purpose of this design.

## Goals

- A unified personal Obsidian experience: one place to read and link across everything personal.
- A knowledge base that is genuinely publishable — useful to others, safe to expose.
- Auth-free read access to the knowledge base from a separate security domain, with no credentials stored there.
- A hard privacy firewall: personal notes are never public and never leave personal infrastructure; content from other security domains never enters this system.
- Low-friction sync within the personal domain: no manual step for everyday edits, and the knowledge base visible on every personal device the moment it's written, with no publish step required.
- Portability: plain markdown files, no proprietary lock-in, recoverable if any one tool disappears.

## Non-goals

- Editing the knowledge base from the read-only consumer (read-only there by design).
- Syncing personal notes outside personal machines.
- Storing content from other security domains anywhere in this system.
- Multi-writer git operations across personal devices — only the laptop ever runs git commands; other personal devices participate via Syncthing only.

## The decision

Two data domains with explicit sync boundaries:

| Domain | Contents | Sync via | Visibility |
|---|---|---|---|
| **Knowledge base** | General, shareable reference (the dictionary, etc.) | **git** → public repo (publishing, external read) + **Syncthing** → personal devices (instant mirror, excluding `.git/` and Obsidian churn files) | Public |
| **Personal notes** | Everything private and personal | **Syncthing** (personal machines only) | Private, local |

The knowledge base folder is the *only* thing in the git repository. Personal notes live in the parent folder, outside the repository. Anything belonging to other security domains stays outside this system entirely.

### Folder layout

```
ParentFolder/                       ← Syncthing-shared root
├── personal notes…
├── .obsidian/                      ← "everything" vault config; churn files Syncthing-ignored
└── Public_Knowledge_Base/           ← git repo + Syncthing mirror
    ├── .git/                        (only on laptop; Syncthing-ignored)
    ├── .obsidian/                   ← KB vault config; churn files Syncthing-ignored and gitignored
    ├── _Home.md
    ├── README.md
    └── Terms/, Domains/, …
```

The knowledge base is nested *inside* the personal parent folder so that opening the parent in Obsidian gives a unified "everything" view across both domains. Syncthing shares the parent folder and propagates everything within it across personal devices, with an ignore list (below) that excludes git internals and high-churn Obsidian config — so the two sync mechanisms (git and Syncthing) overlap on the knowledge base safely rather than conflicting.

## Sync topology

- **Primary laptop** — the source of truth. Holds the parent folder, personal notes, and the full knowledge base (working tree *and* `.git/`). All git operations (commit, push, pull) happen here. Edits to anything in the system can originate here.
- **Other personal machine(s)** — receive the parent folder via Syncthing, which includes the knowledge-base working tree as a live mirror. They do *not* hold `.git/` (it is Syncthing-excluded). Edits made on these devices propagate back to the laptop via Syncthing, where they get committed. No git operations run on these devices.
- **Read-only consumer (separate security domain)** — holds a git clone or downloaded snapshot of the public knowledge base. Read-only by design. No personal notes, no Syncthing, no credentials.

The single-writer-on-laptop discipline (only one machine runs git) is the property that makes Syncthing-mirroring the knowledge base across personal devices safe; the operating rules and configuration sections below codify it.

## Obsidian setup

Two vaults over the same files, opened as needed:

- **Everything vault** — open the parent folder. Sees personal notes and the knowledge base together. Its config folder, `ParentFolder/.obsidian/`, sits outside the repo and therefore stays private automatically.
- **Knowledge-base vault** — open the `Public_Knowledge_Base/` subfolder for a focused view. Backlinks, graph, search, and quick-switcher all scope to just the knowledge base.

Each vault keeps its own `.obsidian/` config (plugins, hotkeys, theme), so those are configured per vault. The unified "everything" view is equally complete on any personal device, since the knowledge base content is mirrored across all of them via Syncthing.

Wikilinks resolve only within the open vault's scope: a link that crosses from one domain to another resolves in the parent vault but dangles in the narrower knowledge-base vault, because its target lies outside that subtree. This is expected scoping, not breakage.

## Operating rules

These are the habits the structure mostly enforces, plus the few it cannot:

1. **Knowledge-base notes link only to other knowledge-base notes.** In the unified parent vault, Obsidian autocompletes titles across *both* domains when you type `[[`. Accepting a personal-note suggestion inside a KB note would publish that note's *title* into the public repo and create a link that dangles for anyone who clones it. This is the one rule vigilance must hold.
2. **Personal → knowledge-base links are fine.** They live in private notes and are never published.
3. **All git operations originate on the laptop.** Reading a public repo needs no auth; *pushing* requires credentials even to a public repo. Keeping git operations on the laptop preserves the no-credentials-needed-elsewhere property and keeps the design single-writer from git's perspective — which is what makes Syncthing-mirroring the KB across personal devices safe. Edits on other personal devices are fine; they propagate back to the laptop via Syncthing and get committed there.
4. **No git automation outside the laptop.** Do not install Obsidian Git, auto-commit plugins, or any other git automation on a non-laptop personal device. That would break the single-writer discipline and reintroduce the multi-writer git corruption risk that the design explicitly avoids. Run git in exactly one place.
5. **Commit before pulling.** Avoids tangling uncommitted working-tree state with incoming changes.
6. **Treat every knowledge-base commit as a publication.** Public git history is permanent; a secret or private fragment committed by accident does not go away when deleted.
7. **Other security domains stay in their own systems.** Their content never enters the parent folder, the repo, or Syncthing.

## Configuration

**Syncthing — `.stignore` in `ParentFolder/`** (lives in the Syncthing-shared root; patterns apply throughout the tree):

```
.git
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache
*.sync-conflict-*
```

This excludes git's internal directory (`.git/` is laptop-only) and the high-churn Obsidian workspace state (which is per-device by nature) while still syncing the stable Obsidian config — plugins, themes, hotkeys, snippets — across personal devices.

**Git — `.gitignore` in `Public_Knowledge_Base/`** (keeps Obsidian's per-device files out of the public repo):

```
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache
.trash/
*.sync-conflict-*
```

The overlap between the two ignore lists is intentional — they're serving different purposes (don't publish vs don't sync) and the files in question deserve both treatments.

## Risks & tradeoffs

- **Double-sync corruption (designed out via single-writer + `.git` exclusion).** The catastrophic git-corruption failure modes — mismatched refs, dueling `index.lock` files, `index.sync-conflict-*` artifacts inside `.git` — only arise when two machines both run git against a Syncthing-replicated `.git/`. This design eliminates that risk in two layers: only the laptop runs git operations (single-writer discipline), and `.git/` itself is excluded from Syncthing so its internals never travel. The knowledge-base working tree is freely Syncthing-mirrored because it's just text files.
- **The safety-margin trap.** The single-writer property is a *choice*, not a structural guarantee. The day someone installs Obsidian Git on a tablet "just to try it," the design becomes multi-writer; even with `.git/` excluded from Syncthing the personal devices' git histories will silently diverge from the laptop's. Operating rule 4 exists precisely to hold this line.
- **Working-tree edit conflicts.** Editing the same note on two personal devices between Syncthing rounds produces a Syncthing `.sync-conflict-*` file (not a git problem, a file-sync one). Rare with normal use; the `.sync-conflict-*` glob in both ignore lists keeps any that do appear from leaking into either sync system.
- **No-auth access is read-only.** The read-only consumer cannot push without credentials. Accepted: writes are not wanted from that domain. If that ever changes, it reintroduces the coupling this design avoids.
- **Public history is forever.** Mitigated by rule 6 and by the structural fact that only the knowledge base is ever in the repo.
- **Cross-OS friction.** If the read-only consumer runs a different OS from the laptop, watch git's line-ending normalization (`core.autocrlf`) and case-insensitive filesystems — a case-only rename (`note.md` → `Note.md`) is the classic silent breakage. Low impact, occasional surprise.
- **Per-vault config duplication.** Nested vaults mean multiple `.obsidian/` folders to set up and maintain. Accepted as the price of the focused/global toggle.

## Rejected alternatives

- **One repository for everything, public.** Fails the privacy requirement outright — personal notes cannot be public.
- **One repository for everything, private.** Would force credentials onto every consuming machine and place personal notes inside any security domain that cloned it. Breaks the firewall.
- **Git everywhere, no Syncthing.** Workable, but requires a *second* (private) repo for personal notes plus auth on every machine, and adds a manual commit step to trivial personal edits. The chosen split keeps the private half entirely out of git, with zero-friction Syncthing instead.
- **Syncthing across security domains.** Puts personal notes in environments that shouldn't hold them, and assumes those environments allow peer sync. Breaks the firewall.
- **Knowledge base as a sibling folder, not nested.** Clean for sync, but forfeits the unified "everything" Obsidian vault, which is a stated goal. Nesting plus the targeted Syncthing ignores preserves the unified view safely.
- **Syncthing ignores the whole knowledge-base folder; git as sole sync path for the KB.** This was an earlier version of the chosen design. Rejected because it forces a commit-and-push every time the latest KB state is wanted on another personal device — the workflow "see what I just wrote, immediately, everywhere I work" wasn't possible without conflating "saved" with "published." The chosen approach mirrors the KB via Syncthing across personal devices, with `.git/` excluded and single-writer discipline preventing the corruption modes that would otherwise come with overlap.

## Notes on this document

This describes a personal-machine setup and contains no secrets or sensitive content, so it is safe to keep at the knowledge-base repo root (e.g. `ARCHITECTURE.md`) if the pattern is useful to others — or to keep among personal notes if you'd rather not publish your machine topology. Update it as the system grows (new personal machines, additional read-only consumers, structural changes to the vault).
