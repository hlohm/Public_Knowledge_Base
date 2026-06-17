---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["Cross-Site Scripting"]
tags: ["threat", "appsec"]
status: "developed"
---

# XSS

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** Cross-Site Scripting

**C**ross-**S**ite **S**cripting. Injecting script into a web page viewed by other users. Variants: **reflected**, **stored**, **DOM-based**.

**Context.** The browser trusts whatever the site sends, so injected script runs with the victim's session — stealing cookies, keylogging, or riding the user's privileges. The three variants need the same core fix: context-aware output encoding, reinforced by a strict Content-Security-Policy. Stored XSS is the worst (persists, hits every viewer); DOM-based moves the bug entirely client-side, out of server logs.

## See also

- [[CSRF]]
- [[CSP]]
- [[Same-Origin Policy]]
- [[OWASP Top 10]]

## Often confused with

- [[CSRF]] — XSS = attacker injects script into other users' browsers. CSRF = attacker uses an authenticated user's browser to make requests.
- [[SSRF]] — XSS attacks the browser; SSRF attacks the server.

## Further reading

- [OWASP: Cross Site Scripting (XSS)](https://owasp.org/www-community/attacks/xss/)
