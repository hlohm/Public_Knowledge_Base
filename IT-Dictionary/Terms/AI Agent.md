---
type: "term"
branch: "AI & Machine Learning"
aliases: ["Agentic AI", "LLM Agent"]
tags: ["ai", "modern"]
status: "developed"
---

# AI Agent

> **Branch:** [[13 - AI & Machine Learning|AI & Machine Learning]]
> **Also known as:** Agentic AI, LLM Agent

An [[LLM]] wired to *act*: given tools (shell, file access, web fetch, API calls) and a goal, it loops — reason, call a tool, read the result, repeat — until the task is done or a limit is hit. The step from chatbot to agent is the step from *producing text* to *taking actions in the world*.

**Context.** Agency is what makes agents useful and what makes them dangerous. The same loop that lets a coding agent run tests and open a PR lets a compromised one exfiltrate secrets or pivot through a network. Because an agent carries its operator's authority across every tool call, it is a standing [[Confused Deputy Problem|confused deputy]], and [[Prompt Injection]] is the trick that redirects it — an agent that reads attacker-influenceable content will eventually follow instructions buried in it. There is no reliable "just tell it not to"; the model can't cleanly separate instruction from data (see [[Context Window]]). Practical safety is therefore containment, not persuasion: assume injection succeeds and engineer so obedience is survivable — break the [[Lethal Trifecta]], sandbox the runtime, scope the credentials, keep a human in the loop for consequential actions. [[Model Context Protocol]] standardizes how agents acquire tools, which is convenient and is exactly how the trifecta gets assembled by accident.

## See also

- [[LLM]]
- [[Prompt Injection]]
- [[Lethal Trifecta]]
- [[Model Context Protocol]]
- [[System Prompt]]
- [[Sandbox]]
- [[Confused Deputy Problem]]

## Often confused with

- [[RAG]] — RAG retrieves documents to ground an answer; an agent *acts* through tools. An agent may use retrieval, but retrieval alone isn't agency.

## Further reading

- [Simon Willison: The lethal trifecta for AI agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
- [Wikipedia: Intelligent agent](https://en.wikipedia.org/wiki/Intelligent_agent)
