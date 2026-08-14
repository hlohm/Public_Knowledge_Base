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
- **[[ssh]]** — remote shell, keys, tunnels, plus `scp`/`sftp`
- **[[ssh_config]]** — client config file: `Host`/`Match` blocks, jump hosts, multiplexing
- **[[dns]]** — `dig`, `host`, record types, DNSSEC validation, troubleshooting
- HTTP — **[[curl]]** for requests, headers, debugging *(also [[CLI Tools]])*
- **[[scp-sftp]]** — SCP and SFTP file transfer over SSH; FTP legacy reference
- **[[openssl]]** — inspecting certs, testing TLS endpoints, generating keys/CSRs
- **[[nc]]** — netcat: raw TCP/UDP, port checks, banner grabbing, ad-hoc transfer
- **[[syncthing]]** — continuous P2P file sync: devices, folders, untrusted/receive-encrypted, the CLI
- **[[wireshark]]** — GUI packet analysis: capturing, display filters, name resolution, the time column, statistics, artifact extraction
- **[[tshark]]** — the CLI family: `dumpcap` capture & ring buffers, tshark filtering/field extraction, `capinfos`/`mergecap`/`editcap`
- **[[tcpdump]]** — capture on the box that has nothing else installed: BPF filter language, flag surgery, rotation, remote-capture-into-GUI

## Playbooks
- **[[Network Infrastructure Hardening]]** — decision-tree hardening reference for routers, switches, firewalls, DNS, VPN gateways, and wireless infrastructure; covers the three-plane model (management/control/data), BGP/RPKI, L2 security, DNSSEC, and OOB management across Cisco IOS, JunOS, Arista EOS, VyOS, and pfSense
- **[[Packet-Capture Augury]]** — reading captures with a defender's intent: signs indexed by protocol *and* by adversary phase, each with the display filter that surfaces it and the benign twin that fools you

## See also
- [[Linux Administration]] · [[CLI Tools]]
