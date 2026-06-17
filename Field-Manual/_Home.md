---
type: home
---

# Field Manual — Home

The **do** companion to the [IT-Dictionary](../IT-Dictionary/_Home.md)'s **know**. Where the
dictionary answers *"what is this and why does it matter,"* this vault answers
*"how do I actually do it"* — command references, procedures, and reusable boilerplate
you reach for while your hands are on the keyboard.

Everything here is meant to be **consulted under load**: scannable, copy-pasteable,
annotated so the *why* is on the page, not just the *what*.

## What's in here

Four kinds of note, by what you need in the moment:

- 📋 **Cheatsheets** — command/keybind references for one tool or topic. *"Which flag was it?"*
- 🛠️ **Runbooks** — step-by-step procedures for a recurring task, with verification at each step. *"Walk me through the restore."*
- 🚨 **Playbooks** — decision-oriented response to a symptom. *"It's down — what do I check first?"*
- ✂️ **Snippets** — drop-in boilerplate (script headers, unit files, configs). *"Give me the skeleton."*

## Areas

Each note has one home **area** (its Map). Browse a Map top-to-bottom, or follow links.

- [[Shells & Scripting]] — bash, sh, zsh, fish, PowerShell, and the scripting idioms that span them
- [[CLI Tools]] — git, nvim, tmux, curl, and the rest of the everyday command line
- [[Containers]] — docker & compose, and the container surface around them
- [[Backup & Recovery]] — borgmatic/borg, restore drills, the recover-from-disaster path
- [[Linux Administration]] — systemd, users, packages, networking, storage, logs
- [[Windows Administration]] — PowerShell-first administration of Windows hosts
- [[Programming Languages]] — Python, C, Java, Perl, JavaScript, SQL reference
- [[Networking & Protocols]] — ssh, DNS, HTTP, (S)FTP, TLS on the wire

## How this vault works

Notes link with `[[wikilinks]]`; open any note and check **Backlinks** to see what points
back. Every note declares its `type:` and home `area:` in frontmatter, and a `status:`
(`stub` → `draft` → `working` → `stable`) so you can see at a glance what's load-bearing
and what's a placeholder. A faded "ghost" link in a Map is a **to-do** — a note worth
writing next.

This is a **separate vault** from the IT-Dictionary on purpose (different shape, different
use). Links *into* the dictionary resolve only in the unified parent vault, not here — so
reference dictionary concepts by name and don't hard-depend on cross-vault links.

## Adding to it

See [[How to Extend]]. Short version: copy the matching template from `Templates/`,
drop it in the right folder, fill it in, add it to its area Map. See also [[README]] and
[[Conventions]] — and keep it **English, generic, and secret-free** (this repo is public).
