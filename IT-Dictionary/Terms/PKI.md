---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["Public Key Infrastructure"]
tags: ["crypto", "trust"]
status: "developed"
---

# PKI

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** Public Key Infrastructure

**P**ublic **K**ey **I**nfrastructure. The ecosystem of CAs, certificates, and trust chains that makes public keys usable at internet scale.

**Context.** Running your own PKI means owning the full lifecycle: offline root, issuing intermediates, templates and naming rules, revocation, and — the part everyone underestimates — renewal automation, because every issued certificate is a future outage with a date on it. Tooling spans Windows AD CS, smallstep, EJBCA, and HashiCorp Vault. A homelab PKI is one of the best ways to internalize all of this.

## See also

- [[Certificate Authority]]
- [[X.509]]
- [[Chain of Trust]]
- [[TLS]]

## Further reading

- [Wikipedia: Public key infrastructure](https://en.wikipedia.org/wiki/Public_key_infrastructure)
- [Smallstep: Everything PKI](https://smallstep.com/blog/everything-pki/)
