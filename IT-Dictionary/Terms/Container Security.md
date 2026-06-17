---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
tags: ["endpoint", "cloud"]
status: "note"
---

# Container Security

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]

Image scanning, runtime protection, admission control for Docker/Kubernetes workloads.

**Context.** The lifecycle view: scan images for vulnerable packages before deploy (Trivy, Grype), admit only signed/approved images, run minimal non-root containers, and watch runtime behavior (Falco). The recurring sins are giant base images full of CVEs nobody needed, and `latest` tags that make "what are we even running?" unanswerable.

## See also

- [[CWPP]]
- [[KSPM]]
- [[SBOM]]
