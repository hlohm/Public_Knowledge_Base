---
type: playbook
area: Linux Administration
tags: [incident, systemd, troubleshooting]
status: stable
---

# Service Down — Triage & Recovery

> **Area:** [[Linux Administration]]

A systemd service isn't running (or keeps dying). This is the fast path from "it's down" to a
root cause, using [[systemd]]'s tooling. Read-only triage first; only change state once you know
why.

## Symptom
- A service is `inactive`/`failed`, clients can't reach it, or it flaps (restarts repeatedly).

## Quick triage (first 3 commands)
```bash
systemctl status <svc>                      # state, last exit, recent log lines
journalctl -u <svc> -n 50 --no-pager        # the actual error
systemctl --failed                          # is anything else failed too?
```
Read the **exit code / signal** in `status` and the **last error** in the journal before doing
anything else. The cause is usually right there.

## Decision branches
- **`status` shows a config/exit error** (e.g. "failed to parse", non-zero exit) →
  it's the unit or app config → *Fix A*.
- **Journal shows "Address already in use" / port conflict** → something else holds the port →
  *Fix B*.
- **Journal shows "No space left on device"** → disk full → *Fix C*.
- **`status` shows `start-limit-hit`** (flapping, hit the restart limit) →
  reset the counter after fixing the underlying cause → *Fix D*.
- **Unit not found / masked** → `systemctl cat <svc>` (does it exist?), `is-enabled <svc>`
  (masked?) → unmask/enable.

## Fixes
### Fix A — config / unit error
```bash
systemctl cat <svc>                                  # inspect the unit
sudo systemd-analyze verify /etc/systemd/system/<svc>.service   # validate the unit file
# fix the app config or unit, then:
sudo systemctl daemon-reload                         # required after editing a unit file
sudo systemctl restart <svc>
```

### Fix B — port already in use
```bash
sudo ss -tlnp | grep ':<port>'      # who holds the port?
# stop/relocate the conflicting process, then:
sudo systemctl restart <svc>
```

### Fix C — disk full
```bash
df -h                               # confirm which filesystem is full
sudo journalctl --disk-usage        # journal is a common culprit
sudo journalctl --vacuum-size=500M  # reclaim journal space, then restart the service
sudo systemctl restart <svc>
```

### Fix D — flapping (start limit hit)
```bash
# After fixing the real cause, clear the rate-limit counter:
sudo systemctl reset-failed <svc>
sudo systemctl start <svc>
```

## Escalation / after-action
- **Confirm recovery:** `systemctl status <svc>` is `active (running)` and
  `journalctl -u <svc> -f` is quiet/healthy.
- **If it recurs:** capture `journalctl -u <svc> -b` for the full boot, note the trigger, and
  consider an upstream fix (resource limits, a `healthcheck`, log rotation) rather than just
  restarting.
- **Write it up** if it was non-obvious — a future you (or teammate) hitting the same symptom
  should find the cause here. Promote recurring fixes into this playbook.
