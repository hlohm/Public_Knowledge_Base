---
type: playbook
area: "Networking & Protocols"
aliases: [packet analysis, traffic analysis, pcap triage]
tags: [networking, pcap, security, blue-team, analysis]
status: draft
---

# Packet-Capture Augury

> **Area:** [[Networking & Protocols]]

Reading the signs in a packet capture — what traffic patterns portend, from a defender's intent. Two indexes over the same signs: **by protocol** (what you're looking at) and **by adversary phase** (what it means). Every entry names the **benign twin** — the innocent traffic that produces the same omen — because the difference between augury and paranoia is knowing the false positives. Tools: [[wireshark]] · [[tshark]].

*This is a reading guide, not an attack manual: the filters detect the patterns, they don't produce them.*

## Symptom

- You've been handed a pcap ("is something wrong in here?"), or an alert fired and the capture is your ground truth, or a baseline just shifted and you want to know why.

## Quick triage (first 3 commands)

```bash
capinfos trace.pcapng                       # when, how long, how many, dropped? — orient before reading
tshark -r trace.pcapng -q -z io,phs         # protocol hierarchy: what's in here that shouldn't be?
tshark -r trace.pcapng -q -z conv,ip        # conversations: top talkers, durations, direction of bulk
```

Then in [[wireshark]]: Conversations with Relative-Start/Duration bars, and the I/O Graph. **Volume, direction, and rhythm before packet contents.**

---

## 1. Signs by protocol

### ARP / L2
| Sign | Portent | Filter | Benign twin |
| --- | --- | --- | --- |
| Same IP claimed by two MACs | ARP spoofing / MitM | `arp.duplicate-address-detected` | DHCP reassignment, HA failover (VRRP/CARP flapping a virtual IP) |
| Gratuitous ARP bursts | Cache poisoning attempt | `arp.isgratuitous == 1` | Normal failover announcements, VM live-migration |
| One host ARP-ing the whole subnet in seconds | L2 network scan | `arp` + sort by time, one src | Network monitoring / inventory tools doing discovery |

### DNS
| Sign | Portent | Filter | Benign twin |
| --- | --- | --- | --- |
| Very long / high-entropy query names | DNS tunneling (C2 or exfil) | `dns.qry.name.len > 50` | CDNs, DGA-looking but legit cloud SaaS names, DNSBL lookups |
| NXDOMAIN bursts from one host | DGA malware hunting its C2 | `dns.flags.rcode == 3` | Typos, stale config, Chrome-style probe queries, search-domain suffixing |
| TXT-record volume from an endpoint | Tunnel/beacon channel | `dns.qry.type == 16` | Email auth lookups (SPF/DKIM/DMARC) from a mail host — *expected on an MTA, odd on a desktop* |
| Client resolving via an external server, bypassing local resolver | Policy evasion, hardcoded malware resolver | `dns && !(ip.dst == <local resolver>)` | Hardcoded 8.8.8.8 in IoT junk, DoH fallback |

### TCP
| Sign | Portent | Filter | Benign twin |
| --- | --- | --- | --- |
| SYN fan-out: one src, many ports/hosts, no data | Port scan (half-open if RST follows SYN/ACK) | `tcp.flags.syn == 1 && tcp.flags.ack == 0` then sort by src | Monitoring health checks, load balancers, P2P mesh dialing (Syncthing, Tor relays *look like this by design*) |
| Flag nonsense: no flags, or FIN+PSH+URG | Null / Xmas scan — stack fingerprinting | `tcp.flags == 0` · `tcp.flags.fin==1 && tcp.flags.push==1 && tcp.flags.urg==1` | Practically none — broken middleboxes at worst; treat as real |
| RST storms | Scan responses, or injected resets | `tcp.flags.reset == 1` sorted by src/dst | Service restarted mid-conversation; aggressive clients |
| Long-lived, low-volume, outbound-initiated session | Reverse shell / C2 channel | Conversations table: duration long, bytes small, initiated from inside | SSH session someone left open, database keepalives, message-queue subscriptions |

### TLS
| Sign | Portent | Filter | Benign twin |
| --- | --- | --- | --- |
| SNI that resolves nowhere / mismatches the IP's known role | Domain fronting, C2 | column on `tls.handshake.extensions_server_name` | CDN sharing, SNI-less internal services |
| Self-signed or absent cert chain on an outbound session | C2 with lazy TLS | `tls.handshake.type == 11` + inspect cert | *Your own estate* — internal services with self-signed certs are everywhere; know your inventory |
| Old TLS versions / weak ciphers suddenly in play | Downgrade, ancient tooling | `tls.record.version < 0x0303` | Legacy appliances, printers, embedded junk |
| ClientHello fingerprint (JA3/JA4) unlike any browser | Non-browser tool speaking TLS | external tooling (Zeek, ja4+) — Wireshark shows the raw hello | Every legitimate CLI tool, updater, and agent also has a non-browser fingerprint — fingerprint *changes* matter more than fingerprints |

### HTTP (cleartext)
| Sign | Portent | Filter | Benign twin |
| --- | --- | --- | --- |
| Same URI hit at metronome intervals, tiny responses | Beacon check-in | I/O Graph + `http.request.uri` column | Polling: RSS, update checks, dashboards, healthchecks-style pings |
| Upstream bytes ≫ downstream on POSTs | Exfil over HTTP | `http.request.method == "POST"` + conversations direction ratio | Backups, telemetry uploads, cloud sync clients |
| User-Agent unlike the host's known software, or absent | Scripted tool / implant | column on `http.user_agent`, `uniq -c` it via [[tshark]] | Package managers, monitoring agents, curl-driven cron jobs |
| Downloads of executables over plain HTTP | Initial access / staging | `http.content_type contains "application"` + Export Objects | Internal mirrors and legacy repos still doing plain HTTP |

### ICMP
| Sign | Portent | Filter | Benign twin |
| --- | --- | --- | --- |
| Echo payloads larger/odder than the platform default, high frequency | ICMP tunnel | `icmp.type == 8` + `data.len` column | MTU discovery probes, exotic monitoring |
| Unreachable/port-unreachable bursts converging on one src | UDP scan echo | `icmp.type == 3` | One misconfigured client retrying a dead service |

### SMB / Kerberos / AD (east-west)
| Sign | Portent | Filter | Benign twin |
| --- | --- | --- | --- |
| Admin-share access (`C$`, `ADMIN$`) from a workstation | Lateral movement staging | `smb2.tree contains "$"` | Admin jump hosts and management tooling — *source* matters, not the share |
| NTLM where Kerberos is expected | Relay/downgrade, pass-the-hash territory | `ntlmssp` presence on modern AD segments | Legacy apps, non-domain devices, IP-address (not hostname) connections |
| TGS-request bursts for many services from one user | Kerberoasting sweep | `kerberos.msg_type == 12` volume per client | Service-heavy logon storms at shift start; monitoring service accounts |
| Workstation→workstation SMB/WinRM/RDP at all | Lateral movement — most estates should be hub-and-spoke | conversations matrix within the client subnet | Helpdesk remote support, peer file shares where policy allows them |

### Rhythm (protocol-agnostic — often the strongest omen)
- **Periodicity**: beacons keep time; humans don't. I/O Graph with a tight Y-axis, or export timestamps via [[tshark]] and look at inter-arrival deltas. Add jitter tolerance — good implants wobble on purpose, so look for *distribution* regularity, not exact intervals.
- **Benign twin, loudly**: infrastructure is *full* of legitimate metronomes — NTP, monitoring, keepalives, sync clients, dead-man's-switch pings. Periodicity **selects candidates**; destination + volume + content convict.

## 2. The same signs, by adversary phase

- **Recon** → ARP sweeps, SYN fan-out, flag-nonsense scans, ICMP unreachable echoes. *Wire shape: one source, many destinations, tiny packets, no payload.*
- **Initial access / staging** → executable downloads, plain-HTTP staging, odd User-Agents. *Shape: one inbound-triggered outbound fetch, modest size, novel destination.*
- **C2 / persistence** → beacon rhythm, long-lived thin sessions, DNS tunnels, self-signed TLS, non-browser fingerprints. *Shape: outbound-initiated, low volume, high regularity, long duration.*
- **Lateral movement** → admin shares, NTLM surprises, Kerberoast bursts, workstation-to-workstation anything. *Shape: east-west where the estate should be hub-and-spoke.*
- **Exfiltration** → direction ratio inversion (client uploading ≫ downloading), DNS TXT/long-name volume, POST-heavy sessions to fresh destinations. *Shape: sustained upstream bulk from a host whose job is downstream.*

The phase axis is what turns a sign into a story: a SYN sweep *and* a fresh TGS burst *and* a new metronome from the same host is not three alerts — it's one intrusion, narrated in order.

## Decision branches

- **Sign confirmed, benign twin excluded** → treat as incident: preserve the pcap (hash it), carve the relevant conversations ([[tshark]] `-w`), start a timeline from the earliest related packet.
- **Benign twin plausible** → check the *inventory* answer (is that host supposed to do this?) before the *packet* answer; most augury false-positives die on "oh, that's the backup job."
- **Can't decide** → widen the window: one pcap rarely convicts; a ring-buffer recapture at the right vantage point ([[tshark]] §dumpcap) usually settles it.

## Escalation / after-action

- Preserve originals read-only, hash them, work on copies; note capture vantage point and clock source (UTC — see [[wireshark]] §time).
- Every confirmed sign becomes a **detection**: encode it in the IDS/SIEM so the *next* occurrence pages you instead of relying on manual augury.
- Every false positive becomes a **baseline note**: the benign-twin tables above only work if you know your own estate's metronomes and admin paths. Keep that inventory current — augury is 20 % reading packets and 80 % knowing what normal looks like.
