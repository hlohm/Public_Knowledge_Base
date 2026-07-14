---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
aliases: ["Sandbox Breakout"]
tags: ["endpoint", "threat"]
status: "developed"
---

# Sandbox Escape

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]
> **Also known as:** Sandbox Breakout

Code breaking out of the isolated environment meant to contain it — reaching the host filesystem, network, or processes that the [[Sandbox]] policy denies. The VM flavor (guest code reaching the hypervisor or host) is called VM escape.

**Context.** Escapes come in tiers matching the isolation primitive: browser-sandbox escapes (usually chained with a renderer exploit), container escapes (kernel vulns, leaked host mounts, an exposed container-engine socket), namespace/seccomp sandbox escapes (procfs tricks like `/proc/self/root/...`, forgotten inherited file descriptors), and the rare, high-value hypervisor escapes. Two design consequences: isolation layers are ranked — a [[Virtual Machine]] boundary is stronger than a namespace sandbox, which is stronger than a policy inside one process — and sandboxes should be *nested*, so an inner escape lands inside an outer boundary instead of on your host. A special modern case: an [[AI Agent]] whose sandbox is configured in files the agent itself can write doesn't need an exploit — "disable the sandbox to finish the task" is a reasoning step. Policy must live outside the sandboxed party's write set.

## See also

- [[Sandbox]]
- [[Virtual Machine]]
- [[Container Security]]
- [[seccomp]]
- [[Privilege Escalation]]

## Further reading

- [Wikipedia: Virtual machine escape](https://en.wikipedia.org/wiki/Virtual_machine_escape)
