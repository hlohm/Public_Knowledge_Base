---
type: "term"
branch: "Security"
domain: "Application Security"
aliases: ["Interactive Application Security Testing"]
tags: ["appsec", "testing"]
status: "note"
---

# IAST

> **Domain:** [[08 - Application Security|Application Security]]
> **Also known as:** Interactive Application Security Testing

**I**nteractive **A**pplication **S**ecurity **T**esting. Instrumented running app — hybrid of SAST and DAST.

**Context.** Instruments the app from inside during testing, so it sees the data flow SAST guesses at and the runtime context DAST lacks — yielding low false positives with precise line-level findings. The catch is operational: it needs an agent in the runtime and exercise of the code (often piggybacking on existing test/QA traffic), so it fits mature pipelines more than first AppSec steps.

## See also

- [[SAST]]
- [[DAST]]
- [[RASP]]
