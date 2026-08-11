---
type: "term"
branch: "Operating Systems"
aliases: ["RAID Rebuild", "Rebuild"]
tags: [os]
status: "developed"
---

# Resilvering

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** RAID Rebuild, Rebuild

Rebuilding redundancy onto a new or replaced disk by copying (mirror) or reconstructing from parity (RAID 5/6, RAID-Z) the data of the surviving members. "Resilver" is the [[ZFS]] word — with the twist that ZFS only copies *live* data, so a half-full pool rebuilds twice as fast as a dumb block-level [[RAID]] rebuild.

**Context.** The rebuild window is the most dangerous time in an array's life: redundancy is already spent, and the operation hammers the surviving drives with sustained reads — drives that are typically the same age and batch as the one that just failed. That math is why RAID 6 exists, why hot spares shorten the exposure, and why replacing *both* halves of a worn mirror is done one disk at a time, waiting for each resilver to finish. Scrub first if you can: a latent read error discovered mid-rebuild is data loss.

## See also

- [[RAID]]
- [[ZFS]]
- [[SSD Endurance]]

## Further reading

- [Wikipedia: RAID — Rebuilding](https://en.wikipedia.org/wiki/RAID)
