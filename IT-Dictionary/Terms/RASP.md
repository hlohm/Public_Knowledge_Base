---
type: "term"
branch: "Security"
domain: "Application Security"
aliases: ["Runtime Application Self-Protection"]
tags: ["appsec"]
status: "note"
---

# RASP

> **Domain:** [[08 - Application Security|Application Security]]
> **Also known as:** Runtime Application Self-Protection

**R**untime **A**pplication **S**elf-**P**rotection. In-app agent that detects and blocks attacks at runtime.

**Context.** Lives inside the app and sees real execution context, so it can block an exploit with fewer false positives than a WAF guessing from outside — but at the cost of an in-process agent, runtime overhead, and language support limits. Niche compared to WAF/EDR; most value where you can't patch a critical app quickly and need targeted virtual patching from within.

## See also

- [[IAST]]
- [[WAF]]
