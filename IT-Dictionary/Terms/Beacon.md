---
type: "term"
branch: "Security"
domain: "SecOps, Detection & Response"
aliases: ["Implant"]
tags: ["secops", "threat"]
status: "note"
---

# Beacon

> **Domain:** [[11 - SecOps Detection and Response|SecOps, Detection & Response]]
> **Also known as:** Implant

Persistent agent that calls home periodically to receive commands. Also called an **implant**.

**Context.** The heartbeat that betrays C2: an implant phoning home on an interval, often with jitter and sleep to blend in, sometimes over DNS or a CDN to hide. Network detection hunts the *pattern* — regular callouts, suspicious JA3/SNI, long-lived low-volume connections — because the payload is encrypted. "Beacon" is also Cobalt Strike's specific implant, hence the name's ubiquity in IR reports.

## See also

- [[C2]]
- [[RAT]]
- [[Persistence]]
