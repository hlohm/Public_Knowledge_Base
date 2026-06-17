---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["Mutual TLS"]
tags: ["crypto", "modern"]
status: "note"
---

# mTLS

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** Mutual TLS

**M**utual **TLS**. Both client *and* server authenticate with certificates. Common in service-to-service auth.

**Context.** Flips TLS from "client trusts server" to mutual proof, replacing passwords and API keys with certificates. The natural fit is machine-to-machine: service meshes, device fleets, internal APIs — anywhere you can automate certificate issuance and rotation. That automation is the real cost; without it, mTLS deployments rot into outages.

## See also

- [[TLS]]
- [[Service Mesh]]
- [[Zero Trust]]
