---
type: runbook
area: "Backup & Recovery"
tags: [backup, restore, bare-metal, linux, recovery]
status: working
---

# Bare-Metal Restore

> **Area:** [[Backup & Recovery]]

Rebuild a Linux host from nothing after a disk failure, hardware replacement, or deliberate decommission. This runbook covers the full sequence from bootable media to a restored, operational host.

> **Before you need this:** run the [[Backup Restore Drill]] regularly. The first time you restore from backup should not be during an incident.

---

## Pre-conditions

Before starting, confirm you have:

- [ ] Bootable rescue media (live USB: SystemRescue, Ubuntu live, Arch ISO)
- [ ] Backup destination reachable (SFTP server, S3, NAS, external drive)
- [ ] Backup tool credentials (restic passphrase, borgmatic key, SSH key for backup host)
- [ ] List of what was backed up (which paths, last successful backup timestamp)
- [ ] Network access from the rescue environment

---

## Step 1 — Boot the rescue environment

```bash
# Boot from live USB / PXE
# Connect to network:
ip link set eth0 up
dhclient eth0              # or configure manually with ip addr add

# Confirm connectivity
ping -c 3 8.8.8.8
ssh user@backup-host "ls /backups/"    # confirm backup is reachable
```

---

## Step 2 — Prepare the new disk

```bash
lsblk                      # identify the target disk (/dev/sda, /dev/nvme0n1, …)

# Partition (UEFI system: GPT + EFI partition)
fdisk /dev/sda             # or: gdisk, parted

# Typical partition layout:
# /dev/sda1  512M   EFI System Partition (vfat, type EF00)
# /dev/sda2  100%   Linux (ext4 / XFS / Btrfs, or LUKS + LVM)

# Format
mkfs.vfat -F32 /dev/sda1          # EFI
mkfs.ext4 /dev/sda2               # root
# Or: mkfs.xfs, mkfs.btrfs

# LUKS (if the original system used full-disk encryption)
cryptsetup luksFormat /dev/sda2 --cipher aes-xts-plain64 --key-size 512 --hash sha256
cryptsetup open /dev/sda2 cryptroot
mkfs.ext4 /dev/mapper/cryptroot
```

---

## Step 3 — Mount and prepare the restore target

```bash
mount /dev/sda2 /mnt              # or /dev/mapper/cryptroot for LUKS
mount --mkdir /dev/sda1 /mnt/boot/efi

# If restoring into LVM:
pvcreate /dev/sda2
vgcreate vg0 /dev/sda2
lvcreate -L 50G -n lv_root vg0
mkfs.ext4 /dev/vg0/lv_root
mount /dev/vg0/lv_root /mnt
```

---

## Step 4 — Restore from backup

### restic

```bash
# Install restic in the rescue environment
apt install -y restic   # or: download the binary

export RESTIC_REPOSITORY="sftp:user@backup-host:/backups/hostname"
export RESTIC_PASSWORD='<passphrase>'

restic snapshots                          # list available snapshots
restic restore latest --target /mnt/      # restore to the new root
# Or: restore a specific snapshot:
restic restore <snapshot-id> --target /mnt/
```

### borgmatic / borg

```bash
apt install -y borgbackup
export BORG_REPO="ssh://user@backup-host/backups/hostname"
export BORG_PASSPHRASE='<passphrase>'

borg list                                 # list archives
borg extract ::latest --exclude='*.socket' --exclude='*.pid'
# Borg extracts relative to the current directory; cd /mnt first:
cd /mnt
borg extract "$BORG_REPO"::latest
```

### rsync hard-link snapshots

```bash
rsync -aAX backup-host:/backups/snapshots/latest/ /mnt/
# -A: preserve ACLs; -X: preserve extended attributes
```

---

## Step 5 — Restore non-backed-up system directories

The following are usually excluded from backups but must be present:

```bash
# Create required virtual filesystem mount points
mkdir -p /mnt/{dev,proc,sys,run,tmp}

# Recreate /tmp permissions
chmod 1777 /mnt/tmp
```

---

## Step 6 — Chroot and reinstall bootloader

```bash
# Bind-mount virtual filesystems for chroot
mount --rbind /dev  /mnt/dev
mount --rbind /proc /mnt/proc
mount --rbind /sys  /mnt/sys
mount --bind  /run  /mnt/run

# Enter the restored system
chroot /mnt /bin/bash
# Or: arch-chroot /mnt   (if using Arch rescue ISO)

# Confirm the OS is intact
cat /etc/os-release
ls /home/

# Reinstall GRUB (UEFI)
apt install -y --reinstall grub-efi-amd64   # Debian/Ubuntu
grub-install --target=x86_64-efi --efi-directory=/boot/efi --recheck /dev/sda
update-grub

# RHEL/Rocky:
dnf reinstall -y grub2-efi-x64 grub2-efi-x64-modules shim-x64
grub2-install --target=x86_64-efi --efi-directory=/boot/efi
grub2-mkconfig -o /boot/grub2/grub.cfg

# Update initramfs (if kernel or drivers changed)
update-initramfs -u -k all    # Debian/Ubuntu
dracut --force                # RHEL/Fedora
mkinitcpio -P                 # Arch
```

---

## Step 7 — Verify fstab and LUKS configuration

```bash
# Inside the chroot:
cat /etc/fstab

# If UUIDs have changed (new disk):
blkid /dev/sda2                    # get new UUID
# Update /etc/fstab with new UUID
# Update /boot/grub/grub.cfg if it contains UUID references

# LUKS: update /etc/crypttab with the new device UUID
blkid /dev/sda2 | grep UUID
# Edit /etc/crypttab:
# cryptroot UUID=<new-uuid> none luks

# Regenerate initramfs after fstab/crypttab changes
update-initramfs -u -k all
```

---

## Step 8 — Exit, unmount, and reboot

```bash
# Exit chroot
exit

# Unmount everything (in reverse order)
umount -R /mnt/dev
umount -R /mnt/sys
umount -R /mnt/proc
umount /mnt/boot/efi
umount /mnt

# Reboot
reboot
```

---

## Post-restore checklist

- [ ] System boots without errors
- [ ] All services start: `systemctl --failed`
- [ ] Network configured correctly: `ip addr`, `ip route`
- [ ] SSH accessible with correct keys: `~/.ssh/authorized_keys` intact
- [ ] No unexpected cronjobs or services compared to pre-incident
- [ ] Backup agent running and performing scheduled backups: test with a new snapshot
- [ ] Monitoring agent re-enrolled (if host is managed)

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| GRUB not found at boot | EFI boot entry missing | Boot from live USB, chroot, run `efibootmgr -c` to create entry |
| initramfs panic: cannot find root | UUID in fstab doesn't match new disk | Update fstab and crypttab UUIDs, regenerate initramfs |
| LUKS prompt doesn't appear | crypttab not updated | Update UUID in /etc/crypttab, regenerate initramfs |
| SSH host key mismatch | New disk = new keys generated | Update known_hosts on clients; or restore /etc/ssh/ from backup |

## See also

- [[Backup Restore Drill]] — rehearsed, lightweight restore test to run before you need this
- [[restic]] · [[borgmatic]] · [[rsync-snapshots]] — backup tools
- [[linux-storage]] — disk, LVM, LUKS
