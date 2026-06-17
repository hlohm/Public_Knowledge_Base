---
type: "term"
branch: "Networking"
aliases: ["Network Packet"]
tags: ["net", "fundamental"]
status: "developed"
---

# Packet

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** Network Packet

The unit of data at the network layer: a header (addresses, TTL, protocol) plus payload. Each layer wraps the one above — TCP **segment** inside an IP **packet** inside an Ethernet **frame**.

**Context.** Encapsulation is the load-bearing idea: every device only reads the headers of its own layer, which is why a switch forwards frames without understanding IP and a router rewrites frames while leaving the packet intact. 'Packet' is also used loosely for all of these — precise people say frame/packet/segment/datagram by layer.

## See also

- [[IP]]
- [[TCP]]
- [[UDP]]
- [[Ethernet]]
- [[OSI Model]]

## Further reading

- [Wikipedia: Network packet](https://en.wikipedia.org/wiki/Network_packet)
