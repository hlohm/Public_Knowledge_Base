---
type: "term"
branch: "Security"
domain: "Offensive Security & Testing"
aliases: ["Bind Shell"]
tags: ["offense"]
status: "note"
---

# Reverse Shell

> **Domain:** [[12 - Offensive Security and Testing|Offensive Security & Testing]]
> **Also known as:** Bind Shell

**Reverse**: target connects back to attacker (firewall-friendly). **Bind**: target listens, attacker connects.

**Context.** The direction is the trick: outbound connections sail through firewalls that block inbound, so the target dials *out* to the attacker's listener — which is exactly why egress filtering and outbound monitoring matter. A server initiating an unexpected outbound shell-like connection is a high-quality detection. Bind shells (target listens) are the textbook opposite and rarely work against a real perimeter.

## See also

- [[Shellcode]]
- [[Payload]]
