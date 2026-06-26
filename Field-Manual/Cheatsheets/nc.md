---
type: cheatsheet
area: Networking & Protocols
aliases: [netcat, ncat]
tags: [networking, tcp, udp, debugging]
status: working
---

# nc

> **Area:** [[Networking & Protocols]]

The "TCP/IP Swiss Army knife": read and write raw TCP/UDP from the command line. The
everyday uses are connectivity testing, port checks, banner grabbing, ad-hoc listeners, and
quick file transfer. Pairs with [[ssh]] (for anything that needs to be secure, tunnel over
ssh instead) and [[curl]] for HTTP specifically.

> **There are several incompatible `nc` implementations — flags differ.** Know which one you
> have before trusting a flag (see §1). This is the single biggest source of "the cheat sheet
> said X but it didn't work."

---

## 1. Which `nc` am I running?

```bash
nc -h 2>&1 | head -1        # the help banner usually names the variant
readlink -f "$(command -v nc)"   # is it really ncat, busybox, etc.?
```

| Variant | Package / source | Notes |
| --- | --- | --- |
| **OpenBSD netcat** | `netcat-openbsd` — the default `nc` on most modern Linux | Listen as `nc -l PORT` (no `-p`); **no `-e`** (command exec removed by design — §8) |
| **traditional / GNU** | `netcat-traditional` | Listen as `nc -l -p PORT`; may have `-e` only if built with it |
| **ncat** | ships with **Nmap** | Modern; adds `--ssl`, `--exec`, `--allow`/`--deny`. The recommended one |
| **busybox nc** | embedded / containers / Alpine | Minimal subset; expect missing flags |

The examples below note where OpenBSD vs traditional syntax diverges.

---

## 2. Connectivity & port testing

```bash
# Is a TCP port open? -z = zero-I/O scan mode, -v = verbose, -w = timeout (seconds)
nc -zv host 22
nc -zv -w 3 host 443

# Scan a small range of ports (OpenBSD nc supports ranges)
nc -zv host 20-30

# UDP instead of TCP
nc -zuv host 53

# Quick "can this box reach that service at all?" from inside a container/jump host
nc -zv db.internal 5432 && echo reachable || echo blocked
```

`-z` is great for TCP but **unreliable for UDP**: UDP is connectionless, so a silent port can
look "open." Treat `nc -zu` results as a hint, not proof (§9).

---

## 3. Talking to a service / banner grabbing

```bash
# Interactive: connect and type at the service (Ctrl-C to quit)
nc -v host 25            # SMTP — it greets you with its banner; type EHLO host

# Non-interactive HTTP probe (prefer curl for real HTTP work — see [[curl]])
printf 'HEAD / HTTP/1.0\r\n\r\n' | nc -w 3 host 80

# Grab whatever a service announces on connect
nc -w 2 host 22 </dev/null     # e.g. an SSH version string
```

The `\r\n\r\n` matters for HTTP — many servers ignore bare `\n` line endings.

---

## 4. Listeners & a throwaway server

```bash
# Listen on a port (OpenBSD nc):           nc -lv 1234
# Listen on a port (traditional nc):       nc -lvp 1234
# -k (where supported) keeps listening after a client disconnects:
nc -lvk 1234

# One-shot "is anything able to reach me on this port?" test:
# terminal A (server):   nc -lv 8080
# terminal B (client):   nc -v <server-ip> 8080      # then type — text appears on A
```

Use a listener to validate firewall/security-group rules end to end: open a listener on the
target host, connect from where traffic should originate, and watch whether bytes arrive.

---

## 5. File transfer (quick, unencrypted)

The classic sender/receiver pair. **Start the receiver first.**

```bash
# Receiver (the machine that will hold the file):
nc -l 1234 > received.bin            # OpenBSD;  traditional: nc -l -p 1234 > received.bin

# Sender:
nc <receiver-ip> 1234 < tofile.bin
```

```bash
# Send a directory by piping tar through the socket
# Receiver:
nc -l 1234 | tar xzvf -
# Sender:
tar czf - ./dir | nc <receiver-ip> 1234
```

On **traditional** netcat the sender may not close after EOF — add `-q 0` (`nc -q 0 host 1234 < file`)
so it quits when the input ends. This is plaintext with no auth or integrity; for anything
real, use `scp`/`rsync` over [[ssh]] instead.

---

## 6. ncat (the modern replacement)

If you have Nmap's `ncat`, it covers the same ground with TLS and access control built in:

```bash
ncat -lv 1234                         # listen
ncat --ssl -lv 8443                   # TLS-wrapped listener
ncat --ssl host 8443                  # TLS client (test an HTTPS endpoint's handshake)
ncat -lv --allow 10.0.0.5 1234        # only accept from one host
ncat -lvk 1234                        # keep listening across connections
```

Prefer `ncat` when you need encryption or to restrict who can connect — plain `nc` does
neither.

---

## 7. Daily workflows

### "Is this port actually open / reachable from here?"
```bash
nc -zv -w 3 host 443    # exit status 0 = open; non-zero = closed/filtered
```

### "Is something listening locally, and can I poke it?"
```bash
ss -tlnp | grep ':8080'      # confirm a local listener exists (see [[Linux Administration]])
nc -v localhost 8080         # then actually talk to it
```

### "Move a file between two hosts on a trusted LAN, no ssh set up"
```bash
# receiver:  nc -l 1234 > out.bin
# sender:    nc <receiver-ip> 1234 < in.bin
```

### "Does this firewall rule work?"
```bash
# on the destination host:   nc -lv 9000
# from the source host:      nc -zv <dest-ip> 9000
```

---

## 8. Command execution & shells — what a defender needs to know

Traditional netcat (and `ncat --exec`/`--sh-exec`) can wire a program's stdin/stdout/stderr to
the socket via `-e`. That single capability is the basis of netcat **bind shells** (a listener
that hands callers a shell) and **reverse shells** (a host that connects *outbound* and serves a
shell to a remote listener). Because it's so easily abused, **`netcat-openbsd` omits `-e`
entirely** — its absence on your default `nc` is a feature, not a missing flag.

You don't need the payloads to defend against them; you need to recognize and block the
pattern:

- **Reverse shells are outbound**, which is why attackers favor them — they sail past
  inbound firewall rules. Defense is **egress filtering** and monitoring unexpected outbound
  connections to odd high ports.
- **Spot the indicators:** an `nc`/`ncat` process running with `-e`/`--exec`, an unexpected
  listener (`ss -tlnp` showing `nc`), or `nc` invoked with a remote host + a shell. Command-line
  auditing (auditd/EDR, Sysmon on Windows) catches these — `nc` showing up at all on a server
  that shouldn't have it is itself a signal.
- **Reduce the surface:** don't ship `nc` on production hosts that don't need it; prefer the
  no-`-e` OpenBSD build; restrict with `ncat --allow`/`--deny` when a listener is legitimate.

For the attacker-technique catalogue behind this, the MITRE ATT&CK and LOLBAS references in your
[[IT-Dictionary]] are the right home; this sheet stays on detection and hardening.

---

## 9. Gotchas / Golden rules

1. **Check your variant first (§1).** OpenBSD `nc -l 1234` vs traditional `nc -l -p 1234` is the
   most common "why won't it listen" trap. `-p` on OpenBSD nc sets the *source* port for an
   outbound connection, not the listen port.
2. **`-z` is unreliable for UDP.** A silent UDP port looks open. Confirm with an actual probe or
   a tool built for UDP.
3. **Always set `-w`** on scripted connections — without a timeout, `nc` can hang indefinitely on
   a filtered port.
4. **`nc` is plaintext, unauthenticated, no integrity.** Fine for LAN debugging and tests; for
   real transfers use `scp`/`rsync` over [[ssh]], and for HTTP use [[curl]].
5. **Start the receiver before the sender** in file-transfer and chat setups.
6. **Don't leave listeners running.** A forgotten `nc -lk` is an open door — and on a server, an
   unexplained `nc` listener is exactly what your own §8 monitoring should flag.

## Further reading
- [ncat(1)](https://nmap.org/ncat/guide/index.html) (Nmap's netcat) ·
  `man nc` on your box (read it — it tells you *which* variant you have)
