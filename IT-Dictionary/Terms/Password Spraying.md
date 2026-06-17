---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
tags: ["threat"]
status: "note"
---

# Password Spraying

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]

Trying a few common passwords against many accounts (evades lockouts).

**Context.** Inverts the brute-force loop — one password (`Winter2026!`) against thousands of accounts — precisely to stay under per-account lockout. It evades counters that only watch single accounts, so detection needs a tenant-wide view of failed logins, and the real fix is MFA plus banning predictable passwords. A perennial winner against exposed M365/OWA portals.

## See also

- [[Brute Force]]
- [[MFA]]
