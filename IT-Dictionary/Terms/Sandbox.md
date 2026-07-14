---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
tags: ["endpoint"]
status: "note"
---

# Sandbox

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]

Isolated execution environment used to analyze suspicious files or run untrusted code safely.

**Context.** Two distinct uses share the name: analysis sandboxes that detonate suspicious mail attachments and report behavior (any.run, Joe Sandbox, the detonation step in mail gateways), and isolation sandboxes that contain damage (browser process sandboxes, Windows Sandbox for that dubious installer). Malware checks for both — sandbox-evasion via sleep timers and VM detection is standard now.

## See also

- [[EDR]]
- [[Container Security]]
- [[Sandbox Escape]]
- [[seccomp]]
- [[AI Agent]]
