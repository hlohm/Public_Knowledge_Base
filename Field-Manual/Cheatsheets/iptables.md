---
type: cheatsheet
area: Networking & Protocols
aliases: [ip6tables, netfilter, netfilter-persistent, iptables-persistent]
tags: [firewall, networking, netfilter, security]
status: working
---

# iptables

> **Area:** [[Networking & Protocols]]

Daily-use reference for `iptables`/`ip6tables` packet filtering on a Linux host — inspecting,
adding, ordering and **persisting** rules with `netfilter-persistent`. For the host-firewall
layer that sits *below* an appliance firewall, and the partner to [[fail2ban]] (which injects
its ban rules straight into these chains).

> Almost everything here needs root. On modern distros `iptables` is usually a shim over the
> **nftables** backend (`iptables-nft`) — the commands below work unchanged; see Gotchas for the
> one place it matters. IPv4 and IPv6 are **separate rulesets** — every rule you write for
> `iptables` you must mirror in `ip6tables` or leave a v6 hole.

---

## 1. Mental model (tables → chains → rules)

Packets traverse **chains**; each chain is an ordered list of **rules**; the **first match
wins** and its target (`-j`) decides the packet's fate. Chains live in **tables**:

| Table | What it's for | Chains you'll touch |
| --- | --- | --- |
| `filter` (default) | allow/deny — the firewall | `INPUT`, `OUTPUT`, `FORWARD` |
| `nat` | address/port translation | `PREROUTING`, `POSTROUTING` |
| `mangle` | packet header rewriting (TTL, marks) | rarely, by hand |
| `raw` | conntrack exemptions (`NOTRACK`) | rarely |

- `INPUT` — packets destined **for this host**. (Your SSH lockout risk lives here.)
- `OUTPUT` — packets **originating from this host**.
- `FORWARD` — packets **routed through** this host (gateways, NAT boxes, containers).
- **Policy** — a chain's fallback when no rule matches (`ACCEPT` or `DROP`).

---

## 2. Inspect what's loaded

```bash
# The filter table, numeric (no DNS/port-name lookups = fast), verbose, with rule numbers
sudo iptables -L -n -v --line-numbers

# A specific chain only
sudo iptables -L INPUT -n -v --line-numbers

# The NAT table (port forwards, masquerade)
sudo iptables -t nat -L -n -v --line-numbers

# The complete ruleset in restore format (the real source of truth — copy/paste/save-able)
sudo iptables-save
sudo ip6tables-save                # IPv6 is a SEPARATE ruleset — always check it too

# Per-rule packet/byte counters (is a rule actually matching traffic?)
sudo iptables -L INPUT -n -v       # pkts/bytes columns on the left
sudo iptables -Z                   # zero the counters to watch fresh
```

---

## 3. Add, order, remove rules

Order is everything — the first matching rule wins, so **placement** matters more than the rule
itself.

```bash
# -A append to END of chain;  -I insert at TOP (or at position N)
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT          # appended last
sudo iptables -I INPUT 1 -p tcp --dport 443 -j ACCEPT       # inserted as rule #1

# -D delete: by exact spec, or by rule number (numbers shift after each delete!)
sudo iptables -D INPUT -p tcp --dport 80 -j ACCEPT          # by spec (safe, unambiguous)
sudo iptables -D INPUT 3                                    # by number (re-list between deletes)

# -R replace rule N in place
sudo iptables -R INPUT 2 -p tcp --dport 22 -s 203.0.113.0/24 -j ACCEPT

# -F flush a chain (REMOVES RULES, does NOT change policy — see the lockout warning in §7)
sudo iptables -F INPUT

# -P set the default policy for a chain
sudo iptables -P INPUT DROP
```

---

## 4. The canonical default-deny INPUT ruleset

The standard safe skeleton — accept the things that must work, then drop the rest. **Order as
shown**; the SSH allow must exist before the policy flips to DROP.

```bash
sudo iptables -A INPUT -i lo -j ACCEPT                                          # loopback, always
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT     # replies to our own traffic
sudo iptables -A INPUT -m conntrack --ctstate INVALID -j DROP                   # malformed/oddball
sudo iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT               # ping (optional)
sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -j ACCEPT   # SSH (scope with -s!)
# ...your other service allows here...
sudo iptables -P INPUT DROP                                                     # default-deny LAST
sudo iptables -P FORWARD DROP                                                   # not a router? drop it
```

Tighten the SSH rule to a source range whenever you can: `-s 203.0.113.0/24` on the `--dport 22`
line turns "open to the internet" into "open to my admin network".

```bash
# Poor-man's rate limit (a crude fail2ban substitute for SSH brute-force) using the recent module
sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set --name SSH
sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW \
     -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP
# For real log-driven banning with backoff, use [[fail2ban]] instead.
```

---

## 5. NAT (forwarding & masquerade)

```bash
# Enable forwarding first (and persist it in /etc/sysctl.d/ to survive reboot)
sudo sysctl -w net.ipv4.ip_forward=1

# MASQUERADE — share one egress IP (SNAT for a dynamic WAN address)
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# DNAT — forward an inbound port to an internal host (needs the matching FORWARD allow)
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 8080 \
     -j DNAT --to-destination 10.0.0.5:80
sudo iptables -A FORWARD -p tcp -d 10.0.0.5 --dport 80 \
     -m conntrack --ctstate NEW -j ACCEPT
```

---

## 6. Persistence — netfilter-persistent (the part that bites)

**Runtime rules are lost on reboot.** They live in kernel memory until you save them to disk and
arrange for reload at boot. On Debian/Ubuntu that's the `netfilter-persistent` framework (pulled
in by the `iptables-persistent` package).

```bash
# One-time install (the prompt offers to save current rules immediately)
sudo apt install iptables-persistent       # provides netfilter-persistent + the boot service

# SAVE the live ruleset to disk — run this after EVERY change you want to keep
sudo netfilter-persistent save             # writes /etc/iptables/rules.v4 AND rules.v6

# Reload the saved rules now (e.g. after hand-editing the files)
sudo netfilter-persistent reload

# The boot service that restores them
systemctl status netfilter-persistent.service
```

Under the hood it's just `iptables-save`/`iptables-restore` to fixed files — you can do it by
hand on any distro:

```bash
sudo iptables-save  | sudo tee /etc/iptables/rules.v4 >/dev/null
sudo ip6tables-save | sudo tee /etc/iptables/rules.v6 >/dev/null
sudo iptables-restore < /etc/iptables/rules.v4         # reload manually
```

> **Cloud-host double firewall (e.g. Oracle/OCI, AWS):** the provider's network ACL / security
> list is a **separate layer** from on-instance iptables — a port must be open in **both**. And
> the instance rules vanish on reboot unless you `netfilter-persistent save`. Two independent
> places to get wrong; check both when "the port is open but nothing connects" or "it worked
> until I rebooted".

---

## 7. Editing rules over SSH without locking yourself out

`-P INPUT DROP` + a flushed or wrong allow rule = instant, total lockout with no console. Treat
every remote firewall edit as the dangerous operation it is.

- [ ] **Snapshot the working ruleset first**, so you can restore blind:
      ```bash
      sudo iptables-save > /root/iptables.good
      ```
- [ ] **Arm a dead-man's-switch** that reverts in N minutes unless you cancel it (survives a
      lockout because it's already scheduled):
      ```bash
      echo 'iptables-restore < /root/iptables.good' | sudo at now + 5 minutes
      ```
- [ ] **Make your changes.** Keep the SSH allow rule intact; never `-F` a chain whose policy is
      `DROP` while connected remotely.
- [ ] **Open a SECOND ssh session** to the host *without closing the first*. If the new session
      connects, the rules are sane.
- [ ] **Persist** only after the second session proves it: `sudo netfilter-persistent save`.
- [ ] **Cancel the dead-man's-switch:** `sudo atq` then `sudo atrm <job-id>`.
- [ ] If you DID lock yourself out: wait for the `at` job to fire, or use the provider's serial /
      VNC console to `iptables-restore < /root/iptables.good`.

---

## 8. Daily workflows

### "Is this port actually open at the host firewall?"
```bash
sudo iptables -L INPUT -n -v --line-numbers | grep -E 'dpt:<port>|ACCEPT'
sudo iptables-save | grep -- '--dport <port>'
# remember to check the v6 side and the cloud security list too
```

### "Block a single abusive IP right now"
```bash
sudo iptables -I INPUT 1 -s 203.0.113.66 -j DROP    # top of chain = takes effect immediately
sudo netfilter-persistent save                      # keep it across reboot
```

### "Temporarily open a port for a test, then revert"
```bash
sudo iptables -I INPUT -p tcp --dport 9000 -j ACCEPT   # do NOT save → gone on reboot
# ...test...
sudo iptables -D INPUT -p tcp --dport 9000 -j ACCEPT   # or just reboot / netfilter-persistent reload
```

### "What's hitting my DROP rule?"
```bash
sudo iptables -Z INPUT                                  # zero counters
# ...wait...
sudo iptables -L INPUT -n -v --line-numbers             # watch the pkts column on the drop rule
```

---

## 9. Files & locations

| Path | Purpose |
| --- | --- |
| `/etc/iptables/rules.v4` | persisted IPv4 ruleset (loaded at boot) |
| `/etc/iptables/rules.v6` | persisted IPv6 ruleset — **don't forget this one** |
| `/etc/sysctl.d/*.conf` | persist `net.ipv4.ip_forward` and friends |
| `/usr/share/netfilter-persistent/plugins.d/` | save/restore plugin hooks |
| `man iptables`, `man iptables-extensions` | match/target reference (conntrack, recent, limit…) |

---

## Gotchas / Golden rules

1. **First match wins; order is the rule.** A correct rule below a broad `DROP` never runs. Use
   `-I` to place, not just `-A` to pile on.
2. **Runtime ≠ persisted.** Nothing survives reboot until `netfilter-persistent save` (or a
   manual `iptables-save` to `/etc/iptables/rules.v4`).
3. **IPv4 and IPv6 are separate firewalls.** A v4-only ruleset on a dual-stack host is an open v6
   door. Mirror every rule in `ip6tables` and save `rules.v6`.
4. **`-F` does not touch policy.** Flushing allow rules while policy is `DROP` locks you out.
   Always work behind the dead-man's-switch in §7.
5. **Cloud hosts have two firewalls.** Provider security list **and** instance iptables — a port
   needs opening in both, and the instance side must be persisted.
6. **`iptables` may be nftables underneath.** On `iptables-nft` systems, don't mix raw `nft`
   rules and `iptables` rules in ways that fight; pick one tool per host. `iptables -L` won't show
   native `nft` rules added outside the shim — use `nft list ruleset` to see the whole picture.
7. **Scope SSH by source where you can.** `-s <admin-range>` on the port-22 allow shrinks the
   attack surface from "the internet" to "my network".

## Further reading
- [iptables(8)](https://man7.org/linux/man-pages/man8/iptables.8.html) ·
  [iptables-extensions(8)](https://man7.org/linux/man-pages/man8/iptables-extensions.8.html) ·
  [netfilter-persistent](https://manpages.debian.org/netfilter-persistent) ·
  [Arch Wiki: iptables](https://wiki.archlinux.org/title/Iptables)
