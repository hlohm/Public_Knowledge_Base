---
type: "term"
branch: "Security"
domain: "Cloud & Modern Architecture"
aliases: ["IMDSv2", "\"Instance Metadata Service\""]
tags: ["cloud"]
status: "note"
---

# IMDS

> **Domain:** [[10 - Cloud and Modern Architecture|Cloud & Modern Architecture]]
> **Also known as:** IMDSv2, "Instance Metadata Service"

**I**nstance **M**etadata **S**ervice. Cloud VM endpoint exposing credentials and metadata. Notorious SSRF target — use **IMDSv2**.

**Context.** The canonical cloud privilege-escalation pivot: an SSRF in any app on the VM can read `169.254.169.254` and walk away with the instance's role credentials — the Capital One breach in one sentence. Fixes: enforce IMDSv2 (session tokens, hop limit), minimal instance roles, and egress monitoring for metadata-credential misuse.

## See also

- [[SSRF]]
