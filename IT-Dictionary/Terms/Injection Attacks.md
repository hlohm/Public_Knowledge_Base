---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["SQL Injection", "\"Command Injection\"", "\"Prompt Injection\""]
tags: ["threat", "appsec"]
status: "note"
---

# Injection Attacks

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** SQL Injection, "Command Injection", "Prompt Injection"

Tricking an interpreter into running attacker-controlled input: **SQL injection**, **command injection**, **LDAP injection**, **NoSQL injection**, **prompt injection**.

**Context.** One root cause unites the family: untrusted data crosses into a context that interprets it as code. The fix is structurally the same everywhere — separate code from data (parameterized queries, prepared statements, safe APIs) rather than sanitize by blocklist. Prompt injection is the newest member and the least solved, because LLMs have no clean code/data boundary to enforce.

## See also

- [[XSS]]
- [[Input Validation]]
- [[OWASP Top 10]]
- [[Prompt Injection]]
