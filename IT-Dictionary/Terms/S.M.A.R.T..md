---
type: "term"
branch: "Hardware & Architecture"
aliases: ["SMART", "Self-Monitoring, Analysis and Reporting Technology"]
tags: [hardware]
status: "developed"
---
ppppppSS
# S.M.A.R.T.

> **Branch:** [[02 - Hardware & Architecture|Hardware & Architecture]]
> **Also known as:** SMART, Self-Monitoring, Analysis and Reporting Technology

A drive's built-in self-monitoring: counters, thresholds, and self-tests (reallocated sectors, media errors, temperature, wear) that the disk exposes so the host can spot impending failure before it happens. NVMe drives report the same idea through a health log; `smartctl` reads both.

**Context.** S.M.A.R.T. only helps if something *reads* it — `smartd` can watch drives and mail warnings, but an unmonitored delivery path silently eats them, and the classic failure mode is discovering months-old wear warnings stuck in a local mail queue. Attribute semantics are vendor-defined, so trends matter more than absolute values; the unambiguous ones are reallocated/pending sectors on HDDs and media errors plus *Percentage Used* on NVMe, where ≥100 % means the drive is past its rated [[SSD Endurance]].

## See also

- [[SSD]]
- [[HDD]]
- [[SSD Endurance]]
- [[Monitoring]]
- [[Dead Man's Switch]]

## Further reading

- [Wikipedia: Self-Monitoring, Analysis and Reporting Technology](https://en.wikipedia.org/wiki/Self-Monitoring,_Analysis_and_Reporting_Technology)
