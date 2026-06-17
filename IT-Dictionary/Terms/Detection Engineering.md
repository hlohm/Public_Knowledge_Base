---
type: "term"
branch: "Security"
domain: "SecOps, Detection & Response"
tags: ["secops"]
status: "note"
---

# Detection Engineering

> **Domain:** [[11 - SecOps Detection and Response|SecOps, Detection & Response]]

The discipline of building and maintaining detections, including testing them with adversary emulation.

**Context.** Treats detections as code: version-controlled rules, tested against emulated attacks, tuned for the true-positive rate, and retired when they stop earning their alerts. The maturity marker is detection-as-code with CI and a feedback loop from every incident ("why didn't we catch this?" → new rule). Sigma is the portable rule format; the discipline is what separates a SOC from an alert firehose.

## See also

- [[SIEM]]
- [[MITRE ATT&CK]]
- [[Adversary Emulation]]
- [[Threat Hunting]]
