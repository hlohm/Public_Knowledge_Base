---
type: map
area: Networking & Protocols
status: working
---

# Networking & Protocols

> **Area Map** — the protocols you operate on, from the command line.

The *concepts* (what TCP, DNS, TLS are) live in the IT-Dictionary; this is the
*operational* side — the commands, the troubleshooting, the day-to-day.

## In this area
- **[[ssh]]** — remote shell, keys, config, tunnels, plus `scp`/`sftp`
- DNS — `dig`, `host`, record types in practice, resolution troubleshooting
- HTTP — `curl` for requests, headers, debugging
- (S)FTP / SCP — file transfer over SSH and FTP
- TLS / openssl — inspecting certs, testing endpoints
- **[[nc]]** — netcat: raw TCP/UDP, port checks, banner grabbing, ad-hoc transfer
- **[[syncthing]]** — continuous P2P file sync: devices, folders, untrusted/receive-encrypted, the CLI

## Playbooks
- **[[Network Infrastructure Hardening]]** — decision-tree hardening reference for routers, switches, firewalls, DNS, VPN gateways, and wireless infrastructure; covers the three-plane model (management/control/data), BGP/RPKI, L2 security, DNSSEC, and OOB management across Cisco IOS, JunOS, Arista EOS, VyOS, and pfSense

## See also
- [[Linux Administration]] · [[CLI Tools]]
