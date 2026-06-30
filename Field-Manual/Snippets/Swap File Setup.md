---
type: snippet
area: "Linux Administration"
tags: [linux, swap, memory, storage, fstab, sysctl]
status: stable
---

# Swap File Setup

> **Area:** [[Linux Administration]]

Add a swap file to a running Linux system — no repartitioning required. One-time setup; persists across reboots.

**When you need this:** The system has no swap at all (common on cloud VMs), swap ran out during a memory spike, or you are following the [[Out of Memory]] playbook and need to add swap headroom without rebooting.

---

```bash
# 1. Allocate a contiguous 2 GB file (adjust size to taste)
sudo fallocate -l 2G /swapfile
# fallocate is instant — it reserves disk blocks without writing zeros.
# Use dd if fallocate fails (e.g., on Btrfs, ZFS, or some network filesystems):
# sudo dd if=/dev/zero of=/swapfile bs=1M count=2048 status=progress

# 2. Restrict permissions — readable only by root
#    swapon will refuse to use a file that is world-readable
sudo chmod 600 /swapfile

# 3. Format as swap
sudo mkswap /swapfile

# 4. Activate immediately (takes effect without reboot)
sudo swapon /swapfile

# 5. Persist across reboots
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 6. Set swappiness (10 = use RAM first; only swap under real pressure)
#    Default is 60, which is aggressive for a desktop or lightly-loaded server
echo 'vm.swappiness=10' | sudo tee /etc/sysctl.d/99-swappiness.conf
sudo sysctl -p /etc/sysctl.d/99-swappiness.conf   # apply without reboot
```

---

## Verify

```bash
swapon --show                   # should list /swapfile, size, and usage
free -h                         # confirm Swap row is non-zero
cat /proc/sys/vm/swappiness     # should read 10
grep swapfile /etc/fstab        # confirm fstab entry is present
```

## Adjust or remove

```bash
# Resize: deactivate, remove, recreate at new size
sudo swapoff /swapfile
sudo rm /swapfile
# ... repeat setup with new size ...

# Remove swap entirely
sudo swapoff /swapfile
sudo rm /swapfile
sudo sed -i '/swapfile/d' /etc/fstab
```

## Gotchas

- **Btrfs**: `fallocate` creates a sparse file on Btrfs, which `mkswap` rejects. Use `dd` instead, or place the swap file on a non-Btrfs filesystem.
- **Already-full disk**: you cannot `fallocate` if the filesystem has less than 2 G free — check with `df -h /` first.
- **Cloud VMs with ephemeral storage**: if `/swapfile` is on an ephemeral disk, it disappears on stop/start. Either use persistent storage or accept that and skip the fstab entry.
- **swappiness is not a percentage**: `vm.swappiness=10` does not mean "swap when 90% of RAM is used" — it adjusts a kernel weight. Values of 1–10 are sensible for servers; 0 means "never swap unless absolutely forced" (can trigger OOM kills instead).

## See also

- [[Out of Memory]] — what to do when the system is already in trouble
- [[linux-storage]] — disk, fstab, LVM reference
