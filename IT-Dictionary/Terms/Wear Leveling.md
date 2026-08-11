---
type: "term"
branch: "Hardware & Architecture"
aliases: ["Wear Levelling"]
tags: [hardware]
status: "developed"
---

# Wear Leveling

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** Wear Levelling

The [[SSD]] controller technique of spreading writes across all flash blocks so no block exhausts its limited program/erase cycles early — remapping logical addresses to whichever physical block is least worn.

**Context.** Wear leveling is why an SSD's lifetime is quoted for the whole drive ([[SSD Endurance]]) rather than per sector, and why "overwriting" a file on flash doesn't necessarily destroy the old copy — the controller may have written the new data elsewhere, which changes how secure deletion works compared to an HDD. *Dynamic* leveling only rotates among free blocks; *static* leveling also migrates cold data out of pristine blocks so they join the rotation. TRIM supports the whole scheme by telling the controller which blocks are genuinely free.

## See also

- [[SSD]]
- [[SSD Endurance]]
- [[S.M.A.R.T.]]

## Further reading

- [Wikipedia: Wear leveling](https://en.wikipedia.org/wiki/Wear_leveling)
