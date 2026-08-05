---
type: "term"
branch: "Security"
domain: "Core Principles & Models"
aliases: ["Fail Safe"]
tags: [principle]
status: "note"
---

# Fail Secure

> **Domain:** [[01 - Core Principles|Core Principles & Models]]
> **Also known as:** Fail Safe

When something breaks, default to denying access. Opposite of *fail open*.

**Context.** 'Fail safe' originally means safe *for the user* (e.g. doors unlock in a fire) — opposite trade-off from 'fail secure'. Choose deliberately. The same choice governs software gates: a permission check that errors should deny, not allow — the design rule behind fail-closed agent hooks and firewalls that drop on rule-load failure.

## See also

- [[PreToolUse Hook]]
- [[Defense in Depth]]
- [[Least Privilege]]
- [[Zero Trust]]
- [[Break-Glass Access]]
