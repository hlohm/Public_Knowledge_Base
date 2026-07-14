---
type: "term"
branch: "AI & Machine Learning"
aliases: ["System Message", "Developer Prompt"]
tags: ["ai", "modern"]
status: "note"
---

# System Prompt

> **Branch:** [[13 - AI & Machine Learning|AI & Machine Learning]]
> **Also known as:** System Message, Developer Prompt

The instructions an application places ahead of the user's input to set an [[LLM]]'s role, rules, tools, and tone — the operator's standing brief, distinct from the per-turn user message.

**Context.** The system prompt is where an application tries to assert control: "you are a support agent, never reveal these keys, use only these tools." The catch is that it's a *soft* boundary — it lives in the same [[Context Window]] as everything else, so a model weighs it against later content rather than treating it as privileged. This is why [[Prompt Injection]] works despite careful system prompts, and why "we told it not to" is not a security control. Related failure: system-prompt leakage, where a user coaxes the hidden instructions back out (they were never secret, just upstream). Treat the system prompt as configuration and UX, not as an access-control mechanism.

## See also

- [[LLM]]
- [[AI Agent]]
- [[Prompt Injection]]
- [[Jailbreak]]
- [[Context Window]]

## Further reading

- [Wikipedia: Prompt engineering](https://en.wikipedia.org/wiki/Prompt_engineering)
