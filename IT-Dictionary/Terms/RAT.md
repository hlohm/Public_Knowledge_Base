---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["Remote Access Trojan"]
tags: ["threat"]
status: "note"
---

# RAT

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** Remote Access Trojan

**R**emote **A**ccess **T**rojan. Gives attacker interactive control of the compromised host.

**Context.** Gives hands-on-keyboard control: file access, keylogging, screen capture, webcam, pivot point. Commodity RATs (AsyncRAT, Remcos, njRAT) arrive via phishing attachments; the line between a RAT and a legitimate remote-admin tool (AnyDesk, TeamViewer) is intent, which is why attackers increasingly just abuse the legitimate ones. EDR behavioral detection is the practical counter.

## See also

- [[Trojan]]
- [[C2]]
- [[Beacon]]
