---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["Session Theft", "Cookie Hijacking"]
tags: [threat, appsec, web]
status: "developed"
---

# Session Hijacking

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** Session Theft, Cookie Hijacking

Taking over an authenticated [[Session]] by stealing its identifier — usually the session [[Cookie]] — and presenting it as your own. Because the session ID is a [[Bearer Token]], a valid stolen copy makes the attacker indistinguishable from the user, MFA included.

**Context.** This is the attack that makes the bearer model dangerous in practice. The ID is lifted by whatever channel is open: [[XSS]] reading a non-`HttpOnly` cookie, a [[MITM]] on an unencrypted link, or — the modern workhorse — infostealer [[Malware]] reading the browser's cookie store straight off disk, which `HttpOnly`/`Secure` do nothing to stop because the theft never travels through the browser's request path. Defences stack: `HttpOnly` + `Secure` + `SameSite` cookies, TLS everywhere, short idle timeouts, regenerating the ID on privilege change, and binding the session to client context. The one that removes the bearer weakness rather than narrowing it is [[DBSC]] — device-bound credentials make an exfiltrated cookie un-replayable elsewhere.

## See also

- [[Session]]
- [[Cookie]]
- [[Bearer Token]]
- [[Replay Attack]]
- [[DBSC]]

## Often confused with

- [[Session Fixation]] — hijacking steals an *existing* valid session ID; fixation plants a *known* ID and waits for the victim to authenticate into it.

## Further reading

- [OWASP: Session hijacking attack](https://owasp.org/www-community/attacks/Session_hijacking_attack)
