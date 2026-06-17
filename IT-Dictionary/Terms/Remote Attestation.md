---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
aliases: ["Attestation"]
tags: ["security", "endpoint", "hw"]
status: "developed"
---

# Remote Attestation

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]
> **Also known as:** Attestation

Proving to a remote party *what software a machine booted*, by having a hardware root of trust (typically the TPM) sign the measurements recorded during boot.

**Context.** Attestation is the verification half of [[Measured Boot]]: measuring alone changes nothing — value appears when a verifier checks the signed PCR values and gates access on them (device health checks before VPN/ZTNA access, confidential-computing enclaves proving their identity). The hard parts are practical: knowing what 'good' measurements look like and handling legitimate change (every firmware update shifts the values).

## See also

- [[TPM]]
- [[Measured Boot]]
- [[Secure Boot]]
- [[Confidential Computing]]
- [[Zero Trust]]

## Further reading

- [Wikipedia: Trusted Computing](https://en.wikipedia.org/wiki/Trusted_Computing)
