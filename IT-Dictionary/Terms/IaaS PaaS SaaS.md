---
type: "term"
branch: "Security"
domain: "Cloud & Modern Architecture"
aliases: ["IaaS", "\"PaaS\"", "\"SaaS\"", "\"FaaS\""]
tags: ["cloud"]
status: "note"
---

# IaaS PaaS SaaS

> **Domain:** [[10 - Cloud and Modern Architecture|Cloud & Modern Architecture]]
> **Also known as:** IaaS, "PaaS", "SaaS", "FaaS"

**I**nfrastructure / **P**latform / **S**oftware **as a Service**. Spectrum of how much the provider runs. **FaaS** (Function as a Service) is the serverless variant.

**Context.** The model determines your security to-do list: IaaS leaves you the OS, patching, and network config; PaaS reduces you to code, data, and identity; SaaS reduces you to configuration and access — which is why "secure M365" means tenant settings and identity, not servers. Misjudging the layer is how SaaS tenants end up unhardened: everyone assumed the provider had it.

## See also

- [[Shared Responsibility Model]]
