---
type: cheatsheet
area: "Backup & Recovery"
aliases: []
tags: [backup, restic, encryption, deduplication, recovery]
status: working
---

# restic

> **Area:** [[Backup & Recovery]]

Single-binary backup tool with content-addressable, deduplicated, encrypted, compressed snapshots. Supports local, SFTP, S3, B2, Azure, GCS, and REST-server backends. The modern alternative to [[borgmatic]].

> All data is encrypted client-side with AES-256 before leaving your machine. The repository server never sees plaintext.

---

## 1. Initialise and configure

```bash
# Set credentials in environment (avoid shell history)
export RESTIC_REPOSITORY=/backup/myrepo
export RESTIC_PASSWORD='<strong-passphrase>'   # or RESTIC_PASSWORD_FILE=/etc/restic-pass

# Initialise a new repository
restic init                         # local
restic -r sftp:user@host:/backup init           # SFTP
restic -r s3:s3.amazonaws.com/<bucket> init     # S3 (set AWS_* env vars)
restic -r b2:<bucket>:<path> init               # Backblaze B2 (set B2_* env vars)

# Verify the repository is accessible
restic snapshots                    # lists snapshots (empty on a new repo)
```

## 2. Backup

```bash
restic backup /home/alice/           # back up a directory
restic backup /home/alice/ /etc/     # back up multiple paths
restic backup --verbose /data/       # show file-by-file progress

# Exclude patterns
restic backup /home/alice/ \
  --exclude='.cache' \
  --exclude='*.iso' \
  --exclude-file=/etc/restic-excludes.txt

# Tags (useful for filtering snapshots later)
restic backup /data/ --tag daily --tag production

# Backup from stdin (e.g., a database dump)
mysqldump mydb | restic backup --stdin --stdin-filename db.sql
pg_dump mydb | restic backup --stdin --stdin-filename mydb.sql
```

## 3. List and inspect snapshots

```bash
restic snapshots                    # all snapshots
restic snapshots --tag daily        # filter by tag
restic snapshots --host myserver    # filter by host
restic snapshots --json | jq .      # machine-readable

restic ls <snapshot-id>             # list files in a snapshot
restic ls latest                    # latest snapshot (special keyword)
restic ls latest /home/alice/       # files in a subdirectory of latest

restic stats                        # repository size and deduplication stats
restic stats latest                 # stats for the latest snapshot only
```

## 4. Restore

```bash
# Full restore
restic restore latest --target /restore/

# Restore a specific snapshot
restic restore <snapshot-id> --target /restore/

# Restore only specific files/paths
restic restore latest --target /tmp/restore --include '/home/alice/.ssh/'

# Mount the repository as a filesystem (requires FUSE)
restic mount /mnt/restic            # browse all snapshots as a filesystem
ls /mnt/restic/snapshots/           # each snapshot is a directory
# Ctrl+C to unmount

# Restore a single file
restic restore latest --target /tmp/restore --include '/path/to/file.conf'
# File lands at /tmp/restore/path/to/file.conf
```

## 5. Forget and prune (retention)

```bash
# Define a retention policy and apply it
restic forget \
  --keep-daily   7  \
  --keep-weekly  4  \
  --keep-monthly 6  \
  --keep-yearly  2

# Forget + prune in one step (removes unreferenced data)
restic forget --keep-daily 7 --keep-weekly 4 --prune

# Dry run: see what would be forgotten
restic forget --keep-daily 7 --keep-weekly 4 --dry-run

# Prune without forgetting (free space after forget)
restic prune
```

## 6. Verify integrity

```bash
restic check                        # check repository metadata integrity
restic check --read-data            # also read and verify all data blobs (slow; thorough)
restic check --read-data-subset=10% # verify 10% of data blobs (faster; use regularly)
```

## 7. Automation pattern

```bash
#!/bin/bash
# /usr/local/bin/restic-backup.sh
set -euo pipefail
export RESTIC_REPOSITORY=/backup/myrepo
export RESTIC_PASSWORD_FILE=/etc/restic-password

restic backup \
  --verbose \
  --exclude-file=/etc/restic-excludes.txt \
  --tag daily \
  /home/ /etc/ /var/lib/ 2>&1

restic forget \
  --keep-daily   7  \
  --keep-weekly  4  \
  --keep-monthly 6  \
  --prune 2>&1

restic check --read-data-subset=5% 2>&1
```

Run via systemd timer or cron. See [[linux-timers]].

---

## Daily workflows

### "Back up and verify a quick snapshot"
```bash
restic backup /home/alice/
restic snapshots | head -5
restic check
```

### "Restore a single accidentally deleted file"
```bash
restic snapshots | head -10                   # find the snapshot
restic ls <snapshot-id> | grep 'filename'     # confirm it's there
restic restore <snapshot-id> --target /tmp/restore --include '/home/alice/important.txt'
ls /tmp/restore/home/alice/important.txt
```

### "Verify you can actually restore (run regularly)"
```bash
restic restore latest --target /tmp/restore-test
ls -la /tmp/restore-test
rm -rf /tmp/restore-test
```

## Files & locations

| Path | What |
|---|---|
| `RESTIC_REPOSITORY` | Backend path (env var) |
| `RESTIC_PASSWORD_FILE` | Path to file containing the passphrase |
| `/etc/restic-excludes.txt` | One glob pattern per line |

## Gotchas / Golden rules

1. **Lose the passphrase = lose your backups** — restic cannot be brute-forced; store the passphrase in a password manager, offline, and with your emergency kit.
2. **`forget` does not free disk space; `prune` does** — `forget` just marks snapshots for removal; run `--prune` or a separate `restic prune` to actually reclaim space.
3. **`restic check` is not a restore test** — check verifies the repository structure; only `restic restore` confirms you can actually get your data back. Run restore tests regularly.
4. **The repository must not be modified by anything other than restic** — never `rsync` or `cp` into a restic repo directory; restic maintains an internal index that will become inconsistent.
5. **`--stdin-filename` is required for stdin backups** — without it, restic names the backed-up data `stdin`; using a descriptive name makes restoring from specific database dumps practical.
