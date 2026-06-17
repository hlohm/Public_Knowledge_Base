---
type: "term"
branch: "Cloud & Infrastructure"
tags: [cloud, modern]
status: "developed"
---

# Pod

> **Branch:** [[11 - Cloud & Infrastructure|Cloud & Infrastructure]]

Kubernetes' smallest deployable unit — one or more tightly-coupled containers sharing network and storage, scheduled together on a node.

**Context.** Usually one main container per pod; extra ones are sidecars (logging, proxies, mesh). Pods are ephemeral and disposable by design — you don't nurse them, you let controllers (Deployments, ReplicaSets) recreate them, which is the whole cattle-not-pets philosophy.

## See also

- [[Kubernetes]]
- [[Container]]
- [[Sidecar Pattern]]
- [[Node]]
- [[Deployment]]

## Further reading

- [Wikipedia: Kubernetes](https://en.wikipedia.org/wiki/Kubernetes)
