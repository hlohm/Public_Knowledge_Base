---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Network Access Control"]
tags: ["network"]
status: "note"
---

# NAC

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Network Access Control

**N**etwork **A**ccess **C**ontrol. Decides whether a device joining the network is allowed and what posture it must have.

**Context.** Answers "what just plugged into our wall port / Wi-Fi?" — 802.1X with certificates for managed devices, a quarantine VLAN for the rest. The rollout pain is the exception list: printers, badge readers, and lab gear that can't do 802.1X end up MAC-authenticated, and that list needs an owner or it becomes the bypass.

## See also

- [[Zero Trust]]
- [[Network Segmentation]]
