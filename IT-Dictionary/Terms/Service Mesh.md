---
type: "term"
branch: "Cloud & Infrastructure"
tags: [cloud, modern]
status: "developed"
---

# Service Mesh

> **Branch:** [[11 - Cloud & Infrastructure|Cloud & Infrastructure]]

A dedicated infrastructure layer handling service-to-service communication — mTLS, retries, load balancing, observability — via sidecar proxies, transparently to the app.

**Context.** Lifts cross-cutting networking concerns out of application code into the platform (Istio, Linkerd). Powerful for large microservice fleets, but adds real operational complexity and per-hop latency — frequently more than smaller systems need.

## See also

- [[Microservices]]
- [[Sidecar Pattern]]
- [[Kubernetes]]
- [[mTLS]]
- [[Load Balancer]]

## Further reading

- [Wikipedia: Service mesh](https://en.wikipedia.org/wiki/Service_mesh)
