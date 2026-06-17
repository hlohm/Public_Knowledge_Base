# Public Knowledge Base

A growing personal reference, written in plain Markdown and organized as a set of
interlinked dictionaries. Each subject is its own self-contained Obsidian vault, built
up term by term — small, well-cross-referenced notes designed to make a subject's
vocabulary easy to learn and easy to navigate.

Everything here is published so it's reachable from anywhere without authentication,
and shared in case any of it is useful to others.

## Index

- **[IT Dictionary](./IT-Dictionary/_Home.md)** — ~690 interlinked notes covering the
  vocabulary of information technology across 16 branches — computing foundations,
  hardware, operating systems, networking, the web, data, programming, software
  engineering, algorithms, theory, cloud, DevOps, AI/ML, media & HCI, standards, and
  security — with concept maps, study paths, and a cross-IT "false friends" reference
  for commonly confused pairs. Grown out of the original security-vocabulary vault,
  which lives on intact as the Security branch.
- **[Field Manual](./Field-Manual/_Home.md)** — hands-on operations & development
  reference: cheat-sheets, runbooks, playbooks, and reusable boilerplate for the everyday
  command line, systems administration, and coding. The practical *how-to* counterpart to
  the IT-Dictionary's conceptual *what/why*.

*More subjects may join over time, each as its own vault.*

## How it's organized

The repository is a collection of independent vaults — one folder per subject. Each is
a complete Obsidian vault you can open on its own, and follows roughly the same shape:

- `_Home.md` — entry point with a short tour
- `Terms/` — one short note per concept (flat)
- `Maps/` — Maps of Content grouping terms by area
- `Templates/` — note templates for adding new entries
- `Conventions.md`, `How to Extend.md` — the format rules and the workflow for growing it

Notes link to each other via Obsidian-style `[[wikilinks]]`. These render natively in
[Obsidian](https://obsidian.md); on the web they appear as plain text, and the folder
structure plus full-text search make navigation straightforward.

Each term note follows a consistent shape: a one-paragraph definition, a *Context* note
on why the concept matters and where it appears in practice, a *See also* list of
related terms, an *Often confused with* section for the field's false friends, and a
*Further reading* link to a canonical source.

## Using this with Obsidian

Clone or download the repo, then in Obsidian choose **Open folder as vault** and point
at the subject folder you want — e.g. `IT-Dictionary/`. The full graph, backlinks, and
quick-switcher become available, scoped to that subject; start at its `_Home.md`. Each
subject is a separate vault, so open the subject folder, not the repo root.

## Reading without Obsidian

Every file is plain Markdown. Browse on the repo's web interface, view in any text
editor, or render with whatever Markdown tool you prefer — no special tooling required.

## Status

Active and evolving. Subjects and terms are added and expanded over time; existing
notes are periodically refined as the surrounding vocabulary grows. Spotted an error or
have a suggestion? Open an issue.
