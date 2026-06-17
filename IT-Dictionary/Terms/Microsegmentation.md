---
type: "term"
branch: "Security"
domain: "Network Security"
tags: ["network", "modern"]
status: "note"
---

# Microsegmentation

> **Domain:** [[05 - Network Security|Network Security]]

Segmentation at workload or process level, often in cloud or SDN environments.

**Context.** The end state of segmentation thinking: policy follows the workload ("web tier may reach DB tier on 5432") instead of the subnet, enforced by host firewalls, hypervisor, or eBPF rather than VLAN boundaries. The discovery phase is the real project — you can't write allow-rules for flows you haven't mapped.

## See also

- [[Network Segmentation]]
- [[Zero Trust]]
- [[SDN]]
- [[Service Mesh]]
