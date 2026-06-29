---
type: cheatsheet
area: "Linux Administration"
aliases: [journalctl, syslog, rsyslog, logrotate, logs]
tags: [linux, logging, journald, journalctl, syslog]
status: working
---

# Logging & journald

> **Area:** [[Linux Administration]]

Querying and managing logs on systemd-based Linux systems. See [[systemd]] for the service side of journald. Traditional `/var/log` syslog patterns are also covered for non-systemd or forwarded logs.

---

## 1. journalctl — query the systemd journal

```bash
journalctl                          # all logs (oldest first; press G to jump to end)
journalctl -r                       # reverse: newest first
journalctl -f                       # follow (like tail -f)
journalctl -n 100                   # last 100 lines
journalctl -e                       # jump to end of journal
journalctl --no-pager               # dump all to stdout (pipe-friendly)
```

## 2. Filter by unit / process

```bash
journalctl -u nginx                 # logs for the nginx service
journalctl -u nginx -u php-fpm      # multiple units
journalctl -u nginx -f              # follow a specific service
journalctl _SYSTEMD_UNIT=nginx.service  # same as -u, explicit field match

# By process or PID
journalctl _PID=1234
journalctl _COMM=nginx              # by executable name (not service name)
journalctl _EXE=/usr/sbin/nginx     # by full binary path

# By boot
journalctl -b                       # current boot
journalctl -b -1                    # previous boot
journalctl -b -2                    # two boots ago
journalctl --list-boots             # list all boots with ID, date, time
```

## 3. Filter by time

```bash
journalctl --since "2024-06-01"
journalctl --since "2024-06-01 12:00:00" --until "2024-06-01 13:00:00"
journalctl --since "1 hour ago"
journalctl --since "yesterday"
journalctl -u nginx --since "10 minutes ago"    # combine with unit filter
```

## 4. Filter by priority (severity)

```bash
journalctl -p err                   # errors and above (err, crit, alert, emerg)
journalctl -p warning               # warnings and above
journalctl -p debug                 # debug and above (everything)
journalctl -p 3                     # numeric: 0=emerg … 7=debug

# Priority levels:
# 0=emerg  1=alert  2=crit  3=err  4=warning  5=notice  6=info  7=debug
```

## 5. Output formats

```bash
journalctl -o json                  # one JSON object per log entry
journalctl -o json-pretty           # pretty-printed JSON
journalctl -o short                 # default text format
journalctl -o short-iso             # with ISO 8601 timestamps
journalctl -o cat                   # message text only, no metadata
journalctl -o verbose               # all journal fields

# Export for analysis
journalctl -u nginx --since today -o json | jq '.MESSAGE' -r
```

## 6. Journal disk usage and housekeeping

```bash
journalctl --disk-usage             # how much disk the journal is using
journalctl --vacuum-size=500M       # shrink journal to 500 MB max
journalctl --vacuum-time=30d        # delete entries older than 30 days
journalctl --rotate                 # rotate the active journal file now

# Persistent journal (logs across reboots)
# /etc/systemd/journald.conf:
# [Journal]
# Storage=persistent    # auto (default), volatile, persistent, none
# SystemMaxUse=2G
# MaxRetentionSec=90day
# Compress=yes          # default
mkdir -p /var/log/journal           # creating this dir also enables persistence
systemctl restart systemd-journald
```

## 7. Traditional /var/log and syslog

```bash
# Common log files (location varies by distro)
/var/log/syslog        # general system log (Debian/Ubuntu)
/var/log/messages      # general system log (RHEL/Fedora)
/var/log/auth.log      # authentication events (Debian)
/var/log/secure        # authentication events (RHEL)
/var/log/kern.log      # kernel messages
/var/log/dmesg         # kernel ring buffer at boot
dmesg                  # kernel ring buffer (current)
dmesg -T               # with human-readable timestamps
dmesg | tail -50       # last 50 kernel messages
dmesg -l err,warn      # errors and warnings only

# tail multiple logs at once
tail -f /var/log/syslog /var/log/auth.log
multitail /var/log/syslog /var/log/nginx/error.log   # if installed
```

## 8. logrotate

```bash
logrotate /etc/logrotate.conf --debug   # dry run: see what would be rotated
logrotate /etc/logrotate.d/nginx --force   # force rotation now (for testing)
cat /var/lib/logrotate/status              # last rotation times

# Drop-in config: /etc/logrotate.d/myapp
# /var/log/myapp/*.log {
#     daily
#     rotate 14
#     compress
#     delaycompress        # don't compress the most recent rotation (postrotate may need it)
#     missingok            # don't error if log file doesn't exist
#     notifempty           # don't rotate empty files
#     create 0640 myapp adm  # create new log file with permissions
#     postrotate
#         systemctl kill --signal=USR1 myapp  # signal the app to reopen logs
#     endscript
# }
```

## 9. rsyslog (forwarding and filtering)

```bash
# Forward all logs to a remote syslog server
# /etc/rsyslog.d/99-remote.conf:
# *.* @@logserver.example.com:514   # @@ = TCP; @ = UDP

# Filter and redirect
# :msg, contains, "ERROR"  /var/log/errors-only.log
# auth,authpriv.*          /var/log/auth.log

systemctl restart rsyslog
rsyslogd -N1               # validate config syntax (dry run)
```

---

## Daily workflows

### "Follow a service's logs in real time"
```bash
journalctl -u myservice -f
```

### "Find all errors in the last hour"
```bash
journalctl -p err --since "1 hour ago"
```

### "Check what happened at boot"
```bash
journalctl -b --no-pager | head -200
dmesg -T | head -100
```

### "Extract log lines matching a pattern"
```bash
journalctl -u nginx --since today | grep 'ERROR\|WARN'
journalctl -u nginx -o json | jq 'select(.PRIORITY | tonumber <= 4) | .MESSAGE'
```

### "Reduce journal size when disk is tight"
```bash
journalctl --disk-usage
journalctl --vacuum-size=200M
```

## Files & locations

| Path | What |
|---|---|
| `/run/log/journal/` | Volatile journal (lost on reboot if not persistent) |
| `/var/log/journal/` | Persistent journal (create directory to enable) |
| `/etc/systemd/journald.conf` | journald config: size limits, retention, storage |
| `/etc/logrotate.conf` | Global logrotate config |
| `/etc/logrotate.d/` | Per-application logrotate drop-ins |
| `/etc/rsyslog.conf` | rsyslog main config |
| `/etc/rsyslog.d/` | rsyslog drop-ins |

## Gotchas / Golden rules

1. **Journal is binary, not text** — `grep`ing `/var/log/journal/` directly returns nothing useful; always use `journalctl`.
2. **Without `/var/log/journal/` the journal is volatile** — logs are lost on reboot; create the directory to persist them, then set `SystemMaxUse` so it doesn't grow unbounded.
3. **`journalctl -f` shows new messages from all units** — pair with `-u` to follow a specific service; otherwise it's very noisy on a busy system.
4. **Time filters use the system's local timezone** — `--since "2024-06-01"` is interpreted in local time; add ` UTC` explicitly if you work across timezones.
5. **`--vacuum` operations are immediate and irreversible** — there is no "are you sure?" prompt; double-check the `--disk-usage` output before vacuuming.
