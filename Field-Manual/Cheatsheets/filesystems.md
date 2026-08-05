---
type: cheatsheet
area: "Linux Administration"
aliases: [fs, ext4, xfs, zfs, exfat, ntfs, tmpfs, overlayfs, nfs]
tags: [linux, storage, filesystem, zfs, nfs, decision]
status: working
---

# Filesystems

> **Area:** [[Linux Administration]]

The filesystem landscape as a **decision reference**: what each commonly-found filesystem
is good at, where it belongs, where it doesn't, and the axes that actually matter when
choosing or auditing one. Commands for day-to-day storage work live in [[linux-storage]];
Btrfs operations in [[btrfs]]. This sheet is about *which*, not *how*.

---

## 1. The axes that actually differentiate filesystems

Most "X vs Y" debates collapse into a handful of design axes. Know these and every
filesystem below slots into place:

- **Crash consistency model** — *journaling* (ext4, XFS, NTFS: replay a log of metadata
  changes after a crash) vs *copy-on-write* (Btrfs, ZFS, APFS: never overwrite live data,
  so the on-disk state is always consistent) vs *nothing* (FAT/exFAT: run `fsck` and hope).
- **Data integrity** — CoW filesystems checksum **data and metadata** and can detect (and
  with redundancy, self-heal) silent corruption. Journaling filesystems protect metadata
  consistency only — a bit-flipped file reads back wrong with no error.
- **Snapshots & clones** — CoW makes them nearly free (Btrfs, ZFS, APFS). On ext4/XFS you
  need LVM underneath to fake it, at a performance cost.
- **Volume management** — ZFS and Btrfs absorb the RAID/LVM layer (pools, multi-device,
  rebalance). ext4/XFS are "one device, one filesystem" and rely on mdraid/LVM below.
- **Resize story** — grow online is near-universal; **shrink** is the differentiator
  (ext4: offline yes; XFS: never; Btrfs: online yes; ZFS: effectively no).
- **Scaling shape** — some optimize for huge files and parallel streaming (XFS), some for
  many small files and general use (ext4), some for raw flash (F2FS).
- **Repair story** — ext4's `fsck` is battle-hardened; XFS repair is solid; Btrfs repair is
  the sharp knife (see [[btrfs]] gotchas); ZFS has *no* fsck — scrub + redundancy *is* the
  repair model.
- **Maturity & support surface** — who ships it as default, how long it's been boring, and
  whether it's in-tree (ZFS never will be — CDDL vs GPL).

---

## 2. Linux-native disk filesystems

### ext4 — the boring default
- Journaling, in-tree since 2008, the most battle-tested repair tooling on Linux.
- Good all-round performance, especially small files and metadata-heavy work.
- Limits: 16 TiB max file; volumes beyond 16 TiB need the (now default) `64bit` feature.
- **Inode count is fixed at `mkfs` time** — a filesystem for millions of tiny files needs
  `-i`/`-N` planned up front, or you hit "disk full" with space free (`df -i`).
- Shrink: offline only. Grow: online.
- **Use for:** root filesystems, general servers, VMs, anywhere you want zero surprises.
- **Avoid when:** you want snapshots/checksums/compression without extra layers.

### XFS — the big-file workhorse
- Journaling; from SGI (1994 heritage), default in RHEL. Excellent parallel I/O and
  large-file/streaming performance; allocation groups scale across CPUs.
- Reflinks (`cp --reflink`) give CoW file clones without a CoW filesystem.
- **Cannot shrink. Ever.** Size partitions accordingly.
- fsck-equivalent (`xfs_repair`) is good, but historically less forgiving of exotic damage
  than e2fsck.
- **Use for:** large filesystems, media/scientific data, databases on LVM, RHEL-land.
- **Avoid when:** you'll ever need to shrink, or want built-in snapshots.

### Btrfs — CoW, in-tree
- CoW, checksums on data+metadata, subvolumes, snapshots, transparent compression (zstd),
  send/receive, multi-device with built-in RAID 0/1/10. Default in Fedora and openSUSE.
- **RAID 5/6 remains not trusted for production** (write hole); use RAID 1/10 profiles.
- `df` lies on Btrfs; repair tooling is the sharp edge — full treatment in [[btrfs]].
- **Use for:** root filesystems where snapshots/rollback matter (snapper), homelab NAS on
  mirror profiles, backup targets (send/receive).
- **Avoid when:** heavy random-rewrite workloads (VM images, databases) without planning
  (`nodatacow` trades away the integrity features), or parity RAID is required.

### ZFS — the storage appliance in software
- Pooled storage: filesystem + volume manager + RAID (RAID-Z1/2/3, mirrors) in one.
  Checksums with **self-healing** (repairs from redundancy on read/scrub), snapshots,
  clones, send/recv, transparent compression (lz4/zstd — just leave it on), optional
  encryption, dedup (RAM-hungry; almost never worth it).
- ARC cache wants RAM: ~1 GiB baseline + more for big pools; budget for it. ECC is
  *recommended like for any server*, not a hard requirement — the "ZFS without ECC eats
  data" meme is folklore.
- **CDDL-licensed → permanently out-of-tree** (OpenZFS via DKMS/packages); kernel updates can lag.
  First-class on FreeBSD/TrueNAS, well-supported on Ubuntu.
- Rigid shapes: vdevs are forever-ish (RAID-Z expansion only landed in OpenZFS 2.3, one
  disk at a time; no shrink, limited device removal). **Plan the pool layout up front.**
- **Use for:** NAS/file servers, backup targets, anywhere data integrity is the point,
  VM/jail hosts on FreeBSD/Proxmox.
- **Avoid when:** RAM-starved machines, root-on-Linux without distro support, or you need
  to grow/shrink flexibly one disk at a time.

### F2FS — for raw flash
- Log-structured, designed around NAND behavior (eMMC, SD, cheap SSDs without fancy FTLs).
  Default on many Android devices.
- **Use for:** SBCs, phones, SD-card roots (Raspberry Pi-class).
- **Avoid when:** ordinary SATA/NVMe SSDs — ext4/XFS/Btrfs are fine there; TRIM matters
  more than FS choice.

### Honorable mentions
- **ext2/ext3** — legacy; ext2 (no journal) occasionally still used for `/boot` or flash.
- **bcachefs** — CoW newcomer with tiering/caching ambitions; merged in 6.7, removed
  again in 6.18 after maintainer conflict (now an out-of-tree DKMS module).
  Experimental — watch, don't deploy.
- **ReiserFS** — removed from the kernel (6.13). Historical.

---

## 3. Interchange & foreign filesystems

| FS | Journal | Max file | Native OS | Linux support | Use it for |
| --- | --- | --- | --- | --- | --- |
| **FAT32** | ❌ | **4 GiB − 1** | everything | full | EFI system partition, ancient devices |
| **exFAT** | ❌ | effectively unlimited | Win/macOS | in-kernel since 5.4 | USB sticks, SD cards, cross-OS drives |
| **NTFS** | ✔ (metadata) | 16 EiB | Windows | `ntfs3` in-kernel (5.15+), else ntfs-3g/FUSE | Windows disks you must read/write |
| **ReFS** | CoW | huge | Win Server / Dev Drive | none | Windows-side integrity volumes |
| **APFS** | CoW | huge | macOS | read-only-ish, 3rd-party | Mac disks (read from Linux at best) |
| **HFS+** | ✔ | 8 EiB | old macOS | rw (fragile) | legacy Mac media |
| **ISO 9660 / UDF** | ❌ | — | everything | full | optical media, ISO images |

- **The 4 GiB FAT32 file limit** is the #1 "why won't this copy" ticket. exFAT is the
  fix for removable media; it's also the only FS all three desktop OSes write natively.
- exFAT/FAT have **no journal and no permissions** — fine for transfer, wrong for
  anything that stays plugged in and matters.
- The EFI System Partition **must** be FAT (spec requirement) — don't get clever.

---

## 4. Network filesystems

- **NFS** — the Unix native. v4.x: single port 2049, ACLs, Kerberos (`sec=krb5*`), pNFS.
  Unix uid/gid semantics — id-mapping across hosts is the eternal footgun. Mount options
  that matter: `hard` vs `soft` (default `hard`; `soft` can corrupt on timeout),
  `vers=4.2`, `noatime`. Use for Linux↔Linux shares, VM/container host storage.
- **SMB/CIFS** — the Windows native, served from Linux by Samba. Better auth story for
  mixed fleets (AD), worse Unix-permission fidelity. Use when Windows or macOS clients
  are in the picture.
- **SSHFS** — FUSE over sftp. Zero server setup, mediocre performance, per-user. Ad-hoc
  mounts only — see [[scp-sftp]].
- **virtiofs / 9p** — host↔guest sharing for VMs; virtiofs is the modern, fast one.
- Rule of thumb: **network filesystems are a consistency trade** — locking, caching, and
  atomicity are all weaker than local. Don't put SQLite/mail spools/DB files on NFS or
  SMB unless the application explicitly supports it.

### Distributed / clustered (know they exist)
- **CephFS / RBD** — scale-out replicated storage; the serious answer for multi-node
  (Proxmox clusters, Kubernetes). Wants 3+ nodes and real NICs; overkill below that.
- **GlusterFS** — simpler scale-out; in maintenance decline, avoid for new builds.
- **Lustre / BeeGFS** — HPC parallel filesystems; niche.

---

## 5. Special-purpose & pseudo filesystems

- **tmpfs** — RAM-backed, swappable, size-capped (`size=`). `/tmp` on many distros,
  `/run`, build scratch. Contents vanish on reboot — that's the feature.
- **ramfs** — tmpfs without swap or size cap; can OOM the box. Rarely what you want.
- **overlayfs** — union mount: RO lower layer(s) + RW upper. The engine of container
  images ([[docker]]) and live-USB persistence.
- **squashfs** — compressed, read-only image FS: live ISOs, snaps, appliance firmware.
  Pair with overlayfs for "immutable base + writable top".
- **procfs / sysfs / devtmpfs / cgroup2** — kernel interfaces wearing a filesystem
  costume; nothing on disk.
- **FUSE** — filesystems in userspace: sshfs, rclone mounts, ntfs-3g. Flexible, slower,
  and root-squashed by default (`allow_other` to share).

---

## 6. Feature matrix — the local big four

| | ext4 | XFS | Btrfs | ZFS |
| --- | --- | --- | --- | --- |
| Model | journal | journal | CoW | CoW |
| Data checksums | ❌ | ❌ | ✔ | ✔ (self-healing) |
| Snapshots | via LVM | via LVM | ✔ native | ✔ native |
| Compression | ❌ | ❌ | ✔ zstd | ✔ lz4/zstd |
| Multi-device / RAID | mdraid/LVM | mdraid/LVM | built-in (1/10 ✔, 5/6 ⚠) | built-in (mirror/RAID-Z) |
| Send/receive replication | ❌ | ❌ | ✔ | ✔ |
| Reflink clones | ❌ | ✔ | ✔ | file-clone (2.2+) |
| Shrink | offline | **never** | online | effectively no |
| In-tree | ✔ | ✔ | ✔ | ❌ (CDDL) |
| Repair story | excellent | good | ⚠ careful | scrub, no fsck |
| RAM appetite | tiny | tiny | small | ARC — feed it |
| Ships as default in | Debian/Ubuntu | RHEL | Fedora/openSUSE | FreeBSD/TrueNAS |

---

## 7. Decision guide — scenario → pick

| Scenario | Pick | Why |
| --- | --- | --- |
| Server / VM root, no surprises | **ext4** | maturity, repair tooling, zero tuning |
| Desktop/laptop root with rollback | **Btrfs** + snapper | free snapshots, boot-into-yesterday |
| Big single-purpose data volume | **XFS** (on LVM) | streaming performance at scale |
| NAS / backup target, integrity-first | **ZFS** (or Btrfs mirror) | checksums + self-heal + send/recv |
| Proxmox / VM host storage | **ZFS** | zvols, snapshots, replication |
| Database volume | **XFS** or **ext4** | CoW fragments under random rewrite |
| VM images / DBs *on* Btrfs anyway | subvolume with `nodatacow` | accepts the integrity trade |
| SD card / eMMC root (SBC) | **F2FS** (or ext4) | flash-aware allocation |
| USB stick shared with Windows/macOS | **exFAT** | the only universal writable FS |
| EFI system partition | **FAT32** | spec says so |
| Linux↔Linux share | **NFSv4** | native semantics |
| Mixed Windows/macOS share | **SMB** (Samba) | client support + AD auth |
| Container image layers | **overlayfs** | that's what it's for |
| Scratch that must die on reboot | **tmpfs** | RAM speed, auto-clean |
| 3+ node cluster storage | **Ceph** | replicated scale-out |

---

## 8. Evaluating an existing choice — audit questions

1. **What happens on a torn write / power loss?** Journal, CoW, or prayer? Does the answer
   match how much the data matters?
2. **Would silent corruption be detected?** No checksums → the backup dutifully backs up
   the corrupted file. Pair checksum-less filesystems with application-level verification
   ([[borgmatic]] `check`).
3. **Does the workload fight the design?** Random-rewrite on CoW (fragmentation), millions
   of files on default-inode ext4, tiny-file churn on XFS, database on NFS.
4. **Is the resize direction you'll need actually possible?** (XFS/ZFS shrink: no.)
5. **Snapshots: taken, and restore actually drilled?** A snapshot nobody has rolled back
   is a hope, not a capability — see [[Backup Restore Drill]].
6. **Who un-breaks it at 3am?** ext4 fsck is a well-trodden path; Btrfs/ZFS recovery
   assumes operator skill. Choose what the team can actually operate.
7. **Mount options sane?** `noatime` almost always; discard/TRIM via `fstrim.timer` rather
   than `discard` mount option; `hard` on NFS.

---

## Gotchas / Golden rules

1. **A snapshot is not a backup.** Same disk, same pool, same failure domain. Replicate
   (send/receive) or back up ([[borgmatic]]) to different hardware.
2. **RAID (any flavor) is availability, not backup.** It replicates your `rm -rf` at disk
   speed.
3. **FAT32's 4 GiB file limit** strikes exactly when someone copies a video/ISO to a
   stick. Reformat exFAT.
4. **XFS cannot shrink; ZFS pools effectively can't either.** Decide sizes like they're
   permanent — because they are.
5. **Btrfs RAID 5/6: still no.** Mirror profiles or ZFS RAID-Z instead.
6. **`df` lies on CoW filesystems.** Use `btrfs filesystem usage` / `zpool list` — see
   [[btrfs]].
7. **CoW + random-rewrite workloads fragment badly.** VM images and databases on
   Btrfs/ZFS need `nodatacow` / tuned `recordsize` (and you lose or weaken checksumming
   where you disable CoW).
8. **ZFS is out-of-tree.** A kernel upgrade without a matching module = pool won't import.
   Pin kernels or use a distro that ships it (Ubuntu, Proxmox).
9. **Don't put databases or mail spools on NFS/SMB** unless the app documents support —
   locking and cache-coherency semantics differ from local disk.
10. **Scrub on a schedule.** Checksums only help if something reads the data: monthly
    `zpool scrub` / `btrfs scrub` via a [[systemd]] timer.
11. **exFAT/FAT have no permissions and no journal** — transfer media, not storage.
12. **The ESP is FAT32.** Never "upgrade" it.
