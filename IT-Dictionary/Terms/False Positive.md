---
type: "term"
branch: "Security"
domain: "SecOps, Detection & Response"
aliases: ["False Negative", "\"True Positive\""]
tags: ["secops"]
status: "note"
---

# False Positive

> **Domain:** [[11 - SecOps Detection and Response|SecOps, Detection & Response]]
> **Also known as:** False Negative, "True Positive"

Alert that wasn't a real attack. **False negative** = real attack that wasn't alerted on. **True positive** = real, actionable alert (the goal).

**Context.** The quiet SOC-killer: too many false positives and analysts start rubber-stamping "benign" — which is how a real alert (the Target breach) gets ignored. The whole craft of detection engineering is the precision/recall tradeoff: loosen rules and miss attacks (false negatives), tighten them and drown in noise. Alert fatigue is a security risk, not just a morale one.

## See also

- [[Detection Engineering]]
- [[SIEM]]
