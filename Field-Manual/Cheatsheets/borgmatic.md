---
type: cheatsheet
area: Backup & Recovery
aliases: [borg]
tags: [backup, encryption]
status: stable
---

# borgmatic

> **Area:** [[Backup & Recovery]]

Daily-use reference for `borgmatic` (and its underlying `borg`). Commands assume your config
is in a standard location: `/etc/borgmatic/config.yaml`, `/etc/borgmatic.d/*.yaml`, or
`~/.config/borgmatic/config.yaml`. Most read-only actions work without `sudo`; anything
touching system paths or system-wide configs needs root.

> **Syntax note:** modern borgmatic (1.8+) split repo-level from archive-level commands.
> `repo-create`, `repo-info`, `repo-list` operate on the repository; `info`, `list`,
> `extract` operate on individual archives (need `--archive`).

---

## 1. Configuration

```bash
# Generate a fresh sample config with all options documented
sudo borgmatic config generate --destination /etc/borgmatic/config.yaml

# Validate the config file(s) – run this after every edit
borgmatic config validate

# Show the merged effective config (after includes, overrides, etc.)
borgmatic config show

# Where does borgmatic look for config? (in order)
#   /etc/borgmatic/config.yaml
#   /etc/borgmatic.d/*.yaml
#   ~/.config/borgmatic/config.yaml
#   ~/.config/borgmatic.d/*.yaml

# Restore the config itself from a backup (useful after disaster)
borgmatic config bootstrap --repository <repo> --archive latest --destination /tmp/restore
```

---

## 2. Repository setup

```bash
# Create a brand-new encrypted repository (only once, ever)
borgmatic repo-create --encryption repokey-blake2

# Encryption modes worth knowing:
#   repokey-blake2          key stored in repo, encrypted with passphrase (recommended)
#   keyfile-blake2          key stored only on client (safest, but key loss = data loss)
#   none                    no encryption (don't)

# Show repo summary (size on disk, encryption mode, ID)
borgmatic repo-info

# List all archives in the repo
borgmatic repo-list

# Same, but with sizes/dates
borgmatic repo-list --json | jq '.[].archives[] | {name, start, end}'
```

---

## 3. Creating backups

```bash
# Default action: create + prune + compact + check (per config)
sudo borgmatic

# Just create, nothing else
sudo borgmatic create

# Verbose + stats + progress – great for the first manual run
sudo borgmatic create --stats --progress --verbosity 1

# Dry-run: shows what would be backed up, writes nothing
sudo borgmatic create --dry-run --list

# Force a specific config file
sudo borgmatic --config /etc/borgmatic.d/lab.yaml create

# Pick which actions to run explicitly
sudo borgmatic create prune compact check

# Skip a specific action (e.g. only back up, skip checks)
sudo borgmatic --skip-actions check
```

---

## 4. Inspecting archives

```bash
# Repo-level overview (disk usage, dedup stats)
borgmatic repo-info

# Archive-level info (one specific snapshot)
borgmatic info --archive latest
borgmatic info --archive <host>-2026-05-22T03:00:00

# List files inside an archive
borgmatic list --archive latest

# List files matching a pattern
borgmatic list --archive latest --find '*.conf'

# Diff between two archives (what changed?)
borgmatic --verbosity 1 borg diff <archive1> <archive2>
```

---

## 5. Restore: extract & mount

### Extract (copy files out)

```bash
# Extract entire archive to current directory (mind where you are!)
borgmatic extract --archive latest

# Extract to a specific destination
borgmatic extract --archive latest --destination /tmp/restore

# Extract only specific paths (no leading slash!)
borgmatic extract --archive latest \
    --path etc/nginx \
    --path home/<user>/.config \
    --destination /tmp/restore

# Strip leading components from extracted paths
# e.g. with --strip-components 2: "home/<user>/Documents" -> "Documents"
borgmatic extract --archive latest --path home/<user>/Documents --strip-components 2

# Dry-run extract (verifies the archive reads end-to-end, writes nothing)
borgmatic extract --archive latest --dry-run
```

### Mount (browse like a filesystem)

```bash
# Mount latest archive read-only via FUSE
borgmatic mount --archive latest --mount-point /mnt/borg

# Mount the whole repo (every archive as a subdirectory)
borgmatic mount --mount-point /mnt/borg

# Unmount when done
borgmatic umount --mount-point /mnt/borg
```

Mount is the killer feature for "I just want one file" – no full extraction needed.

### Restore databases (separate from file extract)

```bash
# borgmatic extract does NOT restore databases. Use restore for that.
borgmatic restore --archive latest

# Restore one specific database
borgmatic restore --archive latest --database mydb
```

---

## 6. Maintenance

```bash
# Apply retention policy (delete old archives per config)
sudo borgmatic prune

# IMPORTANT: with Borg 1.2+, prune only marks segments for deletion;
# you must run compact to actually free disk space.
sudo borgmatic compact

# Verify repo integrity (fast – metadata only)
sudo borgmatic check

# Full data verification (slow – reads every chunk, re-hashes)
sudo borgmatic check --only data

# Break a stale lock (after a crashed run; check no borg process is alive first!)
borgmatic break-lock
```

---

## 7. Key management

```bash
# Export the repo key – BACK THIS UP SOMEWHERE OUTSIDE THE REPO
borgmatic key export --path /secure/path/repo.key

# Export as printable paper key (for offline cold storage)
borgmatic key export --paper

# Import a key back
borgmatic key import --path /secure/path/repo.key

# Change the passphrase
borgmatic key change-passphrase
```

Without the key + passphrase, the repo is unrecoverable. Store both separately from the repo
itself (a password manager for the passphrase; paper/USB for the key).

---

## 8. Pass-through to raw borg

```bash
# Run any borg command using borgmatic's config (repo path, passphrase, etc.)
borgmatic borg <borg-subcommand>

borgmatic borg list                          # raw borg listing
borgmatic borg info                          # raw borg info output
borgmatic borg with-lock -- some-command     # run a command holding the repo lock
borgmatic borg debug dump-archive <archive>  # advanced debugging
```

---

## 9. systemd integration

```bash
# Status of scheduled borgmatic runs
systemctl status borgmatic.timer
systemctl status borgmatic.service

# When does it run next?
systemctl list-timers borgmatic.timer

# Run a backup right now (uses the systemd unit's env / hardening)
sudo systemctl start borgmatic.service

# Tail the live log
journalctl -u borgmatic.service -f

# Last run's output
journalctl -u borgmatic.service -n 200 --no-pager

# Disable/enable the schedule
sudo systemctl disable --now borgmatic.timer
sudo systemctl enable --now borgmatic.timer
```

See also [[systemd]] for the unit/timer surface, and [[systemd Service and Timer]] for a template.

---

## 10. Useful environment variables

```bash
# Passphrase (avoid in shell history – use a file or a password-manager integration)
export BORG_PASSPHRASE='...'
export BORG_PASSCOMMAND='cat /path/to/borg-passphrase'

# SSH options for remote repos (custom port, identity file)
export BORG_RSH='ssh -i /path/to/borg_ed25519 -p 2222'

# Auto-answer "yes" to relocate/checks prompts (use carefully)
export BORG_RELOCATED_REPO_ACCESS_IS_OK=yes
export BORG_UNKNOWN_UNENCRYPTED_REPO_ACCESS_IS_OK=yes
```

In borgmatic config these map to `encryption_passcommand:` and `ssh_command:`.

---

## Daily workflows

### "Did the backup actually run last night?"
```bash
systemctl status borgmatic.timer
journalctl -u borgmatic.service --since yesterday
borgmatic repo-list | tail -5
```

### "I need to restore a single file"
```bash
borgmatic mount --archive latest --mount-point /mnt/borg
# ...browse, cp, scp, whatever...
borgmatic umount --mount-point /mnt/borg
```

### "Test restore drill"
See the full procedure: [[Backup Restore Drill]].

### "Backup is too big / repo growing fast"
```bash
borgmatic repo-info                              # dedup stats
borgmatic info --archive latest                  # this run's contribution
sudo borgmatic prune --stats --list              # what would prune remove?
sudo borgmatic compact                           # reclaim space after prune
```

### "Repo is locked"
```bash
ps aux | grep borg          # make sure no borg process is running first!
borgmatic break-lock
```

### "Migrating to a new repo / new host"
```bash
borgmatic transfer --source-repository <old-repo> --repository <new-repo>   # preserves dedup
```

---

## Files & locations

| Path | What |
| --- | --- |
| `/etc/borgmatic/config.yaml` | Primary system config |
| `/etc/borgmatic.d/*.yaml` | Multiple configs (per-job style) |
| `~/.config/borgmatic/config.yaml` | User-level config |
| `~/.cache/borg/` | Borg's chunk cache (large, regeneratable) |
| `~/.config/borg/keys/` | Repo keyfiles (for keyfile-* modes) |
| `/var/log/borgmatic.log` | Optional log file (if configured) |

---

## Golden rules

1. **A backup you've never restored is not a backup.** Schedule restore drills.
2. **Back up the key separately from the repo.** A paper key in a safe is not paranoid.
3. **`prune` without `compact` does not free space** on Borg 1.2+.
4. **`check --only data` is expensive but priceless.** Run it monthly or so.
5. **Document the repo path, key location, and passphrase store** somewhere that survives the
   server dying.

## Further reading
- [borgmatic documentation](https://torsion.org/borgmatic/)
- [Borg documentation](https://borgbackup.readthedocs.io/)
