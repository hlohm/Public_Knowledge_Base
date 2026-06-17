---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
tags: ["threat"]
status: "note"
---

# Exfiltration

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]

The unauthorized transfer of data out of a controlled environment — the "actions on objectives" payoff of most data-theft intrusions.

**Context.** Attackers hide it in the noise: HTTPS to a cloud bucket, DNS tunneling, or a slow trickle under DLP thresholds. Modern ransomware exfiltrates *before* encrypting (double extortion), so blocking outbound matters as much as preventing entry. Detection leans on egress monitoring, DLP, and unusual-volume baselines — staged archives (a sudden 40 GB .rar) are a classic tell.

## See also

- [[DLP]]
- [[C2]]
