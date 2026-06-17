---
type: "term"
branch: "Security"
domain: "Offensive Security & Testing"
tags: ["offense"]
status: "note"
---

# Shellcode

> **Domain:** [[12 - Offensive Security and Testing|Offensive Security & Testing]]

Small, position-independent payload, often spawning a shell.

**Context.** Hand-crafted, position-independent machine code small enough to fit in an exploit's available space — historically to `exec` a shell, now usually a stager that pulls down a bigger payload. Writing it teaches how exploitation actually works at the memory level (and why ASLR/DEP hurt), which is why it's a rite of passage in exploit-dev and OSCP-style training.

## See also

- [[Payload]]
- [[Reverse Shell]]
- [[Buffer Overflow]]
