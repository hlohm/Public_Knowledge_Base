---
type: "term"
branch: "Internet & Web"
tags: [web, modern]
status: "developed"
---

# WebSocket

> **Branch:** [[05 - Internet & Web|Internet & Web]]

A protocol providing a persistent, full-duplex connection between browser and server over a single TCP connection, after an HTTP upgrade handshake.

**Context.** The fix for HTTP's request/response one-directionality when you need server push (chat, live dashboards) without polling. Stateful, so it complicates load balancing and scaling.

## See also

- [[HTTP]]
- [[TCP]]
- [[Server-Sent Events]]

## Further reading

- [Wikipedia: WebSocket](https://en.wikipedia.org/wiki/WebSocket)
