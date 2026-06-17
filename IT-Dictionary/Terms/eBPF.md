---
type: "term"
branch: "Security"
domain: "Cloud & Modern Architecture"
tags: ["cloud", "modern"]
status: "developed"
---

# eBPF

> **Domain:** [[10 - Cloud and Modern Architecture|Cloud & Modern Architecture]]

Linux kernel technology enabling deep observability and security tooling with low overhead (Cilium, Falco).

**Context.** Why security tooling converged on it: kernel-level visibility into syscalls, network flows, and process activity without kernel modules or per-app instrumentation, at production-tolerable overhead. The flagship projects — Cilium (networking/policy), Falco and Tetragon (runtime detection) — are effectively the Linux answer to EDR internals. Same power makes eBPF-based rootkits a research topic.

## See also

- [[Microsegmentation]]
- [[EDR]]

## Further reading

- [ebpf.io](https://ebpf.io/)
