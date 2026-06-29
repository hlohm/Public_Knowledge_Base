---
type: map
area: Shells & Scripting
status: working
---

# Shells & Scripting

> **Area Map** — interactive shells and the scripting idioms that span them.

The shells differ most in their *interactive* features (completion, history, prompt) and
their *scripting* dialects. POSIX `sh` is the portable baseline; `bash` is the de-facto
Linux default; `zsh`/`fish` win on interactivity; PowerShell is object-oriented and the
Windows native (filed under [[Windows Administration]]).

## In this area
- **[[bash]]** — the default Linux shell and scripting workhorse
- **[[sh]]** — POSIX baseline: portability, `[ ]` vs `[[ ]]`, getopts, POSIX-safe idioms
- **[[zsh]]** — interactive: completion, extended globbing, parameter expansion, setopt
- **[[fish]]** — friendly interactive shell: autosuggestions, abbreviations, argparse
- PowerShell — see [[Windows Administration]]

## Boilerplate
- **[[Bash Strict Mode Header]]** — the safe script preamble
- **[[Argument Parsing Skeleton]]** — bash long-option parsing skeleton
- **[[getopts Template]]** — POSIX-compatible short-option parsing

## See also
- [[CLI Tools]] · [[Linux Administration]]
