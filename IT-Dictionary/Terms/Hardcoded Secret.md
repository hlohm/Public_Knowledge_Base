---
type: "term"
branch: "Security"
domain: "Application Security"
tags: ["appsec", "anti-pattern"]
status: "note"
---

# Hardcoded Secret

> **Domain:** [[08 - Application Security|Application Security]]

Credential checked into source code. Found constantly by secret scanners.

**Context.** The vulnerability that never dies because it's so easy to create: an API key in source, a password in a config committed "temporarily", a token in a mobile app's strings. Git history makes it permanent — rotating the secret, not deleting the line, is the only real remediation. Pre-commit scanning (gitleaks) and a secrets manager prevent the next one.

## See also

- [[Secret]]
- [[Secrets Manager]]
