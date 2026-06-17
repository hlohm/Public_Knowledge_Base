---
type: "term"
branch: "Security"
domain: "Network Security"
tags: ["network"]
status: "note"
---

# DPI

> **Domain:** [[05 - Network Security|Network Security]]

**D**eep **P**acket **I**nspection. Examining payload, not just headers.

**Context.** What separates a port-based ACL from real traffic understanding: DPI identifies the application regardless of port and spots protocol abuse like tunneling. Encryption is its natural limit — without TLS interception, DPI sees metadata only, which is why modern inspection leans on SNI, JA3 fingerprints, and behavioral signals.

## See also

- [[IDS and IPS]]
- [[TLS Inspection]]
