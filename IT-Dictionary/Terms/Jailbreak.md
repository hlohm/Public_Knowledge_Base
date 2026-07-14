---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
aliases: ["Jailbreaking"]
tags: ["threat", "ai", "mobile"]
status: "developed"
---

# Jailbreak

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]
> **Also known as:** Jailbreaking

Defeating a system's built-in restrictions from the position of its own user. Two senses share the name: device jailbreaking (removing an OS vendor's lockdown, classically iOS, to run unsigned code) and LLM jailbreaking (crafting prompts that get a model to produce output its safety training refuses).

**Context.** In both senses the *user is the attacker* and the vendor's policy is the target — which is exactly what distinguishes LLM jailbreaking from [[Prompt Injection]], where the user is the victim of third-party content. The distinction matters operationally: a jailbreak embarrasses the model vendor; an injection steals *your* data. Developers who conflate them tend to dismiss injection as "the vendor's problem" and ship the vulnerability. LLM jailbreak technique churns fast (role-play framing, encoding tricks, many-shot flooding), and like sandbox-evasion it's an arms race, not a solved problem.

## See also

- [[Prompt Injection]]
- [[LLM]]
- [[System Prompt]]

## Often confused with

- [[Prompt Injection]] — injection plants instructions in content an application processes; jailbreaking is the user attacking the model's own refusals directly.

## Further reading

- [Simon Willison: Prompt injection and jailbreaking are not the same thing](https://simonwillison.net/2024/Mar/5/prompt-injection-jailbreaking/)
- [Wikipedia: iOS jailbreaking](https://en.wikipedia.org/wiki/IOS_jailbreaking)
