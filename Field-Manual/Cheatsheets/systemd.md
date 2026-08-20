---
type: cheatsheet
area: Linux Administration
aliases: [systemctl, journalctl, systemd-analyze]
tags: [init, services, logging, boot]
status: stable
---

# systemd

> **Area:** [[Linux Administration]]

Quick reference for `systemctl`, `journalctl` and `systemd-analyze` in daily use. Anything
that changes system state needs `sudo` (or `--user` for user units).

<!-- A few commands below are newer: `systemctl clean` (v243+), `freeze`/`thaw` (v246+),
     `systemd-analyze condition`/`security` (v246+). Check `systemctl --version` on old hosts. -->


---

## 1. systemctl — managing services

### Status & info

```bash
# Show a service's status
systemctl status nginx.service

# Short form: is it active? (returns active/inactive)
systemctl is-active nginx

# Is it enabled at boot?
systemctl is-enabled nginx

# Has it failed?
systemctl is-failed nginx

# Every property systemd knows about the unit (the source of truth)
systemctl show nginx.service

# Just the properties you care about
systemctl show nginx -p MainPID -p ActiveState -p ExecMainStatus -p RestartUSec

# Resolved config of the unit, drop-ins merged in
systemctl cat nginx.service
```

### Start / stop / restart

```bash
sudo systemctl start nginx       # start
sudo systemctl stop nginx        # stop
sudo systemctl restart nginx     # restart

# Reload config without interrupting the service (if supported)
sudo systemctl reload nginx

# Reload if possible, otherwise restart
sudo systemctl reload-or-restart nginx

# Send a signal instead of a full stop (default SIGTERM)
sudo systemctl kill nginx
sudo systemctl kill -s SIGKILL nginx          # last resort, hung process
sudo systemctl kill -s SIGHUP --kill-who=main nginx

# Clear the "failed" state so the unit can start / be retried again
sudo systemctl reset-failed nginx
sudo systemctl reset-failed                   # all failed units at once

# Suspend a unit's processes without stopping it (debugging)
sudo systemctl freeze nginx
sudo systemctl thaw nginx

# Delete a unit's state/cache/logs dirs (StateDirectory=, CacheDirectory=, …)
sudo systemctl clean --what=cache nginx
```

### Autostart at boot

```bash
sudo systemctl enable nginx          # enable at boot
sudo systemctl enable --now nginx    # enable AND start now
sudo systemctl disable nginx         # disable autostart
sudo systemctl disable --now nginx   # disable AND stop now

# Block a service entirely (can no longer be started)
sudo systemctl mask nginx
sudo systemctl unmask nginx
```

### Listing units

```bash
# All running units
systemctl list-units

# All services (including inactive)
systemctl list-units --type=service --all

# Only failed units (often the first thing to check after trouble!)
systemctl --failed

# Enabled/disabled state of all services at boot
systemctl list-unit-files --type=service

# What depends on what?
systemctl list-dependencies nginx
systemctl list-dependencies --reverse nginx   # who pulls nginx in?
systemctl list-dependencies --before nginx    # what must nginx start before?
systemctl list-dependencies --after nginx     # what had to be up first?

# Everything currently queued (a hung boot usually shows a stuck job here)
systemctl list-jobs

# Timers — the cron replacement, incl. last/next run
systemctl list-timers --all

# Sockets and their listening addresses
systemctl list-sockets
```

### Editing unit files

```bash
# Show the original unit file
systemctl cat nginx.service

# Create an override (drop-in) — safer than editing the original
sudo systemctl edit nginx.service

# Full override of the original
sudo systemctl edit --full nginx.service

# Name the drop-in file yourself (instead of override.conf)
sudo systemctl edit --drop-in=hardening nginx.service

# Throw away all your drop-ins/overrides, back to the vendor unit
sudo systemctl revert nginx.service

# After changing unit files: re-read the daemon
sudo systemctl daemon-reload

# Restart systemd (PID 1) itself — after a systemd package upgrade
sudo systemctl daemon-reexec

# Which vendor files are shadowed/overridden anywhere on this host?
systemd-delta
```

> Drop-in details and the `ExecStart=` reset trick: [[Drop-in Unit]] · [[systemd.exec]]

### System control

```bash
sudo systemctl reboot         # restart
sudo systemctl poweroff       # shut down
sudo systemctl suspend        # standby
sudo systemctl hibernate      # hibernate

# Show the current "target" (runlevel)
systemctl get-default

# Change the default target (e.g. for a headless server)
sudo systemctl set-default multi-user.target

# Switch target right now (stops everything not in the new target — careful over SSH)
sudo systemctl isolate multi-user.target
sudo systemctl rescue        # single-user-ish, minimal services
sudo systemctl emergency     # only the root shell, no mounts beyond /
```

---

## 2. journalctl — reading logs

### Basics

```bash
journalctl                    # the whole journal (press q to quit)
journalctl -r                 # newest entries first
journalctl -n 50              # last N lines
journalctl -f                 # follow live (like tail -f)
```

### Filter by service

```bash
journalctl -u nginx.service           # logs of one service
journalctl -u nginx -f                # follow one service live
journalctl -u nginx -u php-fpm        # combine multiple services
journalctl -u nginx -n 100            # last 100 lines of a service
journalctl --user-unit syncthing      # a user unit instead of a system one
journalctl -u nginx -x                # add explanatory catalog text to messages
```

### Filter by anything else

```bash
journalctl -g 'timed out' -u nginx    # grep the message text (case-insensitive)
journalctl _PID=1234                  # one process
journalctl _COMM=sshd                 # one binary name
journalctl _UID=1000                  # one user
journalctl /usr/bin/borg              # one executable path
journalctl -F _SYSTEMD_UNIT           # list all values a field ever had
```

### Time filters

```bash
journalctl -b                         # since boot
journalctl -b -1                      # the previous boot
journalctl --list-boots               # list available boots

journalctl --since today
journalctl --since yesterday
journalctl --since "1 hour ago"
journalctl --since "2026-05-22 08:00" --until "2026-05-22 18:00"
journalctl -u nginx --since "10 min ago"
```

### Priority / log level

```bash
journalctl -p err                     # errors and worse (emerg, alert, crit, err)
journalctl -p warning                 # warnings and higher
journalctl -b -p err                  # errors since the last boot
```

Priorities: `emerg(0)`, `alert(1)`, `crit(2)`, `err(3)`, `warning(4)`, `notice(5)`,
`info(6)`, `debug(7)`.

### Kernel / hardware

```bash
journalctl -k                         # kernel messages (like dmesg)
journalctl -k -b                      # kernel messages from the current boot
```

### Handy combinations

```bash
journalctl -b -p err -f               # only the worst errors of this boot, live
journalctl -u sshd --since "1 hour ago"   # what did sshd do in the last hour?
journalctl -u nginx -o json           # logs as JSON (for parsing)
journalctl -u nginx -o cat            # compact, no hostname
journalctl -u nginx -o short-precise  # microsecond timestamps (ordering races)
journalctl -u nginx --output-fields=MESSAGE,_PID -o verbose
```

### Managing journal disk usage

```bash
journalctl --disk-usage               # how much space does the journal use?
sudo journalctl --vacuum-size=500M    # shrink to max 500 MB
sudo journalctl --vacuum-time=2weeks  # keep only the last 2 weeks
sudo journalctl --vacuum-files=5      # keep only the newest 5 journal files

journalctl --verify                   # integrity check of the journal files
sudo journalctl --flush               # push /run journal into /var (persistent)
sudo journalctl --rotate              # close current file, start a new one

# Persistent config: /etc/systemd/journald.conf
#   Storage=persistent
#   SystemMaxUse=500M
```

---

## 3. User units (no sudo, for your own user)

```bash
# Works with all systemctl/journalctl commands + --user
systemctl --user status syncthing
systemctl --user enable --now syncthing
journalctl --user -u syncthing -f

# Let user services run even without an active login
sudo loginctl enable-linger $USER
```

---

## 4. Where do unit files live?

| Path | Purpose |
| --- | --- |
| `/lib/systemd/system/` | Installed by distribution packages |
| `/etc/systemd/system/` | Your own / overriding system units |
| `/etc/systemd/system/foo.service.d/` | Drop-in overrides for `foo.service` |
| `~/.config/systemd/user/` | Your own user units |
| `/run/systemd/system/` | Runtime units (vanish on reboot) |

---

## 5. Daily workflows

### Reconfigured a service — now what?
```bash
sudo systemctl daemon-reload    # after changing the unit file
sudo systemctl restart nginx    # or reload, if supported
systemctl status nginx          # check
```

### A service crashed — what happened?
```bash
systemctl status nginx                          # first overview
journalctl -u nginx -n 50 --no-pager            # recent logs
journalctl -u nginx -p err -b                   # errors since boot
```
For the full procedure, see [[Service Down — Triage & Recovery]].

### What went wrong at the last boot?
```bash
systemctl --failed                              # what's broken?
journalctl -b -p err                            # all errors this boot
journalctl -b -1 -p err                         # errors from the previous boot
```

### Which services use a lot of CPU/RAM?
```bash
systemd-cgtop                                   # like top, but per service
systemd-cgls                                    # cgroup tree: which PID belongs to which unit
systemctl status                                # hierarchy of all services
```

### The boot feels slow — where did the time go?
```bash
systemd-analyze                                 # total: firmware/loader/kernel/userspace
systemd-analyze blame | head -20                # slowest units (NOT the critical path)
systemd-analyze critical-chain                  # what actually delayed the boot
```
See §6 for how to read the difference.

---

## 6. systemd-analyze — boot time, units, sanity checks

### Boot timing

```bash
# Totals: firmware → bootloader → kernel → initrd → userspace
systemd-analyze
systemd-analyze time                    # same thing, explicit

# Per-unit startup duration, slowest first
systemd-analyze blame
systemd-analyze blame | head -20
systemd-analyze --user blame            # the user session instead of the system

# The critical path: the chain that actually held the boot up
systemd-analyze critical-chain
systemd-analyze critical-chain nginx.service    # chain leading to one unit
```

Reading `critical-chain` output:

| Marker | Meaning |
| --- | --- |
| `@2.351s` | the unit finished activating this long after boot start |
| `+1.204s` | the unit itself took this long to activate |
| indentation | each level waited for the level below it |

**`blame` ≠ the problem.** `blame` ranks units by how long they took, but a slow unit
that nothing waits on costs you nothing. `critical-chain` shows the chain that everything
else was blocked behind — optimise there. A unit high in `blame` but absent from
`critical-chain` is usually safe to ignore.

### Boot graphs & dependency graphs

```bash
# Timeline of every unit as an SVG (open in a browser)
systemd-analyze plot > boot.svg

# Dependency graph in Graphviz form
systemd-analyze dot | dot -Tsvg > deps.svg
systemd-analyze dot 'nginx.*' | dot -Tsvg > nginx-deps.svg
```

### Checking units before they bite

```bash
# Syntax/semantics check of a unit file (also catches missing binaries)
systemd-analyze verify /etc/systemd/system/foo.service

# Sandboxing/hardening score of a unit — 0 (perfect) … 10 (wide open)
systemd-analyze security
systemd-analyze security nginx.service

# Show effective config with all drop-ins merged
systemd-analyze cat-config systemd/journald.conf

# Where does systemd look for units, in which order?
systemd-analyze unit-paths
```

### Parsing helpers (worth memorising)

```bash
# Will my OnCalendar= actually fire when I think? (next 5 runs)
systemd-analyze calendar --iterations=5 'Mon *-*-* 03:30:00'

# Interpret a timespan / timestamp string the way systemd does
systemd-analyze timespan '2h 30min'
systemd-analyze timestamp 'tomorrow'

# Test a ConditionX= / AssertX= line without restarting anything
systemd-analyze condition 'ConditionPathExists=/etc/fstab'

# Decode a seccomp filter set name (SystemCallFilter=@system-service)
systemd-analyze syscall-filter @system-service
```

---

## 7. Neighbouring tools

```bash
# Run a program once under systemd (for testing units/sandboxing)
sudo systemd-run --uid=$USER --gid=$USER /path/to/program
sudo systemd-run --on-active=5min /usr/local/bin/thing    # ad-hoc transient timer
systemd-run --user --scope -p MemoryMax=1G ./hungry-build # cap a shell command

# Escape a path into a unit name (and back)
systemd-escape -p --suffix=mount /srv/data     # → srv-data.mount
systemd-escape -u -p srv-data.mount

# Machine identity / time / locale / logins
hostnamectl                                    # hostname, OS, virtualisation, machine-id
timedatectl                                    # clock, timezone, NTP sync state
timedatectl set-ntp true
localectl                                      # locale + console keymap
loginctl list-sessions                         # who is logged in, on what seat
loginctl enable-linger $USER                   # user units survive logout

# Am I in a VM/container, and which?
systemd-detect-virt
```

See [[systemd Service and Timer]] for a ready-to-fill unit + timer template, and
[[linux-timers]] for the timer-specific reference.

---

## Golden rules

1. **`daemon-reload` after editing any unit file** — otherwise systemd runs the old definition.
2. **Override with drop-ins (`systemctl edit`), don't edit vendor units** — package updates
   overwrite the originals.
3. **`systemctl --failed` is the first command after any boot trouble.**
4. **Timers over cron** on systemd hosts — they log to the journal and have dependencies.
5. **Optimise the critical chain, not the blame list** — a slow unit nobody waits for
   costs zero boot time.
6. **`systemctl show` beats `status` when you need facts** — `status` is a human summary,
   `show` is what systemd actually has in memory.
7. **`systemctl isolate` / `rescue` over SSH will cut your own session.** Use a console or
   set the target and reboot instead.
8. **A unit that hit its start rate limit stays down until `reset-failed`** — restarting it
   over and over just re-triggers the limit.

## Further reading
- [systemctl(1)](https://man7.org/linux/man-pages/man1/systemctl.1.html) ·
  [journalctl(1)](https://man7.org/linux/man-pages/man1/journalctl.1.html) ·
  [systemd-analyze(1)](https://man7.org/linux/man-pages/man1/systemd-analyze.1.html)
