---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
tags: [threat, appsec, web]
status: "developed"
---

# Session Fixation

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]

Forcing a victim to use a session identifier the attacker already knows, then riding that same [[Session]] once the victim logs in. The attacker fixes the ID *before* authentication rather than stealing it afterwards.

**Context.** The classic vector: plant a known session ID in the victim's browser (via a crafted URL, a `Set-Cookie` from a vulnerable subdomain, or injected script), wait for them to authenticate, and the now-privileged session is one the attacker already holds. The fix is simple and standard — *regenerate the session ID at every privilege change*, especially on login — so any pre-set ID is discarded the moment it matters. Defence in depth: reject server-unknown IDs, scope cookies tightly (the `__Host-` prefix blocks subdomain injection), and bind the session to client context.

## See also

- [[Session]]
- [[Cookie]]
- [[Session Hijacking]]

## Often confused with

- [[Session Hijacking]] — fixation plants a known ID and waits for the victim; hijacking steals an already-authenticated ID.

## Further reading

- [OWASP: Session fixation](https://owasp.org/www-community/attacks/Session_fixation)
