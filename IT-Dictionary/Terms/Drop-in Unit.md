---
type: "term"
branch: "Operating Systems"
aliases: ["systemd Drop-in", "Override File"]
tags: [os]
status: "developed"
---

# Drop-in Unit

> **Branch:** [[03 - Operating Systems|Operating Systems]]
> **Also known as:** systemd Drop-in, Override File

A small `.conf` fragment in a `<unit>.d/` directory that systemd merges over a unit file, letting you override or extend individual settings — an environment variable, a resource limit, an `ExecStart` — without touching the file the package manager owns.

**Context.** The clean way to customize a service you didn't write: the vendor unit keeps updating with the package while your delta lives separately (`systemctl edit` creates the override; `systemctl cat` shows the merged result). Typical use: pinning a monitoring agent to one interface via an `Environment=` line instead of patching its service file. Gotchas: list-type directives like `ExecStart=` append rather than replace, so you clear them with an empty assignment first; and nothing applies until `systemctl daemon-reload`.

## See also

- [[Daemon]]
- [[Declarative Configuration]]
- [[Operating System]]

## Further reading

- [systemd.unit(5) — drop-in directories](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html)
