---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
tags: ["iam", "attack"]
status: "note"
---

# Privilege Escalation

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]

Going from low-privilege access to high. **Vertical** = gaining more rights; **horizontal** = accessing another user's data at the same level.

**Context.** In real intrusions this is a phase, not a one-off: initial access lands as a normal user, then misconfigurations do the heavy lifting — unquoted service paths, writable service binaries, stored credentials, kernel exploits as the loud last resort. Defensively, the high-value moves are patching, removing local admin, and credential hygiene so there's nothing lying around to harvest.

## See also

- [[Lateral Movement]]
- [[PAM]]
