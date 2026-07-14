---
type: "term"
branch: "AI & Machine Learning"
aliases: ["MCP"]
tags: ["ai", "modern"]
status: "note"
---

# Model Context Protocol

> **Branch:** [[13 - AI & Machine Learning|AI & Machine Learning]]
> **Also known as:** MCP

An open protocol (Anthropic, 2024) that standardizes how an [[AI Agent]] connects to external tools and data sources. An MCP *server* exposes tools, resources, and prompts; an MCP *client* inside the agent host discovers and calls them — the "USB-C for AI tools" pitch, one interface instead of a bespoke integration per service.

**Context.** MCP is the plumbing that makes agents genuinely capable, and the same plumbing that assembles the [[Lethal Trifecta]] by accident: mixing servers from different sources tends to combine private-data access, exposure to untrusted content, and outbound reach in one session — often within a single tool. Real exploits have chained an MCP server's read of attacker-filed public issues with its access to private repos and its ability to open PRs, exfiltrating the private data. Operational hygiene: treat each server as code you're installing (supply-chain review), prefer least-privilege scopes, keep untrusted-content servers away from sensitive-access ones, and remember a locally-run MCP server executes on *your* machine under the app's permissions — a vendor's remote agent sandbox does not contain it.

## See also

- [[AI Agent]]
- [[Lethal Trifecta]]
- [[Prompt Injection]]
- [[API]]
- [[Supply Chain Attack]]

## Further reading

- [Model Context Protocol — specification](https://modelcontextprotocol.io/)
