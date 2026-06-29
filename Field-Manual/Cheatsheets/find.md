---
type: cheatsheet
area: "CLI Tools"
aliases: []
tags: [search, filesystem, files]
status: working
---

# find

> **Area:** [[CLI Tools]]

Recursively search a directory tree for files matching criteria. The general-purpose filesystem search tool — by name, type, size, modification time, permissions, and more.

> Prefer [[ripgrep]] for searching *inside* files. `find` is for locating files by their metadata.

---

## 1. Core syntax

```bash
find <path> [tests] [actions]

find .            # list every file under the current directory
find /etc -name '*.conf'             # by name (case-sensitive glob)
find /etc -iname '*.conf'            # case-insensitive name match
find . -name '*.log' -o -name '*.tmp'  # OR: files matching either pattern
```

## 2. Type and name

```bash
find . -type f          # regular files only
find . -type d          # directories only
find . -type l          # symbolic links only

find . -name 'Makefile'              # exact filename
find . -name '*.py' -not -name '*test*'   # .py files that are not tests
find . -path '*/migrations/*.py'     # match against the full relative path
```

## 3. Size

```bash
find . -size +100M      # larger than 100 MB
find . -size -1k        # smaller than 1 KB
find . -size +10M -size -1G          # between 10 MB and 1 GB
find . -empty           # zero-size files (and empty directories)
```

## 4. Time

```bash
find . -mtime -7        # modified in the last 7 days
find . -mtime +30       # modified more than 30 days ago
find . -newer /tmp/reference-file    # modified more recently than reference-file
find . -mmin -60        # modified in the last 60 minutes
find . -atime +90       # accessed more than 90 days ago (useful before cleaning)
```

## 5. Permissions and ownership

```bash
find . -perm 644        # exact permissions 644
find . -perm -644       # at minimum bits 644 are set
find . -perm /111       # any executable bit set (owner, group, or other)
find . -perm -4000      # setuid bit set
find . -perm -2000      # setgid bit set

find . -user alice      # owned by alice
find . -group webdev    # owned by group webdev
find . -nouser          # no corresponding /etc/passwd entry (orphaned files)
```

## 6. Actions

```bash
# Default action is -print (one file per line)
find . -name '*.bak' -print

# Execute a command on each result (shell quoting matters)
find . -name '*.log' -exec rm {} \;          # one command per file
find . -name '*.log' -exec rm {} +           # batch: pass multiple files to one invocation (faster)

# Interactive: ask before each action
find . -name '*.bak' -ok rm {} \;

# Print with null delimiter (safe with filenames containing spaces/newlines)
find . -name '*.log' -print0 | xargs -0 rm

# -exec with shell (needed when you want pipes or redirects)
find . -name '*.conf' -exec sh -c 'cp "$1" "$1.bak"' _ {} \;
```

## 7. Pruning and exclusions

```bash
# Exclude a directory from the search
find . -path ./.git -prune -o -name '*.py' -print

# Exclude multiple directories
find . \( -name .git -o -name node_modules -o -name __pycache__ \) -prune -o -type f -print

# Don't cross filesystem boundaries
find / -xdev -name '*.log'
```

---

## Daily workflows

### "Find large files taking up disk space"
```bash
find / -xdev -type f -size +500M -printf '%s %p\n' | sort -rn | head -20
```

### "Find recently modified configs"
```bash
find /etc -type f -mtime -1 -name '*.conf'
```

### "Find and delete old temp files"
```bash
find /tmp -type f -mtime +7 -print0 | xargs -0 rm -f
```

### "Find all setuid binaries on the system"
```bash
find / -xdev -perm -4000 -type f -print
```

### "Find files not accessed in 90 days (before archiving)"
```bash
find /data -type f -atime +90 | tee stale-files.txt
```

## Gotchas / Golden rules

1. **`-exec {} \;` runs one process per file** — use `{} +` for bulk operations; it's much faster.
2. **`-prune` requires `-o -print` after it** — `-prune` alone just stops descent into the directory without printing anything; pair it with `-o -print` or `-o -type f -print` to get the rest of the results.
3. **`-mtime n` means "n×24h ago"** — `-mtime -7` means modified within the last 7×24 hours, not within 7 calendar days; `find` is not timezone-aware.
4. **Always test a destructive find with `-print` before adding `-exec rm`** — run the exact same `find` without the action first, verify the file list, then add `-exec rm {} +`.
5. **`-name` matches the filename only, not the path** — use `-path` (or `-wholename`) when you need to match directory components.
