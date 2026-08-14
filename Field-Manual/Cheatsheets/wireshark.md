---
type: cheatsheet
area: "Networking & Protocols"
aliases: [Wireshark]
tags: [networking, pcap, analysis, troubleshooting]
status: draft
---

# wireshark

> **Area:** [[Networking & Protocols]]

GUI packet analysis — capturing, display filters, name resolution, the time column, statistics, and pulling artifacts out of a trace. CLI capture and batch work live in [[tshark]]; reading captures with a defender's eye lives in [[Packet-Capture Augury]].

---

## 1. Capturing

```text
Capture → Options                # pick interface; traffic sparklines show which ones are live
```

- **Promiscuous mode** (default on): keep it on — otherwise you only see traffic addressed to your own NIC.
- **Snaplen**: capture full frames unless volume forces truncation; truncated payloads break stream reassembly and file export later.
- **Where you capture decides what you see.** A switched port only shows you broadcast + your own unicast. To see someone else's traffic you need a SPAN/mirror port, a tap, or to capture on the endpoint itself. Capturing *on the machine under suspicion* is a last resort — a compromised host can lie about its own traffic.

**Capture filters vs display filters — different languages, different cost:**

```text
Capture filter (BPF, set BEFORE capture):   host 203.0.113.7 and port 443
Display filter (Wireshark syntax, anytime): ip.addr == 203.0.113.7 && tcp.port == 443
```

Capture filters discard packets forever — filter tight only when volume demands it. Display filters just hide; the packets stay in the file. When unsure, capture broad, filter on display.

## 2. Display filters

```text
tcp                              # protocol presence — all TCP
ip.addr == 10.0.0.5              # matches source OR destination
ip.src == 10.0.0.5               # direction-specific
tcp.port in {80, 443, 8080}      # membership test beats chained ==
tcp.flags.syn == 1 && tcp.flags.ack == 0    # SYNs only (connection attempts)
http.request.method == "POST"    # exact string
frame contains "password"        # raw byte search across the frame
dns.qry.name matches "\.xyz$"    # regex (case-insensitive by default)
!(arp || stp)                    # cut broadcast noise
```

- **Green/red bar** in the filter field = valid/invalid syntax. Yellow = valid but probably not what you meant (classic: `ip.addr != x` — use `!(ip.addr == x)`).
- **Right-click any field → Apply as Filter / Prepare as Filter** — fastest way to learn field names; the status bar shows the field name of whatever you click.
- **Right-click a packet → Conversation Filter** — isolate one TCP/IP conversation instantly.
- **Follow → TCP Stream** — reassembled payload both directions; the filter it sets (`tcp.stream eq N`) is worth knowing on its own.

## 3. Name resolution

```text
View → Name Resolution           # MAC / transport / network — three separate toggles
```

- **MAC resolution** (OUI vendor lookup): local database, harmless, leave on — vendor prefixes are triage signal.
- **Port ("transport") resolution**: local table, cosmetic. Fine.
- **Network (DNS) resolution: off by default — keep it off during investigations.** It makes *your analysis machine* fire DNS lookups for every address in the trace: slow, and it tips your hand (an attacker watching their infrastructure's resolver sees you resolving their IPs).
- Need names without leaking? Use a **custom hosts file** inside the profile directory (§Files) — Wireshark resolves from it, nothing leaves the box.

## 4. The time column

```text
View → Time Display Format
```

- Default = **seconds since capture start** (stopwatch). Scan the column for *jumps* — a 4 s → 26 s leap is your slow transaction.
- **Time of day** renders in the *viewing* machine's timezone — a pcap crossing timezones tells each analyst a different story. For anything shared or forensic: **UTC**.
- **Right-click packet → Set/Unset Time Reference**: restarts the stopwatch at that packet — time-to-response from any event you choose. Multiple references allowed.
- Add a **delta time** custom column (`frame.time_delta_displayed`) when hunting latency: sort by it, and the worst gaps float to the top.

## 5. Statistics — read the trace before you read packets

Muscle memory on opening any unknown pcap, in order:

```text
Statistics → Capture File Properties   # duration, packet count, dropped packets
Statistics → Protocol Hierarchy        # what's IN here — and what shouldn't be
Statistics → Conversations             # who talks to whom, how much, how long
```

- In **Conversations**, add/read the **Relative Start + Duration** columns — the gray bars are a timeline of every conversation at a glance: long-lived vs burst, early vs late.
- Sort conversations by **bytes** — the top talker in a "quiet" trace is your first question.
- **Statistics → I/O Graph**: traffic over time; a metronome-regular low-volume series is beaconing until proven otherwise (→ [[Packet-Capture Augury]]).
- **Analyze → Expert Information**: warnings/errors collected across the trace — retransmissions, resets, malformed packets — sorted for you.

## 6. Extracting artifacts

```text
File → Export Objects → HTTP / SMB / DICOM / TFTP    # files carried in the capture, listed & saveable
Follow TCP stream → Save as                          # raw payload when export objects can't parse it
File → Export Specified Packets                      # carve a smaller pcap (displayed packets only)
```

Hash anything you extract before acting on it; the pcap is evidence, the carve is derived.

## 7. Profiles, columns, coloring

```text
Right-click the profile name (bottom-right status bar) → New / Switch
```

- Profiles hold columns, coloring rules, filter bookmarks, and the hosts file — build one per job (troubleshooting, security triage) instead of one overloaded default.
- **Right-click a field → Apply as Column** — e.g. `tls.handshake.extensions_server_name` (SNI) or `http.user_agent` as columns turn scrolling into scanning.

## 8. GeoIP

- Drop the free MaxMind `.mmdb` databases into a directory, register it under `Preferences → Name Resolution → MaxMind database directories`.
- Then **Statistics → Endpoints → IPv4 → Map** plots endpoints geographically, and `ip.geoip.country` becomes filterable.
- Geolocation is a *hint*, not a fact — anycast, VPNs, and CDNs all lie.

---

## Daily workflows

### "Something is slow"
```text
1. Filter to the conversation (right-click → Conversation Filter)
2. Time column → seconds-since-start; scan for jumps, or sort a delta column
3. Set Time Reference on the request; read time-to-response directly
4. Expert Information: retransmissions/zero-window near the gap?
```

### "Unknown pcap, first five minutes"
```text
1. Capture File Properties — when, how long, drops?
2. Protocol Hierarchy — anything present that has no business here?
3. Conversations — sort by bytes; eyeball Relative Start/Duration bars
4. I/O Graph — bursts or metronome regularity?
5. Then, and only then, packets — with [[Packet-Capture Augury]] open
```

## Files & locations

| Path | What |
| --- | --- |
| `~/.config/wireshark/profiles/<name>/` | per-profile config (Linux) |
| `%APPDATA%\Wireshark\profiles\<name>\` | per-profile config (Windows) |
| `hosts` (inside a profile dir) | offline name resolution, no DNS leak |
| `colorfilters`, `dfilters` | coloring rules, saved display filters |

## Gotchas / Golden rules

1. **Capture filters and display filters are different languages** — BPF (`host`, `port`) at capture, field syntax (`ip.addr ==`) at display. Mixing them is the #1 beginner syntax error.
2. **`ip.addr != x` doesn't do what you think** — a packet has two addresses; one of them is always `!= x`. Use `!(ip.addr == x)`.
3. **Network name resolution phones home.** Off during investigations; hosts-file if you need labels.
4. **Time of day is the viewer's timezone.** Share trace files with UTC display or share confusion.
5. **A capture without dropped-packet stats is not evidence of absence** — check Capture File Properties before declaring "it's not in the trace"; if the kernel dropped frames, it may have been.
6. **Statistics before packets.** The trace tells you where to look; don't scroll 30 000 packets hoping.
