---
type: "term"
branch: "Networking"
aliases: ["rpcbind", "portmap", "RPC Portmapper"]
tags: [net]
status: "developed"
---

# Portmapper

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** rpcbind, portmap, RPC Portmapper

The directory service for Sun-RPC. RPC programs bind whatever port the OS gives them and register that number against their well-known *program* number; a client asks the portmapper — itself always on port 111 — which port to actually talk to. `rpcbind` is the modern implementation.

**Context.** Its consumers are NFSv3 and earlier, `rpc.statd` (NFS locking), rquotad, and NIS. **NFSv4 dropped the dependency**: it uses a fixed port 2049 and needs no portmapper at all, so on a v4-only or NFS-free host the service is pure [[Attack Surface]]. It nevertheless turns up uninvited, because cloud images commonly install the NFS client package and the portmapper rides along as a dependency. Two reasons it draws abuse notices: it answers over [[UDP]], which makes it usable as a reflector in an [[Amplification Attack]], and `rpcinfo -p` against an open one is free reconnaissance about what else the host runs. Blocking port 111 upstream stops the reflection but leaves the listener in place — [[Hardening]] means removing or masking the service, so that a later firewall change can't quietly re-expose it.

## See also

- [[UDP]]
- [[Port]]
- [[Amplification Attack]]
- [[Attack Surface]]
- [[Hardening]]

## Further reading

- [Wikipedia: Portmap](https://en.wikipedia.org/wiki/Portmap)
- [RFC 1833: Binding Protocols for ONC RPC Version 2](https://www.rfc-editor.org/info/rfc1833)
