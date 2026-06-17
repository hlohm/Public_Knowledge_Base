---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["Wildcard Cert"]
tags: ["crypto", "pki"]
status: "developed"
---

# Wildcard Certificate

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** Wildcard Cert

A TLS certificate valid for all single-label subdomains of a name via a `*.example.com` entry, so one cert covers `a.example.com`, `b.example.com`, and so on.

**Context.** It saves issuing a cert per host, but the wildcard is exactly *one* level deep: `*.example.com` covers `app.example.com`, not the apex `example.com` and not `x.y.example.com`. Public CAs will only issue wildcards via the [[DNS-01 Challenge|DNS-01]] challenge (you can't prove control of every possible subdomain over HTTP), which ties wildcard issuance to DNS-provider automation. The downside is blast radius — one key now protects every subdomain — so scope it deliberately.

## See also

- [[DNS-01 Challenge]]
- [[TLS]]
- [[ACME]]
- [[Certificate Authority]]

## Further reading

- [Wikipedia: Wildcard certificate](https://en.wikipedia.org/wiki/Wildcard_certificate)
