---
type: "term"
branch: "Hardware & Architecture"
aliases: ["Redundant Array of Independent Disks"]
tags: [hardware]
status: "developed"
---

# RAID

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** Redundant Array of Independent Disks

Combining several physical drives into one logical volume for redundancy, performance, or both. The numbered levels describe the layout: RAID 0 stripes data across drives with **no** redundancy, RAID 1 mirrors, RAID 5/6 stripe with one/two drives' worth of parity, RAID 10 mirrors then stripes.

**Context.** RAID protects against *drive failure*, nothing else — deletion, ransomware, and filesystem corruption replicate to every member instantly, hence "RAID is not a backup." RAID 0 actually *raises* risk: lose any one drive, lose everything, so a two-disk stripe roughly doubles the failure probability of a single disk. Software RAID (mdadm, [[ZFS]] mirrors) has largely displaced hardware controllers outside enterprise gear. The operational gotcha: installers and hosting defaults sometimes create a striped pool where you assumed a mirror — verify the actual topology of a system you inherit rather than trusting the disk count.

## See also

- [[SSD]]
- [[HDD]]
- [[ZFS]]
- [[Resilvering]]
- [[Immutable Backup]]

## Further reading

- [Wikipedia: RAID](https://en.wikipedia.org/wiki/RAID)
