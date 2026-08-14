---
type: cheatsheet
area: "Networking & Protocols"
aliases: [dumpcap, capinfos, mergecap, editcap]
tags: [networking, pcap, cli, analysis]
status: draft
---

# tshark

> **Area:** [[Networking & Protocols]]

Wireshark's command-line family: `dumpcap` to capture, `tshark` to read/filter/extract, `capinfos`/`mergecap`/`editcap` to inspect and reshape trace files. GUI analysis lives in [[wireshark]].

> All of these install alongside Wireshark. If the shell can't find them, the Wireshark install directory isn't on `PATH` (typical on Windows: `C:\Program Files\Wireshark`; macOS: `/Applications/Wireshark.app/Contents/MacOS`).

---

## 1. dumpcap — capture, nothing else

`dumpcap` is the capture engine Wireshark itself uses. On servers and high-throughput links, capture with `dumpcap` (cheap, headless, stable) and analyze elsewhere.

```bash
dumpcap -D                        # list interfaces with index numbers — don't guess
dumpcap -i 1 -w /path/to/out.pcapng        # capture interface 1 to file
dumpcap -i eth0 -f "port 53" -w dns.pcapng # BPF capture filter — dumpcap filters are BPF, not display syntax
dumpcap -i eth0 -s 128 -w hdrs.pcapng      # snaplen: headers only, when payloads don't matter (or mustn't be stored)
```

**Ring buffer — the always-on flight recorder:**

```bash
# rotate at 100 MB per file, keep 10 files (~1 GB cap), overwrite oldest:
dumpcap -i eth0 -w /var/cap/ring.pcapng -b filesize:100000 -b files:10
# rotate by time instead: new file every hour
dumpcap -i eth0 -w /var/cap/ring.pcapng -b duration:3600 -b files:24
```

Ring buffers are how you capture "until the problem happens" without filling the disk — when the incident hits, stop the capture and the last N files hold the window around it.

## 2. tshark — read, filter, extract

```bash
tshark -r trace.pcapng                          # print packets (like the GUI packet list)
tshark -r trace.pcapng -Y "dns"                 # -Y = display filter (Wireshark syntax, not BPF)
tshark -r trace.pcapng -Y "tcp.flags.syn==1 && tcp.flags.ack==0" -c 50   # first 50 matches
tshark -r trace.pcapng -Y "http.request" -T fields -e frame.time -e ip.src -e http.host -e http.request.uri
                                                # field extraction — the pcap-to-CSV workhorse
tshark -r trace.pcapng -T fields -e dns.qry.name | sort | uniq -c | sort -rn | head
                                                # instant "top queried names" — augury staple
tshark -r trace.pcapng -q -z conv,ip            # conversations table, no packet dump (-q)
tshark -r trace.pcapng -q -z io,phs             # protocol hierarchy statistics
tshark -r trace.pcapng -q -z http,tree          # HTTP request/response breakdown
tshark -r trace.pcapng -q -z follow,tcp,ascii,3 # follow TCP stream #3 in the terminal
```

`tshark` can also capture (`-i`), but prefer `dumpcap` for that job — less code between the wire and the file.

## 3. capinfos / mergecap / editcap — file surgery

```bash
capinfos trace.pcapng             # duration, packet count, rates, hash-worthy metadata — ALWAYS first look
mergecap -w all.pcapng a.pcapng b.pcapng       # merge (interleaves by timestamp)
editcap -A "2026-01-01 10:00:00" -B "2026-01-01 10:05:00" big.pcapng window.pcapng
                                                # cut a time window out of a big trace
editcap -c 100000 big.pcapng chunk.pcapng      # split into 100k-packet chunks
editcap -d dup.pcapng dedup.pcapng             # remove exact duplicates (SPAN ports love duplicating)
```

---

## Daily workflows

### "Capture on a headless server, analyze on the laptop"
```bash
# on the server — ring buffer, tight BPF, headers if payload isn't needed:
dumpcap -i eth0 -f "host 203.0.113.7" -b filesize:50000 -b files:6 -w /tmp/case.pcapng
# then transfer the file(s) and open in wireshark locally.
# capturing needs privileges: put the operator in the wireshark group / grant cap_net_raw to dumpcap —
# never run the whole GUI as root.
```

### "Is it in this 5 GB trace at all?"
```bash
capinfos big.pcapng                                   # orient: when, how long, how much
tshark -r big.pcapng -q -z conv,ip | head -30          # who talks to whom
tshark -r big.pcapng -Y "ip.addr == 203.0.113.7" -w suspect.pcapng   # carve the relevant slice
```

## Gotchas / Golden rules

1. **Two filter languages, again**: `-f` (and all of dumpcap) = BPF capture filter; `-Y` = Wireshark display filter. Same trap as the GUI, same fix: capture broad, display narrow.
2. **Unbounded `-w` on a server is a disk-full incident scheduled for later.** Ring buffer (`-b`) is the default posture, not the special case.
3. **Capture privileges ≠ root analysis.** `dumpcap` alone needs the elevated rights; keep tshark/wireshark unprivileged.
4. **`-q` with `-z`** — without `-q`, tshark dumps every packet *and then* the statistics you actually wanted.
5. **SPAN ports duplicate packets** — `editcap -d` before drawing conclusions from retransmission counts.
