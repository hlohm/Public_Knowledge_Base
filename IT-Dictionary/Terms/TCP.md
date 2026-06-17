---
type: "term"
branch: "Networking"
aliases: ["Transmission Control Protocol"]
tags: [net, fundamental]
status: "developed"
---

# TCP

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Transmission Control Protocol

Connection-oriented transport giving ordered, reliable, byte-stream delivery with flow and congestion control, atop unreliable IP.

**Context.** The reliability and ordering cost setup latency (the handshake) and head-of-line blocking — the gap QUIC/HTTP-3 closes.

## See also

- [[UDP]]
- [[Three-way Handshake]]
- [[Congestion Control]]
- [[QUIC]]

## Often confused with

- [[UDP]] — TCP guarantees order + delivery; UDP is fire-and-forget with lower overhead.

## Further reading

- [Wikipedia: Transmission Control Protocol](https://en.wikipedia.org/wiki/Transmission_Control_Protocol)
