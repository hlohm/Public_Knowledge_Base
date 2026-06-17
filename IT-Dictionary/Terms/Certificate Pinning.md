---
type: "term"
branch: "Security"
domain: "Cryptography"
aliases: ["Public Key Pinning"]
tags: ["security", "crypto", "pki"]
status: "developed"
---

# Certificate Pinning

> **Domain:** [[03 - Cryptography|Cryptography]]
> **Also known as:** Public Key Pinning

Hardcoding which certificate or public key a client will accept for a host, instead of trusting anything that chains to a system root CA.

**Context.** Pinning defends against a compromised or coerced CA issuing a fraudulent-but-valid certificate — the one attack the normal chain of trust can't stop. The cost is operational fragility: rotate the pinned key without updating clients and you've locked yourself out. Browsers abandoned HPKP for exactly this reason; pinning survives mainly in mobile apps, and it's also why corporate [[TLS Inspection]] breaks some apps.

## See also

- [[Chain of Trust]]
- [[Certificate Authority]]
- [[TLS]]
- [[TLS Inspection]]
- [[X.509]]

## Further reading

- [OWASP: Certificate Pinning Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Pinning_Cheat_Sheet.html)
