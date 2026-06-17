---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["SSL Decryption"]
tags: ["network"]
status: "note"
---

# TLS Inspection

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** SSL Decryption

Terminating TLS at a gateway to inspect content, then re-encrypting. Privacy-fraught but operationally common.

**Context.** Without it, the IPS/DLP/proxy stack inspects headers of encrypted streams — i.e., almost nothing; with it, you operate an internal CA, push its root to every endpoint, and shoulder real privacy and legal duties (in Germany: works council, and hard exclusions for banking/health/private categories). Certificate-pinned apps will break and need a bypass list. Decide deliberately; both options are defensible, default-drift isn't.

## See also

- [[DPI]]
- [[NGFW]]
- [[SWG]]
