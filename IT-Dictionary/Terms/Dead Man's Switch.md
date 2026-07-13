---
type: "term"
branch: "DevOps & SRE"
aliases: ["Deadman's Switch", "Heartbeat Monitoring"]
tags: ["devops", "monitoring"]
status: "developed"
---

# Dead Man's Switch

> **Branch:** [[12 - DevOps & SRE|DevOps & SRE]]
> **Also known as:** Deadman's Switch, Heartbeat Monitoring

A monitor that triggers when an expected signal *stops* arriving, rather than when something bad is actively reported. A job checks in on a schedule; if the check-in is missed within a grace window, the monitor alerts. It inverts ordinary [[Monitoring]], which fires on a bad event — this one fires on silence.

**Context.** It catches the failure mode threshold-alerting misses: the thing that dies quietly — a backup that stopped running, a host that powered off, an agent that never reported. The load-bearing rule is that the watcher must live *outside* what it watches, or a failure takes the alarm down with it; a hosted check-in service (Healthchecks.io, Cronitor) survives your whole estate going dark precisely because it depends on nothing internal. Tune the grace window to the cadence — too tight and normal jitter pages you, too loose and a dead job stays invisible for days. Its security cousin is the canary token: alert on the *presence* of unexpected access rather than the absence of an expected signal.

## See also

- [[Monitoring]]
- [[Observability]]
- [[Honeypot]]

## Further reading

- [Wikipedia: Dead man's switch](https://en.wikipedia.org/wiki/Dead_man%27s_switch)
