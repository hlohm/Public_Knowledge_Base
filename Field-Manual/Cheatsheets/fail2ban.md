---
type: cheatsheet
area: Networking & Protocols
aliases: [fail2ban-client, jail.local, fail2ban-regex]
tags: [security, firewall, intrusion-prevention, ssh]
status: working
---

# fail2ban

> **Area:** [[Networking & Protocols]]

Daily-use reference for `fail2ban` — log-driven, automatic IP banning — with the jail config
options that actually matter and the operational commands to inspect, test and unban. Bans are
enforced through the firewall, so this pairs directly with [[iptables]]; the SSH log source ties
it to [[ssh]].

> Config edits go in `*.local` files, **never** the shipped `*.conf` (those are overwritten on
> upgrade — same discipline as systemd drop-ins). `enabled = true` is required per jail; nothing
> is on by default. After any edit: `fail2ban-client reload`.

---

## 1. Mental model (jail → filter → action)

A **jail** ties together three things and a threshold:

```
log source ──► FILTER (regex) ──► counts a "failure"
                                      │
            maxretry failures within findtime
                                      ▼
                                   ACTION  ──► ban the IP for bantime (via the firewall)
```

- **Filter** (`/etc/fail2ban/filter.d/*.conf`) — regexes that recognise a failed attempt in a
  log line and extract the offending IP (`<HOST>`).
- **Action** (`/etc/fail2ban/action.d/*.conf`) — what to do on a ban; default is inserting a
  firewall drop rule.
- **Jail** (`/etc/fail2ban/jail.d/*.local`) — binds a filter + log source + action + the
  `maxretry`/`findtime`/`bantime` thresholds, and switches it on.

---

## 2. fail2ban-client — operations

```bash
# Is it running, and which jails are active?
sudo fail2ban-client status

# Detail for one jail: currently failed, currently banned, total counts, the ban list
sudo fail2ban-client status sshd

# Reload after config changes (all jails, or just one)
sudo fail2ban-client reload
sudo fail2ban-client reload sshd

# Unban an address (per-jail, or globally across all jails on newer versions)
sudo fail2ban-client set sshd unbanip 203.0.113.66
sudo fail2ban-client unban 203.0.113.66
sudo fail2ban-client unban --all

# Manually ban an address in a jail
sudo fail2ban-client set sshd banip 203.0.113.66

# Inspect/adjust a live parameter without editing files (lost on reload — for testing)
sudo fail2ban-client get sshd bantime
sudo fail2ban-client set sshd bantime 3600
```

---

## 3. Config layout — where to put things

```bash
# Precedence (later wins): jail.conf  <  jail.d/*.conf  <  jail.local  <  jail.d/*.local
#   - NEVER edit jail.conf (upgrade clobbers it)
#   - global defaults  -> jail.local  [DEFAULT] section
#   - per-service jails -> jail.d/<service>.local   (tidiest; one file per jail)

# A minimal global jail.local
sudoedit /etc/fail2ban/jail.local
```

```ini
[DEFAULT]
# Never ban yourself: loopback + your admin/VPN ranges. THE most important line here.
ignoreip = 127.0.0.1/8 ::1 10.0.0.0/24

bantime  = 1h            # how long a ban lasts
findtime = 10m           # the sliding window failures are counted in
maxretry = 5             # failures within findtime that trigger a ban

# Escalating bans: each repeat offence multiplies bantime (great against persistent scanners)
bantime.increment = true
bantime.factor    = 2
bantime.maxtime   = 1w

# Read logs from the systemd journal rather than files (see §5 — required for modern OpenSSH)
backend   = systemd
banaction = iptables-multiport      # use nftables-multiport on nft-only hosts
```

---

## 4. The jail options that matter

| Option | What it does | Notes / gotcha |
| --- | --- | --- |
| `enabled` | turns the jail on | **required** — nothing runs without it |
| `filter` | which `filter.d` regex set to use | defaults to the jail's name |
| `port` | port(s) the ban action blocks | `ssh`, a number, or `0:65535` for all |
| `logpath` | log file(s) to watch | ignored when `backend = systemd` |
| `backend` | log source: `auto`/`systemd`/`pyinotify` | `systemd` reads journald — see §5 |
| `journalmatch` | narrows the journal query | e.g. `_SYSTEMD_UNIT=ssh.service` |
| `maxretry` | failures before a ban | per the jail's `findtime` window |
| `findtime` | the counting window | failures outside it don't accumulate |
| `bantime` | ban duration | `-1` = permanent (use sparingly) |
| `bantime.increment` | exponential backoff on repeat offenders | with `.factor` / `.maxtime` |
| `ignoreip` | never-ban allowlist | **add your own subnets / VPN** here |
| `action` / `banaction` | how the ban is enforced | `iptables-multiport`, `nftables-*`, etc. |
| `mode` | filter aggressiveness (sshd: `normal`/`ddos`/`aggressive`) | aggressive catches more, risks false positives |

---

## 5. The OpenSSH 9.8+ `sshd-session` trap

OpenSSH 9.8 split the daemon: the listener stays `sshd`, but each connection is handled by a
separate **`sshd-session`** (and `sshd-auth`) process — and that's where auth-failure lines now
come from. The consequences for fail2ban:

- The **file/syslog backend** keys on the program name in the log prefix. Lines tagged
  `sshd-session` don't match an older `sshd` filter's prefix, so **failures go uncounted and
  nothing gets banned** — silently. The jail looks healthy; it just never fires.
- **The fix has two parts, both required:**
  1. **fail2ban ≥ 1.1.0** — its `sshd` filter was updated to recognise `sshd-session`/`sshd-auth`.
  2. **`backend = systemd`** — matching the journal on the *unit* (`_SYSTEMD_UNIT=ssh.service`)
     catches everything the SSH unit emits, regardless of which child process logged it.

```bash
# Check your version against the 1.1.0 floor
fail2ban-client version

# Verify the jail is on the systemd backend and actually counting failures
sudo fail2ban-client get sshd logencoding   # sanity that the jail loaded
sudo fail2ban-client status sshd            # "Currently failed" should rise during a brute-force
```

> If `status sshd` shows zero failures while `journalctl -u ssh -g 'Failed password'` clearly
> shows attempts, you're hitting this trap (or a filter mismatch) — go straight to §6.

---

## 6. Testing a filter (why isn't it banning?)

`fail2ban-regex` replays a log source through a filter and reports exactly what matched. This is
*the* debugging tool — use it before touching thresholds.

- [ ] **Run the filter against the real log** and read the match count:
      ```bash
      # File backend:
      sudo fail2ban-regex /var/log/auth.log /etc/fail2ban/filter.d/sshd.conf
      # systemd backend (replay the journal for the ssh unit):
      sudo fail2ban-regex "systemd-journal[journalmatch='_SYSTEMD_UNIT=ssh.service']" sshd
      ```
- [ ] **Read "Lines: matched / missed".** Matched 0 with known failures present → filter/backend
      mismatch (often the §5 trap), not a threshold problem.
- [ ] **Confirm the source actually has failures:**
      ```bash
      sudo journalctl -u ssh --since "1 hour ago" -g "Failed|Invalid"
      ```
- [ ] **Check the jail loaded the filter you think it did:** `sudo fail2ban-client status sshd`
      → the *Filter* / *File list* / *Journal match* lines.
- [ ] **Watch the ban land** after fixing: re-trigger, then `status sshd` → "Currently banned" > 0,
      and confirm the firewall rule appeared:
      ```bash
      sudo iptables -L -n | grep f2b      # fail2ban's chain holds the active bans
      ```

---

## 7. Daily workflows

### "Did someone get banned overnight?"
```bash
sudo fail2ban-client status sshd                       # currently/total banned
sudo journalctl -u fail2ban --since yesterday -g Ban
```

### "I locked myself / a colleague out"
```bash
sudo fail2ban-client set sshd unbanip <ip>
# then ADD their range to ignoreip in jail.local so it can't recur
```

### "Harden the ssh jail" (drop-in)
```bash
sudoedit /etc/fail2ban/jail.d/sshd.local
```
```ini
[sshd]
enabled  = true
backend  = systemd
mode     = aggressive
maxretry = 3
findtime = 10m
bantime  = 1h
bantime.increment = true
```
```bash
sudo fail2ban-client reload sshd
```

### "Protect a service that has no shipped filter"
```bash
# Write a filter.d/<name>.conf with a failregex containing <HOST>, test it with fail2ban-regex,
# then add a matching jail.d/<name>.local. Always fail2ban-regex BEFORE enabling.
```

---

## 8. Files & locations

| Path | Purpose |
| --- | --- |
| `/etc/fail2ban/jail.conf` | shipped defaults — **read, never edit** |
| `/etc/fail2ban/jail.local` | your global `[DEFAULT]` + jail overrides |
| `/etc/fail2ban/jail.d/*.local` | per-jail config (tidiest layout) |
| `/etc/fail2ban/filter.d/*.conf` | the failregex sets (`<HOST>` captures the IP) |
| `/etc/fail2ban/action.d/*.conf` | ban actions (firewall, mail, etc.) |
| `/var/log/fail2ban.log` | fail2ban's own log (or `journalctl -u fail2ban`) |
| run: `fail2ban-client`, `fail2ban-regex` | operate / test |

---

## Gotchas / Golden rules

1. **`enabled = true` per jail, or it does nothing.** No jail is on by default.
2. **Edit `*.local`, never `*.conf`.** Upgrades overwrite the shipped files.
3. **Put your own subnets in `ignoreip`.** The first lockout you prevent is your own.
4. **Modern OpenSSH needs `backend = systemd` + fail2ban ≥ 1.1.0.** Otherwise `sshd-session`
   lines slip past the filter and the jail silently never bans (§5).
5. **`fail2ban-regex` before you trust a jail.** "Matched 0" with real failures = filter/backend
   problem, not a threshold to tune.
6. **Bans live in the firewall.** fail2ban inserts rules into an `f2b-*` chain ([[iptables]]);
   if the chain isn't there, the ban action isn't working — check `banaction` matches your
   firewall backend (iptables vs nftables).
7. **`bantime.increment` is the cheap win** against persistent scanners — escalating bans cost
   you nothing and wear them down.

## Further reading
- [fail2ban manual](https://github.com/fail2ban/fail2ban/wiki) ·
  [jail.conf(5)](https://manpages.debian.org/jail.conf.5) ·
  [fail2ban-regex(1)](https://manpages.debian.org/fail2ban-regex.1) ·
  [Arch Wiki: fail2ban](https://wiki.archlinux.org/title/Fail2ban)
