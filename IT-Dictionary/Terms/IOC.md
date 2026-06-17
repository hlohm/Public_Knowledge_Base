---
type: "term"
branch: "Security"
domain: "SecOps, Detection & Response"
aliases: ["Indicator of Compromise"]
tags: ["secops"]
status: "note"
---

# IOC

> **Domain:** [[11 - SecOps Detection and Response|SecOps, Detection & Response]]
> **Also known as:** Indicator of Compromise

**I**ndicator **o**f **C**ompromise. Forensic artifact of a breach: file hash, IP, domain, registry key. Tactical and short-lived.

**Context.** Cheap to share and match, which is their value (threat feeds, blocklists, retro-hunts) — and cheap for the attacker to change, which is their limit. A hash blocks exactly one file; rebuild and it's useless. Use IOCs for fast, broad coverage and retrospective hunting, but don't mistake an IOC feed for detection of a determined adversary, who rotates them by design.

## See also

- [[IOA]]
- [[Threat Intelligence]]
- [[Pyramid of Pain]]

## Often confused with

- [[IOA]] — IOC = artifact ('we saw this hash'). IOA = behavior ('we saw process injection'). IOAs are harder for attackers to change.
