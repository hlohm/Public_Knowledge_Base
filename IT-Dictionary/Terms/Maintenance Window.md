---
type: "term"
branch: "DevOps & SRE"
aliases: ["Quiet Hours", "Planned Maintenance"]
tags: [devops]
status: "developed"
---

# Maintenance Window

> **Branch:** [[12 - DevOps & SRE|DevOps & SRE]]
> **Also known as:** Quiet Hours, Planned Maintenance

A pre-announced period during which a system may be degraded or down for planned work — and during which [[Monitoring]] is expected to hold its fire, so scheduled downtime doesn't page anyone or burn alert credibility.

**Context.** The craft is in the silencing mechanics, because the failure modes point in opposite directions: silence too little and you train yourself to ignore alerts (fatigue), silence too much or forget to unsilence and you're blind when real trouble follows the maintenance. Tools offer two shapes — *scheduled* quiet hours (alerts suppressed during a recurring or one-off window) and *pausing* a check with auto-resume on its next successful ping, the latter being safer precisely because it can't be forgotten. [[Dead Man's Switch]]-style checks need the pause variant: while the host is off they'd otherwise fire by design. SLAs typically carve planned windows out of downtime math — but only if announced in advance.

## See also

- [[Monitoring]]
- [[Dead Man's Switch]]
- [[SLA]]
- [[Rollback]]

## Further reading

- [Wikipedia: Maintenance window](https://en.wikipedia.org/wiki/Maintenance_window)
