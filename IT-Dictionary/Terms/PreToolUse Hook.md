---
type: "term"
branch: "Security"
domain: "Endpoint & Host Security"
aliases: ["Pre-Tool-Use Gate", "Tool-Use Hook"]
tags: ["endpoint", "ai"]
status: "developed"
---

# PreToolUse Hook

> **Domain:** [[06 - Endpoint and Host Security|Endpoint & Host Security]]
> **Also known as:** Pre-Tool-Use Gate, Tool-Use Hook

A callback an [[AI Agent]] runtime fires *before* a tool call executes: it receives the tool name and arguments on stdin and returns an allow/deny decision with a reason. Because it runs upstream of the runtime's built-in permission evaluation, it can enforce policy the permission layer cannot express — or gets wrong.

**Context.** The pre-permission position is the point: where a runtime's permission rules for web tools are buggy or too coarse, a hook still sees every call first — a fetch-domain allowlist, a hard deny on search tools, an audit log. Held against the [[Reference Monitor]] checklist: *always invoked* for matched tools; *tamper-proof* only if the script is owned outside the agent's write set (a root-owned hook the agent cannot edit — if the agent can rewrite its fence, there is no fence); *verifiable* because a gate is a few dozen lines. Two design rules recur: the gate must fail closed ([[Fail Secure]]) — parse errors and unexpected input emit an explicit deny, never fall through — and hostname extraction is itself a security boundary, so parse URLs with a real parser (userinfo tricks like `https://good.example@evil.example/` defeat string matching), lowercase, strip trailing dots, then suffix-match.

## See also

- [[AI Agent]]
- [[Fail Secure]]
- [[Reference Monitor]]
- [[Prompt Injection]]
- [[Sandbox]]

## Further reading

- [Claude Code: hooks documentation](https://code.claude.com/docs/en/hooks)
