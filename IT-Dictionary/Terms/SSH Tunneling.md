---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["SSH Port Forwarding", "Reverse SSH Tunnel"]
tags: ["network", "hardening"]
status: "developed"
---

# SSH Tunneling

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** SSH Port Forwarding, Reverse SSH Tunnel

Carrying arbitrary TCP connections inside an authenticated [[SSH]] session. Local forwarding (`-L`) exposes a remote service on the client; remote or *reverse* forwarding (`-R`) exposes a client-side service on the server; dynamic forwarding (`-D`) turns the session into a SOCKS proxy.

**Context.** The connection's direction and the *credential's* direction are independent — that's the design lever. A reverse tunnel lets a trusted machine dial out to an untrusted one and push a service into its loopback, so the untrusted side holds keys to nothing. The server can pin each key to exactly one capability: a dedicated account with a `nologin` shell, an `sshd_config` `Match` block (`AllowTcpForwarding remote`, `PermitListen`, `PermitTTY no`), and per-key `authorized_keys` options (`restrict,port-forwarding,permitlisten="…"`) — three independent layers, each of which alone stops shell access. The same mechanism is standard attacker tradecraft for [[Pivoting]] past segmentation, which is why [[Egress Filtering]] treats outbound SSH from servers with suspicion.

## See also

- [[SSH]]
- [[Bastion Host]]
- [[Egress Filtering]]
- [[Pivoting]]

## Often confused with

- [[VPN]] — a VPN moves whole IP packets at the network layer; an SSH tunnel forwards individual TCP connections at the application layer.

## Further reading

- [Wikipedia: Port forwarding](https://en.wikipedia.org/wiki/Port_forwarding)
- [OpenSSH manual: ssh(1)](https://man.openbsd.org/ssh.1)
