---
type: playbook
area: "Linux Administration"
tags: [linux, disk, storage, triage, incident]
status: working
---

# Disk Full

> **Area:** [[Linux Administration]]

A filesystem has hit 100% (or close to it). Writes are failing, services are erroring, or you've received an alert. Work through this playbook to identify the cause, free space immediately, and prevent recurrence.

---

## Situation

- `df -h` shows a filesystem at 100% (or `No space left on device` errors in logs)
- A service failed to start or is crashing with write errors
- Disk usage alert from monitoring

## Quick assessment

```bash
df -h                                    # which filesystem is full?
df -i                                    # also check inodes — can be exhausted independently
du -sh /* 2>/dev/null | sort -rh         # top-level directories

# Quickly find the biggest things
du -sh /var/log/*/  2>/dev/null | sort -rh | head -10
du -sh /home/*/     2>/dev/null | sort -rh | head -10
find / -xdev -type f -size +100M -printf '%s\t%p\n' 2>/dev/null | sort -rn | head -20
```

---

## Decision branches

| Observation | Go to |
|---|---|
| `df -i` shows 100% inodes but `df -h` shows free space | Fix I — Inode exhaustion |
| `/var/log` is the culprit | Fix A — Log accumulation |
| Core files or crash dumps filling space | Fix B — Core dumps |
| Container or Docker storage | Fix C — Container storage |
| Database data directory | Fix D — Database growth |
| Package cache | Fix E — Package cache |
| User home directories | Fix F — User data |
| Temporary files | Fix G — Temp files |
| Deleted files still held open | Fix H — Deleted files held open |

---

## Fix A — Log accumulation

```bash
du -sh /var/log/*/  | sort -rh | head -10

# Compressed old logs (respects logrotate rules)
logrotate --force /etc/logrotate.conf

# Check for services logging too verbosely
journalctl --disk-usage
journalctl --vacuum-size=500M         # trim journal immediately

# Truncate a specific log file (do not delete an active log — the process holds the fd)
truncate -s 0 /var/log/myapp/app.log
# Then: signal the app to reopen:
systemctl kill --signal=USR1 myapp   # or: kill -HUP <pid>

# Fix the root cause: set LogLevel appropriately; configure logrotate
```

## Fix B — Core dumps

```bash
ls -lah /var/crash/ /tmp/ /core*     # common dump locations

# Disable core dumps for non-debug systems
ulimit -c 0                           # current session
echo "* hard core 0" >> /etc/security/limits.conf

# Clean existing dumps
find /var -name 'core' -o -name 'core.*' | xargs ls -lah
find /var -name 'core' -o -name 'core.*' | xargs rm -f

# systemd coredump storage
coredumpctl list                      # list saved core dumps
journalctl -u systemd-coredump        # related logs
# /etc/systemd/coredump.conf: Storage=none (to disable)
```

## Fix C — Container storage (Docker / Podman)

```bash
docker system df                      # usage breakdown: images, containers, volumes
docker system prune -f                # remove stopped containers, dangling images, unused networks
docker image prune -a                 # remove ALL unused images (including non-dangling)
docker volume prune                   # remove unused volumes (data loss risk — confirm first)

# Identify storage location
docker info | grep 'Docker Root Dir'
du -sh $(docker info -f '{{.DockerRootDir}}')
```

## Fix D — Database growth

```bash
# PostgreSQL
psql -c "SELECT pg_database_size(datname), datname FROM pg_database ORDER BY 1 DESC;"
psql -c "SELECT pg_size_pretty(pg_total_relation_size(relid)), relname FROM pg_stat_user_tables ORDER BY 1 DESC LIMIT 20;"
# Vacuum to reclaim space from dead tuples
psql -c "VACUUM FULL mydb;"   # locks table; use during maintenance window

# MySQL / MariaDB
mysql -e "SELECT table_schema, SUM(data_length+index_length)/1024/1024 MB FROM information_schema.tables GROUP BY 1 ORDER BY 2 DESC LIMIT 10;"
mysqlcheck --optimize --all-databases  # reclaim fragmented space

# General: check binary logs / WAL files
ls -lah /var/lib/mysql/mysql-bin.*   # MySQL binary logs
ls -lah /var/lib/postgresql/*/main/pg_wal/   # PostgreSQL WAL
```

## Fix E — Package cache

```bash
# Debian/Ubuntu
apt clean             # remove all cached .deb files
apt autoremove        # remove orphaned packages

# RHEL/Fedora
dnf clean all         # remove all cached metadata and packages

# Pacman
pacman -Sc            # remove old (non-current) package files from cache
paccache -rk2         # keep last 2 versions of each package
```

## Fix F — User data

```bash
du -sh /home/*/  | sort -rh
du --exclude='.cache' -sh /home/alice/   # how much is not cache?

# Large files in home
find /home -type f -size +500M 2>/dev/null | xargs ls -lah
find /home -type f -name '*.iso' -o -name '*.vmdk' 2>/dev/null
```

## Fix G — Temp files

```bash
ls -lah /tmp/
ls -lah /var/tmp/
du -sh /tmp/ /var/tmp/

# Find old temp files (older than 7 days)
find /tmp -type f -mtime +7 | head -20

# Systemd-tmpfiles handles /tmp and /var/tmp cleanup automatically on systemd systems
systemd-tmpfiles --clean
# /etc/tmpfiles.d/ — add rules if needed
```

## Fix H — Deleted files still held open

A process can hold a file descriptor open even after the file has been deleted from the directory. The space is not freed until the process closes or releases the fd. Common cause: log files deleted while the service was running.

```bash
# Find deleted files still held open (requires root)
lsof | grep '(deleted)'
lsof | grep 'deleted' | awk '{print $2, $9}' | sort -u

# The PID in column 2 is the process holding the file open
# Options:
# 1. Restart the process (closes the fd, frees the space)
# 2. Truncate via /proc (does not require restart):
truncate -s 0 /proc/<PID>/fd/<FD>
# Find FD: lsof -p <PID> | grep deleted
```

## Fix I — Inode exhaustion

```bash
df -i                      # which filesystem has 100% inode usage?
for dir in /*/; do echo "$dir: $(find "$dir" -maxdepth 0 -type d -printf '' && find "$dir" | wc -l)"; done
# Or more efficiently:
find / -xdev -type d | while read d; do echo "$(find "$d" -maxdepth 1 | wc -l) $d"; done | sort -rn | head -20

# Common causes: mail spool, node_modules, PHP session files, package cache fragments
find /var/spool -type f | wc -l      # mail spool
find /tmp -type f | wc -l            # temp file count

# Clean PHP sessions
find /var/lib/php/sessions -type f -mtime +1 -delete

# Clean npm/node_modules recursively (use only in dev contexts)
find . -name 'node_modules' -type d -prune -exec rm -rf {} +
```

---

## Immediate space recovery (emergency)

When you need to free space fast to restore service, in this priority order:

1. `apt clean` / `dnf clean all` — safe, 100–500 MB typical
2. `journalctl --vacuum-size=200M` — safe, potentially GBs
3. `docker system prune -f` — safe if containers aren't in use
4. Delete old log archives: `find /var/log -name '*.gz' -mtime +7 -delete`
5. Delete large temp files: `find /tmp -size +100M -mtime +1 -delete`
6. Kill the worst offender (note: this may take a service down)

**Do not:** delete files from running database data directories, delete active log files (truncate instead), or delete files owned by running services without understanding the impact.

---

## Prevent recurrence

- **logrotate** — ensure every application's logs have a logrotate config; check `/etc/logrotate.d/`
- **Monitoring** — alert at 80%, page at 90%; never wait for 100%
- **Quotas** — `quotaon` / `edquota` for per-user limits on shared systems
- **Filesystem sizing** — separate filesystems for `/var/log`, `/var/lib/docker`, databases; prevents one runaway from taking down the whole host
- **Automated cleanup** — `systemd-tmpfiles` for temp dirs; `cron` job for old log archives

## See also

- [[linux-storage]] — disk inspection, LVM, SMART
- [[linux-logging]] — journald config and logrotate
- [[linux-processes]] — finding the process causing the issue
