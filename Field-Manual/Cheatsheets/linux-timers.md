---
type: cheatsheet
area: "Linux Administration"
aliases: [cron, crontab, at, systemd-timer]
tags: [linux, cron, scheduling, systemd, timer, at]
status: working
---

# Cron & Timers

> **Area:** [[Linux Administration]]

Scheduling recurring and one-shot jobs: `crontab` for classic cron, `at` for one-off tasks, and systemd timer units for the modern approach. See [[systemd]] for timer unit examples; [[Bash Strict Mode Header]] for the recommended script preamble.

---

## 1. crontab

```bash
crontab -e           # edit this user's crontab (opens $EDITOR)
crontab -l           # list this user's crontab
crontab -r           # remove this user's crontab (careful: no confirm)
crontab -u alice -e  # edit another user's crontab (as root)
```

**Crontab syntax:**

```
# m  h  dom  mon  dow  command
# │  │   │    │    │
# │  │   │    │    └─ day of week   (0-7; 0 and 7 = Sunday)
# │  │   │    └────── month         (1-12)
# │  │   └─────────── day of month  (1-31)
# │  └─────────────── hour          (0-23)
# └────────────────── minute        (0-59)

# Shortcuts:
# @reboot    — run once at startup
# @hourly    — 0 * * * *
# @daily     — 0 0 * * *
# @weekly    — 0 0 * * 0
# @monthly   — 0 0 1 * *
# @yearly    — 0 0 1 1 *
```

**Example entries:**

```cron
# Every day at 02:30
30 2 * * * /usr/local/bin/backup.sh

# Every 15 minutes
*/15 * * * * /usr/local/bin/healthcheck.sh

# Weekdays at 08:00
0 8 * * 1-5 /usr/local/bin/report.sh

# First of each month at midnight
0 0 1 * * /usr/local/bin/monthly-cleanup.sh

# On boot
@reboot /usr/local/bin/startup-task.sh

# Suppress output (don't email cron)
0 3 * * * /usr/local/bin/noisy-script.sh > /var/log/noisy.log 2>&1

# Only if the last run has finished (lock-file pattern)
0 * * * * flock -n /run/myjob.lock /usr/local/bin/myjob.sh
```

**System-wide cron:**

```bash
/etc/crontab          # system crontab (has a USER column: m h dom mon dow user cmd)
/etc/cron.d/          # drop-in files (same format as /etc/crontab)
/etc/cron.daily/      # scripts run daily by cron (just drop a script in here)
/etc/cron.hourly/
/etc/cron.weekly/
/etc/cron.monthly/
```

```bash
# View the cron daemon log to check if jobs ran
journalctl -u cron
grep CRON /var/log/syslog     # Debian/Ubuntu
grep crond /var/log/messages  # RHEL
```

## 2. at — one-off scheduled tasks

```bash
at now + 10 minutes <<'EOF'
/usr/local/bin/send-report.sh
EOF

at 23:00 tomorrow <<'EOF'
/usr/local/bin/nightly-task.sh
EOF

at -f /path/to/script.sh 14:30

atq                  # list pending jobs
atrm 3               # remove job 3
```

## 3. systemd timers (modern approach)

Systemd timers are the preferred method for new work on systemd systems: better logging (journald), dependency management, and activation after missed runs.

Every timer needs a corresponding service unit.

**Create `/etc/systemd/system/myjob.service`:**

```ini
[Unit]
Description=My scheduled job

[Service]
Type=oneshot
ExecStart=/usr/local/bin/myjob.sh
User=myjobuser
```

**Create `/etc/systemd/system/myjob.timer`:**

```ini
[Unit]
Description=Run myjob daily at 02:30
After=network-online.target

[Timer]
OnCalendar=*-*-* 02:30:00       # daily at 02:30
Persistent=true                  # catch up if the system was off during the scheduled time
AccuracySec=1min                 # how precisely to fire (default 1min; reduce for precise timing)

[Install]
WantedBy=timers.target
```

**Enable and manage:**

```bash
systemctl enable --now myjob.timer
systemctl status myjob.timer
systemctl list-timers --all        # all timers and next/last run times
journalctl -u myjob.service        # logs from the job itself
```

**OnCalendar expressions:**

```
*-*-* 00:00:00        # every day at midnight
*-*-* 00/6:00:00      # every 6 hours
Mon *-*-* 08:00:00    # every Monday at 08:00
*-*-1 00:00:00        # 1st of every month at midnight
hourly                # shorthand for *-*-* *:00:00
daily                 # *-*-* 00:00:00
weekly                # Mon *-*-* 00:00:00
```

```bash
# Test a calendar expression
systemd-analyze calendar "*-*-* 02:30:00"
# shows next 10 occurrences
```

**OnBootSec / OnUnitActiveSec (relative timers):**

```ini
[Timer]
OnBootSec=5min               # 5 minutes after boot
OnUnitActiveSec=1h           # then every 1 hour
```

---

## Cron vs systemd timers: when to use which

| | cron | systemd timer |
|---|---|---|
| Logging | Email or redirect to file manually | Automatic via journald |
| Run if missed | No | Yes (with `Persistent=true`) |
| Dependencies | None | Full unit dependencies |
| Per-user | Yes (`crontab -e`) | User units (`~/.config/systemd/user/`) |
| Distro support | Universal | systemd systems only |
| Existing scripts | Drop-in | Wrap in a service unit |

---

## Daily workflows

### "Run a script daily at 03:00"
```bash
crontab -e
# Add: 0 3 * * * /usr/local/bin/script.sh >> /var/log/script.log 2>&1
```

### "Create a systemd timer for a new job"
```bash
# Write the .service and .timer files in /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now myjob.timer
systemctl list-timers myjob.timer
```

### "Find out why a cron job didn't run"
```bash
journalctl -u cron --since "yesterday"
# Check: correct user? correct path? job output mailed? MAILTO=""/>/dev/null?
```

### "Run a one-off task in 30 minutes"
```bash
at now + 30 minutes <<'EOF'
/usr/local/bin/task.sh
EOF
atq     # confirm it's queued
```

## Gotchas / Golden rules

1. **Cron environment is minimal** — `PATH`, `HOME`, and `SHELL` are set but NOT your login profile; always use full paths in cron jobs (`/usr/bin/python3`, `/usr/local/bin/script.sh`) and set `PATH` explicitly at the top of the crontab.
2. **Cron sends output as email by default** — unless `MAILTO=""` is set at the top of the crontab, or you redirect to a log; silently failing jobs with email delivery failures are invisible.
3. **`*/15` means "every 15 minutes past each hour", not "every 15 minutes from now"** — first run is at :00, :15, :30, :45. If the script takes 20 minutes, the next run overlaps; use `flock -n` to prevent overlap.
4. **`Persistent=true` in systemd timers runs missed jobs at next boot** — useful for backup jobs on laptops; not appropriate for jobs that must not run twice if the system was off for several cycles.
5. **The `run-parts` mechanism in `/etc/cron.daily/` strips dots from filenames** — a script named `cleanup.sh` in `/etc/cron.daily/` won't run (the `.` disqualifies it); name it `cleanup` without an extension.
