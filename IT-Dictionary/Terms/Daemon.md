---
type: "term"
branch: "Operating Systems"
aliases: ["Service", "Background Process"]
tags: [os]
status: "developed"
---

# Daemon

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** Service, Background Process

A long-running background process with no controlling terminal, providing a service (web server, sshd, cron). On Windows the equivalent is a 'service'.

**Context.** Daemons are started and supervised by an init system (systemd on most Linux), which handles dependencies, restarts, and logging. The name nods to Maxwell's demon, not the malevolent kind.

## See also

- [[Init System]]
- [[systemd]]
- [[Process]]

## Further reading

- [Wikipedia: Daemon (computing)](https://en.wikipedia.org/wiki/Daemon_(computing))
