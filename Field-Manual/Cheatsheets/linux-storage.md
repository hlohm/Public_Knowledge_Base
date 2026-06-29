---
type: cheatsheet
area: "Linux Administration"
aliases: [lsblk, mount, lvm, df, du, fdisk]
tags: [linux, storage, lvm, filesystem, mount, disk]
status: working
---

# Storage

> **Area:** [[Linux Administration]]

Disk inspection, mounting, filesystems, LVM, and disk health. See [[btrfs]] for the Btrfs-specific sheet.

---

## 1. Inspect disks and partitions

```bash
lsblk                          # block device tree: disks, partitions, mount points
lsblk -f                       # + filesystem type and UUID
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT,UUID   # custom columns
lsblk --json | jq .            # JSON output for scripting

fdisk -l /dev/sda              # partition table (MBR and GPT)
parted /dev/sda print          # partition table with sizes
gdisk -l /dev/sda              # GPT-focused (gdisk)

blkid                          # all block devices with UUID and filesystem type
blkid /dev/sda1                # one device
```

## 2. Disk usage

```bash
df -h                          # filesystem disk usage (human-readable)
df -h /home                    # specific filesystem
df -i                          # inode usage (a full inode table = "disk full" even with free space)
df -Th                         # + filesystem type

du -sh /var/log/               # total size of a directory
du -sh /var/log/*/             # subtotal per subdirectory
du -sh /* 2>/dev/null          # top-level usage from root
du -h --max-depth=1 /var/      # one level deep

# Find the largest files / directories
du -ah /var | sort -rh | head -20
find / -xdev -type f -size +500M -printf '%s\t%p\n' | sort -rn | head -20
```

## 3. Filesystems: create and check

```bash
# Create (format)
mkfs.ext4 /dev/sdb1
mkfs.xfs  /dev/sdb1
mkfs.vfat /dev/sdb1            # FAT32 (USB drives, EFI partition)

# Check and repair (must be unmounted)
fsck /dev/sdb1                 # auto-detect type
fsck.ext4 -f /dev/sdb1        # force check
e2fsck -f /dev/sdb1           # ext4 check with prompt
xfs_repair /dev/sdb1          # XFS repair
```

## 4. Mount and unmount

```bash
mount /dev/sdb1 /mnt/data      # mount by device
mount UUID=<uuid> /mnt/data    # mount by UUID (preferred in fstab)
mount -t ext4 /dev/sdb1 /mnt/data  # explicit type
mount -o ro /dev/sdb1 /mnt/    # read-only
mount -o remount,rw /mnt/      # remount read-write

umount /mnt/data
umount /dev/sdb1
umount -l /mnt/data            # lazy: detach even if busy (safe when processes have open files)

# What is mounted where?
mount | column -t
findmnt                        # tree view of mounts
findmnt /mnt/data              # info about a specific mount point
```

### /etc/fstab

```
# <device>   <mountpoint>  <type>  <options>         <dump>  <pass>
UUID=<uuid>  /home         ext4    defaults,noatime  0       2
UUID=<uuid>  /var          xfs     defaults           0       2
//server/share /mnt/smb   cifs    credentials=/etc/samba/creds,uid=1000  0  0
tmpfs        /tmp          tmpfs   defaults,size=2G,mode=1777  0  0

# options of note:
# noatime — don't update access time on reads (significant I/O reduction on SSDs)
# noexec  — prevent execution of binaries (security: /tmp, /var)
# nosuid  — ignore setuid bits
# nofail  — don't fail boot if device is absent (external drives, NAS)
```

```bash
mount -a                       # mount everything in fstab not yet mounted (test fstab changes)
systemctl daemon-reload        # if systemd mount units are involved
```

## 5. LVM (Logical Volume Manager)

```bash
# Physical Volume management
pvcreate /dev/sdb /dev/sdc     # initialise disks as PVs
pvdisplay                      # show PVs and free space
pvremove /dev/sdc              # remove PV

# Volume Group management
vgcreate vg_data /dev/sdb /dev/sdc   # create VG from PVs
vgdisplay vg_data                     # show VG info
vgextend vg_data /dev/sdd            # add a PV to existing VG
vgremove vg_data

# Logical Volume management
lvcreate -n lv_data -L 100G vg_data   # create 100 GB LV
lvcreate -n lv_data -l 100%FREE vg_data  # use all available space
lvdisplay                              # show LVs
lvs                                    # concise LV list

# Extend a LV and filesystem (online for ext4/xfs)
lvextend -L +50G /dev/vg_data/lv_data    # extend LV by 50 GB
lvextend -l +100%FREE /dev/vg_data/lv_data  # extend to use all VG free space
resize2fs /dev/vg_data/lv_data           # resize ext4 filesystem (after lvextend)
xfs_growfs /mnt/data                     # resize XFS filesystem (while mounted)

# Snapshot (for backup / testing)
lvcreate -L 10G -s -n snap_data /dev/vg_data/lv_data
mount -o ro /dev/vg_data/snap_data /mnt/snap   # mount read-only for backup
lvremove /dev/vg_data/snap_data               # remove when done
```

## 6. Disk health (SMART)

```bash
smartctl -i /dev/sda           # device info
smartctl -H /dev/sda           # health summary (PASSED/FAILED)
smartctl -a /dev/sda           # full SMART attributes
smartctl -t short /dev/sda     # start a short self-test
smartctl -t long  /dev/sda     # start a long self-test
smartctl -l selftest /dev/sda  # view test results

# Attributes to watch:
# 5   = Reallocated Sectors Count  (>0 = dying drive)
# 187 = Uncorrectable Error Count  (>0 = serious)
# 197 = Current Pending Sectors    (>0 = potentially dying)
# 198 = Offline Uncorrectable      (>0 = serious)
```

---

## Daily workflows

### "Identify why a disk is full"
```bash
df -h               # which filesystem?
du -sh /var/log/*/  # biggest directories
find /var -xdev -type f -size +100M -printf '%s\t%p\n' | sort -rn | head
```

### "Add a new disk and mount it"
```bash
lsblk                          # confirm device name, e.g. /dev/sdb
mkfs.ext4 /dev/sdb
mkdir /mnt/data
blkid /dev/sdb                 # get UUID
echo "UUID=<uuid> /mnt/data ext4 defaults,noatime 0 2" >> /etc/fstab
mount -a
```

### "Extend a logical volume online"
```bash
lvextend -l +100%FREE /dev/vg_data/lv_data
resize2fs /dev/vg_data/lv_data    # ext4
# or: xfs_growfs /mountpoint       # xfs
```

## Gotchas / Golden rules

1. **Inode exhaustion looks like "disk full" but `df -h` shows free space** — check `df -i`; millions of small files (mail spools, package caches, node_modules) exhaust inodes before disk space.
2. **XFS cannot be shrunk** — only grown; plan LV sizing for XFS volumes; ext4 can shrink with `e2fsck` + `resize2fs` (offline only).
3. **Never `fsck` a mounted filesystem** — it will corrupt the filesystem; always unmount first or use single-user mode / rescue environment.
4. **LVM snapshots are not backup** — they are point-in-time copies on the same physical storage; a disk failure destroys both the origin and the snapshot.
5. **`noatime` mount option is almost always the right choice** — `relatime` is the default (update atime only if mtime is newer); `noatime` is better for I/O-intensive workloads and SSDs.
