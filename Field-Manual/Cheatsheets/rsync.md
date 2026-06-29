---
type: cheatsheet
area: "CLI Tools"
aliases: []
tags: [backup, sync, remote, ssh, transfer]
status: working
---

# rsync

> **Area:** [[CLI Tools]]

Fast incremental file transfer. Compares source and destination, transfers only the delta. Works locally or over SSH. The backbone of push/pull backups and deployment pipelines.

> **`-a` (archive mode) is the default starting point** for almost every rsync invocation. It implies `-rlptgoD`: recursive, preserve symlinks, permissions, modification times, group, owner, and device files.

---

## 1. Core syntax and flags

```bash
rsync [options] <source> <destination>

# Trailing slash on source matters:
rsync -a /src/dir/  /dst/dir/    # sync *contents* of dir/ into dst/dir/
rsync -a /src/dir   /dst/dir/    # sync dir/ itself into dst/dir/ → dst/dir/dir/
# Rule: source trailing slash = "contents of"; no trailing slash = "the directory itself"
```

Key flags:

```bash
-a          # archive: recursive + preserve permissions, times, symlinks, owner, group
-v          # verbose: show files as they are transferred
-z          # compress data during transfer (useful on slow links; skip on fast LAN)
-P          # --progress + --partial: show per-file progress; resume interrupted transfers
-n          # --dry-run: show what would be transferred without actually doing it
-c          # --checksum: compare by checksum rather than mtime+size (slower, more accurate)
-u          # --update: skip files newer at the destination (don't overwrite newer)
--delete    # delete destination files that no longer exist at the source
--delete-excluded  # also delete destination files that match exclude patterns
-e ssh      # use SSH as the transport (default when host: prefix is present)
-x          # --one-file-system: don't cross filesystem boundaries
-H          # preserve hard links (expensive; omit unless needed)
--stats     # print a summary of transfer statistics at the end
```

## 2. Local sync

```bash
rsync -av /home/alice/ /backup/alice/            # sync home directory contents to backup
rsync -av --delete /src/ /dst/                   # exact mirror: deletions included
rsync -avn /src/ /dst/                           # dry run: see what would change
```

## 3. Remote sync over SSH

```bash
# Push: local → remote
rsync -avz /local/path/ user@host:/remote/path/

# Pull: remote → local
rsync -avz user@host:/remote/path/ /local/path/

# Custom SSH port
rsync -avz -e 'ssh -p 2222' /local/ user@host:/remote/

# Custom SSH key
rsync -avz -e 'ssh -i ~/.ssh/backup_key' /local/ user@host:/remote/

# Restrict to SSH (no shell, only rsync) — server-side authorized_keys trick:
# command="rsync --server --sender -logDtpre.iLsfxC . /backup" ssh-rsa ...
```

## 4. Filtering: include / exclude

```bash
# Exclude by pattern (shell glob, matched against relative paths)
rsync -av --exclude='*.log' /src/ /dst/
rsync -av --exclude='.git/' --exclude='node_modules/' /src/ /dst/

# Exclude list from a file (one pattern per line)
rsync -av --exclude-from=.rsyncignore /src/ /dst/

# Include takes precedence — order matters: include patterns must come before their parent excludes
rsync -av --include='*.conf' --exclude='*' /etc/ /backup/etc/

# Exclude by size (skip files larger than 100 MB)
rsync -av --max-size=100m /src/ /dst/
```

## 5. Hard-link snapshot backups

The `--link-dest` pattern creates space-efficient snapshot backups: each snapshot directory looks complete, but unchanged files are hard links to the previous snapshot rather than copies.

```bash
# Snapshot layout:
# /backup/
#   2024-01-01/
#   2024-01-02/   ← unchanged files are hard links to 2024-01-01/
#   latest → 2024-01-02/

DEST=/backup/$(date +%Y-%m-%d)
LAST=/backup/latest

rsync -a --delete \
  --link-dest="$LAST" \
  /src/ "$DEST/"

# Update the 'latest' symlink
ln -sfn "$DEST" /backup/latest
```

Deleting an old snapshot directory frees only the disk space used by files that changed since the previous snapshot — other files remain via hard links in the newer snapshots.

## 6. Bandwidth and connection control

```bash
rsync -av --bwlimit=5000 /src/ user@host:/dst/   # cap at ~5 MB/s (KiB/s)
rsync -av --timeout=60 /src/ user@host:/dst/      # abort if idle for 60 s
rsync -avP --partial-dir=.partial /src/ /dst/     # hold partial files in a staging dir
```

## 7. Integrity verification

```bash
# -c computes checksums instead of relying on mtime+size; much slower but catches corruption
rsync -avc /src/ /dst/

# After a large transfer, verify the destination independently
rsync -avcn /src/ /dst/   # dry run with checksums — zero files transferred = identical
```

---

## Daily workflows

### "Backup a local directory to a remote host"
```bash
rsync -avz --delete /home/alice/ backup-host:/backups/alice/
```

### "Deploy a website to a remote server (dry run first)"
```bash
rsync -avzn --delete --exclude='.git/' /var/www/site/ web@server:/var/www/site/
# Review the plan, then remove -n:
rsync -avz  --delete --exclude='.git/' /var/www/site/ web@server:/var/www/site/
```

### "Create a daily snapshot backup"
```bash
DEST=/backup/$(date +%F)
rsync -a --delete --link-dest=/backup/latest /data/ "$DEST/"
ln -sfn "$DEST" /backup/latest
```

### "Pull a remote directory to inspect it locally"
```bash
rsync -avz --dry-run user@host:/var/log/ /tmp/remote-logs/
```

## Files & locations

| Path | What |
|---|---|
| `/etc/rsyncd.conf` | rsync daemon config (for pull-from-daemon mode) |
| `~/.ssh/authorized_keys` | per-key `command=` restriction for rsync-only access |

## Gotchas / Golden rules

1. **Source trailing slash is the most common mistake** — `rsync /src /dst` creates `/dst/src`; `rsync /src/ /dst` syncs the contents. When unsure, do a `-n` dry run and check the printed paths.
2. **`--delete` without `--dry-run` is irreversible** — always run `-n` first when using `--delete` against a destination you care about.
3. **Exclude patterns match relative to the transfer root, not the filesystem** — `--exclude='/tmp'` in a sync of `/home/` won't match `/home/alice/tmp`; use `--exclude='tmp/'` (without leading slash).
4. **Hard-link snapshots break across filesystems** — `--link-dest` requires source and destination to be on the same filesystem (hard links cannot cross filesystems); plan backup storage accordingly.
5. **`-z` (compress) can slow transfers on fast networks** — compression CPU overhead exceeds saved bandwidth on a LAN; omit it for local or fast-link transfers.
