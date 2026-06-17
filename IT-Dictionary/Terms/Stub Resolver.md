---
type: "term"
branch: "Networking"
aliases: ["DNS Stub", "Stub"]
tags: [net]
status: "developed"
---

# Stub Resolver

> **Branch:** [[04 - Networking|Networking]]
> **Also known as:** DNS Stub, Stub

The minimal resolver built into the OS or libc that applications call; it doesn't recurse itself but forwards queries to a configured recursive resolver and returns the answer.

**Context.** Everything `getaddrinfo()` touches goes through a stub. On modern Linux the stub is often `systemd-resolved` listening on `127.0.0.53`, and it consults *local* sources first — `/etc/hosts` and its own synthetic records — **before** any DNS query leaves the box. That ordering is a classic footgun: a stale `/etc/hosts` line for a name shadows the real DNS answer and resolves as a *synthetic* record (sub-millisecond, marked authenticated) without the resolver you intended ever being asked. `resolvectl query` shows `Data from: synthetic` when that happens.

## See also

- [[Recursive Resolver]]
- [[Search Domain]]
- [[FQDN]]
- [[Split-horizon DNS]]

## Further reading

- [Wikipedia: Domain Name System](https://en.wikipedia.org/wiki/Domain_Name_System)
