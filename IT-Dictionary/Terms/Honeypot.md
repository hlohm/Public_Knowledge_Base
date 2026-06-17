---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Honeynet"]
tags: ["network", "deception"]
status: "note"
---

# Honeypot

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Honeynet

Decoy system designed to attract attackers, gather intel, and waste their time. A **honeynet** is a network of them.

**Context.** The budget version is the most useful: a canary — fake service account, decoy file share, honeytoken AWS key — that no legitimate process should ever touch, so any interaction is a high-fidelity alert. Full interactive honeypots are research tools; canaries are practical detection for any size of shop.

## See also

- [[Threat Intelligence]]
