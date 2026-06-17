---
type: cheatsheet
area: Linux Administration
aliases: [systemctl, journalctl]
tags: [init, services, logging]
status: stable
---

# systemd

> **Area:** [[Linux Administration]]

Quick reference for `systemctl` and `journalctl` in daily use. Anything that changes system
state needs `sudo` (or `--user` for user units).

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
```

### Editing unit files

```bash
# Show the original unit file
systemctl cat nginx.service

# Create an override (drop-in) — safer than editing the original
sudo systemctl edit nginx.service

# Full override of the original
sudo systemctl edit --full nginx.service

# After changing unit files: re-read the daemon
sudo systemctl daemon-reload
```

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
```

### Managing journal disk usage

```bash
journalctl --disk-usage               # how much space does the journal use?
sudo journalctl --vacuum-size=500M    # shrink to max 500 MB
sudo journalctl --vacuum-time=2weeks  # keep only the last 2 weeks

# Persistent config: /etc/systemd/journald.conf
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
systemctl status                                # hierarchy of all services
```

---

## 6. Useful extras

```bash
# Analyse boot time
systemd-analyze
systemd-analyze blame              # what was slowest?
systemd-analyze critical-chain     # critical path of the boot

# Check a unit file for errors
systemd-analyze verify /etc/systemd/system/foo.service

# Run a program once under systemd (for testing)
sudo systemd-run --uid=$USER --gid=$USER /path/to/program

# List timers (the cron replacement)
systemctl list-timers --all
```

See [[systemd Service and Timer]] for a ready-to-fill unit + timer template.

---

## Golden rules

1. **`daemon-reload` after editing any unit file** — otherwise systemd runs the old definition.
2. **Override with drop-ins (`systemctl edit`), don't edit vendor units** — package updates
   overwrite the originals.
3. **`systemctl --failed` is the first command after any boot trouble.**
4. **Timers over cron** on systemd hosts — they log to the journal and have dependencies.

## Further reading
- [systemctl(1)](https://man7.org/linux/man-pages/man1/systemctl.1.html) ·
  [journalctl(1)](https://man7.org/linux/man-pages/man1/journalctl.1.html)
