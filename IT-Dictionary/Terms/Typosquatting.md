---
type: "term"
branch: "Security"
domain: "Application Security"
tags: ["appsec"]
status: "note"
---

# Typosquatting

> **Domain:** [[08 - Application Security|Application Security]]

Publishing malicious packages with names close to popular ones (`reqeusts` for `requests`).

**Context.** Banks on autopilot: a fat-fingered `reqeusts`, a `python3-dateutil` look-alike, or a domain one keystroke off your bank. In package ecosystems it's a live supply-chain vector — malicious lookalikes get thousands of installs before takedown. Defenses: pin and verify dependencies, use a curated internal registry, and for domains, monitor registrations near your brand.

## See also

- [[Dependency Confusion]]
- [[Supply Chain Attack]]
