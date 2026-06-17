---
type: "term"
branch: "Security"
domain: "Network Security"
tags: ["network"]
status: "note"
---

# Air Gap

> **Domain:** [[05 - Network Security|Network Security]]

Physical isolation from other networks. The strongest form of segmentation; still defeatable (Stuxnet).

**Context.** The gap is only as real as its exceptions: USB sticks, maintenance laptops, and "temporary" update connections are how Stuxnet-class attacks cross it. Where it shines operationally: offline backups that ransomware cannot reach, and offline CA roots. Treat every bridge across the gap as a formal, logged event.

## See also

- [[Network Segmentation]]
- [[Ransomware]]
