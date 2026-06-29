---
type: playbook
area: "Linux Administration"
tags: [linux, memory, oom, triage, incident, performance]
status: working
---

# Out of Memory

> **Area:** [[Linux Administration]]

A Linux host is running out of RAM. The OOM killer may have already fired, a process is swapping heavily, or an application is leaking memory and growing unboundedly. This playbook walks through triage, stabilisation, and root cause.

---

## Situation

- A process was killed unexpectedly and `dmesg` shows "Out of memory: Kill process"
- The system is unresponsive or extremely slow (swapping)
- `free -h` shows negligible available memory and swap heavily used
- A monitoring alert for low available memory

## Quick assessment

```bash
free -h              # total/used/free/available; swap usage
vmstat 1 5           # memory, swap I/O, CPU over 5 seconds; 'si'/'so' = swap in/out
cat /proc/meminfo    # detailed kernel memory breakdown
uptime               # load average; high + heavy swap = likely OOM
dmesg | grep -i 'oom\|killed\|out of memory' | tail -30
journalctl -k | grep -i 'oom\|kill' | tail -30
```

---

## Decision branches

| Observation | Go to |
|---|---|
| OOM killer already fired, process killed | Fix A — Read the OOM kill |
| System is swapping heavily but nothing killed yet | Fix B — Reduce swap pressure |
| One process is growing unboundedly | Fix C — Memory leak investigation |
| Many small processes consuming too much total | Fix D — Reduce process count |
| Kernel or slab memory is high | Fix E — Kernel memory |
| System consistently low on RAM | Fix F — Structural insufficiency |

---

## Fix A — Read the OOM kill

The kernel logs an OOM kill with full context. Learn to read it:

```bash
dmesg | grep -A 30 'Out of memory'
```

Example output:
```
[12345.678] Out of memory: Kill process 9876 (java) score 812 or sacrifice child
[12345.678] Killed process 9876 (java) total-vm:8192000kB, anon-rss:3276800kB
```

Key fields:
- **Kill process NNN (name)** — what was killed
- **score NNN** — OOM badness score (0–1000); higher = more likely to be killed
- **total-vm** — total virtual memory mapped
- **anon-rss** — actual RAM used (anonymous pages — heap, stack, not file-backed)
- **file-rss** — RAM used for file-backed pages (mmap'd files)

```bash
# See the full memory table from the OOM event (who had what)
dmesg | grep -A 80 'Out of memory' | head -100
# Look for the process with the highest rss at the time of the kill
```

## Fix B — Reduce swap pressure immediately

```bash
# How much swap is in use and by whom?
swapon --show
grep VmSwap /proc/*/status 2>/dev/null | sort -t: -k3 -n | tail -20

# Force the system to swap less aggressively
sysctl vm.swappiness=10     # default is 60; lower = prefer RAM to swap (runtime only)
# Persist: echo "vm.swappiness=10" >> /etc/sysctl.d/99-memory.conf

# Clear the page cache (frees cached file data — safe; kernel refills it as needed)
sync; echo 3 > /proc/sys/vm/drop_caches

# If specific services are not critical, stop them to reclaim RAM
systemctl stop heavy-service
```

## Fix C — Memory leak investigation

A process that grows without bound until the OOM killer fires is the classic leak.

```bash
# Watch memory of a suspect process over time
while true; do
  cat /proc/<PID>/status | grep -E 'VmRSS|VmSwap'
  sleep 5
done

# Current top memory consumers
ps aux --sort=-%mem | head -20

# Detailed per-process memory map
pmap -x <PID> | sort -k3 -n | tail -30
cat /proc/<PID>/smaps_rollup    # summary by mapping type

# valgrind (for compiled programs; dev/test environment only — very slow)
valgrind --leak-check=full --track-origins=yes ./myprogram

# For running processes: gdb malloc stats (invasive — attaches and pauses the process)
gdb -p <PID> -batch -ex "call malloc_stats()"
```

**Common causes of leaks:**

| Symptom | Likely cause |
|---|---|
| Java/JVM grows, GC not collecting | Heap too small; GC tuning needed; `-Xmx` too high |
| Python process grows slowly | Objects with circular refs; `__del__` preventing GC |
| C/C++ service grows over days | Classic heap leak; run under valgrind or ASAN |
| Kernel buffers/slabs growing | See Fix E |

**Immediate mitigation for a leaking process** (buy time while you fix the root cause):

```bash
# Set an RSS limit using cgroups v2 (prevents the leak from killing the host)
systemctl set-property myservice.service MemoryMax=2G
systemctl restart myservice

# Or: add to the unit file:
# [Service]
# MemoryMax=2G
# MemorySwapMax=0   # prevent swap for this service
```

## Fix D — Reduce process count

```bash
# How many processes are running?
ps aux | wc -l
pstree | wc -l

# Find the top processes by count (often a fork-happy CGI or daemon)
ps -eo comm | sort | uniq -c | sort -rn | head -20

# If a service is spawning too many workers:
# nginx: worker_processes, worker_connections in nginx.conf
# Apache: MaxRequestWorkers (MPM prefork/worker/event)
# PostgreSQL: max_connections in postgresql.conf
```

## Fix E — Kernel / slab memory

Kernel slabs are caches for frequently allocated kernel objects. In rare cases they grow large:

```bash
cat /proc/slabinfo | sort -k3 -n | tail -20
slabtop                         # interactive view of slab usage

# Common large slabs:
# dentry, inode_cache  — filesystem metadata caches; usually fine (freed under pressure)
# kmalloc-*            — generic kernel allocations

# Force slab reclaim (safe; kernel re-fills as needed)
echo 2 > /proc/sys/vm/drop_caches   # drops dentries and inodes
echo 3 > /proc/sys/vm/drop_caches   # drops page cache + dentries + inodes

# If dentry/inode cache is excessive: many small files, frequent directory traversals
# long-term fix: fewer files, more efficient directory structure
```

## Fix F — Structural insufficiency

If the workload genuinely needs more RAM than the host has, the long-term options are:

1. **Add RAM** — straightforward on physical hardware; vertical scaling on VMs/cloud
2. **Add swap** — temporary relief only; swap is disk I/O and orders of magnitude slower

```bash
# Add a swap file (immediate, no repartitioning needed)
dd if=/dev/zero of=/swapfile bs=1M count=4096   # 4 GB swap file
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# Persist in /etc/fstab:
# /swapfile  none  swap  sw  0  0
```

3. **OOM killer tuning** — ensure the right processes are protected or sacrificed:

```bash
# Protect a process from OOM kill (score -1000 = never kill)
echo -1000 > /proc/<PID>/oom_score_adj

# Make a process the preferred OOM kill target (score 1000 = kill first)
echo 1000 > /proc/<PID>/oom_score_adj

# In a systemd unit:
# [Service]
# OOMScoreAdjust=-900   # protect this service
```

4. **Reduce workload** — fewer concurrent requests, smaller heap sizes, connection pooling

---

## Prevent recurrence

- **Memory limits per service** — `MemoryMax=` in systemd unit files; limits in cgroup v2
- **Alert at 80% memory used** — before swap kicks in; before the OOM killer fires
- **`earlyoom` daemon** — proactively kills high-score processes before the kernel OOM killer fires (faster, more predictable than kernel OOM)
- **Tune `vm.overcommit_memory`** — for databases that need guaranteed allocation, set `vm.overcommit_memory=2` (never overcommit beyond physical RAM + swap)
- **Profiling in production** — use memory profiling on any long-running process in a staging environment that mirrors production load

## See also

- [[linux-processes]] — reading `ps aux`, kill signals, D-state investigation
- [[linux-storage]] — adding swap space
- [[Service Down — Triage & Recovery]] — if the OOM kill took a service down
