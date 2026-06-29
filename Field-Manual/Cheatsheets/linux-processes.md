---
type: cheatsheet
area: "Linux Administration"
aliases: [ps, top, htop, kill, performance]
tags: [linux, processes, performance, monitoring, ps, top]
status: working
---

# Processes & Performance

> **Area:** [[Linux Administration]]

Listing, inspecting, and managing processes; measuring CPU, memory, I/O, and load average. The first tools to reach for when a system is slow or misbehaving.

---

## 1. ps — process snapshot

```bash
ps aux                    # BSD-style: all processes, all users, with resource usage
ps -ef                    # UNIX-style: all processes, full listing (PPID, UID, command)
ps aux | grep nginx        # find a specific process
ps -p 1234                 # specific PID
ps -u alice                # processes owned by alice

# Process tree
ps -ejH                   # show process hierarchy
pstree                    # tree with process names
pstree -p                 # tree with PIDs
pstree alice              # processes belonging to alice

# Column reference (aux):
# USER  PID  %CPU %MEM   VSZ   RSS  TTY  STAT  START   TIME  COMMAND
# VSZ: virtual memory size (includes mapped but not allocated)
# RSS: resident set size (actually in RAM)
# STAT: S=sleeping, R=running, D=uninterruptible I/O wait, Z=zombie, T=stopped
```

## 2. top / htop — live view

```bash
top                       # live process monitor (default sort: CPU)
top -u alice              # only alice's processes
top -p 1234,5678          # watch specific PIDs
```

**top interactive keys:**
| Key | Action |
|---|---|
| `P` | Sort by CPU (default) |
| `M` | Sort by memory |
| `T` | Sort by running time |
| `k` | Kill process (enter PID) |
| `r` | Renice a process |
| `1` | Toggle per-CPU breakdown |
| `q` | Quit |

```bash
htop                      # improved top: colour, scroll, tree view, mouse support
# htop keys: F5 = tree view, F6 = sort column, F9 = kill, F10 = quit
# Arrow keys to select, Space to tag multiple for batch kill
```

## 3. Signals and kill

```bash
kill -l                   # list all signals
kill <PID>                # send SIGTERM (15) — polite, lets process clean up
kill -9 <PID>             # send SIGKILL — force, cannot be caught or ignored
kill -HUP <PID>           # SIGHUP (1) — reload config (for daemons that support it)
kill -STOP <PID>          # pause a process (SIGSTOP)
kill -CONT <PID>          # resume a paused process (SIGCONT)

killall nginx             # kill all processes named nginx (SIGTERM)
killall -9 nginx          # force-kill all nginx processes
pkill -f 'python app.py'  # kill by full command line match
pgrep nginx               # find PIDs by name (no kill — just list)
pgrep -la nginx           # list with command line

# Background and job control
Ctrl+Z                    # suspend foreground process
bg                        # resume in background
fg                        # bring background job to foreground
jobs                      # list current shell's background jobs
nohup command &           # run in background, immune to HUP when terminal closes
```

## 4. System load and CPU

```bash
uptime                    # load average: 1m, 5m, 15m; >nCPU means backlog
nproc                     # number of logical CPUs

# CPU utilisation
mpstat -P ALL 1           # per-CPU stats, 1-second interval (from sysstat)
vmstat 1                  # virtual memory, CPU, I/O summary per second
sar -u 1 10               # CPU utilisation, 1s interval, 10 samples

# Load average interpretation:
# load 1.0 on a 1-CPU host = 100% utilisation; 2.0 = queue
# load 4.0 on a 4-CPU host = 100%; 8.0 = queue
# high 1m but low 15m = recent spike; high 15m = sustained load
```

## 5. Memory

```bash
free -h                   # total/used/free/cached/available (human-readable)
# 'available' is the key number: what can be allocated without swapping
# 'cached' is kernel page cache — it is free for reuse

cat /proc/meminfo         # kernel memory breakdown in detail

# Per-process memory
ps aux --sort=-%mem | head -15    # top memory consumers
cat /proc/<PID>/status | grep -E 'Vm(RSS|Swap|Peak)'

# Swap
swapon --show             # active swap devices and usage
swapoff /dev/sda3         # disable swap on a device
```

## 6. I/O and disk performance

```bash
iostat -xz 1              # per-device I/O stats: util%, await, r/s, w/s
# util% near 100 = device saturated; high await = queue depth or slow device

iotop -o                  # top-like view of per-process I/O (requires root)
# -o = only show processes that are currently doing I/O

# Find which process is writing to a file or device
lsof +D /var/log/         # all open files under /var/log/
lsof -p <PID>             # all files open by a process
fuser /var/log/app.log    # PID(s) using this file
```

## 7. Nice and priority

```bash
nice -n 10 command        # start command with niceness 10 (lower priority; range -20 to +19)
renice 5 -p <PID>         # change niceness of running process
renice -5 -p <PID>        # increase priority (requires root for negative values)

# I/O scheduling priority (ionice)
ionice -c 3 -p <PID>      # idle class: only use I/O when no one else needs it
ionice -c 2 -n 7 command  # best-effort, lowest priority
```

## 8. Specific investigation patterns

```bash
# "System is slow — where is the load?"
uptime                    # load average
top                       # which processes are consuming CPU?
iostat -xz 1              # is disk I/O saturated?
free -h                   # is memory exhausted / swapping?
vmstat 1                  # all of the above in compact form

# "Process is stuck in D state (uninterruptible sleep)"
ps aux | grep ' D '       # find it
# D state = waiting on I/O; usually disk or NFS; check iostat and dmesg
dmesg | tail -20          # kernel messages: I/O errors, hung task warnings

# "Why is this process consuming so much CPU?"
strace -p <PID> -c        # summary of system calls with time spent
perf top -p <PID>         # CPU profiling (requires perf)
cat /proc/<PID>/wchan     # what kernel function the process is waiting in

# "Find all child processes of a parent"
pstree -p <parent-PID>
ps --ppid <parent-PID>
```

---

## Daily workflows

### "Find and kill a runaway process"
```bash
ps aux | grep 'runaway-name'
kill <PID>           # try polite first
kill -9 <PID>        # force if it doesn't respond in a few seconds
```

### "Check overall system health quickly"
```bash
uptime; free -h; df -h; ss -tnlp | wc -l
```

### "Find the top 5 CPU and memory consumers"
```bash
ps aux --sort=-%cpu | head -6
ps aux --sort=-%mem | head -6
```

### "Run a long job without it dying when SSH disconnects"
```bash
nohup ./long-job.sh > job.log 2>&1 &
# Or: use tmux (attach/detach) or 'screen'
```

## Gotchas / Golden rules

1. **Load average > number of CPUs means contention** — a load of 4.0 on a 4-CPU system is 100% utilised; on an 8-CPU system it's 50%. Always compare to `nproc`.
2. **`kill -9` skips cleanup** — the process cannot catch SIGKILL; files it had open may not be flushed, locks not released. Always try `kill` (SIGTERM) first and give it 5-10 seconds.
3. **D-state processes cannot be killed** — a process in uninterruptible sleep (D) is waiting for the kernel; SIGKILL has no effect until the I/O completes or the kernel times out. Investigate the I/O path.
4. **`free`'s "used" includes the page cache** — the "available" column is what matters for "will this start swapping?", not "used."
5. **`ps aux` shows CPU since process start, not current CPU** — for current CPU, use `top` or `ps aux --sort=-%cpu`; the `%CPU` in a single ps snapshot can be misleading for long-running processes.
