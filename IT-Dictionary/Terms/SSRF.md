---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["Server-Side Request Forgery"]
tags: ["threat", "appsec", "cloud"]
status: "developed"
---

# SSRF

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** Server-Side Request Forgery

**S**erver-**S**ide **R**equest **F**orgery. Tricking the server into making requests on the attacker's behalf — often to internal or cloud metadata endpoints.

**Context.** The cloud era's marquee vulnerability: coax a server into making a request *it* is trusted to make, then point it at internal services or the metadata endpoint to steal instance credentials (the Capital One pattern). Defenses are allowlisting outbound destinations, blocking link-local ranges, and — for the metadata case specifically — enforcing IMDSv2.

## See also

- [[IMDS]]
- [[XSS]]
- [[CSRF]]

## Further reading

- [OWASP: SSRF](https://owasp.org/www-community/attacks/Server_Side_Request_Forgery)
