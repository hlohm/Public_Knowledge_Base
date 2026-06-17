---
type: "term"
branch: "Networking"
aliases: ["User Datagram Protocol"]
tags: [net, fundamental]
status: "developed"
---

# UDP

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** User Datagram Protocol

Connectionless transport: send datagrams with no handshake, ordering, or delivery guarantee — minimal overhead.

**Context.** Right when loss is tolerable or recoverable in the app (DNS, VoIP, gaming, QUIC). The app, not the transport, owns any reliability it needs.

## See also

- [[TCP]]
- [[Datagram]]
- [[QUIC]]

## Further reading

- [Wikipedia: User Datagram Protocol](https://en.wikipedia.org/wiki/User_Datagram_Protocol)
