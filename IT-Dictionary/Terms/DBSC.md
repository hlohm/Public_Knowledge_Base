---
type: "term"
branch: "Security"
domain: "Identity & Access Management"
aliases: ["Device Bound Session Credentials", "Device-Bound Session Credentials"]
tags: [iam, web, modern]
status: "developed"
---

# DBSC

> **Domain:** [[04 - Identity and Access Management|Identity & Access Management]]
> **Also known as:** Device Bound Session Credentials

**D**evice **B**ound **S**ession **C**redentials. A browser/server protocol that binds a web session to a private key held in the device's secure hardware — a [[TPM]] or Secure Enclave — that cannot be exported, so a stolen session [[Cookie]] is useless on any other machine.

**Context.** DBSC is the cookie-specific answer to the [[Bearer Token]] problem, an instance of [[Proof of Possession]]. At sign-in the browser generates a non-exportable key pair; the server then issues *short-lived* cookies, and when one expires the browser silently signs a server challenge with the device key to refresh it. An attacker who exfiltrates the cookie has no access to the signing key, so the stolen session dies within minutes — directly defeating [[Session Hijacking]] by infostealer. The lineage matters: the earlier Token Binding tried the same idea at the TLS layer and died on infrastructure complexity, whereas DBSC works at the HTTP layer and passes cleanly through load balancers and CDNs. Know the limits — it stops *exfiltration-and-replay*, not an attacker already resident on the device (who can bind their own key at registration, or proxy through the live browser), and it does nothing for non-browser credentials like Kerberos TGTs or Entra Primary Refresh Tokens.

**Status (mid-2026).** Generally available in Chrome on Windows since Chrome 146 (April 2026), backed by the TPM; macOS support via the Secure Enclave is announced as next. Not shipped on Linux despite the hardware usually being present (TPM 2.0 and kernel support are common) — deprioritised over browser market share and ecosystem fragmentation. Software-backed keys (weaker than hardware, but still defeating remote replay) are on the roadmap for devices without a secure element. Firefox and Safari are evaluating; the protocol is a W3C webappsec specification.

## See also

- [[Bearer Token]]
- [[Proof of Possession]]
- [[Cookie]]
- [[Session]]
- [[TPM]]
- [[Session Hijacking]]

## Often confused with

- [[Passkey]] — both rely on a non-exportable device key, but a passkey authenticates *login* (replacing the password); DBSC protects the *session* that login creates.

## Further reading

- [W3C: Device Bound Session Credentials](https://w3c.github.io/webappsec-dbsc/)
- [Chrome for Developers: DBSC](https://developer.chrome.com/docs/web-platform/device-bound-session-credentials)
