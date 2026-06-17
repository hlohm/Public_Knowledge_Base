---
type: "term"
branch: "Security"
domain: "Cloud & Modern Architecture"
tags: ["cloud"]
status: "developed"
---

# Shared Responsibility Model

> **Domain:** [[10 - Cloud and Modern Architecture|Cloud & Modern Architecture]]

Cloud provider secures *of* the cloud; customer secures *in* the cloud. Exact split depends on service type.

**Context.** Where it bites in practice: backups (the provider's redundancy is not your backup — deleted is deleted, which is why M365 retention/backup is a customer problem), identity (your phished global admin is not Microsoft's incident), and configuration (the public bucket was always your toggle). Read the per-service split; assumptions here are how gaps are born.

## See also

- [[IaaS PaaS SaaS]]

## Further reading

- [Microsoft: Shared responsibility in the cloud](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility)
