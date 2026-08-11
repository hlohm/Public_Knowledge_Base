---
type: "term"
branch: "Hardware & Architecture"
aliases: ["Write Endurance", "TBW", "DWPD"]
tags: [hardware]
status: "developed"
---

# SSD Endurance

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** Write Endurance, TBW, DWPD

The rated amount of data an [[SSD]] can absorb before its flash cells are considered worn out, quoted as TBW (terabytes written over the drive's life) or DWPD (full drive writes per day over the warranty period). NVMe drives report consumption as *Percentage Used* in the S.M.A.R.T. health log.

**Context.** Crossing 100 % doesn't kill a drive on the spot — it means the vendor no longer vouches for it: failure odds climb, spare blocks run down, and the warranty is done. Write-heavy workloads (databases, logging, copy-on-write filesystems with sync-heavy guests) chew through consumer-class ratings far faster than desktop use, which is why enterprise drives quote DWPD in whole numbers while consumer drives quote fractions. [[Wear Leveling]] spreads the damage evenly but can't reduce the total; write amplification inside the controller means host writes understate flash writes. The practical habit: trend *Percentage Used* under [[Monitoring]], and treat a mirrored pair of identical drives as one wear clock — they age together.

## See also

- [[SSD]]
- [[Wear Leveling]]
- [[S.M.A.R.T.]]
- [[RAID]]

## Further reading

- [Wikipedia: Flash memory — Memory wear](https://en.wikipedia.org/wiki/Flash_memory#Memory_wear)
