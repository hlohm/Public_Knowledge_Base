---
type: cheatsheet
area: "Backup & Recovery"
aliases: [hard-link snapshots, rsync backup]
tags: [backup, rsync, snapshots, hard-links]
status: working
---

# rsync Snapshots

> **Area:** [[Backup & Recovery]]

The hard-link snapshot pattern using [[rsync]]'s `--link-dest`. Each snapshot directory appears to contain a complete copy of the source, but unchanged files are hard links to previous snapshots — so only changed files consume new disk space.

> This is a pure-filesystem technique: snapshots are plain directories. Any tool can read them; no special software is needed to restore. The trade-off: no encryption, no deduplication beyond hard links, and no compression.

---

## 1. The pattern

```bash
#!/bin/bash
# /usr/local/bin/snapshot.sh
set -euo pipefail

SRC=/data/                          # source (trailing slash = contents of)
DST=/backup/snapshots               # snapshot root
LATEST="$DST/latest"
SNAP="$DST/$(date +%Y-%m-%dT%H:%M:%S)"

rsync -a --delete \
  ${LATEST:+--link-dest="$LATEST"} \
  "$SRC" "$SNAP/"

ln -sfn "$SNAP" "$LATEST"           # update the 'latest' symlink
```

The `${LATEST:+--link-dest="$LATEST"}` construct passes `--link-dest` only if `$LATEST` resolves (i.e., not on the first run when no previous snapshot exists).

## 2. Layout

```
/backup/snapshots/
  latest -> 2024-06-15T03:00:00    ← symlink, always points to newest
  2024-06-15T03:00:00/             ← newest snapshot (real files)
  2024-06-14T03:00:00/             ← unchanged files are hard links to ^
  2024-06-13T03:00:00/
  2024-06-12T03:00:00/
```

Hard links mean:
- Each directory looks complete (browse, restore files directly)
- `du -sh` on the whole root shows real usage; `du -sh` on individual snapshots over-counts (hard links are counted once per inode)
- Deleting an old snapshot frees only the space occupied by files that changed since the next snapshot

## 3. Remote source (pull backup)

```bash
rsync -a --delete \
  ${LATEST:+--link-dest="$LATEST"} \
  -e 'ssh -i /etc/backup/backup_key -o StrictHostKeyChecking=yes' \
  backup-user@server:/data/ \
  "$SNAP/"
```

Use a dedicated SSH key with command restriction in `authorized_keys`:

```
# /home/backup-user/.ssh/authorized_keys on the source server:
command="rsync --server --sender -logDtpre.iLsfxC . /data/" ssh-rsa <backup-pubkey>
```

This restricts the backup key to read-only rsync access; it cannot be used for a shell.

## 4. Retention: pruning old snapshots

Hard-link snapshots are plain directories. Delete them with `rm -rf`:

```bash
# Keep last 7 daily snapshots
ls -1d /backup/snapshots/????-??-??T* | sort | head -n -7 | xargs -r rm -rf

# Keep last 30 days of daily + last 12 months of monthly
# (implement with a wrapper script or use a tool like tmpreaper)
```

**Safe pruning order:** delete oldest first. Deleting a snapshot does not affect newer snapshots (hard links in newer snapshots remain valid).

## 5. Verify disk usage

```bash
# Real disk usage of the entire snapshot pool
du -sh /backup/snapshots/

# Snapshot-by-snapshot size of NEW (non-linked) files only
# Use rsync's own --stats when taking the snapshot, or:
du --count-links -sh /backup/snapshots/????-??-??T*/  # counts links once per inode (wrong for comparison)
# Better: note the before/after usage of the filesystem:
df -h /backup        # before
# ... take snapshot ...
df -h /backup        # after; difference = new data only
```

## 6. Restore

No special software needed. Snapshots are ordinary directories:

```bash
# Browse
ls /backup/snapshots/latest/

# Restore a single file
cp /backup/snapshots/latest/home/alice/document.txt /home/alice/

# Restore a directory
rsync -a /backup/snapshots/2024-06-14T03:00:00/home/alice/ /home/alice/

# Full restore of the source
rsync -a /backup/snapshots/latest/ /data/
```

---

## Daily workflows

### "Take a snapshot now"
```bash
/usr/local/bin/snapshot.sh
ls -la /backup/snapshots/latest/
```

### "Restore a file from 3 days ago"
```bash
ls /backup/snapshots/ | sort | tail -5     # find the right snapshot
cp /backup/snapshots/2024-06-12T03:00:00/data/important.txt /tmp/
```

### "Check how much space the backup pool is using"
```bash
df -h /backup
du -sh /backup/snapshots/
ls /backup/snapshots/ | wc -l             # how many snapshots exist
```

## Gotchas / Golden rules

1. **Snapshots must be on the same filesystem for hard links to work** — hard links cannot cross filesystem boundaries; keep `$DST` on the same partition or mount point. If using a separate backup disk, mount it at the same location every time.
2. **`latest` is a symlink, not a directory** — `rsync /backup/snapshots/latest /dst` may follow or not follow the symlink depending on the trailing slash; use `rsync /backup/snapshots/latest/ /dst/` (trailing slash on both) to sync the contents.
3. **`--delete` is required for the snapshot to reflect deletions** — without it, files deleted from the source accumulate across all future snapshots; `--delete` removes them from each new snapshot's view.
4. **`du` on individual snapshots over-counts** — because hard-linked files are shared; `du -sh /backup/snapshots/2024-06-14/` shows the sum as if all files were unique. Use `df` on the filesystem to see actual usage.
5. **This pattern provides no encryption** — if the backup destination is untrusted (cloud storage, remote host), use [[restic]] or [[borgmatic]] instead; they encrypt before writing.
