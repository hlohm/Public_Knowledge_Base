---
type: "term"
branch: "Security"
domain: "SecOps, Detection & Response"
tags: ["secops"]
status: "note"
---

# Threat Hunting

> **Domain:** [[11 - SecOps Detection and Response|SecOps, Detection & Response]]

Proactively searching for threats that evade automated detection. Hypothesis-driven.

**Context.** Starts from a hypothesis, not an alert: "if an attacker were living off the land here, I'd see X" — then go looking in the data, assuming the automated detections already missed it. Outputs are findings *and* new detections (a good hunt that finds nothing still hardens the SIEM). Requires good telemetry and an analyst who knows normal; it's a maturity signal, not a starting point.

## See also

- [[Threat Intelligence]]
- [[Detection Engineering]]
- [[Purple Team]]
- [[IOA]]
