---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["0-day", "\"Zero-Day\""]
tags: ["threat", "vuln"]
status: "note"
---

# Zero Day

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** 0-day, "Zero-Day"

Vulnerability unknown to the vendor (and therefore unpatched). The exploit for it is also called a 0-day.

**Context.** Zero days worth their name are scarce and burn on use (each one detected gets patched), so they're spent on high-value targets, not sprayed. For defense the implication is humbling: you cannot patch what's unknown, so you invest in *reducing impact* — least privilege, segmentation, EDR behavioral detection, and exploit mitigations that raise the cost of any memory bug. Most orgs lose to N-days, not zero days.

## See also

- [[N-Day]]
- [[Exploit]]
- [[Vulnerability]]
- [[RCE]]

## Often confused with

- [[N-Day]] — 0-day = unknown to vendor. N-day = known and patched, but still being exploited against unpatched systems. Most real-world attacks are N-day.
