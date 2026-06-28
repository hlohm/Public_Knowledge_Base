---
type: cheatsheet
area: Linux Administration
aliases: [snapper, subvolume, snapshot, btrfs-snapshot]
tags: [storage, filesystem, btrfs, snapshots, backup]
status: working
---

# btrfs

> **Area:** [[Linux Administration]]

Daily-use reference for the btrfs filesystem — subvolumes, snapshots, scrub/balance, device
management — and **snapper** for managed, scheduled, pre/post snapshots on top of it. Pairs
with [[borgmatic]] (whose btrfs hook snapshots subvolumes before archiving) and with
[[systemd.exec]] (the snapshot hook needs `PrivateDevices=no` + `CAP_SYS_ADMIN`/`CAP_DAC_OVERRIDE`).

> Anything mutating the filesystem or its devices needs `sudo`. `btrfs check --repair` and
> `btrfs balance` on a full disk are the two commands that can make a bad day worse — read the
> Gotchas before either.

---

## 1. Filesystem inspection (the df on btrfs lies)

```bash
# All btrfs filesystems, their devices and raw usage
sudo btrfs filesystem show

# REAL space picture — plain `df` is misleading on btrfs (CoW, metadata, RAID profiles).
# Use these instead:
sudo btrfs filesystem usage /            # the one to trust: data/metadata/unallocated split
sudo btrfs filesystem df /               # per-chunk-type allocation (data vs metadata vs system)

# Per-device error counters (watch these — non-zero = failing disk or cable)
sudo btrfs device stats /
```

---

## 2. Subvolumes

A subvolume is an independently-snapshottable, separately-mountable sub-tree. The Arch/CachyOS
convention is a flat layout of top-level subvolumes named `@` (mounted at `/`), `@home`, `@log`,
`@snapshots`, etc.

```bash
# List subvolumes (with IDs; -t for a table; -a for absolute paths)
sudo btrfs subvolume list -t /

# Create / delete a subvolume
sudo btrfs subvolume create /path/sub
sudo btrfs subvolume delete /path/sub        # needs CAP_SYS_ADMIN (matters in hardened units)

# Inspect one subvolume (UUID, parent, received UUID, gen, flags)
sudo btrfs subvolume show /path/sub

# The default subvolume that mounts at the FS root (rollback changes this)
sudo btrfs subvolume get-default /
sudo btrfs subvolume set-default <ID> /
```

---

## 3. Snapshots (CoW — instant, cheap, not a backup)

```bash
# Writable snapshot (a normal subvolume you can modify)
sudo btrfs subvolume snapshot /  /path/snap-rw

# READ-ONLY snapshot (-r) — required as a `btrfs send` source, and what backup hooks take
sudo btrfs subvolume snapshot -r /  /path/snap-ro

# Flip a snapshot's read-only flag if you need to write to it
sudo btrfs property get  /path/snap ro
sudo btrfs property set  /path/snap ro false
```

A snapshot shares blocks with its source (copy-on-write), so it's near-instant and initially
free — but it lives on the **same disk**. It protects against "oops I deleted that / a bad
update", **not** against drive failure. A real backup leaves the device (see §4 and [[borgmatic]]).

---

## 4. send / receive (snapshots that leave the disk)

```bash
# Full send of a read-only snapshot to another btrfs filesystem
sudo btrfs send /path/snap-ro | sudo btrfs receive /mnt/backup/

# Incremental: only the delta since a common parent snapshot (-p)
sudo btrfs send -p /path/snap-prev /path/snap-now | sudo btrfs receive /mnt/backup/

# Over the network (pipe through ssh)
sudo btrfs send -p /path/prev /path/now | ssh <host> 'sudo btrfs receive /mnt/backup/'
```

Both ends must be btrfs, and the source must be **read-only**. The receiving side keeps the
`received_uuid`, which is how the next `-p` incremental finds its common parent.

---

## 5. Integrity & maintenance

```bash
# SCRUB — read every block, verify checksums, repair from a good copy if the profile allows.
# Run periodically (monthly). Safe to run on a mounted, live filesystem.
sudo btrfs scrub start /
sudo btrfs scrub status /
sudo btrfs scrub cancel /

# BALANCE — rewrite/relocate chunks to reclaim partly-empty allocations. Use FILTERS, not a
# bare balance, or you'll rewrite the whole FS. -dusage/-musage limit it to near-empty chunks.
sudo btrfs balance start -dusage=50 -musage=50 /
sudo btrfs balance status /

# DEFRAGMENT — only when you have a specific fragmentation problem (e.g. a CoW DB file).
# -r recursive, -czstd recompress while at it.
sudo btrfs filesystem defragment -r -czstd /path
```

> **CoW + random-write files** (VM images, databases, big append logs) fragment badly. Disable
> CoW per-file/dir with `chattr +C` *before* the file has data (it only takes effect on a
> newly-created, empty file), or mount such a subvolume with `nodatacow`.

---

## 6. Mount options worth knowing

```bash
# Typical fstab line for a compressed, snapshot-friendly root subvolume:
#   UUID=<uuid> /  btrfs  subvol=@,compress=zstd:1,noatime,ssd  0 0
```

| Option | Effect |
| --- | --- |
| `subvol=@` / `subvolid=<N>` | mount a specific subvolume as this path |
| `compress=zstd:1` | transparent compression (1 = fast, low-CPU; up to :15) |
| `noatime` | don't write access times — big win on snapshot-heavy roots |
| `ssd` | SSD allocation heuristics (usually auto-detected) |
| `nodatacow` | disable CoW (and checksums) for this mount — for DB/VM subvolumes |
| `degraded` | mount a multi-device FS with a disk missing (recovery) |

---

## 7. snapper — managed snapshots, pre/post, timelines

snapper wraps the raw snapshot above with configs, automatic timeline snapshots, paired
pre/post snapshots around risky operations, cleanup policies, and diff/rollback.

### Configs
```bash
# Create a config for a subvolume (makes a .snapshots subvol + /etc/snapper/configs/<name>)
sudo snapper -c root create-config /
sudo snapper list-configs

# Per-config policy lives in /etc/snapper/configs/<name> — key knobs:
#   TIMELINE_CREATE="yes"            hourly timeline snapshots on
#   TIMELINE_LIMIT_DAILY="7"         keep 7 dailies (HOURLY/WEEKLY/MONTHLY/YEARLY too)
#   NUMBER_LIMIT="50"                cap for number-cleanup (the pre/post pairs)
#   ALLOW_USERS="<user>"             let a non-root user manage this config
```

### Snapshots
```bash
sudo snapper -c root list                              # all snapshots in a config
sudo snapper -c root create -d "before X"              # a single (lone) snapshot
sudo snapper -c root create -t pre  -p                 # a PRE snapshot; -p prints its number
sudo snapper -c root create -t post --pre-number <N>   # the matching POST snapshot

# Wrap a command in an automatic pre/post pair (cleanest way to bracket a risky change)
sudo snapper -c root create -c number --command "pacman -Syu"

sudo snapper -c root delete <N>                        # delete one; <N1>-<N2> for a range
```

### Compare & undo (without rolling back the whole system)
```bash
sudo snapper -c root status  <N1>..<N2>     # which files changed between two snapshots
sudo snapper -c root diff    <N1>..<N2>     # the actual content diff
sudo snapper -c root diff    <N1>..0        # ...vs the current live state (0 = now)

# Surgically revert just the files that changed between N1 and N2 (NOT a full rollback)
sudo snapper -c root undochange <N1>..<N2>
```

### Rollback — read this before running it
```bash
# Boots the system onto a chosen snapshot as the new default subvolume. Layout-dependent.
sudo snapper -c root rollback <N>      # then reboot
```
> **Layout caveat.** `snapper rollback` expects the snapper/SUSE-style `@` + `.snapshots`
> subvolume layout. On a different layout it may not do what you expect. The **safe first move**
> is to *boot into a read-only snapshot to inspect* via **grub-btrfs** (below), confirm it's
> good, and only then roll back. Don't issue a blind `rollback` on an unfamiliar layout.

### Arch/CachyOS integration (the pieces that make it pleasant)
- **`snap-pac`** — auto pre/post snapshots around every `pacman` transaction. The single
  highest-value add: every update becomes individually revertable.
- **`grub-btrfs`** — adds a GRUB submenu to **boot into any snapshot** (read-only). Your escape
  hatch when an update won't boot. Regenerate its menu after snapshot changes (a path unit
  usually does this automatically; `grub-mkconfig -o /boot/grub/grub.cfg` by hand).
- **Timers** — `snapper-timeline.timer` (creates timeline snapshots) and
  `snapper-cleanup.timer` (applies the cleanup policy). Enable both:
  ```bash
  sudo systemctl enable --now snapper-timeline.timer snapper-cleanup.timer
  systemctl list-timers 'snapper-*'
  ```

---

## 8. Recovery (when it won't mount)

- [ ] **Read-only inventory first — never `--repair` blind:**
      ```bash
      sudo btrfs check /dev/sdX            # READ-ONLY; reports without touching anything
      ```
- [ ] **Try a read-only / recovery mount** to get data off before any repair:
      ```bash
      sudo mount -o ro,rescue=all /dev/sdX /mnt    # newest kernels; or rescue=usebackuproot
      ```
- [ ] **If a device is missing**, mount degraded to copy data out:
      ```bash
      sudo mount -o degraded,ro /dev/sdX /mnt
      ```
- [ ] **Salvage files** without mounting, when mount fails entirely:
      ```bash
      sudo btrfs restore -v /dev/sdX /mnt/recovered/
      ```
- [ ] **Only as a last resort, with a backup taken**, attempt repair — `--repair` can worsen
      damage and is explicitly a last resort per the man page:
      ```bash
      sudo btrfs check --repair /dev/sdX
      ```

---

## 9. Daily workflows

### Bracket a risky change so I can undo it
```bash
sudo snapper -c root create -c number --command "<the risky command>"
# inspect afterwards; revert just the touched files if needed:
sudo snapper -c root status <pre>..<post>
sudo snapper -c root undochange <pre>..<post>
```

### A bad update won't boot
```text
1. Reboot, pick the grub-btrfs submenu, boot a known-good read-only snapshot.
2. Confirm the system is sane from inside it.
3. snapper rollback <N> (layout permitting) -> reboot.   # see §7 layout caveat
```

### Monthly health check
```bash
sudo btrfs scrub start / && sleep 2 && sudo btrfs scrub status /   # checksum-verify everything
sudo btrfs device stats /                                          # any non-zero error counts?
sudo btrfs filesystem usage /                                      # unallocated headroom OK?
```

### "Disk full" but df disagrees
```bash
sudo btrfs filesystem usage /               # look at Unallocated + Data ratio, not df
sudo btrfs balance start -dusage=10 /       # reclaim near-empty data chunks first
```

---

## 10. Files & locations

| Path | Purpose |
| --- | --- |
| `/etc/snapper/configs/<name>` | per-config policy (timeline limits, number limits, users) |
| `/etc/conf.d/snapper` | which snapper configs are active (`SNAPPER_CONFIGS=`) |
| `/.snapshots/` (or `<subvol>/.snapshots`) | where snapper stores a config's snapshots |
| `/etc/fstab` | mount options & which subvolume is `/` (`subvol=@`) |
| `man btrfs-subvolume`, `man btrfs-check` | authoritative per-subcommand docs |

---

## Gotchas / Golden rules

1. **A snapshot is not a backup.** It's copy-on-write on the *same disk* — great against
   mistakes and bad updates, useless against drive failure. Send it off-device or back it up
   ([[borgmatic]]).
2. **`df` lies on btrfs.** Trust `btrfs filesystem usage`. "Full" with free space showing is
   usually unallocated-vs-allocated chunk skew — fix with a filtered `balance`.
3. **Never run a bare `btrfs balance` on a full disk.** Always use `-dusage=`/`-musage=` filters;
   an unfiltered balance rewrites everything and can wedge on a near-full FS.
4. **`btrfs check --repair` is a last resort.** Run read-only `check` first, get data off with a
   `ro`/`rescue` mount or `btrfs restore`, and only repair with a backup in hand.
5. **`btrfs send` needs a read-only snapshot** (`-r`); incrementals (`-p`) need a shared parent
   present on both ends.
6. **CoW fragments DB/VM files.** `chattr +C` on the empty file/dir, or `nodatacow` mount, before
   data lands.
7. **`snapper rollback` is layout-dependent.** Boot a read-only snapshot via grub-btrfs to
   *verify* first; don't blind-rollback on an unfamiliar subvolume layout.
8. **Subvolume snapshot/delete is a privileged ioctl.** In a hardened systemd unit that means
   `PrivateDevices=no` plus `CAP_SYS_ADMIN` (and `CAP_DAC_OVERRIDE` for create) — see
   [[systemd.exec]].

## Further reading
- [btrfs(8) wiki](https://btrfs.readthedocs.io/) ·
  [snapper manual](http://snapper.io/manual.html) ·
  [Arch Wiki: btrfs](https://wiki.archlinux.org/title/Btrfs) ·
  [Arch Wiki: snapper](https://wiki.archlinux.org/title/Snapper)
