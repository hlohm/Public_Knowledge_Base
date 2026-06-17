---
type: "term"
branch: "Security"
domain: "Cloud & Modern Architecture"
tags: ["cloud"]
status: "note"
---

# Sidecar

> **Domain:** [[10 - Cloud and Modern Architecture|Cloud & Modern Architecture]]

Helper container deployed alongside a workload, often providing security/observability.

**Context.** The pattern that lets security and observability be added without touching application code: the service-mesh proxy (Envoy in Istio/Linkerd) doing mTLS and policy is the canonical security sidecar. Trade-offs that drove the newer alternatives (eBPF, ambient mesh): per-pod resource cost and operational complexity.

## See also

- [[Service Mesh]]
