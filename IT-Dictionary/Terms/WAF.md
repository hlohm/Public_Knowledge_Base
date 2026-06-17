---
type: "term"
branch: "Security"
domain: "Network Security"
aliases: ["Web Application Firewall"]
tags: ["network", "appsec"]
status: "developed"
---

# WAF

> **Domain:** [[05 - Network Security|Network Security]]
> **Also known as:** Web Application Firewall

**W**eb **A**pplication **F**irewall. Filters HTTP(S) traffic with awareness of SQL injection, XSS, etc. OWASP CRS is the canonical open ruleset.

**Context.** A virtual-patching layer, not a substitute for fixing the app: when the next framework CVE drops, a WAF rule buys time while the patch is tested. Expect a tuning period — the OWASP Core Rule Set in blocking mode on day one will break legitimate traffic. Logs are an underrated bonus: a WAF is also an attack-attempt sensor.

## See also

- [[OWASP]]
- [[XSS]]
- [[Injection Attacks]]

## Further reading

- [OWASP ModSecurity Core Rule Set](https://coreruleset.org/)
