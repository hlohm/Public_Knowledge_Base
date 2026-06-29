---
type: cheatsheet
area: "CLI Tools"
aliases: []
tags: [archives, compression, backup]
status: working
---

# tar

> **Area:** [[CLI Tools]]

Create, inspect, and extract archives. Combines multiple files/directories into a single file, optionally compressed. The universal Unix archive format.

> Modern tar accepts `tar czf archive.tar.gz dir/` without the leading `-`. Both styles work; the examples here use the short form.

---

## 1. Create archives

```bash
tar czf archive.tar.gz  dir/          # gzip compression  (.tar.gz / .tgz)
tar cjf archive.tar.bz2 dir/          # bzip2 compression (.tar.bz2) — smaller, slower
tar cJf archive.tar.xz  dir/          # xz compression    (.tar.xz)  — smallest, slowest
tar cf  archive.tar     dir/          # no compression (just archive, no compress)
tar czf archive.tar.gz  file1 file2 dir3/   # multiple sources

# Verbose: print each filename as it is added
tar czvf archive.tar.gz dir/
```

## 2. Extract archives

```bash
tar xzf archive.tar.gz                # extract into current directory
tar xzf archive.tar.gz -C /dest/dir/  # extract into a specific directory (must exist)
tar xjf archive.tar.bz2
tar xJf archive.tar.xz
tar xf  archive.tar.gz                # let tar detect compression automatically (GNU tar)

# Extract only specific files/paths
tar xzf archive.tar.gz dir/subdir/file.conf

# Verbose: print each filename as it is extracted
tar xzvf archive.tar.gz
```

## 3. List contents (inspect without extracting)

```bash
tar tzf archive.tar.gz                # list all files in the archive
tar tzf archive.tar.gz | grep '\.conf$'  # filter listing
tar tvf archive.tar.gz                # long listing: permissions, owner, size, mtime
```

## 4. Exclude and filter

```bash
tar czf backup.tar.gz /home/alice/ \
  --exclude='/home/alice/.cache' \
  --exclude='*.log' \
  --exclude-from=.tarignore             # patterns file, one per line

# Exclude files newer than a reference file (e.g., incremental backup)
tar czf incremental.tar.gz /data/ --newer-mtime='2024-01-01'

# Exclude files larger than 100 MB
tar czf backup.tar.gz /home/ --exclude='*.iso'  # simpler to just exclude known large types
```

## 5. Append and update

```bash
tar rf  archive.tar newfile.txt        # append a file (no compression on existing archive)
tar uf  archive.tar changed-file.txt   # update: replace only if newer than the archived copy
```

## 6. Preserve and restore permissions

```bash
tar czf archive.tar.gz --preserve-permissions /etc/   # (default for root; explicit for clarity)
tar xzf archive.tar.gz --preserve-permissions         # restore permissions exactly

# Extract without restoring ownership (useful for non-root restore)
tar xzf archive.tar.gz --no-same-owner
```

## 7. Pipelines

```bash
# Create and stream directly to another host
tar czf - /data/ | ssh user@host 'tar xzf - -C /backup/'

# Stream an archive from a remote host and extract locally
ssh user@host 'tar czf - /data/' | tar xzf - -C /restore/

# Disk-to-disk copy preserving all metadata (alternative to cp -a for edge cases)
tar cf - /src/ | tar xf - -C /dst/
```

---

## Daily workflows

### "Archive a directory to send to someone"
```bash
tar czf project-$(date +%F).tar.gz project/
```

### "Inspect an archive before extracting"
```bash
tar tvf archive.tar.gz | less
```

### "Extract a single config file from a backup archive"
```bash
tar xzf backup.tar.gz -C /tmp/ etc/nginx/nginx.conf
# File lands at /tmp/etc/nginx/nginx.conf
```

### "Compress and stream to remote in one step"
```bash
tar czf - /var/www/html/ | ssh deploy@webserver 'cat > /backups/html-$(date +%F).tar.gz'
```

## Gotchas / Golden rules

1. **Always inspect before extracting to the current directory** — `tar t` first to check for path traversal (absolute paths like `/etc/passwd`) or badly structured archives that unpack into many loose files instead of a single directory.
2. **`-C` must point to an existing directory** — tar will not create it.
3. **Compression suffix does not auto-detect on extract** — except with GNU tar's `-a` (auto-detect from suffix) or bare `xf`; always specify the right flag (`z`/`j`/`J`) or use `xf` and let GNU tar guess.
4. **Appending (`r`/`u`) does not work on compressed archives** — you must decompress first, append, then recompress.
5. **`--exclude` path must match the path as it appears in the archive** — when archiving `/home/alice/`, use `--exclude='/home/alice/.cache'` with the full leading path.
