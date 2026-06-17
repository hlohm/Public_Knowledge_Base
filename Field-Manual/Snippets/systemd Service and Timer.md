---
type: snippet
area: Linux Administration
tags: [boilerplate, systemd]
status: stable
---

# systemd Service and Timer

> **Area:** [[Linux Administration]]

**What & why.** A reusable `oneshot` service plus a timer that runs it on a schedule — the
systemd-native replacement for a cron job (it logs to the journal and can express
dependencies). Drop-in template; fill the bracketed parts. See [[systemd]] for the management
commands.

`/etc/systemd/system/mytask.service`:

```ini
[Unit]
Description=My scheduled task
Wants=network-online.target          # if it needs the network
After=network-online.target

[Service]
Type=oneshot                         # runs, exits — correct type for a timer-driven job
ExecStart=/usr/local/bin/mytask.sh
User=myuser                          # don't run as root unless you must
# Hardening (tighten to taste):
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
NoNewPrivileges=true
ReadWritePaths=/var/lib/mytask       # the one place it's allowed to write
```

`/etc/systemd/system/mytask.timer`:

```ini
[Unit]
Description=Run mytask daily

[Timer]
OnCalendar=*-*-* 03:00:00            # daily at 03:00; see `man systemd.time`
Persistent=true                      # if the machine was off, run on next boot
RandomizedDelaySec=300               # jitter to avoid thundering-herd at exact times

[Install]
WantedBy=timers.target
```

Enable and verify:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now mytask.timer
systemctl list-timers mytask.timer          # when does it next run?
sudo systemctl start mytask.service         # run once now, to test
journalctl -u mytask.service -n 50          # read the result
```

## Customize
- **`OnCalendar`** — `hourly`, `daily`, `weekly`, or explicit `*-*-* HH:MM:SS`. Test an
  expression with `systemd-analyze calendar "Mon *-*-* 09:00"`.
- **`Type`** — `oneshot` for run-and-exit tasks; `simple`/`notify` for long-running services
  (then you usually don't need a timer).
- **Hardening lines** — start strict, loosen only what breaks. `ReadWritePaths` is the usual
  one to add.
- **`User=`** — run unprivileged wherever possible.

## Use
- Service + timer share a basename (`mytask`) so the timer auto-finds its service. To pair a
  timer with a differently-named unit, set `Unit=other.service` in `[Timer]`.
- For a per-user job (no root), put the units in `~/.config/systemd/user/` and use
  `systemctl --user` (plus `loginctl enable-linger $USER` to run without an active login).
