---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["XSRF", "\"Cross-Site Request Forgery\""]
tags: ["threat", "appsec"]
status: "developed"
---

# CSRF

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** XSRF, "Cross-Site Request Forgery"

**C**ross-**S**ite **R**equest **F**orgery. Tricking a logged-in user's browser into making unwanted requests.

**Context.** The browser helpfully attaches the victim's session cookie to a forged cross-site request, so the server can't tell it wasn't intended. Largely solved by design now: SameSite cookies (default Lax in modern browsers) plus anti-CSRF tokens. Worth understanding precisely because it's the mirror image of XSS — CSRF abuses trust in the *user*, XSS abuses trust in the *site*.

## See also

- [[XSS]]
- [[SSRF]]
- [[Same-Origin Policy]]

## Further reading

- [OWASP: CSRF](https://owasp.org/www-community/attacks/csrf)
