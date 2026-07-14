---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["Indirect Prompt Injection"]
tags: ["threat", "ai", "appsec"]
status: "developed"
---

# Prompt Injection

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** Indirect Prompt Injection

Hijacking an LLM application by planting instructions in content the model processes — a web page it summarizes, an email it reads, a document it ingests — so the model follows the attacker's instructions instead of (or alongside) the operator's. Named by analogy to SQL injection: untrusted data crosses into a context that treats it as code.

**Context.** The least solved member of the [[Injection Attacks]] family, because an LLM has no code/data boundary to enforce — everything becomes one token sequence, and models cannot reliably rank instructions by origin. *Direct* injection is attacker text typed straight into the prompt; the dangerous variant is *indirect*: instructions arriving through content an [[AI Agent]] fetches or reads while doing its job, turning the agent into a [[Confused Deputy Problem|confused deputy]] that wields its operator's tools on the attacker's behalf. Detection-based guardrails filter some attacks; none reach the reliability of parameterized queries. Practical defense is therefore architectural: assume injection succeeds and constrain what obedience can cost — see [[Lethal Trifecta]].

## See also

- [[Injection Attacks]]
- [[Lethal Trifecta]]
- [[AI Agent]]
- [[Confused Deputy Problem]]
- [[Exfiltration]]

## Often confused with

- [[Jailbreak]] — jailbreaking attacks the *model's own* refusals (the user is the attacker); prompt injection attacks the *application* through content it processes (the user is the victim).

## Further reading

- [Simon Willison: Prompt injection attacks against GPT-3](https://simonwillison.net/2022/Sep/12/prompt-injection/) — where the term was coined
- [OWASP Top 10 for LLM Applications — LLM01](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Wikipedia: Prompt injection](https://en.wikipedia.org/wiki/Prompt_injection)
