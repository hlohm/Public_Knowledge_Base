---
type: "term"
branch: "Security"
domain: "Offensive Security & Testing"
tags: ["offense"]
status: "note"
---

# Payload

> **Domain:** [[12 - Offensive Security and Testing|Offensive Security & Testing]]

The code the exploit delivers and runs.

**Context.** The distinction worth keeping straight: the exploit is the *technique* that gains execution, the payload is *what runs* once it does — a reverse shell, a beacon, ransomware, or just `whoami` for a proof of concept. Same exploit, swappable payloads. Encoders and packers exist to slip the payload past AV, which is the cat-and-mouse EDR behavioral detection answers.

## See also

- [[Exploit]]
- [[Shellcode]]
- [[Reverse Shell]]
