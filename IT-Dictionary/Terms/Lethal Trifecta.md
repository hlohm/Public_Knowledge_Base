---
type: "term"
branch: "Security"
domain: "Threats & Attacks"
tags: ["threat", "ai", "principle"]
status: "developed"
---

# Lethal Trifecta

> **Domain:** [[07 - Threats and Attacks|Threats & Attacks]]

The combination that turns an [[AI Agent]] into an exfiltration machine: **access to private data** + **exposure to untrusted content** + **the ability to communicate externally**. An agent holding all three can be tricked by [[Prompt Injection]] into reading your secrets and sending them to the attacker; remove any one leg and that attack chain breaks.

**Context.** Coined by Simon Willison (2025) as a design test you can apply without understanding transformers: enumerate an agent's tools and data reach, then check which legs stand. It's the AI-agent rendering of classic risk decomposition — like [[Blast Radius]], it assumes compromise and asks what it costs. The trap is that each leg arrives innocently: connectors add private data, web tools add untrusted content, and *any* outbound channel — an HTTP request, a rendered image URL, even a search query — is external communication. Guardrail products that "detect 95% of attacks" fail the standard applied to every other injection class, so mitigation is structural: sterile environments for agents that read hostile content, egress allowlists, no co-resident secrets. A softer industry variant, the "agents rule of two," allows at most two of: untrusted input, sensitive access, and the ability to change state or communicate out.

## See also

- [[Prompt Injection]]
- [[Exfiltration]]
- [[AI Agent]]
- [[Blast Radius]]
- [[Egress Filtering]]
- [[Least Privilege]]

## Further reading

- [Simon Willison: The lethal trifecta for AI agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
