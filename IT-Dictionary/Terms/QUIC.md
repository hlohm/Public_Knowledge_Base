---
type: "term"
branch: "Networking"
tags: [net, modern]
status: "developed"
---

# QUIC

> **Branch:** [[04 - Networking|Networking]]

A UDP-based transport with built-in TLS 1.3, multiplexed streams, and 0/1-RTT setup — the foundation of HTTP/3.

**Context.** Lives in user space, so it evolves without OS/kernel updates, and its per-stream model removes TCP's head-of-line blocking.

## See also

- [[UDP]]
- [[HTTP-3|HTTP/3]]
- [[TLS]]

## Further reading

- [Wikipedia: QUIC](https://en.wikipedia.org/wiki/QUIC)
