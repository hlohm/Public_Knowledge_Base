---
type: cheatsheet
area: "Networking & Protocols"
aliases: [bpf]
tags: [networking, pcap, cli, analysis]
status: draft
---

# tcpdump

> **Area:** [[Networking & Protocols]]

The ubiquitous capture tool — on every Linux box, BSD, firewall, and appliance you'll ever SSH into, including the ones where nothing else is installed. Capture here, analyze in [[wireshark]]; its filter language is BPF, the same one [[tshark]]/`dumpcap` use with `-f`. Reading the results with intent: [[Packet-Capture Augury]].

---

## 1. The invocation you actually want

```bash
tcpdump -i eth0 -nn -w out.pcap        # capture to file: -nn = no name/port resolution (fast, no DNS leak)
tcpdump -i any -nn                      # all interfaces (Linux; cooked capture — L2 info degraded)
tcpdump -D                              # list interfaces, same idea as dumpcap -D
tcpdump -r out.pcap -nn                 # read a file back
tcpdump -i eth0 -nn -c 100              # stop after 100 packets — always cap live peeking
```

- **`-nn` by default.** Without it tcpdump resolves names and ports — slow, and it fires DNS queries from the capture box (same OPSEC point as [[wireshark]] §name-resolution).
- `-s 0` (full snaplen) is the default on modern tcpdump; only set `-s` to *truncate* deliberately.

## 2. BPF filters — the language

```bash
tcpdump -i eth0 -nn host 203.0.113.7            # to or from
tcpdump -i eth0 -nn src host 203.0.113.7        # direction-specific
tcpdump -i eth0 -nn net 10.0.0.0/8              # whole range
tcpdump -i eth0 -nn port 53                     # src or dst port
tcpdump -i eth0 -nn portrange 8000-8080
tcpdump -i eth0 -nn tcp and port 443            # protocol qualifier
tcpdump -i eth0 -nn 'port 25 or port 465 or port 587'   # mail triage
tcpdump -i eth0 -nn 'host 203.0.113.7 and not port 22'  # mute your own SSH session — the classic
```

Combine with `and`/`or`/`not`, group with parentheses (quote them from the shell). **This is capture filtering — discarded packets are gone forever**; when investigating, prefer broad capture + display-filter later ([[wireshark]] §capture).

**TCP flag surgery (the part nobody remembers):**

```bash
tcpdump -i eth0 -nn 'tcp[tcpflags] & (tcp-syn) != 0 and tcp[tcpflags] & (tcp-ack) == 0'
                                                # SYNs only — connection attempts / scan view
tcpdump -i eth0 -nn 'tcp[tcpflags] & (tcp-rst) != 0'      # resets
tcpdump -i eth0 -nn 'tcp[tcpflags] == 0'                  # null scan packets
tcpdump -i eth0 -nn 'icmp[icmptype] == icmp-echo'         # pings only
```

## 3. Output control (live reading)

```bash
tcpdump -i eth0 -nn -v            # more header detail (-vv, -vvv escalate)
tcpdump -i eth0 -nn -A            # payload as ASCII — cleartext protocols readable on the spot
tcpdump -i eth0 -nn -X            # hex + ASCII — when it isn't cleartext
tcpdump -i eth0 -nn -q            # terse one-liners — rhythm-watching mode
tcpdump -r out.pcap -nn -tttt     # absolute timestamps with date when reading back
```

## 4. Rotation & long captures

```bash
tcpdump -i eth0 -nn -w ring.pcap -C 100 -W 10        # rotate at 100 MB, keep 10 files (ring)
tcpdump -i eth0 -nn -w day-%H.pcap -G 3600           # new file each hour, strftime name
tcpdump -i eth0 -nn -w out.pcap -Z tcpdump           # drop privileges after opening the capture
```

Same flight-recorder pattern as `dumpcap -b` ([[tshark]] §1) — on boxes where only tcpdump exists.

---

## Daily workflows

### "Is the traffic even arriving?" (the 30-second answer)
```bash
tcpdump -i eth0 -nn -c 20 'host 203.0.113.7 and port 443'
# packets appear → network path is fine, problem is above L4.
# nothing → walk the path: try the far side, the gateway, the firewall.
```

### "Capture on an appliance, analyze at the desk"
```bash
tcpdump -i eth0 -nn -w /tmp/case.pcap -C 50 -W 4 'host 203.0.113.7'   # bounded ring, tight filter
# scp it back, open in wireshark. On very thin boxes, stream instead:
ssh <host> "tcpdump -i eth0 -nn -w - 'port 53'" | wireshark -k -i -    # live remote capture into the GUI
```

## Gotchas / Golden rules

1. **Mute your own session** (`not port 22`) or the capture of your SSH traffic generates SSH traffic generates capture — the feedback loop fills the terminal instantly.
2. **Capture filters are unforgiving** — what BPF drops never existed. Tight filters for targeted questions, broad + bounded (`-C`/`-W`) for investigations.
3. **`-i any` loses L2** (Linux cooked mode) — fine for "is it arriving", wrong for ARP/VLAN questions.
4. **Resolution off (`-nn`), timestamps explicit (`-tttt`)** when output feeds a report — same evidence discipline as everywhere else.
5. **VLAN tags bite**: on trunk interfaces `vlan and host x` vs `host x` return different worlds; if a filter mysteriously matches nothing on a trunk, add `vlan`.
6. **Unbounded `-w` is the same disk-full incident** as [[tshark]] warns about — `-C`/`-W` or `-G` always, on anything long-running.
