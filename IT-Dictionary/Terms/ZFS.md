---
type: "term"
branch: "Operating Systems"
aliases: ["OpenZFS"]
tags: [os]
status: "developed"
---

# ZFS

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** OpenZFS

A combined filesystem and volume manager: drives are grouped into pools, and datasets draw from the pool instead of living in fixed partitions. Copy-on-write semantics, end-to-end checksums on every block, cheap snapshots, and built-in redundancy (mirrors, RAID-Z) come as one integrated design rather than stacked layers.

**Context.** The checksums *detect* bit rot on every read and scrub, but ZFS can only *repair* what redundancy allows — a single-disk or striped pool just tells you the data is gone. Which makes pool topology the load-bearing decision: hypervisor installers will happily create the root pool from whatever disks they see, and a "two disks, must be a mirror" assumption can quietly be a stripe ([[RAID]] 0). Snapshots are rollback points sharing the same disks, not backups; replacing a disk triggers [[Resilvering]]. ZFS also loves RAM (ARC cache) and, on copy-on-write, sync-heavy guest workloads amplify writes — a real factor for [[SSD Endurance]].

## See also

- [[File System]]
- [[RAID]]
- [[Resilvering]]
- [[Atomic Write]]
- [[SSD Endurance]]

## Further reading

- [Wikipedia: ZFS](https://en.wikipedia.org/wiki/ZFS)
- [OpenZFS documentation](https://openzfs.github.io/openzfs-docs/)
